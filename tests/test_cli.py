import json
import subprocess
import sys

def invoke(*args, cwd=None):
    return subprocess.run([sys.executable, "-m", "content_planner", *map(str, args)], capture_output=True, text=True, cwd=cwd)


def test_cli_round_trip(tmp_path, request_input):
    source, db, demo = tmp_path / "input.json", tmp_path / "tasks.db", tmp_path / "demo.json"
    source.write_text(json.dumps(request_input))
    demo.write_text('{"now_at":"2030-01-01T10:00:00+08:00"}')
    # Installed data must be available from outside the repository.
    run = invoke("run", "--mode", "mock", "--input", source, "--db", db,
                 "--demo-config", demo, "--output-dir", tmp_path / "examples", cwd=tmp_path)
    assert run.returncode == 0, run.stderr + run.stdout
    result = json.loads(run.stdout)
    inspect = invoke("inspect", "--request-id", request_input["request_id"], "--db", db)
    assert json.loads(inspect.stdout) == result
    exported = invoke("export", "--request-id", request_input["request_id"], "--db", db, "--output-dir", tmp_path / "export")
    assert exported.returncode == 0
    directory = tmp_path / "export" / result["run_id"]
    assert {p.name for p in directory.iterdir()} == {
        "input.json", "output.json", "trace.jsonl", "trace.md", "artifacts.json", "run-metadata.json"}
    events = [json.loads(line) for line in (directory / "trace.jsonl").read_text().splitlines()]
    assert [e["seq"] for e in events] == list(range(1, len(events) + 1))
    assert events[-1]["status"] == "completed"


def test_real_missing_credentials_never_falls_back(tmp_path, monkeypatch):
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    monkeypatch.delenv("DASHSCOPE_BASE_URL", raising=False)
    for name in ['OPENAI_API_KEY', 'OPENAI_BASE_URL', 'OPENAI_MODEL']:
        monkeypatch.delenv(name, raising=False)
    config=tmp_path/'.env'
    config.write_text('OPENAI_API_KEY=\nOPENAI_BASE_URL=\nOPENAI_MODEL=unit-test-model\n')
    run = invoke("run", "--mode", "real", "--env-file", config, "--input", tmp_path / "nonexistent.json", "--db", tmp_path / "real.db")
    assert run.returncode == 5
    result = json.loads(run.stdout)
    assert result["mode"] == "real"
    assert result["reason_code"] == "configuration_error"
    assert not (tmp_path / "real.db").exists()


def test_broken_json(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{broken")
    run = invoke("run", "--mode", "mock", "--input", path)
    assert run.returncode == 4
    assert json.loads(run.stdout)["reason_code"] == "invalid_input"


def test_unknown_request(tmp_path):
    run = invoke("inspect", "--request-id", "missing", "--db", tmp_path / "missing.db")
    assert run.returncode == 4
    assert not (tmp_path / "missing.db").exists()


def test_readable_output_and_explicit_json(tmp_path, request_input):
    source = tmp_path / "input.json"
    source.write_text(json.dumps(request_input))
    demo = tmp_path / "demo.json"
    demo.write_text('{"now_at":"2030-01-01T10:00:00+08:00"}')
    args = ("run", "--mode", "mock", "--input", source, "--demo-config", demo, "--db", tmp_path / "tasks.db")
    text = invoke(*args, "--format", "text")
    assert text.returncode == 0 and "结果：已完成" in text.stdout
    assert "脚本：" in text.stdout and "来源：M001" in text.stdout
    assert "正在请求Mock" in text.stderr
    encoded = invoke(*args, "--format", "json")
    assert json.loads(encoded.stdout)["replayed"] is True
    assert "正在请求" not in encoded.stderr


def test_chat_cli_multiturn_and_resume(tmp_path):
    command = [sys.executable, "-m", "content_planner", "chat", "--mode", "mock", "--session", "cli-test",
               "--db", str(tmp_path / "chat.db"), "--output-dir", str(tmp_path / "output")]
    run = subprocess.run(command, input="咖啡杯营销\n预算10\n一小时后截止\n/exit\n", capture_output=True, text=True, cwd=tmp_path)
    assert run.returncode == 0 and "结果：已完成" in run.stdout
    assert "会话已保存" in run.stdout and "请补充：预算、截止时间" in run.stdout
    resumed = subprocess.run(command, input="/status\n/exit\n", capture_output=True, text=True, cwd=tmp_path)
    assert resumed.returncode == 0 and "回读核验通过" in resumed.stdout
    assert "正在请求Mock" not in resumed.stdout
