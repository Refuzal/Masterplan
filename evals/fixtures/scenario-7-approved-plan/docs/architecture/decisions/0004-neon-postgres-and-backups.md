# ADR-0004: PostgreSQL on Neon, with production kept apart from test copies

- Status: Accepted
- Date: 2026-10-19
- Decided by: Owner (approved the architecture package on 2026-10-19)
- Confidence: High (PostgreSQL), Medium (Neon preview mechanics until verified in M0)
- Change later: Hard (PostgreSQL) / Moderate (provider)

## Context
The data is relational: businesses, clients, pets, services, appointments, messages and consent records (FR-1 to FR-10). Volume is small: about 10,000 clients and under 100,000 appointments a year at the year-one goal (NFR-7), well under 1 GB. Losing bookings would hurt groomers directly (NFR-4). Previews and AI agents must never see real client data (standards › AI-agent guardrails).

## Options considered
1. **Neon (Launch plan)** — managed serverless PostgreSQL; restore to any moment in the last 7 days; database branches for preview deployments; pay for usage with no minimum / branches copy their parent's data, so previews must branch from a seed-data project, not production.
2. **Supabase** — PostgreSQL plus sign-in and storage in one / point-in-time restore is a paid add-on; its browser-facing data API is a known trap when tables lack access rules.
3. **Render PostgreSQL or AWS RDS** — solid / no per-preview branches; RDS needs more operations knowledge.

## Decision
One PostgreSQL database for all businesses (tenancy rules in ADR-0005), hosted on Neon:
- **Production project** (US East): Launch plan with a 7-day restore window. Only the production deployment has its connection string.
- **Development project**: holds a seed branch with fake data only; local development and every preview deployment get their own branch of this project. Production data is never copied into it.
- **Connections**: the app and the dispatcher use Drizzle's `neon-serverless` driver (WebSocket pool) on the pooled connection string, which supports the transactions ADR-0008 needs; migrations use the direct connection. Neon's HTTP-only driver is not used.
- **Independent daily backup**: a scheduled GitHub Actions workflow, in a GitHub environment that only the `main` branch can use, dumps production with a read-only database user to a Backblaze B2 bucket with a 30-day Object Lock, out of reach of the agents' credentials [Assumption: B2 pricing and Object Lock verified in M0]. GitHub emails the owner when the scheduled workflow fails. A restore is tested before the first paying groomer and every quarter; after any restore the dispatcher stays paused until messages are reconciled (ADR-0008).

## Why
- PostgreSQL is the boring, proven choice for relational business data and is portable between providers.
- The 7-day restore window covers the most likely disaster (a bad change or migration) at a small cost; the separate backup covers provider or account problems and slow-to-notice damage.
- Separate projects make "previews never contain real client data" a structural fact rather than a setting someone could change.
- Supabase lost on restore cost and the data-API trap; Render and RDS on preview branching and operations effort.

## Consequences
- Good: cheap at this size; per-change test databases; fast restore.
- Costs and tradeoffs: the per-minute reminder job keeps production compute awake (about $20 a month); two Neon projects to manage; the backup job is one more thing to monitor.
- Follow-up work (M0): create both projects; turn off scale-to-zero on production; connect Vercel previews to the development project only; verify with a preview that only seed data is visible; set up and test the backup job.

## Evidence
- Neon pricing: Launch plan pay-for-usage, no monthly minimum, $0.106 per CU-hour, $0.35 per GB-month, restore window up to 7 days; Free plan 6-hour window and 100 CU-hours per project — https://neon.com/pricing (checked 2026-10-19)
- Neon-managed Vercel integration creates a branch per preview deployment and can delete obsolete branches — https://neon.com/docs/guides/neon-managed-vercel-integration (checked 2026-10-19). The documentation does not say whether the parent branch can be chosen, hence two separate projects.

## Revisit when
- Database storage passes 10 GB or compute regularly runs above 1 CU.
- A data-residency or contract requirement asks for a specific cloud or region.
- Neon pricing or ownership changes materially.
