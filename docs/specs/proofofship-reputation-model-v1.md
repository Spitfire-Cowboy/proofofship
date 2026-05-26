# Proofofship Reputation Model v1

Spec version: 0.1

This spec defines how proofofship computes, displays, and protects reputation scores.

See also: `proofofship-verifier-architecture-v1.md`.

## Core principle

Reputation in proofofship is derived from publicly verifiable receipts.

For humans:
- earned reputation is cumulative and does not decay away
- recent activity is visible as a separate signal

For non-human actors:
- the primary public score can remain recency-sensitive
- recent activity and public reputation may be the same number

## Identity model

- **Actor**: A GitHub user or organization. Identity anchor is GitHub username via OAuth.
- **Workspace**: Not modeled in MVP. Future: could group actors by org.
- **Repo**: A GitHub repository. Receipts reference repos. An actor may have receipts across many repos.
- **Session**: A unit of work that produced a receipt. Opaque to proofofship (defined by the source system, e.g. ship-receipts).

Proofofship does not invent new identities. GitHub is the identity oracle.

## Score formula

### Human actors

```text
reputation_score(actor) = lifetime_score(actor)
lifetime_score(actor) = Σ over verified receipts (verification_depth(r) × dispute_multiplier(r))
recent_activity_score(actor) = Σ over verified receipts (time_weight(r) × verification_depth(r) × dispute_multiplier(r))
```

### Non-human actors

```text
reputation_score(actor) = recent_activity_score(actor)
```

Where:
- the sum is over receipts with status = `verified` for the actor
- `time_weight(r) = 2^(-age_days / half_life)`
- human recent-activity half-life defaults to 365 days
- non-human recent-activity half-life defaults to 90 days
- `verification_depth(r)` ranges from 0.0 to 1.0
- `dispute_multiplier(r)` ranges from 0.0 to 1.0

### Worked example

Human actor with 3 verified receipts:

1. 10 days old, depth 0.8
2. 45 days old, depth 0.6
3. 120 days old, depth 1.0

Results:
- `lifetime_score = 0.8 + 0.6 + 1.0 = 2.4`
- `reputation_score = 2.4`
- `recent_activity_score ≈ 2.13` using the 365-day recent-activity half-life

### Score properties

- Unbounded above (more verified work = higher score)
- Human reputation does not decay simply because someone stops shipping for a while
- Recent activity remains visible as a separate signal
- Single high-depth receipt beats many low-depth receipts
- Score is deterministic from public data

## Public proof surfaces

### What is visible

- Actor GitHub username
- Verified receipts and verification results
- Public score payload and breakdown
- Enough data to replay the published computation

### What is not stored in the public repo

- Passwords, tokens, or secrets
- Private repo data
- PII beyond GitHub username
- Proprietary enforcement or anti-abuse logic

### Endpoints

- `/u/<handle>` — HTML profile page
- `/u/<handle>/score.json` — machine-readable public score object
- `/u/<handle>/receipts.json` — machine-readable verified receipt list

### score.json shape

```json
{
  "handle": "example-builder",
  "actor_kind": "human",
  "reputation_score": 2.4,
  "lifetime_score": 2.4,
  "recent_activity_score": 2.13,
  "receipt_count": 3,
  "recent_activity_half_life_days": 365,
  "formula_version": "0.1",
  "profile_url": "https://proofofship.com/u/example-builder",
  "score_url": "https://proofofship.com/u/example-builder/score.json",
  "receipts_url": "https://proofofship.com/u/example-builder/receipts.json",
  "breakdown": [
    {
      "age_days": 10,
      "verification_depth": 0.8,
      "dispute_multiplier": 1.0,
      "time_weight": 0.98,
      "contribution": 0.78,
      "label": "recent signed receipt"
    }
  ]
}
```

## Anti-gaming controls

### 1. Verification depth as a quality gate

Low-effort receipts contribute very little. Meaningful score growth requires better public evidence.

### 2. Separate reputation from activity

For humans, earned reputation is cumulative. The system shows recent activity separately so sabbaticals, caregiving, illness, or deep research periods do not erase earned credibility. Non-human actors can still be judged more strictly on recency.

### 3. Attestation graph monitoring

Track the graph of who attests for whom. Flag:
- exclusive pairs
- small closed groups
- suspicious reciprocal patterns

MVP: flag and surface for human review. Automated discounting in v2.

### 4. Public auditability

All score inputs are public. Gaming attempts are visible to anyone who inspects the data.

### 5. Private repo exclusion

Receipts referencing private repos get `verification_depth = 0.0`. They do not contribute to public reputation.

## Data retention

- Verified receipts: retained indefinitely (append-only)
- Verification results: retained indefinitely, immutable
- Rejected receipts: retained for dedup, not public
- Score history: computed on demand, not stored as mutable truth
- Actor can request unlisting from public UI; audit-store retention is separate

## Deferred to post-MVP

- Normalized or percentile scores
- Category-specific scores
- Weighted scoring by richer evidence payloads
- Workspace or org-level reputation
- Streak or consistency bonuses
- Automated attestation-graph discounting
