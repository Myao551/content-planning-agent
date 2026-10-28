"""Explicit dotenv configuration; never mutate the process environment."""
import json
import os
from pathlib import Path

from dotenv import dotenv_values


def settings(env_file: Path | None = None):
    path = env_file if env_file is not None else Path.cwd() / ".env"
    if env_file is not None and not path.is_file():
        raise ValueError("指定的 .env 配置文件不存在")
    file_values = dotenv_values(path, encoding="utf-8-sig", interpolate=False) if path.is_file() else {}
    return {**file_values, **os.environ}


def extra_parameters(config, *, legacy=False):
    value = config.get("OPENAI_EXTRA_BODY")
    if value is None:
        return {"enable_thinking": False} if legacy else {}
    try:
        parsed = json.loads(value)
    except (TypeError, ValueError):
        raise ValueError("OPENAI_EXTRA_BODY 必须是 JSON 对象") from None
    reserved = {"model", "messages", "tools", "tool_choice", "stream", "max_tokens", "response_format", "temperature", "parallel_tool_calls"}
    if not isinstance(parsed, dict) or reserved.intersection(parsed):
        raise ValueError("OPENAI_EXTRA_BODY 只能包含厂商扩展参数，不能覆盖消息、工具或通用调用控制参数")
    return parsed


def configured_client(*, api_key_file=None, env_file=None, base_url=None, model=None):
    from .openai_compatible import Credentials, OpenAICompatibleModelClient
    config = settings(env_file)
    legacy = api_key_file is not None or (not config.get("OPENAI_API_KEY") and bool(config.get("DASHSCOPE_API_KEY")))
    name = model or config.get("OPENAI_MODEL") or config.get("DASHSCOPE_MODEL") or ("qwen3.8-flash" if legacy else None)
    if not name or not name.strip():
        raise ValueError("请在 .env 中填写 OPENAI_MODEL，或使用 --model")
    credentials = Credentials.load(api_key_file, base_url, env_file=env_file)
    return OpenAICompatibleModelClient(credentials, name.strip(), extra_body=extra_parameters(config, legacy=legacy))
