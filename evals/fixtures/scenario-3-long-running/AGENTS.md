# AGENTS.md — Property maintenance platform (working name)

A multi-company web app that property management companies use to receive renters' maintenance requests with photos, send work orders to vendors and track every job to completion. Priced per building per month; pilot with about 20 US and Canadian companies in February–March 2027.

Start every session by reading `docs/project/state.md`. It says what is done, what is next, and what is blocked. Building is authorized (see `docs/project/state.md`).

## Map
- Product, users, scope, glossary: `docs/project/overview.md`
- Requirements and acceptance criteria: `docs/project/requirements.md`
- Architecture (current and binding): `docs/architecture/architecture.md`
- Decisions: `docs/architecture/decisions/` (Accepted ADRs are binding; Superseded ones are history only)
- Roadmap: `docs/project/roadmap.md` · Risks, assumptions, open questions: `docs/project/risks.md`
- Engineering standards, quality gates, agent guardrails: `docs/engineering/standards.md`
- Feature specs, written before coding each feature: `docs/features/`

## Stack
Python 3.14 · Django 6.1, server-rendered templates with htmx 2 ([ADR-0001](docs/architecture/decisions/0001-python-django-modular-monolith.md)) · PostgreSQL 18 on Render ([ADR-0002](docs/architecture/decisions/0002-postgresql-managed-on-render.md)) with row-level security per company ([ADR-0003](docs/architecture/decisions/0003-company-isolation-shared-database-rls.md)) · django-allauth for staff, hashed-token links for renters and vendors ([ADR-0004](docs/architecture/decisions/0004-staff-sign-in-and-link-access.md)) · Procrastinate jobs ([ADR-0005](docs/architecture/decisions/0005-background-jobs-procrastinate.md)) · Render, Ohio ([ADR-0006](docs/architecture/decisions/0006-hosting-render.md)) · Cloudflare R2 photos ([ADR-0007](docs/architecture/decisions/0007-photo-storage-cloudflare-r2.md)) · Amazon SES and Twilio ([ADR-0010](docs/architecture/decisions/0010-email-amazon-ses-texts-twilio.md)) · Stripe Billing ([ADR-0009](docs/architecture/decisions/0009-billing-stripe.md)) · uv for packages.

## Commands
- Install: `uv sync --frozen`
- Database for tests: `docker compose up -d db` (PostgreSQL 18 with the app, owner and metrics roles)
- Dev server: `uv run python manage.py runserver` (seed data: `uv run python scripts/seed.py`)
- Tests: `uv run pytest` (isolation tests only: `uv run pytest -m isolation`)
- Checks: `uv run ruff check`, `uv run ruff format --check`, `uv run mypy .`, `uv run lint-imports`
- Accessibility on changed pages: `uv run pytest -m a11y`

## Binding rules
1. Use the glossary in `docs/project/overview.md` exactly. "Company" is the customer account and "renter" is the person in a unit. Never use "tenant" in code, database names or UI.
2. Every company-owned model inherits `CompanyOwnedModel`, and its migration enables row-level security with the standard policy. Company data is read or written only inside a company context set by `core.tenancy`; reads before the company is known go only through `core.tenancy.lookup()`. Never use the owner database role or `BYPASSRLS` in app code.
3. Every staff view checks permissions on the server through `accounts.permissions`, and every new company-scoped page or job gets an isolation test (company A cannot reach company B).
4. Renter and vendor link tokens are created only by `links.tokens`, stored only as hashes, and never logged or shown after sending.
5. Only the owning app calls an outside service: `notifications` (Twilio, Amazon SES), `billing` (Stripe), `media` (R2). Emails, texts, photo processing and Stripe calls run as Procrastinate jobs deferred in the same transaction, never inside a web request (only creating a Stripe Checkout or portal session is allowed in a request). Job payloads hold IDs only.
6. Maintenance request and work order statuses change only through `maintenance.statuses`.
7. All user-facing text goes through Django's translation functions, and every renter page and message shows the company's emergency line.

## How to work
1. Read the docs relevant to your task, then the code. If they disagree, trust the code, say so, and fix the doc.
2. For anything bigger than a small fix, write or update a short spec in `docs/features/` with acceptance criteria before coding.
3. Keep changes small: one feature per session and per pull request.
4. Write or update tests first. Run tests, lint and typecheck before saying you are done.
5. Build only what the roadmap and requirements ask for. Suggest new ideas; do not add them.
6. Before finishing: update `docs/project/state.md` (done, next, blockers) and any doc your change made stale.

## Change control
A change is **material** if it adds or replaces a service, datastore, framework or external provider; changes sign-in, permissions, company isolation (row-level security policies, `core.tenancy`) or the shape of existing data; changes `render.yaml`, hosting or adds recurring cost; or contradicts an Accepted ADR.
For a material change: stop, explain the consequences, draft an ADR with status Proposed in `docs/architecture/decisions/`, and wait for human approval. Everything else is a normal change.

## Never
- Commit secrets, or put credentials or real personal data in code, docs, tests, seeds or logs.
- Use production credentials or data, or run destructive commands (deleting data, force-pushing, applying infrastructure changes) without explicit human approval.
- Weaken, skip or delete a test to make it pass, including isolation tests.
- Disable, bypass or loosen row-level security.
- Add a dependency without checking that it exists, is maintained, and is pinned in the lockfile.
- Rewrite large areas when a smaller change meets the goal.

## Definition of done
Acceptance criteria met · tests added and passing, including isolation tests for new company data · lint, typecheck and import contracts clean · accessibility checks pass on changed pages · feature spec, docs and `docs/project/state.md` updated
