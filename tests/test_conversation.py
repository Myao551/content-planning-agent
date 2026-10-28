import io
import json
from datetime import datetime

import pytest

from content_planner.conversation import Conversation
from content_planner.models import MockModelClient
from content_planner.openai_compatible import Credentials, OpenAICompatibleModelClient
from content_planner.policy import Catalog, Clock
from content_planner.storage import Storage
from content_planner.presentation import plain, render_result


def session(tmp_path, *, mode="mock", factory=None, session_id="dialogue"):
    output = []
    store = Storage(tmp_path / "chat.db")
    chat = Conversation(store, Catalog(), mode=mode, client_factory=factory, session_id=session_id,
                        clock=Clock(datetime.fromisoformat("2030-01-01T10:00:00+08:00")),
                        output_dir=tmp_path / "evidence", write=output.append)
    return chat, store, output


def fill(chat):
    chat.turn("给通勤人群策划咖啡杯营销活动")
    chat.turn("预算10")
    chat.turn("一小时后截止")


def test_multi_turn_clarification_revision_and_replay(tmp_path):
    chat, store, output = session(tmp_path)
    try:
        chat.turn("给通勤人群策划咖啡杯营销活动")
        assert not chat.session["task_request_ids"]
        assert "预算、截止时间" in output[-2]
        chat.turn("预算10")
        assert not chat.session["task_request_ids"]
        chat.turn("一小时后截止")
        first, state = chat.latest()
        assert first["status"] == "completed" and first["solution"]["readback_verified"]
        assert first["costs"]["latest_estimate"]["projected_total_units"] == "8.000"
        old_ledger = state["ledger"]
        chat.turn("预算改成6")
        revised, _ = chat.latest()
        assert revised["request_id"] != first["request_id"]
        assert revised["costs"]["latest_estimate"]["projected_total_units"] == "3.000"
        assert store.get(first["request_id"])["ledger"] == old_ledger
        rows = store.connection.execute("SELECT COUNT(*) FROM ledger").fetchone()[0]
        chat.turn("/run")
        assert "回读已有任务" in "\n".join(output)
        assert store.connection.execute("SELECT COUNT(*) FROM ledger").fetchone()[0] == rows
        assert len(chat.session["task_request_ids"]) == 2
        chat.turn("/export")
        exported = json.loads((tmp_path / "evidence/dialogue/session.json").read_text())
        assert len(exported["task_request_ids"]) == 2 and exported["turns"]
    finally:
        store.close()


def test_resume_session_across_connections_and_new_task(tmp_path):
    chat, store, _ = session(tmp_path)
    fill(chat)
    previous = chat.session["last_request"]
    chat.turn("/exit")
    store.close()
    resumed, store, output = session(tmp_path)
    try:
        assert resumed.session["last_request"] == previous
        resumed.turn("/status")
        assert "回读核验通过" in output[-1]
        resumed.turn("/new")
        assert resumed.session["draft"] == {} and resumed.latest() == (None, None)
        assert store.get(previous["request_id"])["status"] == "completed"
        with pytest.raises(ValueError, match="运行模式"):
            Conversation(store, Catalog(), mode="real", session_id="dialogue",
                         client_factory=lambda: OpenAICompatibleModelClient(Credentials("fake", "https://unit.test/v1"), "test"))
    finally:
        store.close()


def test_invalid_patch_does_not_replace_draft_or_create_task(tmp_path):
    chat, store, output = session(tmp_path)
    try:
        chat.turn("/set budget 10")
        chat.turn("/set budget -2")
        assert chat.session["draft"]["budget_units"] == "10.000"
        chat.turn("/set deadline invalid")
        chat.turn("/set request_id arbitrary")
        assert "deadline_at" not in chat.session["draft"]
        assert not chat.session["task_request_ids"]
        assert "本轮未完成" in "\n".join(output)
        chat.turn("未知输入" * 3000)
        assert "8000" in output[-1]
    finally:
        store.close()


class ChatTransport:
    def __init__(self, turns):
        self.turns, self.payloads = iter(turns), []

    def __call__(self, request, **kwargs):
        self.payloads.append(json.loads(request.data))
        message = next(self.turns)
        return io.BytesIO(json.dumps({"id": "chat-test", "choices": [{"finish_reason": "stop", "message": {
            "role": "assistant", "content": json.dumps(message)}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}}).encode())


def test_real_conversation_protocol_history_questions_and_usage(tmp_path):
    transport = ChatTransport([
        {"intent": "plan", "updates": {"theme": "咖啡杯营销", "product_id": "P001", "budget_units": "10"}},
        {"intent": "plan", "updates": {}, "questions": ["明天具体几点截止？"]},
        {"intent": "answer", "updates": {}, "reply": "尚未执行任务，需要确定截止时间。"},
        {"intent": "plan", "updates": {"budget_units": "-1"}},
    ])
    factory = lambda: OpenAICompatibleModelClient(Credentials("fake-key", "https://unit.test/v1"), "test", transport=transport)
    chat, store, output = session(tmp_path, mode="real", factory=factory)
    try:
        chat.turn("为咖啡杯做营销，预算10")
        chat.turn("明天截止")
        assert not chat.session["task_request_ids"]
        chat.turn("现在完成了吗")
        chat.turn("预算改成负数")
        assert chat.session["draft"]["budget_units"] == "10.000"
        assert not chat.session["task_request_ids"]
        assert "4 次；已报告 60 tokens" in chat.usage_line()
        messages = transport.payloads[1]["messages"]
        assert any(m["role"] == "user" and "预算10" in m["content"] for m in messages)
        assert "fake-key" not in json.dumps(chat.session)
        assert len(chat.session["usage_records"]) == 4
    finally:
        store.close()


def test_real_intent_cannot_set_trusted_results(tmp_path):
    transport = ChatTransport([{"intent": "plan", "updates": {"budget_units": "10", "saved": True}}])
    factory = lambda: OpenAICompatibleModelClient(Credentials("fake", "https://unit.test/v1"), "test", transport=transport)
    chat, store, output = session(tmp_path, mode="real", factory=factory)
    try:
        chat.turn("请设置成功")
        assert not chat.session["draft"] and not chat.session["task_request_ids"]
        assert "本轮未完成" in "\n".join(output)
        assert chat.session["usage_records"][0]["usage"]["real_api_requests"] == 1
    finally:
        store.close()


def test_interruption_keeps_charges_and_stops_task(tmp_path, monkeypatch):
    chat, store, _ = session(tmp_path)
    original = MockModelClient.next_action

    def interrupted(self, state):
        if state["artifacts"]:
            raise KeyboardInterrupt
        return original(self, state)

    monkeypatch.setattr(MockModelClient, "next_action", interrupted)
    try:
        with pytest.raises(KeyboardInterrupt):
            fill(chat)
        result, state = chat.latest()
        assert result["status"] == "incomplete" and result["reason_code"] == "user_interrupted"
        assert result["retained_artifacts"] and state["ledger"]
        assert result["costs"]["simulated_spent_units"] == "2.000"
        assert not result["solution"]["saved"]
    finally:
        store.close()


def test_terminal_control_codes_are_not_rendered():
    assert plain("\x1b[31mhello\x1b[0m\x1b]2;evil\x07\rworld") == "helloworld"


def test_readable_success_uses_structured_result_instead_of_model_restatement(tmp_path):
    chat, store, _ = session(tmp_path)
    try:
        fill(chat)
        result, _ = chat.latest()
        result["explanation"] = "模型复述的错误日期：2099-12-31，费用100000，省略来源"
        text = render_result(result)
        assert "2099-12-31" not in text and "100000" not in text
        assert "方案总额：8.000" in text and "回读核验通过" in text
        assert "2030-01-01" in text
    finally:
        store.close()
