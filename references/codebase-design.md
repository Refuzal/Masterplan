# Codebase design

How to lay out and grow a codebase so it stays easy for agents and people to navigate, test and change, from a small app to a large multi-tenant system. Apply it when writing the architecture, the Milestone 1 skeleton, and every task plan's file map.

Contents: Organize by feature · Deep modules · Ports and adapters · Enforce boundaries · Files and naming · Data and migrations · Errors, config and logging · The scale ladder · Multi-tenant systems · Large systems · Refactoring · Skeletons

## Organize by feature

Group code by what it does for users, not by technical layer. Files that change together live together.

- One folder per feature or domain module (`bookings/`, `clients/`, `billing/`), holding its interface, logic, data access, UI pieces and tests.
- One shared platform folder for cross-cutting plumbing (database connection, sign-in, email and text adapters, jobs, configuration, logging). Platform code knows nothing about features.
- A feature talks to another feature only through that feature's public interface (its index or service module), never by importing its internals or querying its tables.
- Start with few modules. Split a module when it changes for unrelated reasons, not in anticipation.
- Inside a feature, dependencies point one way: types and schemas, then data access, then services (the feature's interface), then the routes and UI that call them. Nothing lower imports anything higher, so an agent can tell where new code goes.

## Deep modules

A good module hides a lot of behavior behind a small interface.

- **Small interface:** few entry points, simple parameters, clear invariants and error modes. Everything a caller must know counts as interface, including ordering rules and performance limits.
- **Deletion test:** if deleting the module would push its complexity into every caller, it earns its place; if complexity vanishes, it was a pass-through and should be folded in.
- **Test through the interface:** the interface is the test surface (testing.md › Seams).
- **Accept dependencies, return results:** pass in collaborators (database handle, clock, adapters) rather than creating them inside; prefer returning values over hidden side effects.
- **Design it twice:** for a module many others will depend on, sketch two different interfaces in a few lines each and keep the simpler one to use; the first idea is rarely the best.
- **No speculative generality:** no options, hooks or abstraction layers a requirement does not need. One implementation behind an interface is just indirection; add the seam when a second implementation (often the test fake) actually exists.

## Ports and adapters

Every external service sits behind a small interface owned by the app (a port), with a production adapter and a test fake.

- Examples: `sendText(to, body)`, `chargeDeposit(customerId, amount, idempotencyKey)`, `storeFile(key, bytes)`, `completeChat(messages)`.
- Only the adapter imports the vendor SDK. Switching vendors, adding retries or recording usage then touches one file.
- Fakes record what was sent so tests can assert on outcomes, and mirror the real response shape completely.
- Outbound effects that must not be lost (texts, emails, webhooks, charges) go through an outbox or job queue with idempotency keys, so a crash or retry neither drops nor duplicates them.

## Enforce boundaries

Rules a tool checks are kept; rules people must remember are not.

- Encode module boundaries as lint rules in CI: dependency-cruiser or eslint-plugin-boundaries (TypeScript), import-linter (Python), ArchUnit (Java), Nx or Turborepo tags (monorepos), or the language's package visibility.
- Typical rules: features may import platform but not each other's internals; only adapters import vendor SDKs; UI code never imports database code directly; generated code is never edited by hand.
- Write the rule's error message as an instruction ("features/billing may not import features/bookings/data; call bookings/index.ts instead"), so the agent that trips it can fix the problem itself. Check in Milestone 0 that a planted violation actually prints that text: some tools hide custom messages in their default output (dependency-cruiser needs `--output-type err-long`).
- Run the checks in CI and as an agent hook where the agent supports hooks (in Claude Code, a PostToolUse hook on file edits that runs the boundary check on changed files), so violations surface while the agent is still working.
- Turn a repeated review finding into a rule or a test, not a paragraph in AGENTS.md.

## Files and naming

- One clear responsibility per file. Prefer focused files of a few hundred lines; when a file grows past its purpose, split it by responsibility as a planned task.
- Names come from the glossary, in code, database, API and UI alike. One concept, one name; list rejected synonyms in the glossary as "avoid" terms so agents do not invent new ones.
- Names say what a thing is or does, not how it works. If no honest name comes, the design is unclear.
- Keep generated files, vendored code and build output out of the paths agents edit, and say so in AGENTS.md.

## Data and migrations

- The database enforces what must never be wrong: foreign keys, unique constraints, not-null, check constraints, exclusion constraints for overlapping time ranges, and row-level security where tenancy uses it.
- Every schema change is a versioned migration committed with the code that needs it. Never edit a migration that has run anywhere shared. Lint migrations in CI where a linter exists (Squawk for PostgreSQL): it catches table locks and destructive steps before they reach live data.
- **Expand → migrate → contract** for changes to live data: add the new column or table, write to both, backfill in batches, switch reads, then remove the old shape in a later release. Each step deploys safely on its own.
- Destructive steps (drops, deletes, rewrites of large tables) need the owner's approval, a fresh backup and a tested restore.
- Money in integer minor units; times stored in UTC and shown in the user's time zone; IDs that are not guessable where they appear in links.

## Errors, config and logging

- Validate input at the edge (forms, API handlers, webhooks, jobs) with a schema; inside the core, trust types.
- Errors carry enough context to act on and never leak secrets or other people's data. Users see plain messages; logs get the detail.
- Configuration comes from environment variables, validated at startup; secrets come from the platform's secret store or a git-ignored `.env`, never the repository.
- Structured logs with a request ID (and a tenant ID in multi-tenant systems). Error tracking from the first deploy. Add tracing (OpenTelemetry) when there is more than one service or queue.
- Risky changes ship behind a feature flag that can be turned off without a deploy.

## The scale ladder

Build for the next step up, not the top of the ladder. Move up a rung only when a measured need or a requirement says so.

| Rung | Shape | Typical additions |
|---|---|---|
| **Small** (one team, hundreds of users) | One app, one database (SQLite or PostgreSQL), feature folders, server-rendered or a single frontend | Backups, error tracking, a deploy that runs tests |
| **Medium** (thousands of users, paying customers) | Modular monolith with enforced boundaries, PostgreSQL, a job queue for slow or retried work, a preview environment per change | Outbox for messages, rate limits, feature flags, uptime checks |
| **Large** (many tenants, tens of thousands of users or more) | Modular monolith first; separate workers; read replicas, caching and search only where measured; services split out only by the criteria below | Per-tenant quotas, tenant-aware observability and cost tracking, staged rollouts, load tests |

**Split out a service only when** a part needs a different scaling profile, a different release cadence owned by a separate team, a different security boundary, or a different runtime; and its interface is already stable inside the monolith. Splitting early turns function calls into network failures.

**Performance:** set budgets from the requirements, measure before optimizing, fix queries and indexes first, then add caching with a clear invalidation rule, then scale out.

## Multi-tenant systems

- One shared database with a `tenant_id` on every tenant-owned row is the default; row-level security in PostgreSQL as a second lock behind the application's own checks. Schema-per-tenant or database-per-tenant only for a contractual isolation requirement or very uneven tenant sizes (technology-selection.md › Sold to many customers).
- The tenant comes from the authenticated session or a verified token, never from user input. Set it once per request or job, and have every data access path require it.
- With row-level security, set the tenant per transaction (`SET LOCAL` or `set_config(..., true)` inside the transaction), never per session: pooled connections are reused, and session settings leak to the next request. The application connects as a role that cannot bypass row-level security; migrations run as a separate owner role.
- PostgreSQL row-level security pitfalls to design around (found and reproduced on PostgreSQL 18 in this skill's test builds; the behaviors are documented in PostgreSQL's row security and pg_dump pages):
  - Once a transaction-local setting has been used on a connection, `current_setting(name, true)` returns an empty string, not NULL, for the rest of that connection's life. Write every policy as `nullif(current_setting(name, true), '')` (cast as needed). Without it, a uuid cast fails at random on reused connections, and a text comparison matches every row whose column is empty, in every tenant.
  - Superusers, roles with `BYPASSRLS` and table owners skip the policies. The app role is none of these and not a member of the owner role; check it at startup and in a schema test.
  - `FORCE ROW LEVEL SECURITY` makes the owner's `pg_dump` fail. Enable without forcing and confine the owner role to migrations and backups, or back up with `--enable-row-security` and test the restore.
  - Foreign-key and unique checks run outside the policies. A plain foreign key accepts another tenant's row ID, and a global unique constraint reveals that a value exists elsewhere. Reference tenant-owned rows with composite keys (`(tenant_id, id)` → `(tenant_id, id)`) so the database rejects cross-tenant links, and make uniqueness per tenant.
  - Lookups that happen before the tenant is known (a link token, an inbound webhook) get their own narrow policy on one exact key, set and cleared by one module; list them in a test so a new one is a deliberate change.
- Put `tenant_id` first in composite indexes and unique constraints (unique per tenant, not globally), so per-tenant queries stay fast and one tenant's data cannot collide with another's.
- Background jobs, exports, search indexes, file storage paths, caches and logs all carry the tenant; each is a place cross-tenant leaks happen.
- An isolation test accompanies every new table, endpoint, job and file path (testing.md › Special cases).
- Protect tenants from each other: per-tenant rate limits and quotas, fair job scheduling, statement timeouts, and cost tracking per tenant once usage-based costs (texts, AI, storage) matter. When one tenant grows far beyond the rest, the usual path is read replicas, then partitioning, then moving that tenant to its own database; not schema-per-tenant for everyone.
- The app's admin role that can see across tenants is separate, audited, and uses its own credentials.

## Large systems

- Split the domain into bounded modules, each with its own glossary section (or glossary file when the language diverges) and a map of how modules relate and which events or interfaces connect them.
- Monorepo with enforced module and package boundaries is the default for one product; one owner per module.
- Shared code goes into small, versioned internal packages with their own tests, only after two real users exist.
- Interfaces between modules are explicit and versioned when separate teams or deployments depend on them; consumer-driven contract tests protect them.

## Refactoring

- Refactor as its own reviewed task, never mixed into a feature task: make the change easy, then make the easy change.
- Keep behavior identical and tests green throughout; when tests break during a pure refactor, they were testing internals.
- When fixing the same kind of bug a third time, stop and question the design (debugging.md).

## Skeletons

Starting layouts for the walking skeleton. Adapt names to the stack's conventions; keep the principle.

TypeScript web app (for example Next.js):
```
src/
  features/<feature>/    # ui/, server/ (actions, routes), data/ (queries), <feature>.test.ts
  platform/              # db/, auth/, email/, sms/, jobs/, config/, logging/
  app/                   # routing only; thin, calls feature interfaces
tests/e2e/               # Playwright journeys
```

Python web app (for example Django):
```
<project>/settings/          # validated environment config
apps/<feature>/              # models, services.py (interface), views, tests/
apps/platform/               # tenancy, adapters (email, sms, payments), jobs
```
with import-linter contracts so apps call each other only through `services.py`.

Mobile or desktop app: `features/<feature>/` for screens, state and logic; `platform/` for storage, sync, notifications; a sync module behind one interface when the app works offline.
