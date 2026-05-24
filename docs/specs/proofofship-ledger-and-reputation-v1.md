# Proofofship Ledger and Reputation v1

**Status:** SPEC
**Date:** 2026-02-25
**Author:** Campion
**Depends on:** proofofship-reputation-model-v1.md, proofofship-verifier-architecture-v1.md
**Research:** 2026-02-arxiv-math-and-reputation-map.md (R4, R5, R8, R18, R19)

---

## Purpose

This spec defines the canonical ledger structure, reputation aggregation formulas, and anti-gaming controls for proofofship. It is the implementation contract for the global layer.

---

## 1. Ledger Model

### 1.1 Append-Only Receipt Store

The ledger is an append-only store of **verified receipt records**. Each record contains:

```python
@dataclass
class LedgerEntry:
    entry_id: str              # ULID, generated at ingest time
    content_hash: str          # sha256:<hex> — THE idempotency key
    envelope_id: str           # ULID from proof envelope
    actor_github: str          # GitHub username (identity anchor)
    receipt: dict              # Full original receipt (embedded)
    verification: VerificationResult  # From pipeline
    ingested_at: str           # ISO 8601 timestamp
    status: str                # "verified" | "rejected" | "pending"
    dispute_status: str        # "none" | "flagged" | "upheld" | "dismissed"
```

### 1.2 Immutability Contract

- Once written, a `LedgerEntry` is **never modified**.
- Status changes (disputes, re-verification) create **new records** referencing the original `entry_id`.
- Re-verification after API recovery creates a new `VerificationResult` linked to the same `entry_id`.

### 1.3 Storage Backend (v1)

SQLite with WAL mode. Tables:

```sql
CREATE TABLE ledger (
    entry_id TEXT PRIMARY KEY,
    content_hash TEXT NOT NULL UNIQUE,
    envelope_id TEXT NOT NULL,
    actor_github TEXT NOT NULL,
    receipt_json TEXT NOT NULL,
    verification_json TEXT NOT NULL,
    ingested_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    dispute_status TEXT NOT NULL DEFAULT 'none',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_ledger_actor ON ledger(actor_github);
CREATE INDEX idx_ledger_content_hash ON ledger(content_hash);
CREATE INDEX idx_ledger_status ON ledger(status);
CREATE INDEX idx_ledger_ingested_at ON ledger(ingested_at);
```

---

## 2. Envelope Ingestion

### 2.1 Ingestion Pipeline

```
INPUT: proof envelope JSON

1. SCHEMA VALIDATION
   - Validate against proof-envelope.v1.json schema
   - Reject with specific error on failure

2. IDEMPOTENCY CHECK
   - SELECT entry_id FROM ledger WHERE content_hash = ?
   - If exists: return existing entry_id, HTTP 200 (not 409)
   - Idempotent: submitting the same envelope twice is safe and returns same result

3. IDENTITY BINDING
   - actor.github_username must match authenticated session
   - Reject if mismatch

4. VERIFICATION PIPELINE
   - Run 6-stage verification (see verifier-architecture-v1)
   - Produces verification_depth ∈ [0.0, 1.0]

5. LEDGER APPEND
   - Generate entry_id (ULID)
   - INSERT into ledger with status = verification result status
   - Return entry_id + verification summary

6. REPUTATION UPDATE
   - Trigger async reputation recomputation for actor
   - (Or: reputation is always computed on demand — see §3)
```

### 2.2 Rejection Reasons

| Code | Reason | Retry? |
|------|--------|--------|
| `SCHEMA_INVALID` | Envelope doesn't match schema | No (fix and resubmit) |
| `IDENTITY_MISMATCH` | Actor doesn't match session | No |
| `DUPLICATE` | content_hash already in ledger | No (already ingested) |
| `VERIFICATION_FAILED` | Critical verification stage failed | Depends on stage |

### 2.3 Duplicate Handling (Idempotency)

The `content_hash` field is the sole idempotency key. Same content_hash = same receipt, regardless of envelope_id or submitted_at.

```python
def ingest_envelope(envelope: dict, db: Database) -> IngestResult:
    content_hash = envelope["content_hash"]

    existing = db.query("SELECT entry_id, status FROM ledger WHERE content_hash = ?", content_hash)
    if existing:
        return IngestResult(
            entry_id=existing.entry_id,
            status="already_exists",
            is_duplicate=True,
        )

    # ... proceed with validation, verification, append
```

---

## 3. Reputation Aggregation

### 3.1 Core Formula

```python
import math
from datetime import datetime, timezone

HALF_LIFE_DAYS = 90

def reputation_score(actor: str, ledger: list[LedgerEntry], as_of: datetime = None) -> float:
    """
    reputation(actor) = Σ time_weight(r) × verification_depth(r) × dispute_multiplier(r)

    Over all ledger entries for actor where status = "verified".
    """
    if as_of is None:
        as_of = datetime.now(timezone.utc)

    total = 0.0
    breakdown = []

    for entry in ledger:
        if entry.actor_github != actor:
            continue
        if entry.status != "verified":
            continue

        # Dispute multiplier: flagged/upheld → 0.0
        d_mult = dispute_multiplier(entry)
        if d_mult == 0.0:
            continue

        age_days = (as_of - datetime.fromisoformat(entry.ingested_at)).days
        time_weight = math.pow(2, -age_days / HALF_LIFE_DAYS)
        depth = entry.verification.verification_depth

        contribution = time_weight * depth * d_mult
        total += contribution

        breakdown.append({
            "entry_id": entry.entry_id,
            "age_days": age_days,
            "time_weight": round(time_weight, 4),
            "depth": depth,
            "dispute_mult": d_mult,
            "contribution": round(contribution, 4),
        })

    return round(total, 4), breakdown
```

### 3.2 Time Decay Function

```
time_weight(age) = 2^(-age_days / 90)
```

| Age (days) | Weight |
|-----------|--------|
| 0 | 1.000 |
| 10 | 0.926 |
| 30 | 0.794 |
| 45 | 0.707 |
| 90 | 0.500 |
| 180 | 0.250 |
| 365 | 0.063 |

**Properties:**
- Half-life = 90 days (score halves every 90 days without new receipts)
- Smooth exponential decay, no cliff edges
- Recent work dominates naturally
- Parameterized: `HALF_LIFE_DAYS` is a tunable constant

### 3.3 Dispute Multiplier

```python
def dispute_multiplier(entry: LedgerEntry) -> float:
    if entry.dispute_status in ("none", "dismissed"):
        return 1.0
    if entry.dispute_status in ("flagged", "upheld"):
        return 0.0
    return 1.0  # Unknown status → default to unaffected
```

### 3.4 Verification Depth Mapping

From verifier-architecture-v1:

| Stages Passed | Depth |
|--------------|-------|
| Schema only | 0.2 |
| Schema + Artifact | 0.4 |
| Schema + Artifact + Signature | 0.6 |
| Schema + Artifact + Signature + Attestation | 0.8 |
| All stages including future stages | 1.0 |

### 3.5 Score Properties

- **Unbounded above:** More verified work = higher score. No ceiling.
- **Naturally decaying:** Trends to 0 without fresh verified receipts.
- **Quality-weighted:** One high-depth receipt > many low-depth receipts.
- **Deterministic:** Same inputs → same score. Publicly recomputable.
- **Dispute-aware:** Flagged/upheld receipts contribute 0.

---

## 4. Confidence Score (Actor-Level)

```python
def actor_confidence(reputation: float, receipt_count: int) -> str:
    """
    Actor-level confidence tier for display.
    Combines reputation magnitude with evidence breadth.
    """
    if receipt_count == 0 or reputation == 0:
        return "unrated"
    if reputation < 0.5:
        return "emerging"      # New builder, limited track record
    if reputation < 2.0:
        return "established"   # Consistent contributor
    if reputation < 5.0:
        return "trusted"       # Strong track record
    return "authority"          # Exceptional verified output
```

---

## 5. Anti-Gaming Controls

### 5.1 Receipt Stuffing (volume attack)
- **Mitigation:** Time decay means rapid submission of low-depth receipts yields diminishing returns. 100 receipts at depth 0.2 = 20 points. 5 receipts at depth 0.8 = 4 points. Volume helps but quality dominates.
- **Future:** Rate limiting (max N envelopes per actor per day).
- **Source:** R9 (strategic evaluation), R10 (optimal rating)

### 5.2 Sybil Attack (multiple fake identities)
- **Mitigation v1:** GitHub OAuth as identity anchor. Creating GitHub accounts has friction. Each account must independently produce verifiable work in public repos.
- **Future:** Graph-based Sybil detection on attestation graph (R15).
- **Source:** R15 (SYBILGAT)

### 5.3 Collusion (mutual attestation rings)
- **Mitigation v1:** Attestation graph monitoring. Flag exclusive pairs (A only attests B, B only attests A) and small closed groups. Surface for human review.
- **Future:** Automated cycle detection and discounting (R16).
- **Source:** R16 (collusion rings), R17 (strategic peer assessment)

### 5.4 Shadow Farming (private repo reputation)
- **Mitigation:** Private repos get `verification_depth = 0.0`. Cannot contribute to reputation.
- **Source:** R5 (ARMS)

### 5.5 Stale Reputation Exploitation
- **Mitigation:** Time decay with 90-day half-life. A builder who shipped heavily 1 year ago but nothing since has ~6% of peak reputation.
- **Source:** R4 (trust in motion)

### 5.6 Replay Attack (duplicate envelopes)
- **Mitigation:** Content-hash idempotency. Same hash = same entry, no double-counting.
- **Source:** R18 (transparency protocol verification)

### 5.7 Fabricated Verification Claims
- **Mitigation:** Proofofship never trusts local_score_snapshot from envelopes. All verification is re-done independently against GitHub API.
- **Source:** R5 (ARMS), R11 (trustworthy anomaly detection)

---

## 6. Public API (Score Endpoints)

### GET /u/{handle}/score.json

```json
{
  "actor": "example-builder",
  "reputation_score": 3.42,
  "confidence": "established",
  "total_receipts": 8,
  "verified_receipts": 7,
  "disputed_receipts": 0,
  "computed_at": "2026-02-25T15:30:00Z",
  "half_life_days": 90,
  "formula_version": "1.0",
  "breakdown": [
    {
      "entry_id": "01HWXYZ...",
      "age_days": 5,
      "time_weight": 0.9623,
      "depth": 0.6,
      "contribution": 0.5774
    }
  ]
}
```

### GET /u/{handle}/receipts.json

Returns all verified receipts for the actor with verification results. Paginated (100 per page).

---

## 7. Data Retention

| Data | Retention | Mutable? |
|------|-----------|----------|
| Verified receipts | Indefinite | No (append-only) |
| Verification results | Indefinite | No (new results for re-verify) |
| Rejected receipts | 90 days (dedup window) | No |
| Reputation scores | Computed on demand | N/A |
| Dispute records | Indefinite | No (new records for status changes) |

---

## Appendix: Test Vectors

### Vector 1: Single fresh verified receipt
Actor: alice, 1 receipt, 0 days old, depth 0.6, no disputes.
Expected: reputation = 2^(-0/90) × 0.6 = 1.0 × 0.6 = 0.6

### Vector 2: Three receipts with decay
Actor: bob
- Receipt A: 10 days old, depth 0.8 → 0.926 × 0.8 = 0.7408
- Receipt B: 45 days old, depth 0.6 → 0.707 × 0.6 = 0.4242
- Receipt C: 120 days old, depth 1.0 → 0.397 × 1.0 = 0.397
Expected: reputation = 0.7408 + 0.4242 + 0.397 = 1.562

### Vector 3: Disputed receipt excluded
Actor: carol
- Receipt A: 5 days old, depth 0.8, dispute_status="none" → contributes
- Receipt B: 10 days old, depth 0.6, dispute_status="upheld" → excluded
Expected: reputation = 2^(-5/90) × 0.8 = 0.962 × 0.8 = 0.7696

### Vector 4: Duplicate envelope
Envelope with content_hash already in ledger.
Expected: Ingest returns existing entry_id, is_duplicate=True, no new entry.


## Identity binding

- Public profile identity is anchored to an authenticated GitHub account in v1.
- The actor handle in a linked public profile should match the authenticated GitHub session login.
- Repo linking controls which public repositories may be surfaced on a profile; it does not weaken independent verification of receipts.
