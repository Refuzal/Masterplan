# Engineering standards

> Purpose: how code is written, checked, shipped and run in this project, sized for tier Standard. Update when a practice changes. Owner: Ravi (backend co-founder, lead engineer).
> Prefer rules a tool can enforce over rules people must remember. Each rule names its check.

## Source control and review
- GitHub (Team plan, needed for protected branches on a private repository). `main` is protected: changes arrive only by pull request, with every required check passing and one human approval. No force-pushes to `main`.
- Coding agents open pull requests from a separate bot account, so Ravi can review and approve them. For pull requests Ravi writes himself, the product owner approves after trying the change in its preview, and an AI reviewer from a different model family comments on the code first.
- CODEOWNERS (from M0) makes Ravi the required reviewer for the guardrail files: `AGENTS.md`, `CLAUDE.md`, `docs/architecture/`, `docs/engineering/`, `.github/`, `render.yaml`, `core/`, `accounts/permissions.py` and `links/tokens.py`. When Ravi himself changes them, the product owner approves and Ravi merges with the recorded admin override. Other documentation (`docs/project/`, `docs/features/`) can be approved by either founder.
- One feature per pull request and per agent session; squash-merge.

## Quality gates (must pass before merge)
| Gate | Tool | Runs where |
|---|---|---|
| Format and lint | Ruff (format and lint, including its security and Django rule sets) | pre-commit hook + CI |
| Typecheck | mypy in strict mode with the django-stubs plugin | CI |
| Tests | pytest with pytest-django against PostgreSQL 18 (never SQLite) | CI |
| Company isolation and schema | pytest tests marked `isolation` (ADR-0003) | CI, required |
| Architecture boundaries | import-linter contracts (architecture.md › Components and boundaries) | CI |
| Migrations | `manage.py makemigrations --check`; a human reviews every migration that alters or drops existing columns | CI + review |
| Dependency audit | pip-audit against `uv.lock` | CI + weekly scheduled run |
| Secret scanning | gitleaks in CI; GitHub secret scanning with push protection | pre-commit + CI |
| Static security analysis | Semgrep with its Python and Django rule sets | CI |
| End-to-end and accessibility | Playwright for Python on the key journeys, with axe-core checks on every page visited | CI |
| Mutation testing | mutmut on `core.tenancy`, `accounts.permissions`, `links.tokens` and `maintenance.statuses` | Weekly scheduled run; surviving mutants become tests |

Required checks should finish within 10 minutes; end-to-end tests run as their own parallel job.

## Testing
- Unit tests for business rules (statuses, permissions, link expiry, billing quantity).
- Integration tests run against a real PostgreSQL 18 database with row-level security switched on, exactly as in production.
- Authorization tests for every staff view and every role.
- Isolation tests: two companies with full data; every company-scoped URL, link page and job is tried with the other company's IDs and must return "not found" or do nothing.
- End-to-end journeys (Playwright): renter submits a request with a photo → staff create a work order → vendor accepts, schedules and completes it; staff import a spreadsheet; company admin subscribes in Stripe test mode.
- Test data comes from factories with fake data only; real renter, staff or vendor data never appears in tests, seeds, fixtures or preview environments.
- Tests live next to the app they test (`<app>/tests/`); end-to-end tests live in `e2e/`.

## Architecture enforcement
- Layer and independence contracts: import-linter (architecture.md › Components and boundaries).
- Only the owning app imports an external SDK: `notifications` (Twilio, Amazon SES), `billing` (Stripe), `media` (boto3 for R2). import-linter forbidden contracts.
- Every model with `company_id` inherits `CompanyOwnedModel`, and every company table has row-level security enabled and forced: schema test in the isolation suite.
- Status changes go through `maintenance.statuses` only: unit tests plus mutation testing.
- Side effects (email, texts, photo processing, Stripe calls) run as jobs deferred inside the transaction, never in the request; the one exception is creating a Stripe Checkout or customer-portal session. Checked by code review and a test that the `notifications` send functions refuse to run outside a job.
- Job payloads hold IDs only (never names, phone numbers, email addresses or message text) and stay compatible for one release: a test inspects every registered job's arguments.
- Lookups before the company is known go only through `core.tenancy.lookup()` and the listed lookup policies: a test compares the policies in the database with the approved list (ADR-0003).

## Environments and configuration
- Environments: local, one preview per pull request, production (architecture.md › Environments and deployment).
- Configuration comes from environment variables read in one typed settings module. `.env.example` lists every variable with a fake value; `.env` is ignored by git.
- Production secrets live in Render environment groups, readable only by the founders. Previews use test-mode keys only.

## Data and migrations
- Migrations are committed, reviewed and never edited after they run anywhere shared.
- A new company table gets its row-level security policy in the same migration.
- Changes are backward compatible with the previous release: add, backfill, switch, and only then remove, in separate releases.
- Before any destructive migration, confirm a fresh backup exists and get human approval.

## Security baseline
- Every staff request is authorized on the server (`accounts.permissions`); every query runs in a company context (`core.tenancy`).
- Input is validated with Django forms at every boundary; webhooks (Stripe, Twilio, Amazon SES) are verified by signature and processed once.
- Django security settings on: HTTPS only, HSTS, secure and HttpOnly cookies, CSRF protection, `X-Frame-Options: DENY`, a content security policy, `Referrer-Policy: no-referrer` on link pages.
- Rate limits on sign-in, two-step verification, link opening and photo upload links; link re-issue limited per contact (one per 10 minutes, three per day) and per company per day (ADR-0004).
- Uploads: size and type limits; decoded only on the `media` worker with pixel and time limits; re-encoded before display; originals deleted.
- A sign-in and admin-action audit log; founder support access is logged.
- Dependency updates weekly through Dependabot pull requests, which pass the same gates.

## Observability
- Sentry for errors and performance in production and previews, with request bodies, phone numbers, email addresses and link tokens scrubbed.
- Structured JSON logs that never include tokens or message bodies.
- Better Stack uptime checks, the worker heartbeat and the public status page; alert routing in architecture.md › Operations.

## Backups and recovery
- Render point-in-time recovery (7 days) plus a nightly encrypted backup in a separate Cloudflare account, kept 30 days; agents and the app's normal credentials cannot delete it.
- Restore drill before the pilot and every quarter, timed against NFR-3, with the result recorded in architecture.md › Operations.

## Releases and rollback
- Production deploys automatically from `main` after merge; previews come first for every pull request.
- Rollback: redeploy the previous release in Render; migrations are backward compatible, so this is always safe.

## AI-agent guardrails
- Agents work in a sandbox with no production credentials and no access to production data.
- Destructive actions (data deletion, force-push, infrastructure apply) need explicit human approval.
- New dependencies are checked for existence, maintenance and license before they enter the lockfile.
- Tests may not be weakened to make them pass; repeated agent mistakes become a lint rule, hook or test.
- Agents install only from the lockfile (`uv sync --frozen`) and add packages with `uv add` after the check above.
- Changes to the guardrail files listed under Source control need Ravi's review, even when small (CODEOWNERS).
- An AI reviewer from a different model family comments on pull requests; it never replaces the human approval.

## Add these controls when…
| Trigger | Add |
|---|---|
| First paying customer | Billing-failure handling tested end to end; status page linked from the app |
| First customer asks for single sign-on | New ADR choosing allauth SAML/OIDC or WorkOS (ADR-0004) |
| First customer in Quebec | French (FR-21) and the Law 25 contract clauses (requirements.md › Compliance obligations) |
| A second engineer joins | Two approvals on the guardrail files; the second engineer joins the on-call rotation |
| The first risky change that should reach some companies first | Per-company feature flags in `core` |
| About 50 companies | Load test against NFR-6 before general launch; review cost per company |
| Contractual uptime promises or regulated data | Move to the Critical tier: threat model, operations runbooks, professional review |
| AI features in the product | Evaluation set in CI, spend caps, output logging with redaction |
