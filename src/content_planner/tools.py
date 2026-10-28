import copy
from uuid import uuid4

from .policy import current_artifact, digest, effective_now, estimate, fresh_estimate, script_key
from .schemas import AskArgs, FinishArgs, PlanArgs, PlanRef, SaveArgs, ScriptArgs, ScriptArtifact, SearchArgs

BUSINESS_TOOLS = {"search_materials", "generate_script", "estimate_cost", "save_solution"}
CONTRACTS = {"search_materials": SearchArgs, "update_plan": PlanArgs, "generate_script": ScriptArgs,
             "estimate_cost": PlanRef, "save_solution": SaveArgs, "ask_user": AskArgs, "finish_task": FinishArgs}


class BusinessError(Exception):
    def __init__(self, code, message, retryable=False):
        self.code, self.message, self.retryable = code, message, retryable
        super().__init__(message)


def plan_steps():
    return [{"id": "materials", "action": "search_materials", "depends_on": []},
            {"id": "script", "action": "generate_script", "depends_on": ["materials"]},
            {"id": "verification", "action": "estimate_cost", "depends_on": ["script"]},
            {"id": "save", "action": "save_solution", "depends_on": ["verification"]}]


class Tools:
    def __init__(self, catalog, clock, model, limits):
        self.catalog, self.clock, self.model, self.limits = catalog, clock, model, limits

    def validate(self, state, action):
        if action.name not in CONTRACTS:
            raise BusinessError("unknown_action", "未知动作，未执行")
        args = CONTRACTS[action.name].model_validate(action.arguments)
        if isinstance(args, PlanRef):
            if not state["plan"] or args.plan_id != state["plan"]["id"]:
                raise BusinessError("invalid_plan", "必须引用当前计划")
        if action.name in {"generate_script", "save_solution"}:
            if not fresh_estimate(state):
                raise BusinessError("stale_estimate", "状态变化后须重新估算")
            if not estimate(state, self.catalog, self.clock)["feasible"]:
                raise BusinessError("constraint_violation", "当前预算或截止时间不允许执行")
        if isinstance(args, ScriptArgs):
            if sorted(args.material_ids) != sorted(state["plan"]["material_ids"]) or args.language != state["input"]["language"]:
                raise BusinessError("dependency_mismatch", "脚本输入必须匹配已估算计划")
        if isinstance(args, SaveArgs):
            artifact = current_artifact(state)
            if not artifact or args.artifact_id != artifact["id"]:
                raise BusinessError("missing_artifact", "缺少与当前计划匹配的成功脚本")
        return args

    def charge(self, state, call_id, amount, seconds):
        if amount:
            state["ledger"].append({"id": str(uuid4()), "call_id": call_id, "milliunits": amount})
        state["simulated_seconds"] += seconds

    def search_materials(self, state, args):
        q = args.query.lower()
        if args.product_id:
            candidates = [self.catalog.products[args.product_id]] if args.product_id in self.catalog.products else []
        else:
            candidates = [p for p in self.catalog.products.values()
                          if any(k.lower() in q for k in [p["name"], *p["keywords"]])]
        if len(candidates) != 1:
            state["retrieval"] = {"product": None, "materials": [], "candidates": [p["id"] for p in candidates],
                                  "missing": ["unambiguous_product"]}
        else:
            product = candidates[0]
            materials = [dict(m, match_reason="商品标识匹配", score=sum(k.lower() in q for k in m["keywords"]))
                         for m in self.catalog.materials.values()
                         if m["product_id"] == product["id"] and (args.kind is None or m["kind"] == args.kind)]
            materials.sort(key=lambda m: (-m["score"], m["id"]))
            state["product_id"] = product["id"]
            state["retrieval"] = {"product": product, "materials": materials,
                                  "missing": [] if product["facts"] and materials else ["product_facts_or_materials"]}
        return state["retrieval"]

    def update_plan(self, state, args):
        retrieval = state["retrieval"]
        available = {m["id"]: m for m in (retrieval or {}).get("materials", [])}
        if not retrieval or not retrieval["product"] or not retrieval["product"]["facts"]:
            raise BusinessError("missing_material", "缺少已检索的商品事实")
        if len(set(args.material_ids)) != len(args.material_ids) or not set(args.material_ids) <= available.keys():
            raise BusinessError("missing_material", "计划只能使用检索到的唯一素材标识")
        if args.tier == "reuse" and not any(available[i]["kind"] == "reusable" for i in args.material_ids):
            raise BusinessError("tier_unavailable", "复用方案需要可复用素材")
        # The declared dependency graph must also describe the mandatory business dependencies.
        if [s.model_dump() for s in args.steps] != plan_steps():
            raise BusinessError("invalid_dependencies", "第一版计划使用 materials → script → verification → save 依赖骨架")
        state["plan_versions"].append({"id": "plan-" + str(len(state["plan_versions"]) + 1), **args.model_dump()})
        state["plan"] = state["plan_versions"][-1]
        state["estimate"] = None
        return state["plan"]

    def execute(self, state, action, args, call_id):
        """Mutate only the candidate state. Agent commits it after a successful transaction."""
        name = action.name
        if name == "search_materials":
            result = self.search_materials(state, args)
            self.charge(state, call_id, 0, self.catalog.durations["search_seconds"])
            return result, None
        if name == "update_plan":
            return self.update_plan(state, args), None
        if name == "estimate_cost":
            state["estimate"] = estimate(state, self.catalog, self.clock)
            return state["estimate"], None
        if name == "generate_script":
            cached = current_artifact(state)
            if cached:
                return {"artifact_id": cached["id"], "cached": True}, None
            if state["counts"]["model_calls"] >= self.limits.max_model_calls:
                raise BusinessError("model_call_limit", "脚本生成会超过模型调用上限")
            state["counts"]["model_calls"] += 1
            generated = ScriptArtifact.model_validate(self.model.generate_script(copy.deepcopy(state))).model_dump()
            selected = {i: self.catalog.materials[i] for i in state["plan"]["material_ids"]}
            for segment in generated["segments"]:
                if any(i not in selected or segment["text"] not in selected[i]["facts"] for i in segment["source_ids"]):
                    raise BusinessError("unsupported_fact", "当前严格事实模式只允许逐条引用所选素材的事实")
            artifact = {**generated, "id": str(uuid4()), "fingerprint": script_key(state), "mode": state.get("mode", "mock"),
                        "material_ids": list(state["plan"]["material_ids"])}
            state["artifacts"][artifact["id"]] = artifact
            self.charge(state, call_id, self.catalog.pricing["tiers"][state["plan"]["tier"]]["script_milliunits"],
                        self.catalog.durations["script_seconds"][state["plan"]["tier"]])
            return {"artifact_id": artifact["id"], "cached": False, "script": artifact}, None
        if name == "save_solution":
            if state["solution"]:
                if state["solution"]["plan_id"] != args.plan_id:
                    raise BusinessError("already_saved", "任务已有不同的最终方案，不能覆盖")
                return {"solution_id": state["solution"]["id"], "cached": True}, None
            self.charge(state, call_id, self.catalog.pricing["save_milliunits"], self.catalog.durations["save_seconds"])
            solution = {"id": str(uuid4()), "plan_id": args.plan_id, "artifact_id": args.artifact_id,
                        "plan": state["plan"], "script": current_artifact(state),
                        "saved_at": effective_now(state, self.clock).isoformat()}
            state["solution"] = solution
            solution["costs"] = estimate(state, self.catalog, self.clock)
            return {"solution_id": solution["id"], "saved_at": solution["saved_at"], "saved": True}, solution
        if name == "ask_user":
            state.update(status="needs_input", reason_code="missing_information", explanation=action.summary,
                         missing_fields=args.missing_fields, questions=args.questions)
            return args.model_dump(), None
        if name == "finish_task":
            if args.status == "completed" and not state["solution"]:
                raise BusinessError("false_completion", "没有保存回执，不能完成任务")
            state.update(status=args.status, reason_code=args.reason_code, explanation=args.explanation or action.summary)
            return {"status": state["status"]}, None
        raise BusinessError("unknown_action", "未知动作")
