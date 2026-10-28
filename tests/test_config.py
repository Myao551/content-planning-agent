import io
import json

import pytest

from content_planner.config import configured_client, settings
from content_planner.openai_compatible import Credentials, OpenAICompatibleModelClient


@pytest.fixture(autouse=True)
def isolated_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for key in ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL", "OPENAI_EXTRA_BODY", "DASHSCOPE_API_KEY", "DASHSCOPE_BASE_URL", "DASHSCOPE_MODEL"]:
        monkeypatch.delenv(key, raising=False)


def write_config(path, key="TEST-KEY", url="https://another-provider.example/v1", model="other-tool-model"):
    path.write_text(f'OPENAI_API_KEY="{key}"\nOPENAI_BASE_URL={url}\nOPENAI_MODEL={model}\n', encoding="utf-8")


def test_loads_current_directory_dotenv_without_mutating_environment(tmp_path):
    import os
    write_config(tmp_path/".env")
    client = configured_client()
    assert client.credentials.api_key == "TEST-KEY"
    assert client.credentials.base_url == "https://another-provider.example/v1"
    assert client.model_name == "other-tool-model"
    assert "OPENAI_API_KEY" not in os.environ
    assert client.extra_body == {}


def test_explicit_env_file_and_cli_override(tmp_path):
    path = tmp_path/"custom.env"
    write_config(path)
    client = configured_client(env_file=path, base_url="https://cli.example/custom/v1", model="cli-model")
    assert client.credentials.base_url == "https://cli.example/custom/v1"
    assert client.model_name == "cli-model"


def test_process_environment_overrides_file(tmp_path, monkeypatch):
    write_config(tmp_path/".env")
    monkeypatch.setenv("OPENAI_API_KEY", "ENV-KEY")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://environment.example/v1")
    monkeypatch.setenv("OPENAI_MODEL", "env-model")
    client = configured_client()
    assert client.credentials.api_key == "ENV-KEY" and client.model_name == "env-model"
    assert client.credentials.base_url == "https://environment.example/v1"


def test_explicit_csv_still_overrides_environment_credentials(tmp_path, monkeypatch):
    write_config(tmp_path/".env")
    monkeypatch.setenv("OPENAI_API_KEY", "ENV-KEY")
    csv = tmp_path/"local.csv"
    csv.write_text('apiKey,CSV-KEY\nopenAiCompatible,https://csv.example/v1\n')
    client = configured_client(api_key_file=csv)
    assert client.credentials.api_key == "CSV-KEY"
    assert client.credentials.base_url == "https://csv.example/v1"


@pytest.mark.parametrize("url,normalized", [
    ("https://arbitrary-provider.example/api/v1", "https://arbitrary-provider.example/api/v1"),
    ("https://arbitrary-provider.example/v1/chat/completions", "https://arbitrary-provider.example/v1"),
    ("http://localhost:11434/v1", "http://localhost:11434/v1"),
    ("http://127.0.0.1:8000/v1", "http://127.0.0.1:8000/v1"),
])
def test_generic_and_loopback_endpoints(tmp_path, url, normalized):
    write_config(tmp_path/".env", url=url)
    assert Credentials.load().base_url == normalized


@pytest.mark.parametrize("extension", ['{broken', '[]', '{"messages":[]}'])
def test_bad_extensions_rejected_without_printing_value(tmp_path, extension):
    path=tmp_path/".env"
    write_config(path)
    with path.open('a') as stream: stream.write("OPENAI_EXTRA_BODY='"+extension+"'\n")
    with pytest.raises(ValueError) as caught:
        configured_client()
    assert "TEST-KEY" not in str(caught.value)


def test_explicit_missing_env_file_is_error(tmp_path):
    with pytest.raises(ValueError, match="不存在"):
        settings(tmp_path/"missing.env")


def test_generic_payload_has_no_aliyun_flag_and_extension_is_optional(tmp_path):
    write_config(tmp_path/".env", model="non-qwen-model")
    bodies=[]
    def transport(request, **kwargs):
        bodies.append(json.loads(request.data))
        return io.BytesIO(b'{"id":"fake","choices":[{"message":{"content":"OK"}}],"usage":{"total_tokens":1}}')
    client=configured_client()
    client.transport=transport
    client.chat([{"role":"user","content":"test"}])
    assert 'enable_thinking' not in bodies[-1]
    assert bodies[-1]['model']=='non-qwen-model'
    with (tmp_path/".env").open('a') as stream: stream.write('OPENAI_EXTRA_BODY=\'{"enable_thinking":false}\'\n')
    client=configured_client(); client.transport=transport
    client.chat([{"role":"user","content":"test"}])
    assert bodies[-1]['enable_thinking'] is False
