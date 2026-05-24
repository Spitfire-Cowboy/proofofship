# Proof of Ship

**Independent verification and reputation from public evidence.**

Proof of Ship is the public home for the product narrative, protocol surface, schemas, and landing-page source for `proofofship.com`.

It exists to answer one question:

> *What has this person actually built, and how credible is that claim?*

A builder ships work in a public repository. A local tool such as [`ship-receipts`](https://github.com/Spitfire-Cowboy/ship-receipts) produces a proof envelope. Proof of Ship independently verifies that claim against the public record and turns verified work into a publicly auditable reputation signal.

## What this public repo contains

- public README and docs
- protocol and scoring specs
- public JSON schemas
- the landing-page source for `proofofship.com`
- contribution / security / review config for the public surface

## What this public repo does **not** contain

- private deployment internals
- secrets or environment-specific configuration
- internal staging runbooks
- private anti-abuse heuristics that would be irresponsible to publish prematurely

The hosted implementation and operations remain private for now. This repo is the public contract and narrative layer.

## Core idea in 30 seconds

1. A builder ships work in a public repo.
2. A local tool generates a verifiable proof envelope.
3. Proof of Ship independently verifies the claim against the public record.
4. Verified work contributes to a deterministic, time-decayed reputation score.
5. Anyone can inspect the rules and recompute the score from public inputs.

No self-reported prestige. If it cannot be independently verified, it does not count.

## Repo map

- [`docs/`](./docs/) — public docs index
- [`docs/specs/`](./docs/specs/) — protocol, ledger, scoring, and roadmap specs
- [`docs/web/site/`](./docs/web/site/) — static source for the public landing page

## Relationship to nearby repos

- [`ship-receipts`](https://github.com/Spitfire-Cowboy/ship-receipts) — local receipt generator / evidence layer
- private implementation and operations remain in a separate internal repository for now

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

What is still in progress overall:
- GitHub OAuth web login flow
- account/repo-linking UI
- public profile pages
- hosted verification service as a public code surface

See [`docs/specs/proofofship-roadmap-v1.md`](./docs/specs/proofofship-roadmap-v1.md).

## License

Apache 2.0. See [`LICENSE`](./LICENSE).
