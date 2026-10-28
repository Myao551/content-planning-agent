import io
import json
from datetime import datetime
from urllib.error import HTTPError

import pytest

from content_planner.agent import Agent
from content_planner.bailian import BailianModelClient, Credentials, ModelAPIError, tool_definitions
from content_planner.policy import Clock
from content_planner.tools import plan_steps


URL = "https://unit-test.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
FAKE_KEY = "UNIT-TEST-CREDENTIAL-NEVER-VALID"


def response(message, finish="tool_calls"):
    return io.BytesIO(json.dumps({"id": "test-response", "model": "qwen3.8-flash", "choices": [
        {"finish_reason": finish, "message": message}], "usage": {"prompt_tokens": 10, "completion_tokens": 3, "total_tokens": 13}}).encode())


def test_vertical_csv_credentials(tmp_path):
    path = tmp_path / "credentials.csv"
    path.write_text(f"id,123\napiKey,{FAKE_KEY}\nopenAiCompatible,{URL}\n", encoding="utf-8-sig")
    credentials = Credentials.load(path)
    assert credentials.api_key == FAKE_KEY and credentials.base_url == URL
    assert FAKE_KEY not in repr(credentials)


def test_reject_non_aliyun_endpoint(tmp_path):
    path = tmp_path / "credentials.csv"
    path.write_text(f"apiKey,{FAKE_KEY}\nopenAiCompatible,https://example.com/compatible-mode/v1\n")
    with pytest.raises(ModelAPIError):
        Credentials.load(path)


def test_http_error_does_not_disclose_credentials():
    def fail(req, **kwargs):
        raise HTTPError(req.full_url, 401, "provider message " + FAKE_KEY, {}, io.BytesIO(FAKE_KEY.encode()))
    client = BailianModelClient(Credentials(FAKE_KEY, URL), transport=fail)
    with pytest.raises(ModelAPIError) as caught:
        client.chat([{"role": "user", "content": "test"}])
    assert FAKE_KEY not in str(caught.value)
    assert FAKE_KEY not in json.dumps(client.usage())
    assert client.usage()["usage_complete"] is False


def test_tool_schemas_expose_public_summary_and_observations():
    definitions = tool_definitions()
    assert len(definitions) == 7
    for tool in definitions:
        schema = tool["function"]["parameters"]
        assert "decision_summary" in schema["required"]
        assert "observes_event_ids" in schema["required"]
        assert schema["additionalProperties"] is False


class ScriptedTransport:
    """Tests HTTP/tool protocol only. No real model is used by this transport."""
    def __init__(self):
        self.decisions = 0
        self.requests = []

    def __call__(self, request, **kwargs):
        assert request.get_header("Authorization") == "Bearer " + FAKE_KEY
        assert 0 < kwargs["timeout"] <= 30
        payload = json.loads(request.data)
        self.requests.append(payload)
        if payload.get("response_format"):
            return response({"role": "assistant", "content": json.dumps({"title": "咖啡杯方案", "segments": [
                {"text": "容量 350 毫升", "source_ids": ["M001"]}], "generation_note": "协议测试"})}, "stop")
        self.decisions += 1
        latest = json.loads(payload["messages"][-1]["content"].split("：", 1)[1])
        material_ids = ["M001", "M002"]
        actions = [
            ("search_materials", {"query": "咖啡杯", "product_id": "P001"}),
            ("update_plan", {"tier": "standard", "material_ids": material_ids, "steps": plan_steps()}),
            ("estimate_cost", {"plan_id": "plan-1"}),
            ("generate_script", {"plan_id": "plan-1", "material_ids": material_ids}),
            ("estimate_cost", {"plan_id": "plan-1"}),
            ("save_solution", {"plan_id": "plan-1", "artifact_id": (latest["artifact_ids"] or ["unused"])[0]}),
            ("finish_task", {"status": "completed"}),
        ]
        name, args = actions[self.decisions - 1]
        results = [json.loads(m["content"]) for m in payload["messages"] if m["role"] == "tool"]
        args = {**args, "decision_summary": "协议测试的公开动作说明", "observes_event_ids": [results[-1]["seq"]] if results else []}
        return response({"role": "assistant", "content": None, "reasoning_content": "DO_NOT_STORE_INTERNAL_CONTENT",
                         "tool_calls": [{"id": "native-" + str(self.decisions), "type": "function", "function": {
                             "name": name, "arguments": json.dumps(args)}}]})


def test_real_adapter_protocol_roundtrip_and_replay(storage, request_input):
    transport = ScriptedTransport()
    model = BailianModelClient(Credentials(FAKE_KEY, URL), transport=transport)
    agent = Agent(storage, clock=Clock(datetime.fromisoformat("2030-01-01T10:00:00+08:00")), model=model)
    result, state = agent.run(request_input)
    assert result["status"] == "completed"
    assert result["mode"] == "real"
    assert result["provider_usage"]["real_api_requests"] == 8
    assert result["provider_usage"]["tokens"]["total_tokens"] == 104
    assert state["solution"]["script"]["mode"] == "real"
    serialized = json.dumps(state)
    assert FAKE_KEY not in serialized and "DO_NOT_STORE_INTERNAL_CONTENT" not in serialized
    assert "native-1" in serialized
    # All API tool results refer to the exact original native call IDs.
    for payload in transport.requests:
        pending = set()
        for message in payload["messages"]:
            if message["role"] == "assistant":
                pending.update(c["id"] for c in message.get("tool_calls", []))
            if message["role"] == "tool":
                assert message["tool_call_id"] in pending
                pending.remove(message["tool_call_id"])
        assert not pending
    replay, _ = agent.run(request_input)
    assert replay["replayed"] and replay["provider_usage"]["real_api_requests"] == 0
    assert replay["provider_usage"]["source_run_usage"]["real_api_requests"] == 8
    assert len(transport.requests) == 8
    conflict, _ = Agent(storage).run(request_input)
    assert conflict["reason_code"] == "request_conflict"


def test_multiple_native_calls_are_not_arbitrarily_selected():
    def multiple(request, **kwargs):
        return response({"tool_calls": [{"id": "one"}, {"id": "two"}]})
    client = BailianModelClient(Credentials(FAKE_KEY, URL), transport=multiple)
    state = {"input": {}, "tier_order": [], "limits": {}, "events": [], "plan": None, "retrieval": None,
             "estimate": None, "last_result": None, "counts": {}, "simulated_seconds": 0, "artifacts": {}, "solution": None}
    with pytest.raises(ModelAPIError, match="恰好一个"):
        client.next_action(state)
