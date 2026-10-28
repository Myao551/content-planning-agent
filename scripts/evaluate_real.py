"""A bounded real API evaluation. Credentials stay in memory and never enter artifacts."""
import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from content_planner.agent import Agent
from content_planner.config import configured_client
from content_planner.policy import Catalog
from content_planner.provenance import capture_runtime_version
from content_planner.schemas import DemoConfig, Limits, milliunits
from content_planner.storage import Storage
from content_planner.trace import export_evidence, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key-file", type=Path)
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--base-url")
    parser.add_argument("--model")
    parser.add_argument("--require-clean", action="store_true", help="冻结版本回归：要求 Git 中的实现、数据、脚本和测试干净")
    parser.add_argument("--cases", nargs="+", choices=["normal", "replan", "failure", "missing", "repeat", "infeasible"],
                        default=["normal", "replan", "failure", "missing", "repeat", "infeasible"])
    args = parser.parse_args()
    preflight_version = capture_runtime_version(phase="evaluation_preflight")
    if args.require_clean and (not preflight_version["git_commit"] or preflight_version["git_dirty"] is not False):
        raise ValueError("冻结版本验证要求可定位 Git 提交，且实现、数据、依赖、脚本和测试均无未提交变更；尚未发送 API 请求")
    root = Path(__file__).resolve().parents[1]
    def make_client():
        return configured_client(api_key_file=args.api_key_file, env_file=args.env_file, base_url=args.base_url, model=args.model)
    prototype = make_client()
    batch = str(uuid4())
    output = root / "examples" / "real" / batch
    output.mkdir(parents=True)
    base = {"request_id": "real-normal-" + batch, "theme": "为便携咖啡杯策划新品营销视频内容活动", "product_id": "P001",
            "budget_units": "20.000", "deadline_at": (datetime.now(timezone(timedelta(hours=8))) + timedelta(hours=1)).isoformat()}
    rows = []
    store = Storage(root / ".runtime" / ("real-" + batch + ".db"))
    total_tokens, total_calls = 0, 0
    try:
        for name in args.cases:
            if name not in {"missing", "repeat"} and (total_calls >= 60 or total_tokens >= 150000):
                rows.append({"case": name, "skipped": True, "reason": "达到本批请求或 token 预算上限"})
                continue
            raw = {**base, "request_id": "real-" + name + "-" + batch}
            if name == "repeat":
                if not any(r.get("case") == "normal" for r in rows):
                    raise ValueError("repeat 必须在同一批 normal 之后运行")
                raw = dict(base)
            if name == "replan":
                raw["budget_units"] = "10.000"
            if name == "missing":
                del raw["budget_units"]
            if name == "infeasible":
                raw["budget_units"] = "0.000"
            demo = DemoConfig.model_validate({"faults": [{"tool": "generate_script", "times": 1}] if name == "failure" else []})
            client = make_client()
            result, state = Agent(store, Catalog(), model=client, limits=Limits(), demo=demo).run(raw)
            directory = export_evidence(state, result, output / name)
            usage = result["provider_usage"]
            total_calls += usage["real_api_requests"]
            total_tokens += (usage.get("tokens") or {}).get("total_tokens", 0)
            expected = "needs_input" if name == "missing" else "incomplete" if name == "infeasible" else "completed"
            checks = {"expected_status": result["status"] == expected, "real_mode": result["mode"] == "real"}
            execution = result.get("execution_version", {})
            checks["execution_snapshot_recorded"] = execution.get("status") == "captured"
            if args.require_clean:
                checks["frozen_code_version"] = (execution.get("git_commit") == preflight_version["git_commit"]
                    and execution.get("implementation_hash") == preflight_version["implementation_hash"]
                    and execution.get("git_dirty") is False)
            if result["status"] == "completed":
                checks.update(saved=result["solution"]["saved"] and result["solution"]["readback_verified"],
                              within_budget=milliunits(result["costs"]["latest_estimate"]["projected_total_units"]) <= milliunits(raw["budget_units"]))
            if name == "repeat":
                checks["no_new_api_requests"] = result.get("replayed", False) and usage["real_api_requests"] == 0
                normal = next(r for r in rows if r.get("case") == "normal")
                checks["same_execution_version_as_normal"] = execution == normal["execution_version"]
            if name == "replan" and state:
                checks["observed_over_budget_and_changed"] = len(state["plan_versions"]) >= 2 and any(
                    e.get("tool") == "estimate_cost" and e.get("ok") and not e["data"]["feasible"] for e in state["events"])
            if name == "failure" and state:
                checks["failure_observed"] = any(e.get("error_code") == "injected_tool_failure" for e in state["events"])
                checks["successful_materials_retained"] = bool(state["retrieval"])
            if name == "infeasible" and state:
                checks["budget_rejection_observed"] = not state["solution"] and any(
                    e.get("tool") == "estimate_cost" and e.get("ok") and e["data"]["budget_gap_units"] != "0.000"
                    for e in state["events"])
            row = {"case": name, "expected": expected, "actual": result["status"], "reason_code": result["reason_code"],
                   "execution_version": execution,
                   "checks": checks, "passed": all(checks.values()), "api_requests": usage["real_api_requests"],
                   "tokens": (usage.get("tokens") or {}).get("total_tokens"), "wall_seconds": state["wall_seconds"] if state else None,
                   "evidence": str(directory.relative_to(root)), "tier": result.get("plan", {}).get("tier") if result.get("plan") else None}
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    finally:
        store.close()
    report = {"batch_id": batch, "model": prototype.model_name, "provider": "openai_compatible", "cases": rows,
              "require_clean": args.require_clean, "preflight_version": preflight_version,
              "api_requests": total_calls, "total_tokens": total_tokens, "actual_money": None,
              "billing_note": "API 返回 token 使用量；未查询账单，不能断言完全免费或实际金额",
              "scope": "真实模型决策和严格事实脚本；业务服务、商品与计费均为本地合成", "all_passed": all(r.get("passed", False) for r in rows)}
    write_json(output / "report.json", report)
    print(json.dumps({"report": str((output / "report.json").relative_to(root)), "api_requests": total_calls, "total_tokens": total_tokens}, ensure_ascii=False))
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
