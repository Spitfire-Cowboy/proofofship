# Proofofship Repo Badges v0

This note defines the first honest badge surfaces for third-party repositories.

## Goal

Give a repository owner a compact way to say:
- this repo participates in Proof of Ship
- receipts exist
- public verification data is available

## What we can honestly badge now

### 1. Verified by Proof of Ship

Use when:
- the repo has public receipts
- the repo is linked to a public Proof of Ship profile
- those receipts are being independently verified by the service

Suggested text:
- `Verified by Proof of Ship`
- `Public receipts verified`

### 2. Public score available

Use when:
- the owning profile exposes `score.json`
- the repo is part of that public profile surface

Suggested text:
- `Public score available`
- `Proof of Ship profile live`

## What we should NOT claim yet

### “OSS-free” or “entirely free of OSS projects”

Do **not** badge this today.

Reason:
- Proof of Ship currently verifies positive public evidence about shipping and identity.
- It does **not** currently prove the absence of open-source dependencies, inspiration, copied code, vendored components, transitive dependencies, or training influence.

That is an absence claim, and absence claims are easy to overstate.

## If we want an OSS-independence badge later

It needs a narrower, auditable definition.

Good future badge candidates:
- `No OSS dependencies declared`
- `Lockfile audit passed`
- `Dependency provenance attested`
- `Third-party provenance manifest present`

Those are better because they name the exact evidence surface being checked.

## Recommended first badge contract

Start with two positive badges only:

1. `Verified by Proof of Ship`
2. `Public receipts available`

Both are concrete, narrow, and defensible.


## Example embed snippets

Markdown badge examples the repo can emit now:

```md
[![Verified by Proof of Ship](https://proofofship.com/badges/verified.svg)](https://proofofship.com/u/<handle>)
[![Public receipts available](https://proofofship.com/badges/receipts.svg)](https://proofofship.com/u/<handle>/receipts.json)
```

These should link to a concrete public surface, not to marketing copy.

## Badge design rule

Every badge must answer two questions cleanly:
1. What exactly is being claimed?
2. Where can a skeptical reader inspect the evidence?

If a badge cannot answer both, do not ship it.


## Shipped assets

The public site now serves these static badge assets:

- `https://proofofship.com/badges/verified.svg`
- `https://proofofship.com/badges/receipts.svg`
