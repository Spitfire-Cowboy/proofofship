from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_global_ledger_validator_accepts_sample_file():
    proc = subprocess.run(
        [sys.executable, "scripts/validate_global_ledger.py", "--file", "examples/global-ledger.sample.jsonl"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert proc.stdout.strip() == "ok"


def test_global_ledger_validator_rejects_self_approval(tmp_path: Path):
    path = tmp_path / "bad.jsonl"
    path.write_text('{"receipt_id":"r1","status":"verified","submitter":"alice","created_at":"2026-05-24T12:00:00Z","verifier_hooks":["hook"],"reviewer_ids":["alice"]}\n')
    proc = subprocess.run(
        [sys.executable, "scripts/validate_global_ledger.py", "--file", str(path)],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert proc.returncode == 1
    assert "may not self-approve" in proc.stdout
