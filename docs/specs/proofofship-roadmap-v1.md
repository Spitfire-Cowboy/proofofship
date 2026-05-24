# Proofofship Roadmap v1

This roadmap defines the phased build plan for proofofship as a global verification/reputation layer.

## Relationship to ship-receipts

- **ship-receipts** (~/Projects/ship-receipts): Local receipt generator. Creates verifiable records of shipped work per-repo. Does not compute reputation.
- **proofofship** (~/Projects/proofofship): Global canonical scoreboard. Aggregates receipts from any conformant source, verifies independently, computes and publishes reputation scores.

Ship-receipts is the first integration. Not the only one.

## Phase 0: Spec + Foundation (Current)
- Define architecture: registry-first model
- Define ingestion contract (source-agnostic receipt schema)
- Define verification pipeline (6 stages)
- Define reputation score formula
- Define threat model + anti-gaming controls
- Define public API surface (6 endpoints)
- Establish develop branch

**Exit criteria:** 5 spec docs approved and committed.

## Phase 1: Core Registry (MVP)
- Set up Python project (FastAPI)
- Implement SQLite storage layer (receipts table, verification_results table, actors table)
- Implement receipt ingestion endpoint (POST /api/v1/receipts)
- Implement verification pipeline stages 1-4 (schema, dedup, identity, artifact integrity)
- Implement GitHub OAuth flow
- Implement basic actor profile endpoint (GET /api/v1/actors/:username)
- Implement receipt query endpoint (GET /api/v1/receipts/:id)

**Exit criteria:** Can submit a receipt from ship-receipts, verify it, and retrieve it via API.

## Phase 2: Reputation Engine
- Implement reputation score computation
- Implement time decay (configurable half-life)
- Implement score.json endpoint (/u/<handle>/score.json)
- Implement receipts list endpoint (GET /api/v1/actors/:username/receipts)
- Add GPG/SSH signature verification (stage 5)
- Add verification depth scoring

**Exit criteria:** Actors have live reputation scores computed from verified receipts.

## Phase 3: Public Surface
- Build /u/<handle> profile page (static HTML or lightweight frontend)
- Display reputation score + receipt history + verification details
- Implement score recomputation transparency (show formula inputs)
- Add receipts.json endpoint for machine consumers

**Exit criteria:** Public, human-readable profiles at proofofship.com/u/<handle>.

## Phase 4: Semantic Search
- Integrate ChromaDB
- Embed receipt content on ingestion
- Implement /api/v1/search endpoint
- Enable "find similar shipped work" queries

**Exit criteria:** Semantic search across all receipts works.

## Phase 5: Anti-Gaming Hardening
- Implement attestation graph tracking
- Build monitoring dashboard for attestation patterns
- Flag closed-loop attestation patterns
- Add private repo detection and exclusion
- Implement rate limiting on receipt submission

**Exit criteria:** Known gaming vectors from threat model are monitored.

## Phase 6: Advanced Features (Post-MVP)
- Challenge windows (dispute a receipt)
- Receipt classes (draft/verified/contested/superseded)
- Automated attestation graph discounting
- Non-GitHub identity providers (GitLab, Bitbucket)
- Workspace/org-level reputation
- Category-specific scores
- Pull/crawler-based ingestion
- Federation with other verification systems

## ship-receipts Integration Requirements

For ship-receipts to integrate with proofofship:

1. **Schema conformance:** ship-receipts must emit receipts matching the proofofship ingestion schema (schema_version, source_type, actor, artifact, evidence, submitted_at)
2. **Push mechanism:** ship-receipts adds a `proofofship push` command or post-commit hook that submits receipts to POST /api/v1/receipts
3. **Authentication:** ship-receipts stores a GitHub OAuth token for the actor (or prompts for auth on first push)
4. **No hard coupling:** ship-receipts continues to work standalone. Proofofship push is opt-in.
5. **Evidence payload:** ship-receipts populates the evidence field with session-specific data (session_id, diminishing_returns_signal, files_changed, tests_passed, etc.). Proofofship treats this as opaque but stores it.

## Key Milestones

| Milestone | Description | Phase |
|-----------|-------------|-------|
| First verified receipt | End-to-end: ship-receipts -> proofofship -> verified | Phase 1 |
| First reputation score | Score computed from verified receipts | Phase 2 |
| First public profile | /u/<handle> live and readable | Phase 3 |
| Semantic search live | "Find work like X" queries work | Phase 4 |
| Anti-gaming monitoring | Attestation patterns tracked | Phase 5 |
