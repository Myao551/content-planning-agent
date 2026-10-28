import copy
import json
from pathlib import Path

from content_planner import provenance
from content_planner.agent import Agent
from content_planner.trace import export_evidence


def test_replay_keeps_execution_hash_when_source_and_exporter_change(run_task, storage, request_input, tmp_path, monkeypatch):
    package = tmp_path / "source-package"
    package.mkdir()
    source = package / "sample.py"
    source.write_text("VERSION = 1\n")
    monkeypatch.setattr(provenance, "files", lambda name: package)
    first, state = run_task()
    frozen = copy.deepcopy(state["execution_version"])
    first_dir = export_evidence(state, first, tmp_path / "first")
    source.write_text("VERSION = 2\n")
    replay, replay_state = Agent(storage).run(request_input)
    second_dir = export_evidence(replay_state, replay, tmp_path / "replay")
    before = json.loads((first_dir / "run-metadata.json").read_text())
    after = json.loads((second_dir / "run-metadata.json").read_text())
    assert replay["replayed"]
    assert first["run_id"] == replay["run_id"]
    assert before["execution_version"] == after["execution_version"] == frozen
    assert before["implementation_hash"] == after["implementation_hash"] == frozen["implementation_hash"]
    assert before["exporter_version"]["implementation_hash"] != after["exporter_version"]["implementation_hash"]
    assert storage.get(request_input["request_id"])["execution_version"] == frozen


def test_legacy_replay_never_claims_current_execution_version(run_task, storage, request_input, tmp_path):
    original, state = run_task()
    state.pop("execution_version")
    state["result"].pop("execution_version")
    storage.commit(state)
    result, legacy = Agent(storage).run(request_input)
    directory = export_evidence(legacy, result, tmp_path / "legacy")
    meta = json.loads((directory / "run-metadata.json").read_text())
    assert result["execution_version"]["status"] == "unknown_legacy"
    assert meta["execution_version"]["status"] == "unknown_legacy"
    assert meta["implementation_hash"] is None and meta["python"] is None
    assert meta["exporter_version"]["implementation_hash"]
    assert "execution_version" not in storage.get(request_input["request_id"])


def test_stateless_rejection_has_no_execution_snapshot(tmp_path):
    from content_planner.agent import simple_result
    result = simple_result("invalid_input", "invalid_input", "invalid")
    directory = export_evidence(None, result, tmp_path)
    meta = json.loads((directory / "run-metadata.json").read_text())
    assert meta["execution_version"]["status"] == "not_started"
    assert meta["implementation_hash"] is None
    assert meta["exported_at"]


def test_new_execution_snapshot_persisted_with_task(run_task, storage, request_input):
    result, state = run_task()
    snapshot = state["execution_version"]
    assert snapshot["status"] == "captured"
    assert snapshot["capture_phase"] == "task_creation"
    assert snapshot["implementation_hash"] and snapshot["python"]
    assert result["execution_version"] == storage.get(request_input["request_id"])["execution_version"]


def test_wheel_snapshot_does_not_borrow_caller_git_commit(tmp_path, monkeypatch):
    package = tmp_path / "installed" / "site-packages" / "content_planner"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("# installed wheel fixture\n")
    monkeypatch.setattr(provenance, "files", lambda name: package)
    snapshot = provenance.capture_runtime_version()
    assert snapshot["implementation_hash"]
    assert snapshot["git_commit"] is None and snapshot["git_dirty"] is None


def test_git_metadata_only_for_editable_checkout():
    snapshot = provenance.capture_runtime_version()
    root = Path(__file__).resolve().parents[1]
    if Path(provenance.__file__).resolve().is_relative_to(root / "src"):
        assert snapshot["git_commit"] and len(snapshot["git_commit"]) == 40
        assert isinstance(snapshot["git_dirty"], bool)
    else:
        assert snapshot["git_commit"] is None
    assert "examples" not in snapshot["git_dirty_scope"]


def test_regenerating_offline_report_preserves_real_scope(tmp_path):
    import importlib.util
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("generate_examples_for_test", root / "scripts/generate_examples.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.__file__ = str(tmp_path / "scripts/generate_examples.py")
    (tmp_path / "docs").mkdir()
    real = tmp_path / "docs/06-real-api-evaluation.md"
    real.write_text("Existing real evidence stays unchanged\n")
    assert module.main() == 0
    report = (tmp_path / "docs/03-evaluation.md").read_text()
    assert "真实模型接入留到下一阶段" not in report
    assert "真实模型决策待验证" not in report
    assert "本页仅统计离线" in report and "06-real-api-evaluation.md" in report
    assert real.read_text() == "Existing real evidence stays unchanged\n"


def test_frozen_evaluation_refuses_dirty_code_before_loading_credentials(monkeypatch):
    import importlib.util
    import sys
    import pytest
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("evaluate_real_for_test", root / "scripts/evaluate_real.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "capture_runtime_version", lambda **kwargs: {"git_commit": "a" * 40, "git_dirty": True})
    def should_not_load(**kwargs):
        raise AssertionError("dirty evaluation must stop before credentials or network")
    monkeypatch.setattr(module, "configured_client", should_not_load)
    monkeypatch.setattr(sys, "argv", ["evaluate_real.py", "--require-clean", "--cases", "normal"])
    with pytest.raises(ValueError, match="尚未发送 API 请求"):
        module.main()
