import argparse
import json
import sqlite3
import sys
from pathlib import Path

from pydantic import ValidationError

from .agent import Agent, final_result, simple_result
from .config import configured_client
from .conversation import Conversation
from .policy import Catalog, Clock
from .presentation import progress, render_result
from .schemas import DemoConfig, Limits
from .storage import Storage
from .trace import export_evidence


def parser():
    root = argparse.ArgumentParser(description="内容活动规划；OpenAI 兼容 API 与显式离线 Mock")
    commands = root.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run")
    run.add_argument("--mode", choices=["mock", "real"], required=True)
    run.add_argument("--input", type=Path, required=True)
    run.add_argument("--demo-config", type=Path)
    chat = commands.add_parser("chat", help="持续对话，记住需求并显示易读结果")
    chat.add_argument("--mode", choices=["mock", "real"], default="real")
    chat.add_argument("--session", help="继续已有会话，或指定新会话 ID")
    chat.add_argument("--db", type=Path, help="默认 .runtime/chat-<mode>.db")
    chat.add_argument("--output-dir", type=Path, default=Path(".runtime/chat-output"))
    for command in (run, chat):
        command.add_argument("--data-dir", type=Path)
        command.add_argument("--api-key-file", type=Path)
        command.add_argument("--env-file", type=Path)
        command.add_argument("--base-url")
        command.add_argument("--model")
        command.add_argument("--max-steps", type=int, default=12)
        command.add_argument("--max-tools", type=int, default=10)
        command.add_argument("--max-model-calls", type=int, default=16)
        command.add_argument("--max-runtime-seconds", type=float, default=180)
        command.add_argument("--quiet", action="store_true", help="隐藏逐步执行进度")
    for command in [run, commands.add_parser("inspect"), commands.add_parser("export")]:
        command.add_argument("--db", type=Path, default=Path(".runtime/tasks.db"))
        command.add_argument("--format", choices=["auto", "text", "json"], default="auto",
                             help="默认终端显示中文摘要，重定向/管道输出 JSON")
        if command is not run:
            command.add_argument("--request-id", required=True)
        if command.prog.endswith("export"):
            command.add_argument("--output-dir", type=Path, required=True)
        elif command is run:
            command.add_argument("--output-dir", type=Path)
    return root


def client_for(args):
    return configured_client(api_key_file=args.api_key_file, env_file=args.env_file, base_url=args.base_url, model=args.model)


def limits_for(args):
    return Limits(max_steps=args.max_steps, max_tools=args.max_tools, max_model_calls=args.max_model_calls,
                  max_runtime_seconds=args.max_runtime_seconds)


def run_chat(args):
    # Validate credentials before creating a database; no API request at startup.
    if args.mode == "real":
        client_for(args)
    try:
        import readline  # noqa: F401 - native line editing where available
    except ImportError:
        pass
    database = args.db or Path(f".runtime/chat-{args.mode}.db")
    storage = Storage(database)
    try:
        conversation = Conversation(storage, Catalog(args.data_dir), mode=args.mode, client_factory=lambda: client_for(args),
                                    session_id=args.session, output_dir=args.output_dir, limits=limits_for(args),
                                    on_event=None if args.quiet else lambda event: progress(event, sys.stdout))
        print("内容任务规划 Agent · 持续对话  |  " + args.mode)
        print("会话：" + conversation.session["session_id"])
        print("继续会话：python -m content_planner chat --mode " + args.mode + " --session " + conversation.session["session_id"] + " --db " + str(database))
        print("输入需求即可开始；/help 查看命令，/exit 退出。")
        if args.mode == "mock":
            print("Mock 仅支持简单中文规则和 /set，不是通用对话模型。")
        else:
            print("真实模式：自然语言理解和任务执行均可能产生 API 用量。")
        try:
            while True:
                if not conversation.turn(input("\n你 > ")):
                    break
        except (EOFError, KeyboardInterrupt):
            print("\n已停止输入或执行。")
        finally:
            storage.save_chat_session(conversation.session)
        print("会话已保存。" + conversation.usage_line())
        return 0
    finally:
        storage.close()


def exit_code(result):
    if result["reason_code"] in {"real_not_implemented", "configuration_error"}:
        return 5
    return {"completed": 0, "needs_input": 2, "incomplete": 3, "invalid_input": 4}.get(result["status"], 5)


def main(argv=None):
    args = parser().parse_args(argv)
    storage = None
    state = None
    output_format = getattr(args, "format", "text")
    human = output_format == "text" or output_format == "auto" and sys.stdout.isatty()
    try:
        if args.command == "chat":
            return run_chat(args)
        if args.command == "run":
            # Parse input before creating runtime files; bad JSON is an input error.
            model = None
            if args.mode == "real":
                model = client_for(args)
            try:
                raw = json.loads(args.input.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                result = simple_result("invalid_input", "invalid_input", str(exc), mode=args.mode)
            else:
                demo = DemoConfig.model_validate_json(args.demo_config.read_text(encoding="utf-8")) if args.demo_config else DemoConfig()
                if args.mode == "real" and demo.now_at is not None:
                    raise ValueError("真实模式使用实际时钟；故障注入可用，但不能固定真实运行时间")
                limits = limits_for(args)
                catalog = Catalog(args.data_dir)
                storage = Storage(args.db)
                observer = (lambda event: progress(event, sys.stderr)) if human and not args.quiet else None
                result, state = Agent(storage, catalog, Clock(demo.now_at), model=model, limits=limits, demo=demo, on_event=observer).run(raw)
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
    print(render_result(result, state["input"] if state else None) if human else json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code(result)
