# ADR-0003: Company isolation with a shared database, company IDs and row-level security

- Status: Accepted
- Date: 2026-10-19 (implementation details corrected the same day after the review panel, before any code; see architecture.md › Review log)
- Decided by: Product owner, approving the recommended architecture package on 2026-10-19. Ravi confirms in M0.
- Confidence: Medium (the approach is High; the Render-specific role setup is verified by the M0 spike)
- Change later: Hard

Updated: 2026-12-04 — email provider IDs changed from Postmark to SES (ADR-0010); no change to the decision.

## Context
Every company's data must be private to it (NFR-4), for staff, renter links, vendor links, background jobs and founder support tools. The goal is thousands of companies, run by two founders. AI agents write much of the code, so the most likely leak is a query that forgets to filter by company. Some work must find data before the company is known: opening a renter or vendor link, accepting an invitation, signing in, re-issuing a renter link, handling webhooks, founder metrics and backups.

## Options considered
1. **Shared tables with a company ID, enforced only in application code** — simplest / one forgotten filter leaks data.
2. **Shared tables with a company ID, enforced in one data-access layer and by PostgreSQL row-level security** — one migration path, cheap at any number of companies, and a second lock in the database / more care with migrations, lookups before the company is known, and backups.
3. **A schema per company** — stronger separation / every migration runs once per company; connection and search-path complexity grows with thousands of companies.
4. **A database per company** — strongest separation / cost and operations multiply per company.

## Decision
Option 2, implemented as follows (details in architecture.md › Data model and Security model):
- Every company-owned table has a non-null, indexed `company_id`. Its Django model inherits `CompanyOwnedModel`, whose manager raises an error when no company context is active. The Company table itself uses `id` in place of `company_id`.
- Row-level security is enabled on every company-owned table, with the standard policy `company_id = current_setting('app.company_id', true)::uuid` for reads and writes. With no company context, no rows are visible.
- Roles: an owner role owns the tables and is used only by the migration step and the nightly backup job; the app role, used by web and workers, is not the owner and has no `BYPASSRLS`, so row-level security always applies to it; a read-only metrics role sees all rows only through `SELECT` policies granted to that role, used only by the `metrics` app. No role used by application code has `BYPASSRLS`.
- `core.tenancy` is the only code that sets the context. Every request runs in a transaction (`ATOMIC_REQUESTS`), and the context is set with `set_config('app.company_id', <id>, true)`, which lasts only until the transaction ends, so pooled connections never carry another company's context. Setting a context outside a transaction raises an error. Jobs, management commands, the shell and test fixtures use the same `company_context()` helper.
- Lookups before the company is known use **lookup policies**: an extra `SELECT` policy on a table that matches one exact key held in a transaction-local setting (for example `token_hash = current_setting('app.lookup_token_hash', true)`). Only `core.tenancy.lookup()` sets these keys; it returns the company ID, clears the key and sets the company context. The sanctioned lookups are: link tokens by hash, invitations by token hash, memberships of the signed-in user, renters by exact phone or email (link re-issue), subscriptions by Stripe customer ID, and sender numbers and messages by Twilio or SES message ID. A test lists every lookup policy, and any new one is a material change.
- Staff sign-in tables (users, email addresses, two-step verification devices, sessions) are global and hold only staff sign-in data; staff lists are always reached through company-scoped memberships, and isolation tests cover every page that shows staff.
- Founder tools: the Django admin works inside one chosen company at a time; cross-company pilot metrics (FR-23) use the metrics role behind founder sign-in with two-step verification; every use is logged.

## Why
- Cheapest and simplest to run for thousands of companies, which suits a two-person team.
- Row-level security turns the most likely AI-agent mistake (a missing filter) into an empty result instead of a leak.
- Lookup policies keep every pre-company lookup narrow and listed, without granting any application role a general bypass, which managed PostgreSQL may not allow anyway.
- Options 3 and 4 add per-company operations work that no current requirement justifies.

## Consequences
- Good: a cross-company leak needs two independent failures; isolation is testable in CI.
- Costs and tradeoffs: every new table needs its policy in the same migration; raw SQL must run inside a company context; `company_id` must lead the relevant indexes; owner credentials exist in two places (the migration step and the backup job) and must never be used by application code (a settings test checks this).
- Follow-up work: M0 spike on Render (create the app and metrics roles with SQL; prove one lookup policy and the backup job as owner); M1 builds the tenancy module, the isolation suite, a schema test that fails when a company table lacks row-level security, and tests that the app role is not the owner and lacks `BYPASSRLS`.

## Evidence
- [PostgreSQL 18 documentation: Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) (checked 2026-10-19) — table owners bypass row security unless it is forced; superusers and `BYPASSRLS` roles always bypass; with row security enabled and no policy, no rows are visible; policies can apply to named roles.
- [PostgreSQL 18 documentation: set_config](https://www.postgresql.org/docs/current/functions-admin.html) (checked 2026-10-19) — with `is_local` true, the value applies only during the current transaction.
- [Render database credentials](https://render.com/docs/postgresql-credentials) (checked 2026-10-19) — users created with `CREATE USER` are allowed but not managed by Render. Whether the default user can grant every privilege needed is verified in the M0 spike.

## Revisit when
- The M0 spike shows Render cannot support the role setup (write a superseding ADR before M1).
- A customer contract requires a dedicated database (offer a per-company database for that customer as an enterprise option).
- Row-level security measurably slows key queries (NFR-1).
- The product passes 10,000 companies.
