from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from proofofship.scoring import ReceiptInput, decay_weight, lifetime_score, reputation_score
from proofofship.urls import profile_url, receipts_url, score_url

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_decay_weight_matches_docs_example_shape():
    assert round(decay_weight(45), 3) == 0.707


def test_reputation_score_returns_breakdown_and_total():
    result = reputation_score(
        [
            ReceiptInput(age_days=10, verification_depth=0.8),
            ReceiptInput(age_days=45, verification_depth=0.6),
            ReceiptInput(age_days=120, verification_depth=1.0),
        ]
    )
    assert result["receipt_count"] == 3
    assert round(result["reputation_score"], 2) == 1.56
    assert len(result["breakdown"]) == 3
    assert "lifetime_score" in result
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
    assert round(payload["reputation_score"], 2) == 1.56
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
    assert payload["score_url"].endswith("/u/example-builder/score.json")
    assert payload["formula_version"] == "0.1"


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
