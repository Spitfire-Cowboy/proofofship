# CLI reference

The public `proofofship` CLI is the first shipped product surface in this repo.

Install locally:

```bash
pip install -e '.[dev]'
```

## Commands

### `proofofship weight <age_days>`

Compute the time-decay weight for a receipt age.

Example:

```bash
proofofship weight 45 --json
```

### `proofofship score <receipts_file>`

Compute a reputation score from a JSON array of receipt-like inputs.

Example:

```bash
proofofship score examples/score.sample.json --handle example-builder --json
```

Public-output fields:
- `reputation_score`
- `lifetime_score`
- `receipt_count`
- `half_life_days`
- `formula_version`
- `profile_url`
- `score_url`
- `receipts_url`
- `breakdown`

### `proofofship receipts <handle> <receipts_file>`

Emit a public `receipts.json`-style payload.

Example:

```bash
proofofship receipts example-builder examples/score.sample.json --json
```

### `proofofship badge <verified|receipts> <handle>`

Emit badge material for embedding in third-party repositories.

Examples:

```bash
proofofship badge verified example-builder --markdown
proofofship badge receipts example-builder --json
```

### `proofofship urls <handle>`

Print canonical public profile URLs.

Example:

```bash
proofofship urls example-builder --json
```

### `proofofship validate`

Validate checked-in public examples against bundled JSON schemas.

Example:

```bash
proofofship validate --json
```

### `proofofship check-public-surface`

Run integrity checks against the public repo surface.

Example:

```bash
proofofship check-public-surface --json
```

## Input file shape

Current scoring examples use a JSON array of objects like:

```json
[
  {
    "age_days": 10,
    "verification_depth": 0.8,
    "dispute_multiplier": 1.0,
    "label": "recent signed receipt"
  }
]
```

## Example outputs

See:
- `examples/score.public.sample.json`
- `examples/receipts.public.sample.json`
- `examples/account.github.public.sample.json`
- `examples/linked-repositories.public.sample.json`
