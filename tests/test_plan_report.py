"""The release gate's logic, tested like any other code."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import plan_report  # noqa: E402


def write(tmp_path, name, plan):
    path = tmp_path / name
    path.write_text(json.dumps({"plan": plan}))
    return path


def entry(action, **changes):
    return {"action": action, "changes": {k: {"action": v} for k, v in changes.items()}}


def test_summary_lists_actions_and_hides_noise(tmp_path):
    plan = {
        "resources.jobs.daily": entry(
            "update", timeout_seconds="update", **{"tags['git_commit']": "update"}
        ),
        "resources.schemas.gold": entry("skip"),
        "resources.volumes.landing_files": entry("delete"),
    }
    text = plan_report.summary(write(tmp_path, "p.json", plan))
    assert "`resources.jobs.daily` | **update** | `timeout_seconds`" in text
    assert "git_commit" not in text
    assert "**delete** ⚠️" in text
    assert "schemas.gold" not in text


def test_summary_no_changes(tmp_path):
    text = plan_report.summary(write(tmp_path, "p.json", {"resources.jobs.x": entry("skip")}))
    assert "No changes." in text


def test_compare_ignores_field_values(tmp_path):
    a = write(tmp_path, "a.json", {"resources.jobs.ingest": entry("update", x="update")})
    b = write(tmp_path, "b.json", {"resources.jobs.ingest": entry("update", y="update")})
    assert plan_report.compare(a, b) == 0


def test_compare_catches_a_new_delete(tmp_path, capsys):
    a = write(tmp_path, "a.json", {"resources.jobs.ingest": entry("update")})
    b = write(
        tmp_path,
        "b.json",
        {"resources.jobs.ingest": entry("update"), "resources.schemas.gold": entry("delete")},
    )
    assert plan_report.compare(a, b) == 1
    assert "MISMATCH resources.schemas.gold" in capsys.readouterr().out


def test_cli_usage(capsys):
    assert plan_report.main([]) == 2


def test_drift_ignores_planned_changes(tmp_path):
    planned = {"action": "update", "old": "a.whl", "new": "b.whl", "remote": "a.whl"}
    plan = {"resources.jobs.ingest": {"action": "update", "changes": {"dependencies": planned}}}
    assert plan_report.drift(write(tmp_path, "p.json", plan)) == 0


def test_drift_catches_workspace_edits(tmp_path, capsys):
    edited = {"action": "update", "remote": 60}
    unlocked = {"action": "update", "old": "UI_LOCKED", "new": "UI_LOCKED", "remote": "EDITABLE"}
    changes = {"timeout_seconds": edited, "edit_mode": unlocked}
    plan = {"resources.jobs.daily": {"action": "update", "changes": changes}}
    assert plan_report.drift(write(tmp_path, "p.json", plan)) == 1
    out = capsys.readouterr().out
    assert "timeout_seconds: deployed=None workspace=60" in out
    assert "edit_mode" in out


def test_drift_ignores_server_side_defaults(tmp_path):
    default = {"action": "skip", "remote": "ALL_SUCCESS"}
    plan = {"resources.jobs.daily": {"action": "skip", "changes": {"run_if": default}}}
    assert plan_report.drift(write(tmp_path, "p.json", plan)) == 0
