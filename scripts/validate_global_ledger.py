from __future__ import annotations

import argparse
import json
from pathlib import Path

VALID_STATUSES = {"draft", "verified", "contested", "superseded"}
REQUIRED_FIELDS = {
    "receipt_id": str,
    "status": str,
    "submitter": str,
    "created_at": str,
    "verifier_hooks": list,
    "reviewer_ids": list,
}


def _non_empty_strings(values: list[object]) -> list[str]:
    return [v for v in values if isinstance(v, str) and v.strip()]


def validate_entry(entry: dict, line_no: int) -> list[str]:
    errors: list[str] = []
    for field, typ in REQUIRED_FIELDS.items():
        if field not in entry:
            errors.append(f"line {line_no}: missing required field '{field}'")
        elif not isinstance(entry[field], typ):
            errors.append(f"line {line_no}: field '{field}' must be {typ.__name__}")
    if errors:
        return errors

    if entry["status"] not in VALID_STATUSES:
        errors.append(f"line {line_no}: status must be one of {sorted(VALID_STATUSES)}")

    if entry["status"] == "verified":
        hooks = _non_empty_strings(entry["verifier_hooks"])
        reviewers = _non_empty_strings(entry["reviewer_ids"])
        if not hooks:
            errors.append(f"line {line_no}: verified entries require at least one non-empty verifier_hook")
        if not reviewers:
            errors.append(f"line {line_no}: verified entries require at least one non-empty reviewer_id")
        if entry["submitter"] in reviewers:
            errors.append(f"line {line_no}: verified entries may not self-approve")

    return errors


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    for idx, raw_line in enumerate(path.read_text().splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            entry = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {idx}: invalid JSON ({exc})")
            continue
        if not isinstance(entry, dict):
            errors.append(f"line {idx}: each JSONL row must be an object")
            continue
        errors.extend(validate_entry(entry, idx))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Proof of Ship global-ledger JSONL file")
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    errors = validate_file(Path(args.file))
    if errors:
        for err in errors:
            print(err)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
