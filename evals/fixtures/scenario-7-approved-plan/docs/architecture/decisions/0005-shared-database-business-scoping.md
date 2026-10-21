# ADR-0005: Shared database, every record scoped to its business

- Status: Accepted
- Date: 2026-10-19
- Decided by: Owner (approved the architecture package on 2026-10-19)
- Confidence: High
- Change later: Hard
- See also: ADR-0011 (each groomer has a calendar; one sign-in per business)

## Context
Many businesses use one app, and each business's clients, pets and appointments must stay private to it (FR-6, NFR-5). Version 1 has one groomer per business, but more staff per business is planned (FR-13). Code is written by AI agents, which copy existing patterns and can forget a filter, so isolation must be enforced by structure and tests rather than by memory.

## Options considered
1. **Shared tables with a business ID on every business-owned row, enforced in one data-access layer** — simple, cheap, standard for small SaaS / one missed filter could leak data, so it needs mechanical enforcement.
2. **Option 1 plus PostgreSQL row-level security** — the database itself refuses cross-business reads / every request must set the business in the database session, which adds moving parts that agents often get wrong with serverless connections.
3. **A schema or database per business** — strongest separation / far more operational work; migrations multiplied by every business.

## Decision
Option 1, made mechanical:
- Every business-owned table has a non-null `business_id`; foreign keys between business-owned tables include `business_id`, so an appointment cannot point at another business's pet.
- All database access goes through `src/server/data/`. Every function there takes a business context taken from the signed-in session (or, for the public booking page, from the page's business), never from user input. A lint rule forbids importing the database client anywhere else.
- Automated cross-business tests (two businesses, every read and write path) run in CI and block merging.
- Users belong to a business through a membership with a role (`owner` in version 1), so adding staff later needs no data migration.
- Platform admin is a separate flag on the user, checked on the server; admin screens never load client or pet data.

## Why
- It is the simplest design that keeps each business's data private, provided enforcement is automatic.
- Row-level security lost for now because it adds per-request session setup that is easy to get subtly wrong on serverless connections; the lint rule and isolation tests catch the same mistakes earlier. It stays the first upgrade if the trigger below fires.
- A database per business is far beyond what 50–500 small businesses need.

## Consequences
- Good: one schema, one migration path, cheap.
- Costs and tradeoffs: isolation depends on the data layer, lint rule and tests staying in place; they are binding rules in AGENTS.md.
- Follow-up work: data-access layer and the isolation test pattern in M1; one isolation test per new table or endpoint from then on.

## Evidence
- Planning method guidance for multi-tenant products: shared tables with a tenant ID enforced in one data-access layer, isolation tests as a CI gate (planning skill technology-selection reference, checked 2026-10-19).
- Unverified — general engineering practice as of 2026-10-19: transaction-scoped settings for row-level security with pooled serverless connections are a common source of bugs; to be reconsidered with evidence if the trigger fires.

## Revisit when
- Any cross-business data exposure is found, in testing or production: add row-level security immediately.
- A second developer or a second agent team works on the code in parallel.
- A business customer asks for contractual data isolation, or the product passes 500 businesses.
