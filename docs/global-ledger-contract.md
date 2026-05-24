# Global Ledger Contract (Hardening Slice)

Purpose: define a minimal, machine-checkable contract for receipt entries so high-signal claims cannot bypass independent verification.

## Scope

This slice enforces two hard controls for any `verified` entry:

1. At least one independent verification hook.
2. Reviewer independence (no self-approval).

## Ledger format

- File format: JSON Lines (`.jsonl`)
- One entry per line
- UTF-8 text

## Required fields per entry

- `receipt_id` (string): globally unique receipt id
- `status` (string): one of `draft`, `verified`, `contested`, `superseded`
- `submitter` (string): actor handle/id who submitted the receipt
- `created_at` (string): ISO-8601 UTC timestamp (`YYYY-MM-DDTHH:MM:SSZ`)
- `verifier_hooks` (array of strings): independent verification hooks
- `reviewer_ids` (array of strings): reviewer handles/ids

## Hard rules

### Rule GL-01: Independent verification hooks

If `status == "verified"`, then:

- `verifier_hooks` MUST contain at least 1 non-empty string.

### Rule GL-02: Reviewer independence

If `status == "verified"`, then:

- `reviewer_ids` MUST contain at least 1 non-empty string.
- `submitter` MUST NOT appear in `reviewer_ids`.

## Validator

Use:

```bash
python scripts/validate_global_ledger.py --file examples/global-ledger.sample.jsonl
```

The validator exits non-zero on contract violations and prints line-level failures.
