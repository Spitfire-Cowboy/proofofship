# Proofofship Global Game Loop v1

This spec defines how reputation accrues, how recent activity is surfaced, and how the system resists gaming in proofofship.

## The game loop

The core loop for any actor:

1. **Ship work** — actor commits code in a public repo
2. **Generate receipt** — a local tool creates a verifiable envelope
3. **Submit to proofofship** — receipt enters the registry API
4. **Verify independently** — proofofship checks schema, integrity, origin, and dedup
5. **Update public signals** — verified receipts affect reputation and/or recent activity
6. **Publish public surface** — score and receipts appear at `/u/<handle>`

## Score composition

### Humans

```text
reputation_score = lifetime_score
lifetime_score = sum(verification_depth_i * dispute_multiplier_i)
recent_activity_score = sum(receipt_weight_i * verification_depth_i * dispute_multiplier_i)
```

### Non-human actors

```text
reputation_score = recent_activity_score
```

### verification_depth (0.0 — 1.0)

Measures how thoroughly a receipt was verified:

- 0.2: schema valid only
- 0.4: artifact exists on the public record
- 0.6: public repo plus actor authority check
- 0.8: cryptographic signature evidence
- 1.0: independent attestation from another verified actor

Each level includes the levels below it.

### receipt_weight

Time-decayed recent-activity value of each receipt:

- recent-activity decay function: exponential with configurable half-life
- human recent-activity default: 365 days
- non-human recent-activity default: 90 days
- formula: `weight = 2^(-age_days / half_life)`

### Why this works

- Humans do not lose earned reputation merely for stepping away from constant production
- Recent activity stays visible without overwriting lifetime reputation
- Single high-quality verified receipt beats many low-depth receipts
- Score remains deterministic from public data

## Anti-gaming controls

### 1. Volume resistance

Low-depth receipts contribute very little. One fully verified receipt matters more than many weak ones.

### 2. Attestation graph monitoring

Track who attests for whom. Flag patterns:
- reciprocal exclusive pairs
- small closed groups
- suspicious attestation clusters

MVP: monitor and flag only. Automated discounting comes later.

### 3. Recent-activity decay

No new verified receipts lowers the recent-activity signal over time. For humans this does not erase earned reputation. For non-human actors the recent-activity signal can remain the primary score.

### 4. Public auditability

All inputs to the score formula are public. Anyone can recompute any actor’s published score.

### 5. Private repo exclusion

Only public repos contribute. If proofofship cannot independently verify the artifact, `verification_depth` stays at `0.0`.

## Confidence weighting by verification depth

| Depth | Meaning | Contribution |
|---|---|---|
| 0.0 | Failed verification | Zero |
| 0.2 | Schema valid only | Minimal |
| 0.4 | Artifact exists | Low |
| 0.6 | Public repo + authority | Moderate |
| 0.8 | Signed artifact | High |
| 1.0 | Independent attestation | Full |

This creates a natural incentive gradient: better public evidence earns more reputation.

## Deferred to post-MVP

- Challenge windows
- Receipt classes (draft / verified / contested / superseded)
- Automated attestation-graph discounting
- Weighted scoring by richer evidence payloads
- Streak bonuses or consistency multipliers
