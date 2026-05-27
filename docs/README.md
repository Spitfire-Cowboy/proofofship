# Docs index

## 🔗 Start here

- [Concepts](./concepts.md)
- [CLI reference](./cli.md)
- [Public surfaces reference](./public-surfaces.md)
- [Global ledger contract](./global-ledger-contract.md)

## 🧩 Core specs

- [Reputation model](./specs/proofofship-reputation-model-v1.md)
- [Ledger and reputation](./specs/proofofship-ledger-and-reputation-v1.md)
- [Verifier architecture](./specs/proofofship-verifier-architecture-v1.md)
- [GitHub auth and repo linking](./specs/proofofship-github-auth-and-repo-linking-v1.md)
- [Repo badge guidance](./specs/proofofship-repo-badges-v0.md)
- [Global game loop](./specs/proofofship-global-game-loop-v1.md)
- [Roadmap](./specs/proofofship-roadmap-v1.md)

## 📚 Public schemas

- `docs/schemas/proofofship/score.v0.1.schema.json`
- `docs/schemas/proofofship/receipts.v0.1.schema.json`
- `docs/schemas/proofofship/github-account.v0.1.schema.json`
- `docs/schemas/proofofship/linked-repositories.v0.1.schema.json`
- `docs/schemas/proofofship/link-repository-request.v0.1.schema.json`
- `docs/schemas/proofofship/link-repository-result.v0.1.schema.json`

## 🧪 Public examples

- `examples/score.public.sample.json`
- `examples/receipts.public.sample.json`
- `examples/account.github.public.sample.json`
- `examples/linked-repositories.public.sample.json`
- `examples/link-repository-request.public.sample.json`
- `examples/link-repository-result.public.sample.json`
- `examples/global-ledger.sample.jsonl`

## 🖼️ Site and assets

- [Public site source](./web/site/)
- [Site deploy notes](./web/site/DEPLOY.md)
- `docs/web/site/site.css`
- `docs/web/site/app.css`
- `docs/web/site/badges/verified.svg`
- `docs/web/site/badges/receipts.svg`
- `docs/web/site/favicon.svg`
- `docs/web/site/og-preview.png`
- `docs/web/site/site.webmanifest`
- `docs/web/site/robots.txt`
- `docs/web/site/sitemap.xml`

## 🧱 Boundaries

This public repo is documentation-first.

It focuses on the public contract: docs, schemas, examples, and the public site surface.
Some operator-side and anti-abuse logic is intentionally not part of the public repo.

## 🐍 CLI notes

- install locally with `pip install -e .`
- use `proofofship --help` to inspect the public CLI surface
- the CLI currently exposes deterministic public score math, badge helpers, schema validation, URL helpers, and repo integrity checks
