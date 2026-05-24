# Public surfaces reference

This page maps the currently documented public surfaces of Proof of Ship.

## Status labels

- **live** — publicly reachable today
- **repo-shipped** — present in this public repo as docs/schema/example/asset/CLI output
- **contract-only** — publicly specified here, but not claimed as broadly deployed UI yet

## Website and assets

| Surface | Status | Notes |
|---|---|---|
| `https://proofofship.com/` | live | Public landing page |
| `https://proofofship.com/favicon.svg` | live | Site icon |
| `https://proofofship.com/badges/verified.svg` | live | Badge asset |
| `https://proofofship.com/badges/receipts.svg` | live | Badge asset |

## Public profile routes

| Surface | Status | Notes |
|---|---|---|
| `/u/<handle>` | live | Human-readable public profile route |
| `/u/<handle>/score.json` | live | Public score surface |
| `/u/<handle>/receipts.json` | live | Public receipts surface |

## Auth and account contract

| Surface | Status | Notes |
|---|---|---|
| `GET /auth/github/start` | contract-only | OAuth initiation flow |
| `GET /auth/github/callback` | contract-only | OAuth callback flow |
| `POST /auth/logout` | contract-only | Logout flow |
| `GET /api/v1/account` | contract-only | Account payload schema published |
| `GET /api/v1/account/repositories` | contract-only | Linked repositories payload published |
| `POST /api/v1/account/repositories` | contract-only | Link request/result schemas published |
| `DELETE /api/v1/account/repositories/{owner}/{repo}` | contract-only | Unlink behavior documented |

## Repo-shipped JSON schemas

| File | Status |
|---|---|
| `docs/schemas/proofofship/score.v0.1.schema.json` | repo-shipped |
| `docs/schemas/proofofship/receipts.v0.1.schema.json` | repo-shipped |
| `docs/schemas/proofofship/github-account.v0.1.schema.json` | repo-shipped |
| `docs/schemas/proofofship/linked-repositories.v0.1.schema.json` | repo-shipped |
| `docs/schemas/proofofship/link-repository-request.v0.1.schema.json` | repo-shipped |
| `docs/schemas/proofofship/link-repository-result.v0.1.schema.json` | repo-shipped |

## CLI public surface

| Command | Status | Notes |
|---|---|---|
| `proofofship weight` | repo-shipped | Time-decay math |
| `proofofship score` | repo-shipped | Score payload output |
| `proofofship receipts` | repo-shipped | Receipts payload output |
| `proofofship badge` | repo-shipped | Badge markdown / URL helper |
| `proofofship urls` | repo-shipped | Canonical route helper |
| `proofofship check-public-surface` | repo-shipped | Repo integrity check |
