# Houdini Website

A static replica of the Club Penguin website ("Houdini") — an informational site (home, help) that links out to an external game server for account creation and play.

## Overview

- **Architecture**: Fully static site. No backend server, no database. All pages are plain, pre-rendered HTML served from `public/`.
- **Pages**: `public/index.html` (home), `public/help.html`, `public/404.html`. Assets live in `public/static/` (css, js, images, fonts).
- **Preview server**: `serve.py` is a tiny Python `http.server` wrapper used only for local dev preview (serves `public/`, and returns `public/404.html` on unmatched routes). It plays no role in production — the production deployment target is `static`, which serves `public/` directly with no server process.
- **External links**: "Play Now!", the nav "Play" link, and "Unlock Items" all point to `https://play.cpoldschool.dpdns.org/en/#/login`. "Create Account" links point to `https://play.cpoldschool.dpdns.org/penguin/create`. There is no local login, account creation, or account panel — that functionality now lives entirely on the external game server.

## History

- Originally imported as a Python 2.7/MySQL Flask app, ported to Python 3.12 + Replit PostgreSQL, then later converted to a fully static site (this removed the Flask backend, SQLAlchemy models, and the local login/account panel/database entirely) per user request for zero-maintenance hosting.
- "Play Now", "Create Account", and the nav "Play" link were pointed at the external game server before the static conversion; the static conversion carried those links over unchanged and removed everything else that depended on the local database.

## Notes

- A handful of static JS assets referenced in the pages (e.g. `wbhack.js`, `toolbar.js`, `graph-calc.js`) are missing from the original repo and 404 — this predates the Replit import and is cosmetic/tracking-script related, not a functional issue.
- The original Replit-managed PostgreSQL database is no longer used by the app. All code and config that referenced it (`DATABASE_URL`, SQLAlchemy models, Flask blueprints) was removed. The underlying database resource itself can only be fully de-provisioned from the Database pane in the Replit UI — ask if you want it removed there too.
