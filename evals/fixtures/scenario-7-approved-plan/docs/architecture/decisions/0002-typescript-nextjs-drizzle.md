# ADR-0002: TypeScript, Next.js and Drizzle in one web app

- Status: Accepted
- Date: 2026-10-19
- Decided by: Owner (approved the architecture package on 2026-10-19)
- Confidence: High (language and framework), Medium (database toolkit)
- Change later: Hard

## Context
One web app serves the public booking pages and the groomer screens (ADR-0001, NFR-1). The owner is not a programmer and builds with a coding agent working in this repository, such as Claude Code (confirmed with the architecture package). Agents need fast, deterministic feedback (type errors, failing tests) and a mainstream framework they know well. Version 1 needs server-side code for webhooks (texts, payments), a scheduled job (FR-7) and a database. Scale is small: about 50 businesses and 10,000 clients in year one (NFR-7).

## Options considered
1. **TypeScript (strict) with Next.js** — the most common web stack in agents' training data; strict types catch many agent mistakes at build time; one codebase for pages, server code and webhooks; first-class on the chosen host / framework changes between versions (caching, server components) can confuse agents; more pieces to choose than an all-in-one framework.
2. **Ruby on Rails 8** — all-in-one (sign-in generator, background jobs, mail, migrations); very productive / no static type checking by default, so agent mistakes surface later; preview environments per change cost more on its usual hosts.
3. **Python with Django** — mature, built-in admin and sign-in / optional typing only; less natural fit for a highly interactive calendar screen.

Database toolkit: **Drizzle ORM** (TypeScript schema, SQL-like queries, light on serverless) versus **Prisma** (very familiar to agents, readable schema file).

## Decision
TypeScript in strict mode, Next.js 16 (App Router) on Node.js 24 LTS, Drizzle ORM 0.45 (stable line) with drizzle-kit migrations, pnpm with a committed lockfile. Supporting defaults (two-way doors, no ADR needed): Zod for input validation, Tailwind CSS with accessible shadcn/ui components, Vitest and Playwright for tests, libphonenumber-js for phone numbers, date-fns with @date-fns/tz for time zones.

## Why
- Strict types plus a mainstream framework give the AI tools the best feedback loop; most type errors in model-written code are caught by the compiler (see technology-selection evidence).
- One deployable covers pages, server actions, webhooks and the scheduled job, so there is one thing to build, test and deploy.
- Rails lost on type checking and preview-environment cost; Django on fit for the interactive calendar.
- Drizzle over Prisma: SQL-transparent queries make the business-scoping rule (ADR-0005) easy to see in review, and it runs well on serverless; Prisma remains a good fallback.

## Consequences
- Good: one language end to end; agents get compile errors immediately; huge ecosystem.
- Costs and tradeoffs: Next.js caching and rendering rules change between versions; agents must follow the version-matched docs. Drizzle 1.0 is still a release candidate, so a later upgrade will bring API changes.
- Follow-up work: strict tsconfig; lint rules for boundaries (ADR-0005); pin exact versions; upgrade to Drizzle 1.0 only after it is stable and released for at least a month.

## Evidence
- Next.js blog: Next.js 16.4 released 2026-10-06; security releases 2026-09-30 and 2026-10-14 — https://nextjs.org/blog (checked 2026-10-19)
- Node.js releases: v24 is the latest LTS line (24.22.0); v26 is Current — https://nodejs.org/en/about/previous-releases (checked 2026-10-19)
- Drizzle ORM releases: latest stable 0.45.2; 1.0.0-rc.4 is a pre-release — https://github.com/drizzle-team/drizzle-orm/releases (checked 2026-10-19)
- Mündler et al. 2025, type-constrained code generation (most compile errors in model-written code are type errors) — https://arxiv.org/abs/2504.09246 (from the planning method's references)

## Revisit when
- Next.js or Node.js 24 approaches end of support (Node 24 maintenance ends 2028-04 [Assumption: per the usual Node.js schedule; check before planning upgrades]).
- Agents repeatedly struggle with Next.js rendering or caching rules on this project (three or more incidents traced to it).
- A second app (for example an installed phone app) needs a separate API.
