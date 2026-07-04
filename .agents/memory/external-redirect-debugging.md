---
name: External redirect/proxy debugging methodology
description: How to isolate whether an unexpected redirect/404 comes from app code, DNS, a CDN/proxy edge, or a separate origin server — before touching app code.
---

When a link to an external domain unexpectedly 404s or redirects somewhere wrong, don't assume the bug is in this project's code just because the redirect target happens to be this project's URL.

Diagnostic order that worked:
1. `fetch(url, { redirect: "manual" })` on the failing URL — read the `Location` header and the `server`/`cf-ray` response headers. If `server: cloudflare` (or another CDN) appears, the redirect is happening at the edge/proxy, not at the origin app.
2. DNS lookup (`resolveCname`/`resolve4`) on the exact failing hostname — compare to the working hostname. If both resolve to the same shared anycast IPs (e.g. Cloudflare's `104.21.x`/`172.67.x`), DNS alone doesn't explain routing; the actual origin selection happens in the proxy's rule engine (Redirect Rules, Page Rules, Workers Routes), not in DNS records.
3. Only once the edge is ruled out (200 without redirect, or a redirect that matches the correct origin) should you suspect the origin server's own code/config.

**Why:** In this case, a Cloudflare Redirect Rule scoped with a "contains"-style match on the apex domain (`cpoldschool.dpdns.org`) unintentionally caught all subdomains (`play.cpoldschool.dpdns.org`), silently redirecting an unrelated VPS-hosted service to this project's static site. Nothing in this project's code or deployment config was ever the cause, but the redirect target being this project's own URL made it look that way at first.

**How to apply:** When a user reports "the deployed app links go to the wrong place" or "buttons 404", check response headers for the failing URL before touching app code or redeploying. If the response comes from a CDN/proxy the project doesn't control, the fix lives in that proxy's rule configuration, not in the app.
