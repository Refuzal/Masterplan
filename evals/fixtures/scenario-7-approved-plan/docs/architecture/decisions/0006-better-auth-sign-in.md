# ADR-0006: Groomer sign-in with Better Auth

- Status: Accepted
- Date: 2026-10-19
- Decided by: Owner (approved the architecture package on 2026-10-19)
- Confidence: Medium-High
- Change later: Moderate
- See also: ADR-0011 (only the owner signs in for a business in version 1)

## Context
Groomers and the platform admin sign in; clients never do (FR-3). There will be about 50 groomer accounts in year one. The platform admin account can see every business's status, so it needs two-step sign-in. Custom-built sign-in is ruled out: storing passwords and sessions by hand is a known source of serious bugs.

## Options considered
1. **Better Auth** — open-source library; users and sessions live in our PostgreSQL next to business data; email and password with verification, password reset, rate limiting, and two-step sign-in (authenticator app) as plugins; no per-user fees; actively maintained / its code runs in our app, so configuration mistakes are ours; we keep it updated.
2. **Clerk** — fully managed sign-in with ready-made screens; free plan covers 50,000 retained users / two-step sign-in and removing Clerk branding need the Pro plan ($25 a month billed monthly); user records live in a second system that must be kept in step with ours.
3. **Auth.js (NextAuth)** — familiar / receives security fixes only; its maintainers point new projects to Better Auth.

## Decision
Better Auth with its Drizzle adapter: email and password with email verification and password reset; built-in rate limiting on sign-in; sessions in secure, http-only cookies; two-step sign-in required for platform admins and available to owners. The platform admin flag can only be set on an account that already has two-step sign-in, so no admin account exists without it.

## Why
- Free at any realistic size, including two-step sign-in for the admin account.
- Users sit in the same database as businesses, which keeps memberships (ADR-0005) simple, with nothing to sync.
- Clerk was the closest alternative and is the fallback if sign-in becomes a maintenance burden; it lost on the cost of two-step sign-in and the second user store.

## Consequences
- Good: no vendor fees; full control; simple data model.
- Costs and tradeoffs: security updates to Better Auth must be applied promptly (dependency alerts are on); sign-in flows need end-to-end tests.
- Follow-up work: M1 sets up sign-up, sign-in and sign-out; two-step sign-in ships with the first admin screen (M3) and before any admin account exists in production.

## Evidence
- Better Auth releases: v1.7.2 on 2026-08-26 marked Latest; seven releases between 11 and 26 August — https://github.com/better-auth/better-auth/releases (checked 2026-10-19)
- Clerk pricing: Hobby plan 50,000 monthly retained users per app, MFA not included; Pro $25/month billed monthly — https://clerk.com/pricing (checked 2026-10-19)
- Auth.js status and Lucia deprecation: planning method's known-stale-defaults list (checked October 2026)

## Revisit when
- A Better Auth security advisory is not patched within 7 days, or the project stops regular releases for 6 months.
- Groomers ask for sign-in with Google or Apple, or business customers ask for single sign-on.
