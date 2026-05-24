# Proof of Ship

**Independent verification and reputation from public evidence.**

Proof of Ship is the public home for the product narrative, protocol surface, schemas, landing-page source for `proofofship.com`, and a small Python CLI that exposes the deterministic public scoring math.

It exists to answer one question:

> *What has this person actually built, and how credible is that claim?*

A builder ships work in a public repository. A local tool such as [`ship-receipts`](https://github.com/Spitfire-Cowboy/ship-receipts) produces a proof envelope. Proof of Ship does not trust that local output blindly: it independently re-verifies the claim against the public record and turns verified work into a publicly auditable reputation signal.

## What this public repo contains

- public README and docs
- protocol and scoring specs
- public JSON schemas, including score, receipts, account, and repo-linking payloads
- the landing-page source for `proofofship.com`
- a Python CLI for deterministic score math, URL helpers, and public-surface integrity checks
- contribution / security / review config for the public surface

## What this public repo does **not** contain

- secrets or environment-specific configuration
- operator-only runbooks and machine-local assumptions
- undocumented implementation details that are not part of the public contract
- unsupported claims beyond what this repo actually documents and exposes

This repo is the public contract, documentation, schema, and CLI surface for Proof of Ship. Some operator-side and anti-abuse code remains intentionally proprietary because the project requires hidden enforcement and trust-boundary logic.

## Core idea in 30 seconds

1. A builder ships work in a public repo.
2. A local tool generates a verifiable proof envelope.
3. Proof of Ship independently verifies the claim against the public record.
4. Verified work contributes to a deterministic, time-decayed reputation score.
5. Anyone can inspect the rules and recompute the score from public inputs.

No self-reported prestige. If it cannot be independently verified, it does not count.

## Python CLI

The first public product surface is a **Python CLI**.

Current commands:
- `proofofship weight <age_days>` — compute time-decay weight
- `proofofship score examples/score.sample.json --handle example-builder --json` — emit a public `score.json`-style payload
- `proofofship receipts <handle> examples/score.sample.json --json` — emit a public `receipts.json`-style payload
- checked-in examples live at `examples/score.public.sample.json`, `examples/receipts.public.sample.json`, and repo-linking samples
- `proofofship badge <verified|receipts> <handle>` — emit badge URLs or embeddable markdown
- `proofofship urls <handle>` — print canonical public profile URLs
- `proofofship validate` — validate checked-in public examples against bundled schemas
- `proofofship check-public-surface` — verify the public repo contains the expected files, valid examples, and no obvious secret-like strings

Quick start:

```bash
pip install -e .
proofofship score examples/score.sample.json --handle example-builder --json
```

## Repo map

- [`docs/`](./docs/) — public docs index
- [`docs/specs/`](./docs/specs/) — protocol, ledger, scoring, auth, and roadmap specs
- [`docs/cli.md`](./docs/cli.md) — CLI reference
- [`docs/public-surfaces.md`](./docs/public-surfaces.md) — live vs repo-shipped vs contract-only surfaces
- [`docs/web/site/`](./docs/web/site/) — static source for the public landing page

## Relationship to nearby repos

- [`ship-receipts`](https://github.com/Spitfire-Cowboy/ship-receipts) — local receipt generator / evidence layer
- `proofofship` — independent verifier and public trust surface
- this repo documents the public Proof of Ship surface directly

## Public URLs

- Site: <https://proofofship.com>
- Public profiles: `https://proofofship.com/u/<handle>`
- Public score JSON: `https://proofofship.com/u/<handle>/score.json`
- Public receipts JSON: `https://proofofship.com/u/<handle>/receipts.json`
- Public badges: `https://proofofship.com/badges/verified.svg`, `https://proofofship.com/badges/receipts.svg`

## Status

This public repo now contains both shipped public assets and contract-level docs.

### Publicly shipped today
- live landing page at `proofofship.com`
- live public badge assets
- public profile, score, and receipts route shapes
- public schemas, examples, and badge assets in the repo
- public CLI for scores, receipts, badges, URLs, and repo checks

### Contract-level docs in this repo
- GitHub OAuth and account/repo-linking contract
- verifier architecture and verification-depth semantics
- ledger, reputation, and badge guidance specs

### Still in progress
- GitHub OAuth web login implementation
- account/repo-linking UI

See [`docs/public-surfaces.md`](./docs/public-surfaces.md) for the live vs repo-shipped vs contract-only map.

## License

Apache 2.0. See [`LICENSE`](./LICENSE).
