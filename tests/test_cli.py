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
