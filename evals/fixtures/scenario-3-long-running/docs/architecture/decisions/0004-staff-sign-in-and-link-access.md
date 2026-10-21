# ADR-0004: Staff sign-in with django-allauth; renters and vendors through secure links

- Status: Accepted
- Date: 2026-10-19 (link rules tightened the same day after the review panel, before any code)
- Decided by: Product owner, approving the recommended architecture package on 2026-10-19. Ravi confirms in M0.
- Confidence: High
- Change later: Moderate

## Context
Staff (company admins, property managers, maintenance coordinators) sign in (FR-5, FR-10). Renters and vendors must not need accounts: they use links sent by email or text (FR-1, FR-2, FR-4, NFR-8). Larger customers will eventually ask for single sign-on, which must not require moving existing accounts (FR-9). Budget favors no per-user fees.

## Options considered
Staff sign-in:
1. **django-allauth** — free, mature, built for Django; email login, passwords, passkeys, two-step verification (TOTP, WebAuthn, recovery codes), rate limits, SAML 2.0 and OpenID Connect / the team owns password security settings and per-customer SSO setup.
2. **WorkOS AuthKit** — hosted sign-in, free up to 1 million users; self-serve SSO setup for customers' IT teams at $125 per connection a month / an outside service on every sign-in.
3. **Building sign-in by hand** — rejected (material risk).

Renter and vendor links:
1. **Random tokens stored as hashes, exchanged for a short-lived session** — revocable one by one; a database leak exposes no usable links.
2. **Signed tokens without database storage** — no lookup / cannot revoke a single link without extra machinery.
3. **A one-time code on every visit** — strongest / contradicts "renters just use a link".

## Decision
- Staff sign in with django-allauth: email plus password, or a passkey. Two-step verification (authenticator app or passkey) is required for company admins and available to everyone else. Passwords are hashed with Argon2. Invitations are single-use and expire after 7 days.
- Single sign-on (FR-9) is added when the first customer asks: allauth's SAML or OpenID Connect support, or WorkOS SSO if customers' IT teams need to set it up themselves. Staff accounts stay in our database either way, so nobody's account moves.
- Links: `links.tokens` creates 32-byte random tokens (`secrets.token_urlsafe(32)`) and stores only their SHA-256 hash with the company, kind (renter or vendor), subject, expiry and revocation time. Opening a link exchanges the token for a session cookie (HttpOnly, Secure, SameSite=Lax) and redirects to an address without the token. Link pages send `Referrer-Policy: no-referrer`, and tokens are scrubbed from logs and error reports.
- A renter link opens only that renter's requests. It lasts until staff revoke it, the renter is archived, or it goes 180 days unused. A renter can request a new one by entering their phone number or email (FR-2). Re-issue is limited per contact (one per 10 minutes, three per day) and per company per day; the old link keeps working until the new one is first opened, so nobody can lock a renter out by requesting links; staff see a warning when a contact hits the limit.
- A vendor link opens only one work order and expires 30 days after the work order closes.

## Why
- allauth covers everything version 1 needs and the SSO path, at no per-user cost and with no outside service on the sign-in path.
- Hashed, scoped, revocable links keep the product's "no accounts" promise while limiting what a forwarded or leaked link can do.
- WorkOS remains the faster SSO route if self-serve setup matters more than its per-connection fee.

## Consequences
- Good: no sign-in vendor fees; SSO without account migration; links can be revoked individually.
- Costs and tradeoffs: anyone holding a renter or vendor link can act as that renter or vendor (accepted by product design; limited by scope, expiry and revocation). The team maintains sign-in settings and must keep allauth updated.
- Follow-up work: link and sign-in security tests (NFR-8) in M1 and M2; a sign-in and admin-action audit log.

## Evidence
- [django-allauth on PyPI](https://pypi.org/project/django-allauth/) (checked 2026-10-19) — version 65.20.0 released 2026-10-16; SAML 2.0 and OpenID Connect; supports Django 4.2–6.1.
- [django-allauth MFA documentation](https://docs.allauth.org/en/latest/mfa/introduction.html) (checked 2026-10-19) — TOTP, recovery codes, WebAuthn and passkey login.
- [WorkOS pricing](https://workos.com/pricing) (checked 2026-10-19) — AuthKit free up to 1 million users; SSO $125 per connection a month for the first 15.

## Revisit when
- The first customer asks for single sign-on (choose allauth SAML/OIDC or WorkOS, and record it in a new ADR).
- A link is abused, or customers ask for renter accounts.
- allauth stops being maintained.
