import json
import platform
import hashlib
from importlib.metadata import version
from importlib.resources import files
from pathlib import Path


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def export_evidence(state, result, directory):
    if state is None:
        state = {"run_id": result["run_id"], "task_id": None, "raw_input": result.get("input"),
                 "input_hash": None, "catalog_version": None, "limits": None, "demo": None,
                 "started_at": None, "wall_seconds": None, "events": [], "artifacts": {}}
    directory = Path(directory) / state["run_id"]
    directory.mkdir(parents=True, exist_ok=True)
    write_json(directory / "input.json", state["raw_input"])
    write_json(directory / "output.json", result)
    write_json(directory / "artifacts.json", state["artifacts"])
    real = result.get("mode") == "real"
    metadata = {"mode": result["mode"], "model_driver": result["model_driver"],
                "provider_usage": result.get("provider_usage"), "model_config": state.get("model_config"),
                "real_api_requests": result.get("provider_usage", {}).get("real_api_requests", 0),
                "validation_scope": "真实模型与本地合成工具，非真实视频服务" if real else "仅验证离线流程，不证明真实模型决策效果",
                "run_id": state["run_id"], "task_id": state["task_id"], "input_hash": state["input_hash"],
                "catalog_hash": state["catalog_version"], "limits": state["limits"], "demo": state["demo"],
                "started_at": state["started_at"], "wall_seconds": state["wall_seconds"],
                "python": platform.python_version(), "pydantic": version("pydantic"),
                "package_version": version("content-planning-agent"),
                "replayed": result.get("replayed", False)}
    sources = {p.name: p.read_text(encoding="utf-8") for p in files("content_planner").iterdir() if p.name.endswith(".py")}
    metadata["implementation_hash"] = hashlib.sha256(json.dumps(sources, sort_keys=True).encode()).hexdigest()
    metadata["prompt_hash"] = (state.get("model_config") or {}).get("prompt_hash")
    metadata["prompt_note"] = "真实模型系统提示词摘要" if real else "离线策略没有调用真实模型或模型提示词"
    if real and metadata["real_api_requests"] == 0:
        metadata["validation_scope"] = "真实模式的预检查或历史结果回放；本次未向模型发送请求"
    write_json(directory / "run-metadata.json", metadata)
    (directory / "trace.jsonl").write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in state["events"]), encoding="utf-8")
    lines = ["# " + ("真实百炼模型执行记录" if real else "离线 Mock 实际执行记录"), "",
             "> " + ("模型经原生工具调用作决策；业务工具使用本地合成数据。" if real else "固定策略测试驱动，不是真实模型 ReAct 证据。"), "",
             f"运行：`{state['run_id']}`；终态：`{result['status']}`；回放：`{result.get('replayed', False)}`。", ""]
    if not state["events"]:
        lines.extend(["请求在预检查阶段拒绝，没有调用决策驱动或业务工具。", "", result["explanation"], ""])
    for event in state["events"]:
        lines.extend([f"## {event['seq']}. {event['kind']}", "", event.get("summary", ""), "",
                      "```json", json.dumps(event, ensure_ascii=False, indent=2), "```", ""])
    (directory / "trace.md").write_text("\n".join(lines), encoding="utf-8")
    return directory
