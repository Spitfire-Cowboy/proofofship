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
- checked-in examples live at `examples/score.public.sample.json` and `examples/receipts.public.sample.json`
- `proofofship urls <handle>` — print canonical public profile URLs
- `proofofship check-public-surface` — verify the public repo contains the expected files and no obvious secret-like strings

Quick start:

```bash
pip install -e .
proofofship score examples/score.sample.json --handle example-builder --json
```

## Repo map

- [`docs/`](./docs/) — public docs index
- [`docs/specs/`](./docs/specs/) — protocol, ledger, scoring, auth, and roadmap specs
- [`docs/web/site/`](./docs/web/site/) — static source for the public landing page

## Relationship to nearby repos

- [`ship-receipts`](https://github.com/Spitfire-Cowboy/ship-receipts) — local receipt generator / evidence layer
- `proofofship` — independent verifier and public trust surface
- this repo documents the public Proof of Ship surface directly

## Public URLs

- Site: <https://proofofship.com>
- Planned public profiles: `https://proofofship.com/u/<handle>`
- Planned score JSON: `https://proofofship.com/u/<handle>/score.json`
- Planned receipts JSON: `https://proofofship.com/u/<handle>/receipts.json`

## Status

This public repo is intentionally thin and documentation-first.

What exists publicly here today:
- public landing-page source
- public schemas
- public product and scoring docs
- public GitHub OAuth and repo-linking contract docs

What is still in progress overall:
- GitHub OAuth web login implementation
- account/repo-linking UI
- public profile pages
- hosted verification service as a public code surface

See [`docs/specs/proofofship-roadmap-v1.md`](./docs/specs/proofofship-roadmap-v1.md).

## License

Apache 2.0. See [`LICENSE`](./LICENSE).
