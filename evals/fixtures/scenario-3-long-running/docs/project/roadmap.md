# Roadmap

> Purpose: what gets built in what order, and how each milestone is accepted. Update when a milestone finishes or scope moves. Owner: product owner with Ravi (backend co-founder, lead engineer).

Target: pilot with about 20 companies in February–March 2027 (overview.md › Constraints). Week numbers count from the start of M0 and are estimates.

## M0 — Safe to build (weeks 1–2) — Done 2026-11-02
Goal: make it safe for AI agents and people to change this repository, prove the riskiest assumptions with small spikes, and start the slow outside approvals early.
- [x] Ravi reads ADR-0001 to ADR-0009 and confirms them, or raises a change through `/masterplan change`
- [x] Code in a GitHub repository (Team plan) with a protected `main`; changes arrive through pull requests with one human approval; CODEOWNERS on the guardrail files; a bot account for coding agents (standards.md › Source control)
- [x] CI runs formatting, lint, typecheck, tests, dependency audit and secret scanning on every pull request (standards.md › Quality gates), on an empty Django project skeleton
- [x] Agents cannot reach production credentials or production data; production secrets live in Render environment groups, and agent sessions use test-mode keys only
- [x] Accounts created in test mode: Render (Pro workspace), Cloudflare (two accounts: photos and backups), Amazon SES, Twilio, Stripe, Sentry, Better Stack
- [x] Billing alerts set on every paid service
- [x] Twilio: our own business profile and our staff-alert toll-free number submitted for verification; written confirmation from Twilio support that company numbers for renter and vendor texts plus our number for staff alerts meets their rules; Canadian per-message rates checked (ADR-0008)
- [x] Lawyer engaged for the customer terms (including that urgent alerts are best effort), data processing agreement and privacy notice; accountant engaged for sales tax registrations (risks.md R-5)
- [x] Spike A (ADR-0003): on a Render PostgreSQL 18 test database, create the app and metrics roles with SQL, prove the standard policy, one lookup policy, the metrics `SELECT` policy, and a backup run as the owner role; if Render blocks any of it, write a superseding ADR before M1
- [x] Spike B (ADR-0005): prove that a Procrastinate job deferred inside a rolled-back Django transaction disappears; otherwise switch to `transaction.on_commit` and record it in ADR-0005
- [x] Spike C (ADR-0001): install every planned dependency (Procrastinate, django-allauth, django-storages, pillow-heif, Playwright, mypy with django-stubs) on Python 3.14 with Django 6.1; if any fails, use Python 3.13 and record it in ADR-0001
Verification: a trivial pull request passes every check; a pull request containing a planted fake secret is blocked; a test confirms an agent session has no production environment variables; each spike's result and Ravi's confirmation are recorded in state.md and the ADRs.

## M1 — Walking skeleton (weeks 3–5) — Done 2026-11-23
Goal: the thinnest end-to-end slice through every layer, deployed through the real pipeline. It proves the stack early, when changing it is cheap, and gives agents a working pattern to copy.
Scope: the Django project with the app layout from architecture.md and the import contracts switched on; `core.tenancy` with row-level security, the owner, app and metrics roles, one lookup policy (link tokens) and the isolation test harness; staff sign-in with django-allauth for a seeded company; staff add one building, unit and renter by hand; the renter link opens, and the renter submits a maintenance request with one photo uploaded straight to R2 and processed by a job on the `media` queue; the request appears in the staff queue; Amazon SES sends the staff notification from the `messages` queue; `render.yaml` deploys previews and production; Sentry, the uptime check, both queue heartbeats and the nightly backup job are running.
Acceptance criteria:
- Given a seeded company and staff member, when the staff member signs in and adds a building, unit and renter, then a renter link is created and only its hash is stored.
- Given that renter link, when the renter opens it on an iPhone and on an Android phone and submits a request with a photo, then staff see the request with the processed photo (no location data) and a notification email is sent (captured by the SES mailbox simulator in previews).
- Given two companies, when staff of company A request any company-scoped address using company B's IDs, then they get "not found"; and the schema test confirms row-level security on every company table, that the app role is neither owner nor `BYPASSRLS`, and that the only lookup policies are the listed ones.
- Given a pull request, when it is opened, then a preview environment with seed data is created; when it is merged after approval, then production deploys and the health check passes; when the previous release is redeployed, then the app keeps working.
- Given last night's backup, when the restore runbook (architecture.md › Operations) is followed into a scratch database, then the roles, policies and smoke tests check out and the restore time is recorded against NFR-3.
Verification: CI is green; a founder runs the flow on two real phones against a preview; a test error appears in Sentry; Better Stack shows the check and both heartbeats; the restore drill result is written in architecture.md › Operations; AGENTS.md › Commands is filled in.
Depends on: M0

## M2 — The maintenance loop (weeks 6–10) — Done 2026-12-18
Scope: FR-1 to FR-4 complete, FR-11 (emergency line, and urgent alerts texted from our staff-alert number), FR-12, FR-13, FR-15, FR-16; notifications by email (FR-14 email part).
Acceptance criteria: see requirements.md for each FR.
Verification: the renter → staff → vendor end-to-end journey passes in CI; a founder runs it on real phones; isolation tests cover every new page and job.
Depends on: M1

## M3 — Onboarding and texts (weeks 11–14) — In progress
Progress: FR-10 done (2026-12-30); FR-5 in progress; FR-6 and FR-14 texts not started.
Scope: FR-10 (company setup and invitations), FR-5 (roles and two-step verification for company admins), FR-6 (spreadsheet import), FR-14 texts to renters and vendors (toll-free number per company, verification flow, STOP handling, email fallback).
Acceptance criteria: see requirements.md.
Verification: a new company goes from sign-up to its first renter request without founder help in a preview; a test company's toll-free number is verified in Twilio; STOP replies stop texts.
Depends on: M2

## M4 — Billing and pilot readiness (weeks 15–18)
Scope: FR-7 (Stripe Billing with trials), FR-22 (data export and deletion runbook), FR-23 (pilot metrics); accessibility pass (NFR-5); timed photo-upload test on phones (NFR-1); restore drill (NFR-3); status page live; customer terms, data processing agreement and privacy notice published.
Acceptance criteria: see requirements.md; plus every NFR target measured once and recorded.
Verification: a test company subscribes, adds a building and is charged the right quantity in Stripe test mode; the founders review the metrics page; the readiness of each pilot company's toll-free number is checked.
Depends on: M3

## Buffer (weeks 19–20)
Two weeks held for slips in outside approvals and fixes from the first pilot onboarding. If M2 is not done by week 10, cut in the order in risks.md R-11 rather than move the pilot date (approved by the product owner 2026-10-19).

## Pilot (February–March 2027 onward, about three months)
Onboard about 20 companies in waves of five; measure the success criteria (overview.md › Goals) monthly.

## Later
- Upgrade to Django 6.2 LTS once released (expected April 2027)
- FR-8 Buildium sync (check pilot companies' Buildium plans first, risks.md R-2)
- FR-9 single sign-on (when the first customer asks)
- FR-17 staff limited to their own buildings; FR-20 reports; FR-18 costs, invoices and owner approval; FR-19 recurring maintenance
- FR-21 French, before the first Quebec customer
- Load test against NFR-6 before general launch
