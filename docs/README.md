# Docs index

## Start here

1. [Concepts](./concepts.md)
2. [Global ledger contract](./global-ledger-contract.md)
3. [Roadmap](./specs/proofofship-roadmap-v1.md)

## Core specs

- [Reputation model](./specs/proofofship-reputation-model-v1.md)
- [Global game loop](./specs/proofofship-global-game-loop-v1.md)
- [Ledger and reputation](./specs/proofofship-ledger-and-reputation-v1.md)

## Website

- [Public site source](./web/site/)
- [Site deploy notes](./web/site/DEPLOY.md)

## Notes

This public repo is documentation-first.

It intentionally excludes private deployment internals, staging runbooks, and sensitive operational details from the private implementation repo.

## CLI

- Install locally with `pip install -e .`
- Use `proofofship --help` to inspect the public CLI surface
- The CLI currently exposes deterministic public score math, URL helpers, and repo integrity checks

## Public schemas

- `docs/schemas/proofofship/score.v0.1.schema.json`
- `docs/schemas/proofofship/receipts.v0.1.schema.json`

## Public examples

- `examples/score.public.sample.json`
- `examples/receipts.public.sample.json`
