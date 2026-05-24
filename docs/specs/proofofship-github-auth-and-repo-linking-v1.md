# Proofofship GitHub Auth and Repo Linking v1

This document defines the **public contract** for GitHub sign-in and public-repository linking.

It defines the web-visible behavior and payload shapes that public clients may rely on. It does not attempt to document every operator detail or internal implementation choice.

## Goals

1. Let a builder sign in with GitHub instead of creating a local password.
2. Let a signed-in builder link public repositories they control.
3. Keep the trust boundary explicit: GitHub OAuth proves identity; repo linking proves repository relationship; neither by itself proves authorship of every line of code.
4. Publish enough of the contract that other tools can integrate against stable public behavior.

## Non-goals

- No local username/password accounts
- No promise that every internal policy decision will be externally documented
- No promise that every future identity provider will match GitHub semantics

## Identity model

The canonical authenticated identity is a GitHub user.

Minimum durable fields:
- `provider`: always `github` in v1
- `github_id`: numeric GitHub user id
- `login`: GitHub handle
- `display_name`: optional GitHub profile name
- `avatar_url`: optional avatar URL
- `html_url`: public GitHub profile URL
- `account_status`: `active`, `restricted`, or `pending`

## OAuth web flow

### 1. Start sign-in

The browser requests:

```text
GET /auth/github/start
```

Server behavior:
- creates an OAuth state value
- redirects to GitHub authorization

### 2. GitHub callback

GitHub redirects back to:

```text
GET /auth/github/callback?code=...&state=...
```

Server behavior:
- validates `state`
- exchanges `code` for an access token
- fetches the GitHub user profile
- creates or updates the local account row keyed by `github_id`
- creates an authenticated session
- redirects the browser to the account surface

### 3. Authenticated account read

The web client reads:

```text
GET /api/v1/account
```

Response shape: [`docs/schemas/proofofship/github-account.v0.1.schema.json`](../schemas/proofofship/github-account.v0.1.schema.json)

### 4. Sign out

The browser calls:

```text
POST /auth/logout
```

Server behavior:
- invalidates the local session
- does not delete the underlying account row

## Repository linking model

A linked repository is a **public GitHub repository** that the signed-in account is allowed to associate with its public Proofofship profile.

Linking a repo asserts only:
1. the repo is public
2. the authenticated GitHub user has the required relationship to the repo
3. the repo should count toward that profile's public evidence surface

Linking does **not** assert sole authorship or quality.

### Accepted relationships

A repo may be linked when the signed-in user is at least one of:
- owner
- organization admin for the repo's org
- collaborator with push access

The public contract says **what must be true**, not every implementation detail of how that truth is established.

## Repo-linking endpoints

### Read linked repos

```text
GET /api/v1/account/repositories
```

Response shape: [`docs/schemas/proofofship/linked-repositories.v0.1.schema.json`](../schemas/proofofship/linked-repositories.v0.1.schema.json)

### Link a repo

```text
POST /api/v1/account/repositories
Content-Type: application/json
```

Request shape: [`docs/schemas/proofofship/link-repository-request.v0.1.schema.json`](../schemas/proofofship/link-repository-request.v0.1.schema.json)

Response shape: [`docs/schemas/proofofship/link-repository-result.v0.1.schema.json`](../schemas/proofofship/link-repository-result.v0.1.schema.json)

### Unlink a repo

```text
DELETE /api/v1/account/repositories/{owner}/{repo}
```

Expected behavior:
- removes the repo from the account's linked-repo set
- does not delete previously verified public receipts from the immutable ledger
- may hide the repo from future profile aggregation, depending on policy

## Public payload shapes

### Account payload

`GET /api/v1/account` returns an authenticated account snapshot suitable for a web settings page.

Key fields:
- identity fields copied from GitHub
- canonical profile URL
- linked repo count
- flags for whether repo linking is available and whether the session is authenticated

### Linked repositories payload

`GET /api/v1/account/repositories` returns the signed-in account's current public repo links.

Each item includes:
- GitHub owner/repo
- repo URL
- visibility
- permission relationship
- linked timestamp
- whether the repo currently contributes to profile scoring

### Link result payload

The result of `POST /api/v1/account/repositories` is explicit, not magical. It should say:
- whether linking succeeded
- whether the repo was newly linked or already linked
- which policy checks passed
- why linking failed, if it failed

## Error semantics

Stable public error codes for repo linking:
- `not_authenticated`
- `repo_not_found`
- `repo_not_public`
- `insufficient_repo_permission`
- `provider_mismatch`
- `validation_error`
- `rate_limited`

Private heuristics may produce these public failure categories without exposing the underlying scoring or abuse logic.

## Security notes

- OAuth access tokens are server-side secrets and are never returned in public payloads.
- The public repo does not document token storage internals.
- Public payloads may include GitHub-derived URLs and numeric ids, but not bearer tokens or session secrets.
- Repo linking is a profile-configuration action, not a proof of authorship action.

## Relationship to reputation

Linked repos influence **what evidence may be surfaced on a profile**, not the trust boundary itself. Reputation still comes from independently verified receipts and public artifacts.

## Versioning

All payload shapes in this slice are versioned `v0.1`. Breaking schema changes should bump the version rather than silently mutate existing payloads.
