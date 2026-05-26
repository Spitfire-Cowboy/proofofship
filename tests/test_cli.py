from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from proofofship.scoring import (
    HUMAN_RECENT_ACTIVITY_HALF_LIFE_DAYS,
    NON_HUMAN_RECENT_ACTIVITY_HALF_LIFE_DAYS,
    ReceiptInput,
    decay_weight,
    default_recent_activity_half_life_days,
    lifetime_score,
    reputation_score,
)
from proofofship.urls import profile_url, receipts_url, score_url

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_decay_weight_matches_human_recent_activity_shape():
    assert round(decay_weight(45, half_life_days=HUMAN_RECENT_ACTIVITY_HALF_LIFE_DAYS), 3) == 0.918


def test_default_half_life_days_differs_for_humans_and_agents():
    assert default_recent_activity_half_life_days("human") == 365.0
    assert default_recent_activity_half_life_days("agent") == 90.0
    assert default_recent_activity_half_life_days("bot") == NON_HUMAN_RECENT_ACTIVITY_HALF_LIFE_DAYS


def test_reputation_score_returns_non_decaying_human_reputation_and_recent_activity():
    result = reputation_score(
        [
            ReceiptInput(age_days=10, verification_depth=0.8),
            ReceiptInput(age_days=45, verification_depth=0.6),
            ReceiptInput(age_days=120, verification_depth=1.0),
        ]
    )
    assert result["receipt_count"] == 3
    assert result["actor_kind"] == "human"
    assert result["recent_activity_half_life_days"] == 365.0
    assert round(result["reputation_score"], 2) == 2.4
    assert round(result["lifetime_score"], 2) == 2.4
    assert round(result["recent_activity_score"], 2) == 2.13
    assert len(result["breakdown"]) == 3


def test_agent_reputation_remains_recent_activity_sensitive():
    result = reputation_score(
        [
            ReceiptInput(age_days=10, verification_depth=0.8),
            ReceiptInput(age_days=45, verification_depth=0.6),
            ReceiptInput(age_days=120, verification_depth=1.0),
        ],
        actor_kind="agent",
    )
    assert result["actor_kind"] == "agent"
    assert result["recent_activity_half_life_days"] == 90.0
    assert round(result["reputation_score"], 2) == 1.56
    assert round(result["recent_activity_score"], 2) == 1.56
    assert round(result["lifetime_score"], 2) == 2.4


def test_lifetime_score_excludes_decay():
    result = lifetime_score(
        [
            ReceiptInput(age_days=10, verification_depth=0.8),
            ReceiptInput(age_days=120, verification_depth=1.0),
        ]
    )
    assert round(result["lifetime_score"], 2) == 1.8


def test_public_urls_are_canonical():
    assert profile_url("alice") == "https://proofofship.com/u/alice"
    assert score_url("alice") == "https://proofofship.com/u/alice/score.json"
    assert receipts_url("alice") == "https://proofofship.com/u/alice/receipts.json"


def test_cli_score_json_output():
    receipts = REPO_ROOT / "examples/score.sample.json"
    proc = subprocess.run(
        [sys.executable, "-m", "proofofship.cli", "score", str(receipts), "--json"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["receipt_count"] == 3
    assert payload["actor_kind"] == "human"
    assert round(payload["reputation_score"], 2) == 2.4
    assert round(payload["recent_activity_score"], 2) == 2.13
    assert round(payload["lifetime_score"], 2) == 2.4


def test_cli_public_surface_check_passes():
    proc = subprocess.run(
        [sys.executable, "-m", "proofofship.cli", "check-public-surface", "--json"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True


def test_cli_public_score_payload_with_handle():
    receipts = REPO_ROOT / "examples/score.sample.json"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "proofofship.cli",
            "score",
            str(receipts),
            "--handle",
            "example-builder",
            "--json",
        ],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["handle"] == "example-builder"
    assert payload["actor_kind"] == "human"
    assert payload["score_url"].endswith("/u/example-builder/score.json")
    assert payload["formula_version"] == "0.1"


def test_cli_score_json_output_for_agent_keeps_shorter_recent_activity_window():
    receipts = REPO_ROOT / "examples/score.sample.json"
    proc = subprocess.run(
        [sys.executable, "-m", "proofofship.cli", "score", str(receipts), "--actor-kind", "agent", "--json"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["actor_kind"] == "agent"
    assert payload["recent_activity_half_life_days"] == 90.0
    assert round(payload["reputation_score"], 2) == 1.56


def test_cli_weight_defaults_by_actor_kind():
    proc = subprocess.run(
        [sys.executable, "-m", "proofofship.cli", "weight", "45", "--json"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["actor_kind"] == "human"
    assert payload["recent_activity_half_life_days"] == 365.0
    assert round(payload["time_weight"], 3) == 0.918


def test_cli_receipts_json_output():
    receipts = REPO_ROOT / "examples/score.sample.json"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "proofofship.cli",
            "receipts",
            "example-builder",
            str(receipts),
            "--json",
        ],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["receipt_count"] == 3
    assert payload["receipts_url"].endswith("/u/example-builder/receipts.json")


def test_cli_badge_markdown_output():
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "proofofship.cli",
            "badge",
            "verified",
            "example-builder",
            "--markdown",
        ],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "badges/verified.svg" in proc.stdout
    assert "/u/example-builder" in proc.stdout


def test_cli_badge_json_output():
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "proofofship.cli",
            "badge",
            "receipts",
            "example-builder",
            "--json",
        ],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["badge_url"].endswith("/badges/receipts.svg")
    assert payload["target_url"].endswith("/u/example-builder/receipts.json")


def test_cli_validate_examples_json_output():
    proc = subprocess.run(
        [sys.executable, "-m", "proofofship.cli", "validate", "--json"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True


def test_cli_invalid_input_returns_clean_error():
    bad = REPO_ROOT / "examples" / "bad.json"
    bad.write_text('{"oops": true}\n')
    proc = subprocess.run(
        [sys.executable, "-m", "proofofship.cli", "score", str(bad)],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert proc.returncode == 2
    assert "error:" in proc.stdout
    bad.unlink()
