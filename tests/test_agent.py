import json

import pytest

from content_planner.models import MockModelClient
from content_planner.policy import Catalog
from content_planner.policy import current_artifact, fresh_estimate
from content_planner.schemas import Action, Limits


def actions(state, name):
    return [e for e in state["events"] if e["kind"] == "action_result" and e["tool"] == name]


def test_normal(run_task, storage):
    result, state = run_task()
    assert result["status"] == "completed"
    assert result["solution"]["readback_verified"]
    assert result["costs"]["simulated_spent_units"] == "4.000"
    assert result["costs"]["latest_estimate"]["projected_total_units"] == "12.000"
    assert result["costs"]["latest_estimate"]["remaining_tool_units"] == "0.000"
    assert {e["tool"] for e in state["events"] if e["kind"] == "action_result"} >= {
        "search_materials", "generate_script", "estimate_cost", "save_solution"}
    assert storage.solution(state["task_id"]) == state["solution"]
    assert result["provider_usage"]["real_api_requests"] == 0
    assert state["simulated_seconds"] == 211
    for e in state["events"]:
        if e["kind"] == "decision":
            assert all(i < e["seq"] for i in e["action"]["observes_event_ids"])


@pytest.mark.parametrize("missing", ["budget_units", "deadline_at"])
def test_missing_inputs(run_task, missing):
    result, state = run_task({missing: None})
    assert result["status"] == "needs_input"
    assert missing in result["missing_fields"]
    assert state["counts"]["tools"] == state["counts"]["model_calls"] == 0


def test_budget_replanning(run_task):
    result, state = run_task({"budget_units": "10"})
    assert result["status"] == "completed"
    assert [p["tier"] for p in state["plan_versions"]] == ["standard", "reuse"]
    estimates = actions(state, "estimate_cost")
    assert estimates[0]["data"]["projected_total_units"] == "12.000"
    assert estimates[1]["data"]["projected_total_units"] == "8.000"
    assert result["costs"]["simulated_spent_units"] == "2.000"
    assert len(state["ledger"]) == 1


def test_no_feasible_budget(run_task):
    result, state = run_task({"budget_units": "0"})
    assert result["status"] == "incomplete"
    assert result["reason_code"] == "budget_exceeded"
    assert not state["artifacts"] and not state["solution"]
    assert result["costs"]["latest_estimate"]["budget_gap_units"] == "3.000"


@pytest.mark.parametrize("tool", ["search_materials", "estimate_cost", "generate_script", "save_solution"])
def test_one_failure_then_recovery(run_task, tool):
    result, state = run_task(faults=[{"tool": tool}])
    assert result["status"] == "completed"
    calls = actions(state, tool)
    assert any(not e["ok"] for e in calls)
    assert any(e["ok"] for e in calls)
    assert result["costs"]["simulated_spent_units"] == "4.000"
    assert len(state["artifacts"]) == 1
    if tool == "generate_script":
        assert len(actions(state, "search_materials")) == 1
    assert all(e["status"] == ("succeeded" if e["ok"] else "failed") for e in calls)


def test_permanent_save_failure_preserves_script(run_task, storage):
    result, state = run_task(faults=[{"tool": "save_solution", "times": None}])
    assert result["status"] == "incomplete"
    assert not result["solution"]["saved"]
    assert len(state["artifacts"]) == 1
    assert result["costs"]["simulated_spent_units"] == "4.000"
    assert storage.solution(state["task_id"]) is None
    assert len(actions(state, "save_solution")) == 2
    assert all(not e["ok"] for e in actions(state, "save_solution"))


def test_repeat_no_new_side_effects(run_task, storage):
    first, state = run_task()
    before = {t: storage.connection.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
              for t in ("tasks", "steps", "tool_receipts", "ledger", "solutions")}
    second, replay_state = run_task()
    assert second["replayed"]
    assert first["solution"] == second["solution"]
    assert first["provider_usage"] == second["provider_usage"]
    assert state == replay_state
    assert before == {t: storage.connection.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in before}


def test_conflicting_request(run_task, storage):
    first, _ = run_task()
    second, _ = run_task({"budget_units": "21"})
    assert second["reason_code"] == "request_conflict"
    assert storage.get("test-001")["result"]["solution"] == first["solution"]


@pytest.mark.parametrize("deadline,status,tier", [
    ("2030-01-01T10:01:40+08:00", "completed", "minimal"),
    ("2030-01-01T10:00:40+08:00", "incomplete", "minimal"),
    ("2030-01-01T09:59:00+08:00", "incomplete", None),
])
def test_deadline(run_task, deadline, status, tier):
    result, state = run_task({"deadline_at": deadline})
    assert result["status"] == status
    assert (state["plan"]["tier"] if state["plan"] else None) == tier
    if status == "incomplete":
        assert result["reason_code"] == "deadline_exceeded"


def test_missing_material(run_task):
    result, state = run_task({"product_id": "MISSING"})
    assert result["status"] == "needs_input"
    assert not state["artifacts"] and not state["ledger"]


@pytest.mark.parametrize("limits,reason", [
    (Limits(max_steps=2), "step_limit"),
    (Limits(max_tools=1), "tool_call_limit"),
    (Limits(max_model_calls=1), "model_call_limit"),
    (Limits(max_runtime_seconds=1e-12), "runtime_limit"),
])
def test_limits(run_task, limits, reason):
    result, _ = run_task(limits=limits)
    assert result["status"] == "incomplete"
    assert result["reason_code"] == reason


def test_saved_at_last_step_is_still_incomplete(run_task):
    result, state = run_task(limits=Limits(max_steps=6))
    assert state["solution"]
    assert result["solution"]["saved"]
    assert result["status"] == "incomplete"
    assert result["reason_code"] == "step_limit"


class BadDriver(MockModelClient):
    def next_action(self, context):
        return Action(name="finish_task", arguments={"status": "completed"}, summary="尝试未经保存宣称完成")


class UnknownDriver(MockModelClient):
    def next_action(self, context):
        return Action(name="unknown", arguments={}, summary="无效动作")


class ExtraArgumentsDriver(MockModelClient):
    def next_action(self, context):
        return Action(name="search_materials", arguments={"query": "咖啡杯", "success": True}, summary="注入未知参数")


@pytest.mark.parametrize("driver,error", [(BadDriver(), "false_completion"), (UnknownDriver(), "unknown_action"),
                                         (ExtraArgumentsDriver(), "invalid_arguments")])
def test_invalid_actions_never_succeed(run_task, driver, error):
    result, state = run_task(model=driver, limits=Limits(max_steps=3))
    assert result["status"] == "incomplete"
    assert not state["solution"]
    assert any(e.get("error_code") == error for e in state["events"])


def copy_catalog(tmp_path):
    from importlib.resources import files
    directory = tmp_path / "data"
    directory.mkdir()
    for name in ("products", "materials", "pricing", "durations", "rules"):
        (directory / (name + ".json")).write_text(files("content_planner.data").joinpath(name + ".json").read_text(), encoding="utf-8")
    return directory


def test_changed_prices_change_choice(run_task, tmp_path):
    directory = copy_catalog(tmp_path)
    pricing = json.loads((directory / "pricing.json").read_text())
    pricing["tiers"]["reuse"]["resource_milliunits"] = 9000
    (directory / "pricing.json").write_text(json.dumps(pricing))
    result, state = run_task({"budget_units": "10"}, catalog=Catalog(directory))
    assert result["status"] == "completed"
    assert state["plan"]["tier"] == "minimal"
    assert result["costs"]["latest_estimate"]["projected_total_units"] == "3.000"


def test_no_reusable_material_skips_tier(run_task):
    result, state = run_task({"product_id": "P002", "theme": "收纳盒活动", "budget_units": "10"})
    assert result["status"] == "completed"
    assert [p["tier"] for p in state["plan_versions"]] == ["standard", "minimal"]


def test_charged_failure_keeps_spent_costs(run_task):
    result, state = run_task({"budget_units": "12"}, faults=[{"tool": "generate_script", "after_charge": True}])
    assert result["status"] == "completed"
    assert state["plan"]["tier"] == "reuse"
    assert result["costs"]["simulated_spent_units"] == "6.000"
    assert result["costs"]["latest_estimate"]["projected_total_units"] == "12.000"
    assert len(state["ledger"]) == 2
    failed = [e for e in actions(state, "generate_script") if not e["ok"]]
    assert failed[0]["charged_units"] == "4.000"


def test_transaction_failure_rolls_back_solution(run_task, storage):
    storage.connection.execute("CREATE TRIGGER reject_save BEFORE INSERT ON solutions BEGIN SELECT RAISE(ABORT, 'test-save-error'); END")
    result, state = run_task()
    assert result["status"] == "incomplete"
    assert not result["solution"]["saved"]
    assert len(state["artifacts"]) == 1
    assert storage.connection.execute("SELECT count(*) FROM solutions").fetchone()[0] == 0
    assert storage.connection.execute("SELECT count(*) FROM steps WHERE tool='save_solution' AND status='succeeded'").fetchone()[0] == 0


@pytest.mark.parametrize("changes", [
    {"budget_units": "-1"}, {"budget_units": "nan"}, {"budget_units": "1.0001"}, {"budget_units": 10},
    {"deadline_at": "2030-01-01T10:30:00"}, {"deadline_at": 1893456000}, {"theme": "  "}, {"unexpected": True},
])
def test_invalid_input(run_task, changes):
    result, state = run_task(changes)
    assert result["status"] == "invalid_input"
    assert state is None


class PrematureDraftDriver(MockModelClient):
    def next_action(self, context):
        if context["plan"] and context["estimate"] is None:
            return Action(name="generate_script", arguments={"plan_id": context["plan"]["id"],
                          "material_ids": context["plan"]["material_ids"]}, summary="尝试跳过估算")
        return super().next_action(context)


def test_generation_requires_fresh_estimate(run_task):
    result, state = run_task(model=PrematureDraftDriver())
    assert result["status"] == "incomplete"
    assert result["reason_code"] == "tool_call_limit"
    assert any(e.get("error_code") == "stale_estimate" for e in state["events"])
    assert not state["ledger"] and not state["artifacts"]


class ForgingScriptDriver(MockModelClient):
    def generate_script(self, request):
        return {"title": "产品", "segments": [{"text": "效率提升 80%", "source_ids": ["M001"]}], "generation_note": "测试"}


def test_unsupported_fact_rejected(run_task):
    result, state = run_task(model=ForgingScriptDriver())
    assert result["reason_code"] == "unsupported_fact"
    assert not state["ledger"] and not state["artifacts"]


class DuplicateDraftDriver(MockModelClient):
    repeated = False

    def next_action(self, context):
        if current_artifact(context) and fresh_estimate(context) and not self.repeated:
            self.repeated = True
            return Action(name="generate_script", arguments={"plan_id": context["plan"]["id"],
                          "material_ids": context["plan"]["material_ids"]}, summary="重复相同脚本请求")
        return super().next_action(context)


def test_identical_script_call_uses_receipt(run_task):
    result, state = run_task(model=DuplicateDraftDriver())
    assert result["status"] == "completed"
    assert len(actions(state, "generate_script")) == 2
    assert actions(state, "generate_script")[1]["data"]["cached"]
    assert len(state["artifacts"]) == len(state["ledger"]) == 1


class OverBudgetDriver(MockModelClient):
    def next_action(self, context):
        if context["plan"] and fresh_estimate(context) and not context["estimate"]["feasible"]:
            return Action(name="generate_script", arguments={"plan_id": context["plan"]["id"],
                          "material_ids": context["plan"]["material_ids"]}, summary="尝试越过预算校验")
        return super().next_action(context)


def test_over_budget_action_blocked(run_task):
    result, state = run_task({"budget_units": "10"}, model=OverBudgetDriver())
    assert result["status"] == "incomplete"
    assert any(e.get("error_code") == "constraint_violation" for e in state["events"])
    assert not state["ledger"] and not state["artifacts"]


class ReplanAfterSuccessDriver(MockModelClient):
    changed = False

    def next_action(self, context):
        if current_artifact(context) and not context["solution"] and not self.changed:
            from content_planner.tools import plan_steps
            self.changed = True
            return Action(name="update_plan", arguments={"tier": "reuse", "material_ids": context["plan"]["material_ids"],
                          "steps": plan_steps()}, summary="已有成功脚本后改方案，验证原费用与产物保留")
        return super().next_action(context)


def test_replan_after_success_keeps_old_artifact_and_cost(run_task):
    result, state = run_task(model=ReplanAfterSuccessDriver())
    assert result["status"] == "completed"
    assert len(state["artifacts"]) == 2
    assert result["costs"]["simulated_spent_units"] == "6.000"
    assert result["costs"]["latest_estimate"]["projected_total_units"] == "12.000"
