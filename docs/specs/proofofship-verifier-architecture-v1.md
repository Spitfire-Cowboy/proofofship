# Proofofship Verifier Architecture v1

This spec defines the public verification pipeline for Proof of Ship.

It does not describe every operator-side safeguard. It defines the stages, outputs, and public meanings that downstream consumers may rely on.

## Purpose

The verifier exists to answer one narrow question:

> Given a public proof envelope, how much of its claim can Proof of Ship independently verify from public evidence?

The output is a verification result with:
- a final status
- stage-by-stage outcomes
- a `verification_depth` value in `[0.0, 1.0]`

## Pipeline overview

```text
Input envelope
  -> schema validation
  -> dedup / idempotency check
  -> identity binding
  -> artifact existence check
  -> repository visibility + permission check
  -> cryptographic evidence check
  -> final verification result
```

These stages are ordered. Later stages do not rescue earlier failures.

## Verification stages

### Stage 1 — Schema validation

Checks:
- required envelope fields present
- field types valid
- schema version recognized
- envelope structure parseable

Output:
- pass/fail

Public meaning:
- the claim is at least machine-readable and well-formed

Contribution to depth:
- passing this stage permits a minimum `verification_depth` of `0.2`

### Stage 2 — Dedup / idempotency

Checks:
- content hash seen before?
- envelope already ingested?

Output:
- `new`
- `already_exists`

Public meaning:
- repeated submission of identical evidence does not inflate reputation

Contribution to depth:
- none directly; this is an integrity guardrail

### Stage 3 — Identity binding

Checks:
- claimed actor matches the authenticated GitHub identity for a submission flow that requires identity binding
- actor handle is internally coherent across the envelope

Output:
- pass/fail

Public meaning:
- the submitter is allowed to speak for the claimed actor identity in that submission flow

Contribution to depth:
- identity binding is necessary for a verified receipt, but not exposed as its own public depth increment

### Stage 4 — Artifact existence

Checks:
- referenced commit, PR, branch, tag, or repo exists
- referenced URLs resolve to the claimed public artifact

Output:
- pass/fail

Public meaning:
- the claimed artifact is real, public, and reachable

Contribution to depth:
- schema-valid + artifact-confirmed claims may reach `verification_depth = 0.4`

### Stage 5 — Repository visibility and permission relationship

Checks:
- referenced repository is public
- actor has the required relationship to the repo for the claim being made
- repo is eligible for public reputation treatment

Output:
- pass/fail

Public meaning:
- the actor is not merely naming a random public artifact; there is a verifiable relationship to the repository

Contribution to depth:
- folded into the transition from artifact confirmation toward stronger verified states

### Stage 6 — Cryptographic evidence

Checks:
- commit signature or equivalent public cryptographic evidence is present when required
- hash relationships are internally consistent
- envelope integrity checks pass

Output:
- pass/fail

Public meaning:
- the claim is not just about a visible artifact, but also about stronger provenance evidence

Contribution to depth:
- successful cryptographic verification may raise `verification_depth` to `0.6`

## Public depth tiers

These tiers are the public contract used by the site and score surfaces.

| Depth | Meaning |
|------:|---------|
| `0.0` | Not verified |
| `0.2` | Schema valid |
| `0.4` | Artifact confirmed |
| `0.6` | Cryptographically signed |
| `0.8` | Independently attested *(reserved / planned)* |
| `1.0` | All stages passed with maximum assurance *(reserved / planned)* |

Important:
- `0.8` and `1.0` remain reserved public meanings even if the current public repo does not yet implement every path to them.
- The public site should avoid claiming those deeper states are broadly live unless they actually are.

## Final statuses

A verification run produces one of these statuses:

- `verified`
- `pending`
- `rejected`
- `already_exists`

### verified
The receipt passed the required stages for public reputation treatment.

### pending
The receipt may require asynchronous follow-up or deferred checks.

### rejected
A required validation or verification stage failed.

### already_exists
An identical content hash was already ingested.

## Public error classes

Stable public rejection/error categories:

- `SCHEMA_INVALID`
- `IDENTITY_MISMATCH`
- `ARTIFACT_NOT_FOUND`
- `REPO_NOT_PUBLIC`
- `INSUFFICIENT_REPO_PERMISSION`
- `CRYPTO_EVIDENCE_MISSING`
- `DUPLICATE`
- `VERIFICATION_FAILED`

These are category-level public results, not a promise that every internal decision path is disclosed.

## Relationship to scoring

Verification does not directly compute reputation. It produces the `verification_depth` and status values consumed by the reputation engine.

In simplified form:

```text
reputation contribution = time_weight × verification_depth × dispute_multiplier
```

So the verifier answers: “How much public confidence should this receipt earn?”
The scorer answers: “How much does that confidence contribute right now?”

## Relationship to ship-receipts

`ship-receipts` may generate envelopes and local evidence, but it does not decide the final public verification result.

Proof of Ship always re-verifies from scratch against public evidence.

That firewall is the core trust property of the system.

More generally: the verifier depends on the public envelope and evidence
contract, not on one privileged producer. `ship-receipts` is an example
upstream source, not a mandatory one.
