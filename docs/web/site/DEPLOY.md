# proofofship.com static site deploy notes

This directory is the public static landing page for `proofofship.com`.

## Contents

- `index.html` — Tailwind-based marketing site
- `site.css` — compiled self-hosted stylesheet
- `app.css` — Tailwind source used to build the site stylesheet
- `favicon.svg` — site icon
- `docs/index.html` — first-party docs hub
- `schemas/` — DR schema files used by the static public surface
- `badges/` — embeddable public badge assets

## Current implementation note

The site now uses a compiled, self-hosted Tailwind stylesheet:

- source: `docs/web/site/app.css`
- output: `docs/web/site/site.css`

Build it with:

```bash
npm install
npm run build:site-css
```

Current required CSP shape for the landing page:

```text
Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self';
```

## Deploy options

### 1) GitHub Pages (good for the thin slice)

1. Enable Pages from a branch/folder that publishes this directory.
2. Publish `docs/web/site` as the site root (or copy contents to the selected publish folder).
3. Add a `CNAME` file with `proofofship.com`.
4. Point DNS at GitHub Pages.
5. Verify HTTPS and canonical redirects.

### 2) Netlify or Cloudflare Pages

1. Create a new static site from this repo.
2. Set publish directory to `docs/web/site`.
3. No build command required.
4. Attach custom domain `proofofship.com`.
5. Enable HTTPS and redirects:
   - `http://proofofship.com` -> `https://proofofship.com`
   - `www.proofofship.com` -> `https://proofofship.com`

## Content alignment rule

The homepage should describe what exists now. Keep roadmap and future-state material in docs, not in the marketing page.
