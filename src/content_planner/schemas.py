from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")


def milliunits(value: str) -> int:
    try:
        amount = Decimal(value)
        if not amount.is_finite() or amount < 0 or amount.as_tuple().exponent < -3:
            raise ValueError("预算须为非负、最多三位小数的十进制字符串")
        if amount > Decimal("1000000000"):
            raise ValueError("预算超过支持范围")
        return int(amount * 1000)
    except InvalidOperation as exc:
        raise ValueError("预算不是有效十进制数") from exc


def units(value: int) -> str:
    return format(Decimal(value) / 1000, ".3f")


class TaskInput(Contract):
    request_id: str = Field(min_length=1, max_length=128)
    theme: str = Field(min_length=1, max_length=2000)
    budget_units: str | None = None
    deadline_at: datetime | None = None
    product_id: str | None = None
    audience: str = "普通消费者"
    platform: str = "短视频平台"
    language: str = "zh-CN"

    @field_validator("request_id", "theme")
    @classmethod
    def nonblank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("不能是空白字符串")
        return value.strip()

    @field_validator("budget_units")
    @classmethod
    def budget(cls, value: str | None) -> str | None:
        return units(milliunits(value)) if value is not None else None

    @field_validator("deadline_at")
    @classmethod
    def timezone_required(cls, value: datetime | None) -> datetime | None:
        if value is not None and value.utcoffset() is None:
            raise ValueError("截止时间必须包含时区")
        return value

    @field_validator("deadline_at", mode="before")
    @classmethod
    def iso_time(cls, value):
        if value is None or isinstance(value, datetime):
            return value
        if not isinstance(value, str) or "T" not in value:
            raise ValueError("时间须为 ISO 8601 字符串")
        return value


class PlanStep(Contract):
    id: str = Field(min_length=1)
    action: Literal["search_materials", "generate_script", "estimate_cost", "save_solution"]
    depends_on: list[str] = Field(default_factory=list)


class PlanArgs(Contract):
    tier: Literal["standard", "reuse", "minimal"]
    material_ids: list[str] = Field(min_length=1)
    steps: list[PlanStep] = Field(min_length=1)

    @model_validator(mode="after")
    def valid_dag(self):
        names = [s.id for s in self.steps]
        if len(set(names)) != len(names):
            raise ValueError("步骤标识重复")
        graph = {s.id: s.depends_on for s in self.steps}
        visited, visiting = set(), set()

        def visit(name):
            if name not in graph or name in visiting:
                raise ValueError("依赖不存在或存在循环")
            if name in visited:
                return
            visiting.add(name)
            for dep in graph[name]:
                visit(dep)
            visiting.remove(name)
            visited.add(name)

        for name in graph:
            visit(name)
        if {s.action for s in self.steps} != {"search_materials", "generate_script", "estimate_cost", "save_solution"}:
            raise ValueError("计划须包含四类业务步骤")
        return self


class SearchArgs(Contract):
    query: str = Field(min_length=1, max_length=2000)
    product_id: str | None = None
    kind: Literal["reusable", "reference"] | None = None


class PlanRef(Contract):
    plan_id: str


class ScriptArgs(PlanRef):
    material_ids: list[str] = Field(min_length=1)
    style: Literal["factual"] = "factual"
    language: str = "zh-CN"


class SaveArgs(PlanRef):
    artifact_id: str


class AskArgs(Contract):
    missing_fields: list[str] = Field(min_length=1)
    questions: list[str] = Field(min_length=1)


class FinishArgs(Contract):
    status: Literal["completed", "incomplete"]
    reason_code: str = ""
    explanation: str = ""

    @model_validator(mode="after")
    def reason_required(self):
        if self.status == "incomplete" and not self.reason_code.strip():
            raise ValueError("未完成状态必须包含原因码")
        return self


class Action(Contract):
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    summary: str = Field(min_length=1)
    observes_event_ids: list[int] = Field(default_factory=list)


class ScriptSegment(Contract):
    text: str = Field(min_length=1)
    source_ids: list[str] = Field(min_length=1)


class ScriptArtifact(Contract):
    title: str = Field(min_length=1)
    segments: list[ScriptSegment] = Field(min_length=1)
    generation_note: str


class Limits(Contract):
    max_steps: int = Field(default=12, ge=1, le=100)
    max_tools: int = Field(default=10, ge=1, le=100)
    max_model_calls: int = Field(default=16, ge=1, le=200)
    max_runtime_seconds: float = Field(default=180, gt=0, allow_inf_nan=False)
    max_attempts: int = Field(default=2, ge=1, le=5)


class Fault(Contract):
    tool: Literal["search_materials", "generate_script", "estimate_cost", "save_solution"]
    times: int | None = Field(default=1, ge=1)
    after_charge: bool = False

    @model_validator(mode="after")
    def charging_tool(self):
        if self.after_charge and self.tool != "generate_script":
            raise ValueError("after_charge 仅适用于脚本工具")
        return self


class DemoConfig(Contract):
    now_at: datetime | None = None
    faults: list[Fault] = Field(default_factory=list)

    @field_validator("now_at")
    @classmethod
    def timezone_required(cls, value):
        return TaskInput.timezone_required(value)
