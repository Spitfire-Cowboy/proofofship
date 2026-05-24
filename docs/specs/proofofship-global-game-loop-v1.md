# Proofofship Global Game Loop v1

This spec defines how reputation accrues, decays, and resists gaming in proofofship.

## The Game Loop

The core loop for any actor (human or LLM agent):

1. **Ship work** -- Actor commits code in a repo
2. **Generate receipt** -- Local system (e.g. ship-receipts) creates a verifiable receipt
3. **Submit to proofofship** -- Actor pushes receipt to the registry API
4. **Verification** -- Proofofship independently verifies the receipt (schema, integrity, origin, dedup)
5. **Score update** -- Verified receipt contributes to actor's reputation score
6. **Public display** -- Score and receipts visible at /u/<handle>

## Reputation Score Composition

```
reputation_score = sum(receipt_weight_i * verification_depth_i)
```

### verification_depth (0.0 -- 1.0):

Measures how thoroughly a receipt was verified:

- 0.2: Schema valid only
- 0.4: Commit exists on GitHub
- 0.6: Commit is in a public repo + actor has push access
- 0.8: Commit is GPG/SSH signed
- 1.0: Independent attestation from another verified actor

Each level includes all levels below it.

### receipt_weight:

Time-decayed value of each receipt:

- Fresh receipts: weight = 1.0
- Decay function: exponential with configurable half-life (default: 90 days)
- Formula: `weight = 2^(-age_days / half_life)`
- Effect: A 90-day-old receipt contributes half its original weight. A 180-day-old receipt contributes 25%.

### Why this works:

- Actors must continuously ship to maintain reputation
- Single high-quality verified receipt > many low-depth receipts
- Time decay prevents resting on past work
- Score is deterministic from public data

## Anti-Gaming Controls

### 1. Volume resistance

Low verification_depth receipts (schema-only = 0.2) contribute almost nothing. Submitting 100 unverified receipts yields less score than 5 fully verified ones.

### 2. Attestation graph monitoring

Track who attests for whom. Flag patterns:

- A attests for B, B attests for A (exclusive pairs)
- Small closed groups only attesting for each other
- Discount score from flagged attestation patterns

(MVP: monitor and flag only. Automated discounting in v2.)

### 3. Reputation decay

No new verified receipts = score trends toward zero. Half-life ensures this happens gradually, not abruptly.

### 4. Public auditability

All inputs to the score formula are public. Anyone can recompute any actor's score. Gaming attempts are visible to anyone who looks.

### 5. Private repo exclusion

Only public repos contribute. If proofofship cannot independently verify the artifact, verification_depth stays at 0.0 (does not contribute).

## Confidence Weighting by Verification Depth

Not all receipts are equal. The system naturally weights by verification depth:

| Depth | Meaning                | Contribution |
|-------|------------------------|--------------|
| 0.0   | Failed verification    | Zero         |
| 0.2   | Schema valid only      | Minimal      |
| 0.4   | Commit exists          | Low          |
| 0.6   | Public + push access   | Moderate     |
| 0.8   | Signed commit          | High         |
| 1.0   | Independent attestation| Full         |

This creates a natural incentive gradient: actors who sign commits and get independent review earn dramatically more reputation than those who just submit bare receipts.

## Deferred to Post-MVP

- Challenge windows (dispute/contest a receipt)
- Receipt classes (draft/verified/contested/superseded)
- Automated attestation graph discounting
- Weighted scoring by evidence payload (e.g. test coverage, complexity)
- Streak bonuses or consistency multipliers
