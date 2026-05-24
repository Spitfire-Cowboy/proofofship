# proofofship.com static site deploy notes

This directory is the thin-slice static scaffold for proofofship.com.

## Contents

- `index.html` — landing page
- `style.css` — minimal site styling
- `docs/index.html` — redirect page for `/docs`

## Deploy options

## 1) GitHub Pages (recommended for thin-slice)

1. In GitHub repo settings, enable Pages from the branch/folder that publishes this directory.
2. Publish `docs/web/site` as the site root (or copy contents to the selected publish folder).
3. Add a `CNAME` file with:
   - `proofofship.com`
4. Set DNS records with your registrar to point to GitHub Pages.
5. Verify HTTPS is enabled and force HTTPS redirect.

## 2) Netlify or Cloudflare Pages

1. Create a new static site from this repo.
2. Set publish directory to `docs/web/site`.
3. No build command required.
4. Attach custom domain `proofofship.com`.
5. Enable HTTPS and redirects:
   - `http://proofofship.com` -> `https://proofofship.com`
   - `www.proofofship.com` -> `proofofship.com`

## Content alignment rule

When status changes in the codebase, update section 6 first.

- Live now: code exists and tests pass today.
- Specified, not yet deployed: designed/spec'd but not live.
- Planned: design not finalized.

Keep labels explicit for all non-live features.
