import hashlib
import json
from datetime import datetime, timedelta, timezone
from importlib.resources import files
from pathlib import Path

from .schemas import milliunits, units


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


class Clock:
    def __init__(self, fixed: datetime | None = None):
        self.fixed = fixed

    def now(self) -> datetime:
        return self.fixed or datetime.now(timezone.utc)


class Catalog:
    def __init__(self, directory: Path | None = None):
        root = directory or files("content_planner.data")
        self.raw = {name: json.loads(root.joinpath(name + ".json").read_text(encoding="utf-8"))
                    for name in ("products", "materials", "pricing", "durations", "rules")}
        self.version = digest(self.raw)
        self.products = {p["id"]: p for p in self.raw["products"]}
        self.materials = {m["id"]: m for m in self.raw["materials"]}
        if len(self.products) != len(self.raw["products"]) or len(self.materials) != len(self.raw["materials"]):
            raise ValueError("重复的数据标识")
        self.pricing, self.durations, self.rules = (self.raw[n] for n in ("pricing", "durations", "rules"))
        tiers = {"standard", "reuse", "minimal"}
        if set(self.rules["tier_order"]) != tiers or len(self.rules["tier_order"]) != 3:
            raise ValueError("方案档位配置无效")
        values = [v for row in self.pricing["tiers"].values() for v in row.values()]
        values += [self.pricing[k] for k in ("search_milliunits", "estimate_milliunits", "save_milliunits")]
        values += list(self.durations["script_seconds"].values())
        values += [self.durations[k] for k in ("search_seconds", "estimate_seconds", "save_seconds")]
        if any(type(v) is not int or v < 0 for v in values):
            raise ValueError("费用和耗时须为非负整数")
        # Free discovery/estimation keeps the financial guard independent of recursive estimates.
        if self.pricing["search_milliunits"] or self.pricing["estimate_milliunits"] or self.durations["estimate_seconds"]:
            raise ValueError("第一阶段要求检索/估算免费且估算耗时为零")
        for tier in tiers:
            self.pricing["tiers"][tier]["script_milliunits"]
            self.pricing["tiers"][tier]["resource_milliunits"]
            self.durations["script_seconds"][tier]
        for material in self.materials.values():
            if material["product_id"] not in self.products:
                raise ValueError("素材引用未知商品")


def effective_now(state, clock):
    start = datetime.fromisoformat(state["started_at"])
    return max(clock.now(), start + timedelta(seconds=state["simulated_seconds"]))


def script_key(state):
    p = state["plan"]
    return digest({"theme": state["input"]["theme"], "product": state["product_id"],
                   "audience": state["input"]["audience"], "platform": state["input"]["platform"],
                   "language": state["input"]["language"], "tier": p["tier"],
                   "materials": sorted(p["material_ids"]), "catalog": state["catalog_version"]})


def current_artifact(state):
    if not state["plan"]:
        return None
    return next((a for a in state["artifacts"].values() if a["fingerprint"] == script_key(state)), None)


def estimate_signature(state):
    return digest({"plan": state["plan"], "ledger_version": len(state["ledger"]),
                   "seconds": state["simulated_seconds"], "artifact": (current_artifact(state) or {}).get("id"),
                   "catalog": state["catalog_version"]})


def fresh_estimate(state):
    return bool(state["estimate"] and state["estimate"]["signature"] == estimate_signature(state))


def estimate(state, catalog, clock):
    plan = state["plan"]
    tier = plan["tier"]
    pricing = catalog.pricing["tiers"][tier]
    spent = sum(entry["milliunits"] for entry in state["ledger"])
    draft_needed = current_artifact(state) is None
    save_needed = state["solution"] is None
    remaining = (pricing["script_milliunits"] if draft_needed else 0) + (catalog.pricing["save_milliunits"] if save_needed else 0)
    resource = pricing["resource_milliunits"]
    seconds = (catalog.durations["script_seconds"][tier] if draft_needed else 0) + (catalog.durations["save_seconds"] if save_needed else 0)
    finishes = effective_now(state, clock) + timedelta(seconds=seconds)
    deadline = datetime.fromisoformat(state["input"]["deadline_at"])
    budget = milliunits(state["input"]["budget_units"])
    deficit = max(0, spent + remaining + resource - budget)
    time_deficit = max(0, (finishes - deadline).total_seconds())
    return {"signature": estimate_signature(state), "plan_id": plan["id"],
            "simulated_spent_units": units(spent), "remaining_tool_units": units(remaining),
            "planned_resource_units": units(resource), "projected_total_units": units(spent + remaining + resource),
            "budget_units": units(budget), "budget_gap_units": units(deficit),
            "estimated_finish_at": finishes.isoformat(), "deadline_at": deadline.isoformat(),
            "remaining_seconds": seconds, "time_gap_seconds": time_deficit,
            "feasible": deficit == 0 and time_deficit == 0}
