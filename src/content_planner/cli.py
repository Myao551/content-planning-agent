import argparse
import json
import sqlite3
import sys
from pathlib import Path

from pydantic import ValidationError

from .agent import Agent, final_result, simple_result
from .bailian import BailianModelClient, Credentials
from .policy import Catalog, Clock
from .schemas import DemoConfig, Limits
from .storage import Storage
from .trace import export_evidence


def parser():
    root = argparse.ArgumentParser(description="内容活动规划；真实百炼模型与显式离线 Mock")
    commands = root.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run")
    run.add_argument("--mode", choices=["mock", "real"], required=True)
    run.add_argument("--input", type=Path, required=True)
    run.add_argument("--data-dir", type=Path)
    run.add_argument("--demo-config", type=Path)
    run.add_argument("--api-key-file", type=Path)
    run.add_argument("--base-url")
    run.add_argument("--model", default="qwen3.8-flash")
    run.add_argument("--max-steps", type=int, default=12)
    run.add_argument("--max-tools", type=int, default=10)
    run.add_argument("--max-model-calls", type=int, default=16)
    run.add_argument("--max-runtime-seconds", type=float, default=180)
    for command in [run, commands.add_parser("inspect"), commands.add_parser("export")]:
        command.add_argument("--db", type=Path, default=Path(".runtime/tasks.db"))
        if command is not run:
            command.add_argument("--request-id", required=True)
        if command.prog.endswith("export"):
            command.add_argument("--output-dir", type=Path, required=True)
        elif command is run:
            command.add_argument("--output-dir", type=Path)
    return root


def exit_code(result):
    if result["reason_code"] in {"real_not_implemented", "configuration_error"}:
        return 5
    return {"completed": 0, "needs_input": 2, "incomplete": 3, "invalid_input": 4}.get(result["status"], 5)


def main(argv=None):
    args = parser().parse_args(argv)
    storage = None
    state = None
    try:
        if args.command == "run":
            # Parse input before creating runtime files; bad JSON is an input error.
            model = None
            if args.mode == "real":
                model = BailianModelClient(Credentials.load(args.api_key_file, args.base_url), args.model)
            try:
                raw = json.loads(args.input.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                result = simple_result("invalid_input", "invalid_input", str(exc), mode=args.mode)
            else:
                demo = DemoConfig.model_validate_json(args.demo_config.read_text(encoding="utf-8")) if args.demo_config else DemoConfig()
                if args.mode == "real" and demo.now_at is not None:
                    raise ValueError("真实模式使用实际时钟；故障注入可用，但不能固定真实运行时间")
                limits = Limits(max_steps=args.max_steps, max_tools=args.max_tools, max_model_calls=args.max_model_calls,
                                max_runtime_seconds=args.max_runtime_seconds)
                catalog = Catalog(args.data_dir)
                storage = Storage(args.db)
                result, state = Agent(storage, catalog, Clock(demo.now_at), model=model, limits=limits, demo=demo).run(raw)
        else:
            if not args.db.exists():
                result = simple_result("invalid_input", "not_found", "任务数据库不存在")
            else:
                storage = Storage(args.db)
                state = storage.get(args.request_id)
                result = (state["result"] or final_result(state)) if state else simple_result("invalid_input", "not_found", "任务不存在")
        if getattr(args, "output_dir", None):
            directory = export_evidence(state, result, args.output_dir)
            print("Evidence: " + str(directory), file=sys.stderr)
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error, ValidationError) as exc:
        result = simple_result("incomplete", "configuration_error", str(exc), mode=getattr(args, "mode", "mock"))
    finally:
        if storage:
            storage.close()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code(result)
