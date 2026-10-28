from typing import Protocol

from .policy import current_artifact, fresh_estimate
from .schemas import Action
from .tools import plan_steps


class ModelClient(Protocol):
    def next_action(self, context: dict) -> Action: ...
    def generate_script(self, request: dict) -> dict: ...


class MockModelClient:
    """Deterministic test driver. This is NOT evidence of model intelligence or ReAct."""

    def next_action(self, context):
        state = context
        observed = [state["events"][-1]["seq"]] if state["events"] else []

        def act(name, arguments, summary):
            return Action(name=name, arguments=arguments, summary=summary, observes_event_ids=observed)

        def stop(code, message):
            return act("finish_task", {"status": "incomplete", "reason_code": code, "explanation": message}, message)

        last = state["last_result"]
        if last and not last["ok"]:
            if not last["retryable"] or state["failure_counts"].get(last["attempt_key"], 0) >= state["limits"]["max_attempts"]:
                return stop(last["error_code"], "工具或动作失败，保留已成功结果并停止：" + last["summary"])
        if state["retrieval"] is None:
            return act("search_materials", {"query": state["input"]["theme"], "product_id": state["input"]["product_id"]},
                       "先检索主题对应的商品与素材")
        retrieval = state["retrieval"]
        if retrieval["missing"]:
            return act("ask_user", {"missing_fields": retrieval["missing"],
                       "questions": ["请补充明确的商品标识、商品事实或可用素材。"]}, "检索资料不足，需要用户补充")
        if not state["plan"]:
            return act("update_plan", {"tier": "standard", "material_ids": [m["id"] for m in retrieval["materials"]],
                       "steps": plan_steps()}, "使用已检索素材提出标准方案，随后估算")
        plan_id = state["plan"]["id"]
        if state["solution"]:
            return act("finish_task", {"status": "completed", "explanation": "方案及脚本已保存并可回读；未制作视频或投放广告"},
                       "观察到保存回执，申请结束任务")
        if not fresh_estimate(state):
            return act("estimate_cost", {"plan_id": plan_id}, "计划或执行状态变化，重新核算预算与截止时间")
        est = state["estimate"]
        if not est["feasible"]:
            tried = {p["tier"] for p in state["plan_versions"]}
            tiers = [t for t in state["tier_order"] if t not in tried]
            if not any(m["kind"] == "reusable" for m in retrieval["materials"]):
                tiers = [t for t in tiers if t != "reuse"]
            if not tiers:
                reason = "budget_exceeded" if est["budget_gap_units"] != "0.000" else "deadline_exceeded"
                return stop(reason, f"已尝试可用档位，无可行方案；预算缺口 {est['budget_gap_units']}，时间缺口 {est['time_gap_seconds']} 秒")
            return act("update_plan", {"tier": tiers[0], "material_ids": state["plan"]["material_ids"], "steps": plan_steps()},
                       f"工具估算不可行（预算缺口 {est['budget_gap_units']}，时间缺口 {est['time_gap_seconds']} 秒），调整为 {tiers[0]} 后再估算")
        artifact = current_artifact(state)
        if artifact is None:
            return act("generate_script", {"plan_id": plan_id, "material_ids": state["plan"]["material_ids"],
                       "language": state["input"]["language"]}, "估算可行，生成有来源的离线脚本；如之前失败，按上限有限重试")
        if not state["solution"]:
            return act("save_solution", {"plan_id": plan_id, "artifact_id": artifact["id"]}, "脚本存在且复核可行，尝试保存方案")
        raise RuntimeError("无法确定下一步动作")

    def generate_script(self, request):
        product = request["retrieval"]["product"]
        selected = set(request["plan"]["material_ids"])
        segments = [{"text": fact, "source_ids": [m["id"]]}
                    for m in request["retrieval"]["materials"] if m["id"] in selected for fact in m["facts"]]
        return {"title": product["name"] + "营销内容方案（离线合成）", "segments": segments,
                "generation_note": "Mock 逐条引用合成事实，不代表真实模型创作或翻译能力"}
