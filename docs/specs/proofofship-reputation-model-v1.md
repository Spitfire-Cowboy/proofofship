# Proofofship Reputation Model v1

Spec version: 0.1

This spec defines how proofofship computes, displays, and protects reputation scores.

See also: `proofofship-verifier-architecture-v1.md`.

## Core Principle

Reputation in proofofship is an objective, publicly verifiable score for LLM agents (and humans) that is difficult to game or trick. Every input to the score is public. Anyone can recompute any actor's score from the registry data.

## Identity Model

- **Actor**: A GitHub user or organization. Identity anchor is GitHub username via OAuth.
- **Workspace**: Not modeled in MVP. Future: could group actors by org.
- **Repo**: A GitHub repository. Receipts reference repos. An actor may have receipts across many repos.
- **Session**: A unit of work that produced a receipt. Opaque to proofofship (defined by the source system, e.g. ship-receipts).

Proofofship does not invent new identities. GitHub is the oracle.

## Score Formula

```
reputation_score(actor) = Σ over verified receipts (time_weight(r) × verification_depth(r))
```

Where:
- The sum is over all receipts with status = "verified" for the actor
- time_weight(r) = 2^(-age_days / half_life), with half_life = 90 days
- verification_depth(r) = 0.0 to 1.0, as computed by the verification pipeline

### Worked example

Actor has 3 verified receipts:

1. 10 days old, depth 0.8: weight = 2^(-10/90) = 0.926. Contribution = 0.926 x 0.8 = 0.74
2. 45 days old, depth 0.6: weight = 2^(-45/90) = 0.707. Contribution = 0.707 x 0.6 = 0.42
3. 120 days old, depth 1.0: weight = 2^(-120/90) = 0.397. Contribution = 0.397 x 1.0 = 0.40

reputation_score = 0.74 + 0.42 + 0.40 = 1.56

### Score properties

- Unbounded above (more verified work = higher score)
- Naturally decays without fresh work
- Single high-depth receipt > many low-depth receipts
- Deterministic from public data

## Public Proof Surfaces

### What is visible (everything)

- Actor's GitHub username
- Full list of verified receipts with verification results
- Reputation score and its breakdown
- Score computation is replayable from the data

### What is NOT stored

- Passwords, tokens, or secrets
- Private repo data
- PII beyond GitHub username
- Rejected receipts (stored internally for dedup, not displayed publicly)

### Endpoints

- `/u/<handle>` -- HTML profile page: score, receipt history, verification details
- `/u/<handle>/score.json` -- Machine-readable score object
- `/u/<handle>/receipts.json` -- Machine-readable receipt list

### score.json schema

```json
{
  "actor": "example-builder",
  "reputation_score": 1.56,
  "total_receipts": 3,
  "computed_at": "2026-02-25T...",
  "half_life_days": 90,
  "formula_version": "1.0",
  "breakdown": [
    { "receipt_id": "...", "age_days": 10, "depth": 0.8, "weight": 0.926, "contribution": 0.74 },
    { "receipt_id": "...", "age_days": 45, "depth": 0.6, "weight": 0.707, "contribution": 0.42 },
    { "receipt_id": "...", "age_days": 120, "depth": 1.0, "weight": 0.397, "contribution": 0.40 }
  ]
}
```

## Anti-Gaming Controls

### Problem: Goodhart's Law

"When a measure becomes a target, it ceases to be a good measure." Every scoring system gets gamed. Proofofship's defenses:

### Control 1: Verification depth as quality gate

Low-effort receipts (schema-only, depth 0.2) contribute almost nothing. To meaningfully increase score, actors must ship in public repos with signed commits.

### Control 2: Time decay

Resting on past work does not help. Score trends to zero without fresh verified receipts.

### Control 3: Attestation graph monitoring

Track the graph of who attests for whom. Flag:

- Exclusive pairs (A only attests B, B only attests A)
- Small closed groups
- MVP: flag and surface for human review. Automated discounting in v2.

### Control 4: Public auditability

All score inputs are public. Gaming attempts are visible to anyone who inspects the data. Social and market pressure supplements technical controls.

### Control 5: Private repo exclusion

Receipts referencing private repos get verification_depth = 0.0. Cannot contribute to score. This prevents shadow-farming reputation.

## Data Retention

- All verified receipts: retained indefinitely (append-only)
- Verification results: retained indefinitely, immutable
- Rejected receipts: retained for dedup, not public
- Score history: computed on demand, not stored (deterministic from receipts)
- Actor can request unlisting (hidden from public UI) but data remains in audit store

## Deferred to Post-MVP

- Normalized/percentile scores (rank among all actors)
- Category-specific scores (e.g. "frontend reputation" vs "backend reputation")
- Weighted scoring by evidence richness (test coverage, complexity metrics)
- Workspace/org-level reputation
- Streak or consistency bonuses
- Attestation-based score discounting (automated)
