"""One small configured real request; print only non-secret response metadata."""
import argparse
import json
from pathlib import Path

from content_planner.config import configured_client
from content_planner.openai_compatible import ModelAPIError

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key-file", type=Path)
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--base-url")
    parser.add_argument("--model")
    args = parser.parse_args(argv)
    try:
        client = configured_client(api_key_file=args.api_key_file, env_file=args.env_file, base_url=args.base_url, model=args.model)
    except (ValueError, OSError):
        print(json.dumps({"ok": False, "error": "配置不完整或无效：请填写 .env 的密钥、接口地址和模型，或检查指定配置文件", "usage": {"real_api_requests": 0}}, ensure_ascii=False))
        return 5
    try:
        message, _ = client.chat([{"role": "user", "content": "请只回复 OK"}], kind="connection_probe", max_tokens=32)
        print(json.dumps({"ok": True, "model": client.model_name, "reply": message.get("content"), "usage": client.usage()}, ensure_ascii=False))
        return 0
    except ModelAPIError as exc:
        print(json.dumps({"ok": False, "error": str(exc), "usage": client.usage()}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
