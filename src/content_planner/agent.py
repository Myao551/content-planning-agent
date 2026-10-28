import copy
import sqlite3
import time
from datetime import datetime
from uuid import uuid4

from pydantic import ValidationError

from .models import MockModelClient
from .provenance import capture_runtime_version, execution_version
from .policy import Catalog, Clock, current_artifact, digest, effective_now
from .schemas import Action, DemoConfig, Limits, TaskInput, units
from .tools import BUSINESS_TOOLS, BusinessError, Tools


def simple_result(status, code, message, raw=None, mode="mock"):
    return {"run_id": str(uuid4()), "task_id": None, "status": status, "reason_code": code, "explanation": message, "input": raw,
            "mode": mode, "model_driver": "openai_compatible" if mode == "real" else "mock", "solution": {"saved": False},
            "provider_usage": {"real_api_requests": 0, "tokens": None, "money": None}}


def final_result(state):
    solution = state["solution"]
    return {"request_id": state["input"]["request_id"], "task_id": state["task_id"], "run_id": state["run_id"],
            "execution_version": execution_version(state),
            "mode": state.get("mode", "mock"), "model_driver": state.get("model_config", {}).get("provider", "mock"),
            "validation_scope": "真实模式与本地合成业务工具；请求是否实际发生以 provider_usage 为准" if state.get("mode") == "real" else "本次运行仅验证离线 Mock 流程，不代表真实模型决策验证",
            "status": state["status"], "reason_code": state["reason_code"], "explanation": state["explanation"],
            "replayed": False, "plan": state["plan"], "plan_versions": state["plan_versions"],
            "steps": [e for e in state["events"] if e["kind"] == "action_result"],
            "costs": {"simulated_spent_units": units(sum(e["milliunits"] for e in state["ledger"])),
                      "latest_estimate": solution["costs"] if solution else state["estimate"]},
            "timing": {"deadline_at": state["input"]["deadline_at"], "simulated_seconds": state["simulated_seconds"],
                       "wall_seconds": state["wall_seconds"]},
            "solution": {"saved": bool(solution), "solution_id": solution["id"] if solution else None,
                         "saved_at": solution["saved_at"] if solution else None, "readback_verified": state["readback_verified"]},
            "missing_fields": state["missing_fields"], "questions": state["questions"],
            "retained_artifacts": list(state["artifacts"].values()),
            "provider_usage": state.get("provider_usage", {"real_api_requests": 0, "tokens": None, "money": None,
                               "mock_driver_calls": state["counts"]["model_calls"]}),
            "limits": {"configured": state["limits"], "used": state["counts"]}}


class Agent:
    def __init__(self, storage, catalog=None, clock=None, model=None, limits=None, demo=None, on_event=None):
        self.storage = storage
        self.catalog = catalog or Catalog()
        self.clock = clock or Clock()
        self.model = model or MockModelClient()
        self.mode = getattr(self.model, "mode", "mock")
        self.limits = limits or Limits()
        self.demo = demo or DemoConfig()
        self.tools = Tools(self.catalog, self.clock, self.model, self.limits)
        self.fault_counts = {}
        self.on_event = on_event

    def notify(self, event):
        # Display observers cannot mutate trusted state or prevent persistence.
        if self.on_event:
            try:
                self.on_event(copy.deepcopy(event))
            except Exception:
                pass

    def event(self, state, kind, **payload):
        event = {"seq": len(state["events"]) + 1, "kind": kind, "run_id": state["run_id"],
                 "timestamp": self.clock.now().isoformat(), "plan_id": (state["plan"] or {}).get("id"), **payload}
        state["events"].append(event)
        return event

    def run(self, raw):
        try:
            inp = TaskInput.model_validate(raw).model_dump(mode="json")
        except ValidationError as exc:
            return simple_result("invalid_input", "invalid_input", str(exc), raw, self.mode), None
        existing = self.storage.get(inp["request_id"])
        if existing:
            config = self.model.config() if self.mode == "real" else {"provider": "mock"}
            if (existing["input_hash"] != digest(inp) or existing.get("mode", "mock") != self.mode
                    or existing.get("model_config", config) != config):
                return simple_result("invalid_input", "request_conflict", "请求标识已对应不同输入或模型配置，未覆盖原任务", inp, self.mode), None
            if existing["status"] == "running":
                return simple_result("incomplete", "already_running", "任务仍在运行或需要显式恢复", inp, self.mode), existing
            result = copy.deepcopy(existing["result"])
            result["replayed"] = True
            result["execution_version"] = execution_version(existing)
            if self.mode == "real":
                prior_usage = result["provider_usage"]
                result["provider_usage"] = {"real_api_requests": 0, "tokens": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                                            "requests": [], "money": None, "usage_complete": True, "source_run_usage": prior_usage}
            return result, existing
        started = time.monotonic()
        state = {"task_id": str(uuid4()), "run_id": str(uuid4()), "input": inp, "raw_input": raw,
                 "execution_version": capture_runtime_version(),
                 "mode": self.mode, "model_config": self.model.config() if self.mode == "real" else {"provider": "mock"},
                 "input_hash": digest(inp), "status": "running", "reason_code": "", "explanation": "",
                 "started_at": self.clock.now().isoformat(), "simulated_seconds": 0, "wall_seconds": 0,
                 "catalog_version": self.catalog.version, "tier_order": self.catalog.rules["tier_order"],
                 "limits": self.limits.model_dump(), "demo": self.demo.model_dump(mode="json"),
                 "counts": {"steps": 0, "tools": 0, "model_calls": 0}, "attempts": {}, "failure_counts": {},
                 "plan": None, "plan_versions": [], "product_id": None, "retrieval": None, "estimate": None,
                 "ledger": [], "artifacts": {}, "solution": None, "events": [], "last_result": None,
                 "missing_fields": [], "questions": [], "result": None, "readback_verified": False}
        if not self.storage.claim(state):
            return simple_result("incomplete", "already_running", "请求被另一个运行领取", inp, self.mode), None
        missing = [k for k in ("budget_units", "deadline_at") if inp[k] is None]
        if missing:
            state.update(status="needs_input", reason_code="missing_information", missing_fields=missing,
                         questions=["请补充 " + name for name in missing], explanation="缺少预算或截止时间，未执行业务工具")
        elif self.clock.now() > datetime.fromisoformat(inp["deadline_at"]):
            state.update(status="incomplete", reason_code="deadline_exceeded", explanation="截止时间已经过去")
        while state["status"] == "running":
            if time.monotonic() - started >= self.limits.max_runtime_seconds:
                self.stop(state, "runtime_limit", "实际运行时间达到上限")
                break
            if state["counts"]["steps"] >= self.limits.max_steps:
                self.stop(state, "step_limit", "Agent 动作轮数达到上限")
                break
            if state["counts"]["model_calls"] >= self.limits.max_model_calls:
                self.stop(state, "model_call_limit", "驱动调用次数达到上限")
                break
            state["counts"]["steps"] += 1
            state["counts"]["model_calls"] += 1
            try:
                self.notify({"kind": "model_wait", "step": state["counts"]["steps"], "mode": self.mode})
                self.set_timeout(started)
                action = Action.model_validate(self.model.next_action(copy.deepcopy(state)))
                self.sync_usage(state)
                observations = {e["seq"] for e in state["events"] if e["kind"] == "action_result"}
                if not set(action.observes_event_ids) <= observations:
                    raise ValueError("动作引用了不存在的工具或控制动作结果")
            except Exception as exc:
                self.sync_usage(state)
                self.stop(state, "driver_error", "决策驱动未返回有效动作：" + str(exc))
                break
            self.event(state, "decision", action=action.model_dump(), summary=action.summary)
            self.storage.commit(state)
            self.notify(state["events"][-1])
            if time.monotonic() - started >= self.limits.max_runtime_seconds:
                self.stop(state, "runtime_limit", "驱动返回时已达到实际运行上限，未执行动作")
                break
            if action.name in BUSINESS_TOOLS:
                if state["counts"]["tools"] >= self.limits.max_tools:
                    self.stop(state, "tool_call_limit", "业务工具次数达到上限，未执行本次工具")
                    break
                state["counts"]["tools"] += 1
            self.set_timeout(started)
            state = self.perform(state, action)
            self.sync_usage(state)
            self.notify(state["events"][-1])
            if time.monotonic() - started >= self.limits.max_runtime_seconds:
                self.stop(state, "runtime_limit", "动作返回时达到实际运行上限，保留已有结果")
        if state["status"] == "completed":
            saved = self.storage.solution(state["task_id"])
            if not saved or saved != state["solution"] or saved["plan_id"] != state["plan"]["id"]:
                state["readback_verified"] = False
                self.stop(state, "readback_failed", "保存回执未通过数据库回读核验")
            elif datetime.fromisoformat(saved["saved_at"]) > datetime.fromisoformat(inp["deadline_at"]):
                self.stop(state, "deadline_exceeded", "保存时已超过截止时间")
        state["wall_seconds"] = round(time.monotonic() - started, 6)
        self.sync_usage(state)
        self.event(state, "terminal", status=state["status"], reason_code=state["reason_code"], summary=state["explanation"])
        state["result"] = final_result(state)
        self.storage.commit(state)
        self.notify(state["events"][-1])
        return state["result"], state

    def stop(self, state, code, message):
        state.update(status="incomplete", reason_code=code, explanation=message)

    def set_timeout(self, started):
        if hasattr(self.model, "set_timeout"):
            self.model.set_timeout(self.limits.max_runtime_seconds - (time.monotonic() - started))

    def sync_usage(self, state):
        state["provider_usage"] = self.model.usage() if self.mode == "real" else {
            "real_api_requests": 0, "tokens": None, "money": None, "mock_driver_calls": state["counts"]["model_calls"]}

    def fault(self, name):
        for index, spec in enumerate(self.demo.faults):
            if spec.tool == name:
                used = self.fault_counts.get(index, 0)
                if spec.times is None or used < spec.times:
                    self.fault_counts[index] = used + 1
                    return spec
        return None

    def perform(self, state, action):
        candidate = copy.deepcopy(state)
        call_id = str(uuid4())
        attempt_key = digest({"tool": action.name, "args": action.arguments})
        candidate["attempts"][attempt_key] = candidate["attempts"].get(attempt_key, 0) + 1
        result = {"call_id": call_id, "tool": action.name, "parameters": action.arguments,
                  "provider_call_id": action.provider_call_id,
                  "attempt_key": attempt_key, "ok": False, "retryable": False, "error_code": "",
                  "summary": "", "data": None, "charged_units": "0.000"}
        solution = None
        before = sum(e["milliunits"] for e in state["ledger"])
        try:
            args = self.tools.validate(candidate, action)
            if candidate["failure_counts"].get(attempt_key, 0) >= self.limits.max_attempts:
                raise BusinessError("retry_limit", "同一步骤的尝试次数已达上限")
            injected = self.fault(action.name)
            if injected:
                if injected.after_charge:
                    tier = candidate["plan"]["tier"]
                    self.tools.charge(candidate, call_id, self.catalog.pricing["tiers"][tier]["script_milliunits"],
                                      self.catalog.durations["script_seconds"][tier])
                raise BusinessError("injected_tool_failure", "已注入工具失败" + ("（模拟费用已发生）" if injected.after_charge else "（执行前，无费用）"), True)
            data, solution = self.tools.execute(candidate, action, args, call_id)
            result.update(ok=True, data=data, summary="动作执行成功")
        except ValidationError as exc:
            result.update(error_code="invalid_arguments", summary=str(exc))
        except BusinessError as exc:
            result.update(error_code=exc.code, summary=exc.message, retryable=exc.retryable)
        except Exception as exc:
            # A failed arbitrary tool must not leak partially mutated candidate outputs.
            counts = candidate["counts"]
            candidate = copy.deepcopy(state)
            candidate["counts"] = counts
            candidate["attempts"][attempt_key] = state["attempts"].get(attempt_key, 0) + 1
            result.update(error_code="tool_error", summary=str(exc), retryable=True)
        after = sum(e["milliunits"] for e in candidate["ledger"])
        result["charged_units"] = units(after - before)
        candidate["failure_counts"][attempt_key] = 0 if result["ok"] else candidate["failure_counts"].get(attempt_key, 0) + 1
        candidate["last_result"] = result
        self.event(candidate, "action_result", **result, status="succeeded" if result["ok"] else "failed", task_status=candidate["status"],
                   simulated_seconds=candidate["simulated_seconds"], simulated_spent_units=units(after))
        try:
            self.storage.commit(candidate, receipt=result if action.name in BUSINESS_TOOLS else None, solution=solution)
            if solution:
                if self.storage.solution(candidate["task_id"]) != solution:
                    candidate["readback_verified"] = False
                    self.stop(candidate, "readback_failed", "已提交保存，但回读未通过核验")
                else:
                    candidate["readback_verified"] = True
        except sqlite3.Error as exc:
            candidate = copy.deepcopy(state)
            candidate["attempts"][attempt_key] = state["attempts"].get(attempt_key, 0) + 1
            candidate["failure_counts"][attempt_key] = state["failure_counts"].get(attempt_key, 0) + 1
            result.update(ok=False, error_code="storage_error", summary="事务未成功：" + str(exc), data=None, retryable=True, charged_units="0.000")
            candidate["last_result"] = result
            self.event(candidate, "action_result", **result, status="failed", task_status=candidate["status"],
                       simulated_seconds=candidate["simulated_seconds"], simulated_spent_units=units(before))
            self.storage.commit(candidate, receipt=result if action.name in BUSINESS_TOOLS else None)
        return candidate
