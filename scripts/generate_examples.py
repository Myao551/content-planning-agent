"""Execute offline acceptance cases; never fabricate expected output as execution evidence."""
import copy
import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from content_planner.agent import Agent
from content_planner.policy import Catalog, Clock
from content_planner.schemas import DemoConfig, Limits, milliunits
from content_planner.storage import Storage
from content_planner.trace import export_evidence, write_json


def main():
    root = Path(__file__).resolve().parents[1]
    inputs = root / "examples" / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    base = {"request_id": "01-normal", "theme": "为便携咖啡杯策划新品营销视频内容活动", "product_id": "P001",
            "budget_units": "20.000", "deadline_at": "2030-01-01T10:30:00+08:00"}
    fixed = "2030-01-01T10:00:00+08:00"
    normal_demo = {"now_at": fixed, "faults": []}
    write_json(inputs / "demo-config.json", normal_demo)
    cases = [
        ("01-normal", {}, [], "completed"),
        ("02-missing-budget", {"budget_units": None}, [], "needs_input"),
        ("03-missing-deadline", {"deadline_at": None}, [], "needs_input"),
        ("04-budget-replan", {"budget_units": "10.000"}, [], "completed"),
        ("05-infeasible", {"budget_units": "0.000"}, [], "incomplete"),
        ("06-tool-failure", {}, [{"tool": "generate_script", "times": 1}], "completed"),
        ("07-repeat", {"request_id": "01-normal"}, [], "completed"),
        ("08-save-failure", {}, [{"tool": "save_solution", "times": None}], "incomplete"),
        ("09-deadline", {"deadline_at": "2030-01-01T10:01:40+08:00"}, [], "completed"),
        ("10-missing-material", {"product_id": "UNKNOWN"}, [], "needs_input"),
        ("11-request-conflict", {"request_id": "01-normal", "budget_units": "21"}, [], "invalid_input"),
        ("12-step-limit", {}, [], "incomplete"),
        ("13-charged-failure", {"budget_units": "12.000"}, [{"tool": "generate_script", "after_charge": True}], "completed"),
        ("14-changed-prices", {"budget_units": "10.000"}, [], "completed"),
    ]
    changed = inputs / "changed-prices"
    changed.mkdir(exist_ok=True)
    source = Catalog()
    for name, value in source.raw.items():
        value = copy.deepcopy(value)
        if name == "pricing":
            value["tiers"]["reuse"]["resource_milliunits"] = 9000
        write_json(changed / (name + ".json"), value)
    database = root / ".runtime" / ("evaluation-" + str(uuid4()) + ".db")
    store = Storage(database)
    rows = []
    try:
        for name, changes, faults, expected in cases:
            raw = {**base, "request_id": name, **changes}
            raw = {k: v for k, v in raw.items() if v is not None}
            write_json(inputs / (name + ".json"), raw)
            demo = DemoConfig.model_validate({"now_at": fixed, "faults": faults})
            write_json(inputs / (name + ".demo.json"), demo.model_dump(mode="json"))
            limits = Limits(max_steps=2) if name == "12-step-limit" else Limits()
            catalog = Catalog(changed) if name == "14-changed-prices" else source
            result, state = Agent(store, catalog, Clock(datetime.fromisoformat(fixed)), limits=limits, demo=demo).run(raw)
            directory = export_evidence(state, result, root / "examples" / "mock" / name)
            checks = {"expected_status": result["status"] == expected, "no_real_api": result["provider_usage"]["real_api_requests"] == 0}
            if result["status"] == "completed":
                checks["saved_and_verified"] = result["solution"]["saved"] and result["solution"]["readback_verified"]
                checks["within_budget"] = milliunits(result["costs"]["latest_estimate"]["projected_total_units"]) <= milliunits(raw["budget_units"])
                checks["within_deadline"] = datetime.fromisoformat(result["solution"]["saved_at"]) <= datetime.fromisoformat(raw["deadline_at"])
            if state:
                checks["ledger_matches_output"] = sum(e["milliunits"] for e in state["ledger"]) == milliunits(result["costs"]["simulated_spent_units"])
                checks["limits_respected"] = all(state["counts"][k] <= limit for k, limit in [
                    ("steps", limits.max_steps), ("tools", limits.max_tools), ("model_calls", limits.max_model_calls)])
            if name == "07-repeat":
                checks["replayed_same_solution"] = result["replayed"] and result["solution"] == rows[0]["solution"]
            if name == "04-budget-replan":
                checks["replanned_to_reuse"] = result["plan"]["tier"] == "reuse"
                checks["computed_total_8"] = result["costs"]["latest_estimate"]["projected_total_units"] == "8.000"
            if name == "14-changed-prices":
                checks["changed_choice"] = result["plan"]["tier"] == "minimal"
            if name == "08-save-failure":
                checks["partial_success_preserved"] = bool(result["retained_artifacts"]) and not result["solution"]["saved"]
            if name == "13-charged-failure":
                checks["spent_preserved"] = result["costs"]["simulated_spent_units"] == "6.000"
            rows.append({"case": name, "expected": expected, "actual": result["status"], "passed": all(checks.values()),
                         "checks": checks, "solution": result["solution"],
                         "reason_code": result["reason_code"], "evidence": str(directory.relative_to(root)),
                         "mode": "mock", "real_api_requests": 0})
    finally:
        store.close()
    write_json(root / "examples" / "evaluation-results.json", {"scope": "offline_mock_only", "cases": rows,
               "passed": sum(r["passed"] for r in rows), "total": len(rows)})
    lines = ["# 离线案例索引", "", "这些是 Mock 驱动下的实际程序运行，真实模型决策尚未验证。", "",
             "| 案例 | 预期 / 实际 | 通过 | 输出 | Trace |", "| --- | --- | --- | --- | --- |"]
    for row in rows:
        relative = row["evidence"].removeprefix("examples/")
        lines.append(f"| {row['case']} | {row['expected']} / {row['actual']} | {row['passed']} | [JSON]({relative}/output.json) | [记录]({relative}/trace.md) |")
    (root / "examples" / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    report = ["# 离线评估与实际证据", "", "**验证范围：离线流程已验证，真实模型决策待验证。**", "",
              "案例使用固定业务时钟、本地合成数据和确定性 Mock；所有输出与 Trace 来自实际程序执行。",
              "预期业务失败返回 needs_input / incomplete / invalid_input 是正确结果，不等于这些任务已完成。", ""]
    test_file = root / "examples" / "test-results.json"
    if test_file.exists():
        test = json.loads(test_file.read_text())
        report += ["## 自动化测试", "", f"实际执行 `python -m pytest -q`，退出码 {test['exit_code']}，{test['passed_tests']} 项通过。",
                   "[原始测试输出](../examples/test-results.txt)、[测试元信息](../examples/test-results.json)。", "",
                   "覆盖输入、费用、时限、错误动作、上限、事务回滚、重复请求、脚本复用、无依据事实、规则变化、已有支出保留和 CLI。", ""]
    report += ["## 案例结果", "", f"本批 {len(rows)} 个离线案例，{sum(r['passed'] for r in rows)} 个满足各自预期与程序断言。",
               "这不是任务全部完成的比例，也不代表真实模型成功率。", "",
               "| 案例 | 预期 | 实际 | 检查通过 | 实际输出 | 实际 Trace |",
               "| --- | --- | --- | --- | --- | --- |"]
    for row in rows:
        base_link = "../" + row["evidence"]
        report.append(f"| {row['case']} | {row['expected']} | {row['actual']} | {row['passed']} | [JSON]({base_link}/output.json) | [记录]({base_link}/trace.md) |")
    report += ["", "[逐项断言及结果](../examples/evaluation-results.json)；运行元信息与输入在每个案例目录中。", "",
               "## 结果解释与限制", "",
               "- 正常与预算调整分别运行四工具核心链路；预算 10 的示例实际观察标准 12 后改为复用 8。",
               "- 替换费用表使复用方案不再可行，离线策略改为简化方案，避免把参考金额硬编码为结果。",
               "- 缺预算与缺截止时间分别返回待补信息；工具失败案例保留已完成检索，并有限重试。",
               "- 重复请求回读同一方案；输入冲突不覆盖原结果。事务回滚通过自动化测试另行注入。",
               "- 保存持续失败保留脚本与已发生费用；已扣费再失败的案例保留旧费用，再估算可行替代方案。",
               "- 截止时间和步数上限均有实际案例；其他边界由自动化测试覆盖。",
               "- 所有真实 API 请求为零；Mock 动作说明不是真实模型推理过程或决策证据。",
               "- 没有测量真实创作质量、实际转化效果、供应商性能、分布式并发或跨进程恢复。", "",
               "## 复现", "", "在仓库根目录安装后运行 `python scripts/verify.py`，生成新的一批结果。",
               "单例命令、固定时钟和退出码说明见 [README](../README.md)。真实模型接入留到下一阶段。", ""]
    if (root / "examples" / "installation-check.json").exists():
        report += ["## 安装检查", "", "另在全新虚拟环境安装构建的 wheel，并从仓库外运行 CLI。",
                   "[安装检查结果](../examples/installation-check.json)、[wheel 环境测试输出](../examples/wheel-test-results.txt)。", ""]
    (root / "docs" / "03-evaluation.md").write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"passed": sum(r["passed"] for r in rows), "total": len(rows), "database": str(database)}, ensure_ascii=False))
    return 0 if all(r["passed"] for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
