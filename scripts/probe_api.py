"""One small real request; print only non-secret response metadata."""
import argparse
import json
from pathlib import Path

from content_planner.bailian import BailianModelClient, Credentials, ModelAPIError

parser = argparse.ArgumentParser()
parser.add_argument("--api-key-file", type=Path, required=True)
parser.add_argument("--model", default="qwen3.8-flash")
args = parser.parse_args()
client = BailianModelClient(Credentials.load(args.api_key_file), args.model)
try:
    message, _ = client.chat([{"role": "user", "content": "请只回复 OK"}], kind="connection_probe", max_tokens=32)
    print(json.dumps({"ok": True, "reply": message.get("content"), "usage": client.usage()}, ensure_ascii=False))
except ModelAPIError as exc:
    print(json.dumps({"ok": False, "error": str(exc), "usage": client.usage()}, ensure_ascii=False))
    raise SystemExit(1)
