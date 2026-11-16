import json
from concurrent.futures import Future
from pathlib import Path

import pytest
from click.testing import CliRunner
from latch_eval_tools.harness import runner as harness_runner
from scbench import cli


class ImmediateExecutor:
    def __init__(self, max_workers):
        self.max_workers = max_workers

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def submit(self, function, *args):
        future = Future()
        future.set_result(function(*args))
        return future


@pytest.mark.parametrize("parallel", [1, 2])
def test_batch_canonical_evals_excludes_manifest(tmp_path, monkeypatch, parallel):
    eval_dir = Path(__file__).resolve().parents[1] / "evals"
    evals = [
        json.loads(path.read_text())
        for path in eval_dir.rglob("*.json")
        if path.name != "manifest.json"
    ]
    answers = {item["task"]: item["grader"]["config"]["ground_truth"] for item in evals}
    downloads = []

    def setup_workspace(eval_id, *args):
        work_dir = tmp_path / eval_id
        work_dir.mkdir()
        return work_dir

    monkeypatch.setattr(harness_runner, "setup_workspace", setup_workspace)
    monkeypatch.setattr(harness_runner, "download_data", lambda *args: [])
    monkeypatch.setattr(
        harness_runner, "cleanup_workspace", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(cli, "batch_download_datasets", downloads.append)
    monkeypatch.setitem(
        cli.agent_registry,
        "minisweagent",
        ("mock", lambda task, work_dir, **kwargs: answers[task]),
    )
    monkeypatch.setattr(cli, "ProcessPoolExecutor", ImmediateExecutor)
    output = tmp_path / "results"

    result = CliRunner().invoke(
        cli.main,
        [
            "batch",
            str(eval_dir),
            "--agent",
            "minisweagent",
            "--parallel",
            str(parallel),
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0, result.output
    summary = json.loads((output / "batch_results.json").read_text())
    assert summary["metadata"]["total_evals"] == 6
    assert summary["metadata"]["passed"] == 6
    assert summary["metadata"]["errors"] == 0
    assert summary["metadata"]["pass_rate"] == 100.0
    assert {item["test_id"] for item in summary["results"]} == {
        item["id"] for item in evals
    }
    assert len(downloads) == 1
