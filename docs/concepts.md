# Concepts

## Ship Receipts
A **Ship Receipt** is a small, verifiable record of shipped work: artifact + verify hooks + provenance.

Public integration today:
- https://github.com/Spitfire-Cowboy/ship-receipts

## Diminishing Returns (DR)
A lightweight “stop/ship” signal for multi-agent or long conversations.

This concept informs the broader Proof of Ship constellation, but its implementation is not required to understand this public repo.

## Renderable Prompt Object (RPO)
A prompt IR that can be rendered into different targets (UI, API, chat) with stable structure.

Included here only as background context for the broader ecosystem.

## This repo (Proof of Ship)
This is the public product and protocol layer: public docs, schemas, and landing-page source for the hosted verification and reputation surface.

Deliberate constraint: keep the public surface small, explicit, and auditable. Public claims should match what this repo actually documents and exposes. Proof of Ship also requires some hidden and proprietary enforcement code; the public repo should not pretend otherwise.
