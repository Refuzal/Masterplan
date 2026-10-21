# Technology selection

How to pick technology from this project's evidence rather than habit or fashion.

Contents: Procedure · Criteria and weighting · Simplicity defaults · Archetype playbooks · Build or buy · Evidence rules · Pushback · Cost sketch · Presenting the package

## Procedure

For each consequential decision:

1. **Frame it.** Name the decision, the requirements that drive it (FR and NFR IDs), and how hard it is to reverse.
2. **Eliminate.** Drop options that break a hard constraint: platform, offline needs, compliance or data residency, budget, existing systems, the team's skills.
3. **Shortlist two or three credible candidates**, always including the boring, proven option.
4. **Weigh the criteria for this project** (below). Look for a clear winner. If it is close, prefer the option that is easier to operate and easier to reverse.
5. **Verify current facts** for the leading candidates (Evidence rules).
6. **Decide.** One recommendation, the strongest alternative, why the others lost, your confidence (High, Medium, Low), and what would make you revisit.
7. **Low confidence on a hard-to-reverse decision?** Propose a spike: a small, time-boxed experiment in Milestone 0 or 1 that settles it with evidence, instead of guessing.

Spend effort in proportion to reversibility. One-way doors deserve research: the data store, the language, the tenancy model, the identity provider, the mobile approach. Two-way doors (UI component kit, logging library, date library) get a sensible default and no question.

## Criteria and weighting

Evaluate against: requirements fit · engineering complexity · long-term maintainability · reliability and operational burden · performance and scalability · security and ecosystem maturity · initial development effort · total cost of ownership · lock-in and migration difficulty · suitability for AI-assisted development · documentation and community · difficulty of reversal.

Weight them for the project, not universally:
- **Light:** initial effort, running cost and simplicity dominate.
- **Standard:** maintainability, reliability, security, total cost and AI-suitability dominate.
- **Critical:** security, reliability, compliance fit, maturity and auditability dominate; initial effort matters least.
- **Always:** the team's existing fluency and assets. A team fluent in Rails or Django should usually stay there; switching stacks is a cost, not a free upgrade.

**AI-assisted development suitability** means agents get fast, deterministic feedback and stay on well-trodden paths:
- Typed languages with strict compilers. In one study 94% of compile errors in LLM-generated code were type-check failures, which a compiler catches immediately ([Mündler et al. 2025](https://arxiv.org/abs/2504.09246)).
- Mainstream frameworks. Models produce worse and less secure code on less widely used backend frameworks ([BaxBench, ICML 2025](https://proceedings.mlr.press/v267/vero25a.html)).
- Stable, well-documented APIs; conventions over configuration; fast test runs.
- Caution with very new major versions or young frameworks that models know poorly. If chosen, plan to give agents current docs (a docs file in the repo or a docs connection).

## Simplicity defaults

Starting hypotheses that win unless a requirement says otherwise. They are not answers; each still gets evaluated.

- **One deployable** (a monolith, organized as modules with clear boundaries) until there is a concrete reason to split: separate teams that need to release independently, parts with very different scaling or reliability needs, or isolation required for security.
- **One primary database.** Relational (PostgreSQL) for most business data. Embedded SQLite for desktop, mobile-local and single-user tools. Add a second store only for a measured need.
- **Managed services over self-hosting** when nobody's job is operations. Running infrastructure is a different skill from writing code: unless the owner says someone has run the proposed infrastructure in production (cloud networking, permissions, databases, upgrades), choose a managed platform the builders can operate from day one. A requirement that might arrive later (a customer demanding in-country storage, a compliance regime) is a recorded trigger with a migration path, not a reason to take on the heavier setup now.
- **Fewest moving parts for a first-time builder working with AI tools:** one framework for pages and server code, one host, a hosted database with a web console, and no tool they must configure by hand that the platform could handle.
- **Buy commodity capabilities**: sign-in, payments, email and text delivery, error tracking (see Build or buy).
- **Count the accounts.** Each extra vendor is another bill, sign-in, and point of failure for the owner. Prefer a platform's built-in option (its database, cron, backups, logs) over adding a vendor, unless a requirement needs more. Before a reviewer's or your own fix adds a new account, check whether an account the owner already has can do the job (an error tracker that also watches scheduled jobs, a host that also sends uptime alerts); verify that it can, on its current plan, before relying on it.
- **Request/response first.** Add a job queue when work is slow, must retry, or runs on a schedule. Add event streaming only for real fan-out or volume.
- **No cache, search engine, vector database or message broker until measured.** Start with database indexes, PostgreSQL full-text search, and pgvector.
- **One region with tested backups.** Multi-region only for an explicit availability or data-residency requirement.
- **Containers on a managed platform before Kubernetes.** Kubernetes needs people who run it.
- **Serverless or always-on:** serverless suits spiky or low traffic and short requests; always-on suits long-running connections (websockets, streaming), heavy background work and steady load. Check execution time limits, cold starts, and how background jobs will run.

## Archetype playbooks

Starting candidates are examples, checked in October 2026. Re-verify status, versions and pricing at decision time; this field moves monthly.

### Known stale defaults (checked October 2026)
Models often suggest these from older training data. Verify before recommending any of them:
- **Sign-in libraries:** Lucia is deprecated ([repo](https://github.com/lucia-auth/lucia)); Auth.js/NextAuth receives security fixes only and its maintainers point new projects to Better Auth ([announcement](https://www.better-auth.com/blog/authjs-joins-better-auth)).
- **Frameworks:** Remix v2 is end-of-life (React Router is its successor; "Remix 3" is a different framework) ([Remix blog](https://remix.run/blog/react-router-v8)). Nuxt 3 ([roadmap](https://nuxt.com/docs/3.x/community/roadmap)) and .NET 8/9 ([support policy](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core)) have reached or are reaching end of support; use the current long-term releases.
- **Hosting:** AWS App Runner is closed to new customers (AWS points to ECS Express Mode) ([AWS](https://docs.aws.amazon.com/apprunner/latest/dg/apprunner-availability-change.html)); Heroku is no longer adding features ([DevClass](https://www.devclass.com/development/2026/02/09/heroku-future-in-doubt-as-salesforce-freezes-features-to-focus-on-ai/4090238)); Cloudflare's Pages docs now say to start new projects on Workers ([Cloudflare](https://developers.cloudflare.com/pages/)); Fly.io has no free tier for new organizations ([pricing](https://docs.fly.io/about/pricing)).
- **Sync and AI libraries:** Replicache is in maintenance mode (its makers point to Zero) ([Replicache](https://replicache.dev/)); ElectricSQL's hosted cloud is winding down ([Electric](https://electric.ax/blog/2026/08/11/electric-joining-databricks.md)); LlamaIndex.TS is archived.
- **Data:** Redis 8 is offered under RSALv2, SSPL or AGPLv3 ([Redis](https://redis.io/legal/licenses/)); Valkey is the BSD-licensed fork. PostgreSQL 14 support ends November 2026 ([PostgreSQL](https://www.postgresql.org/support/versioning/)). Use pgvector 0.8.2 or later ([security fix](https://www.postgresql.org/about/news/pgvector-082-released-3245)).
- **Pricing models changed recently** at Vercel, Netlify, Render and Auth0 ([Netlify](https://www.netlify.com/changelog/2026-04-14-pricing-updates-april-2026/), [Render](https://render.com/changelog/updated-plans-for-render-workspaces), [Auth0](https://auth0.com/pricing)). Always price from the current pricing page.
- **Free-tier traps.** Several free plans pause, expire or forbid commercial use: for example, Supabase free projects pause after a week without activity and have no backups, and Vercel's free plan is for non-commercial use only. For a paid product, budget the first paid tier from launch day; for a hobby project, pick a free plan that never sleeps.
- **Official guides lag their own ecosystems.** A framework's guide can still recommend a renamed or deprecated package; confirm package status in the registry (npm, PyPI) before naming it in a plan.

### Web app or SaaS
- Decide: rendering approach, language/framework, database, sign-in, hosting, background jobs, email.
- Candidates: TypeScript with Next.js, React Router or SvelteKit (TanStack Start reached 1.0 only in October 2026: promising, young); Python with Django; Ruby on Rails; PHP with Laravel; C# with ASP.NET Core on a current long-term release. PostgreSQL, managed (Neon, Supabase, AWS RDS, or the hosting platform's own).
- Sign-in: a managed provider (for example Clerk, Auth0, WorkOS when enterprise single sign-on matters, or Supabase Auth) or a maintained library (for example Better Auth, or the framework's built-in authentication in Django, Rails or Laravel).
- Hosting: Vercel, Netlify or Cloudflare Workers for web-first apps; Render, Railway, Fly.io, Google Cloud Run, Azure Container Apps or AWS ECS for always-on services and workers. Look at each platform's recent incident history as well as its price.
- Background jobs: the framework's own queue (Solid Queue, Celery, BullMQ) or a managed workflow service (Inngest, Temporal Cloud) when jobs are long or multi-step.
- Traps: a separate API service and frontend repository for a small app; database access rules left off (for example Supabase tables created by raw SQL without row-level security); background work squeezed into request handlers.

### Sold to many customers (multi-tenant)
Add these decisions to the web playbook:
- **Tenancy model.** Shared database with a tenant ID on every row, enforced in one data-access layer and ideally by database row-level security (default). Schema-per-tenant or database-per-tenant only for strict isolation needs or large enterprise customers. Hard to reverse: decide deliberately and record an ADR.
- **Organizations, users and roles**; invitations; what an admin can do.
- **Enterprise sign-in** (SAML or OIDC single sign-on) when selling to larger companies; pick an identity provider or library that supports it later without migration, and record the extension point in the sign-in ADR: users keyed by a stable internal ID (not email), a per-company sign-in policy (password, SSO, or SSO required), verified email domains that route people to their company's SSO, and accounts created or removed from the SSO directory.
- **Customer API and webhooks** when customers will integrate: design the internal module interfaces as if they were public (stable IDs, pagination, idempotency keys), so a versioned API and signed webhooks can be added later without reshaping the data.
- **Billing** through a provider; plans, trials, and what happens when payment fails.
- **Isolation tests**: automated tests that prove one tenant cannot read or change another's data. Make them a CI gate.
- **Audit log**, per-tenant rate limits, per-tenant data export and deletion, and cost per tenant.

### Community and marketplace apps
For apps where members of the public post content, message each other, trade, or meet in person. Add these decisions to the web playbook and record them under the "Trust and safety" ledger area:
- **Location privacy.** Show approximate areas (ZIP code, neighborhood, rounded distance), never street addresses; let people share exact details privately. Strip GPS and other metadata from uploaded photos.
- **Meeting strangers.** Safety tips at the point of arranging a meetup; suggest public places.
- **Abuse handling.** Report and block from day one (app stores require them for user-generated content), an admin queue to remove posts and members, and contact details kept private by default.
- **Age.** Decide a minimum age, and check whether local law adds duties for minors.
- **Prohibited items and content.** House rules, plus anything illegal to trade where the app operates; research the specifics.
- **Account deletion and data export** for members.
- Traps: exposing contact details in listings; photos that reveal home locations; no moderation plan for the owner's time.

### Internal business tool
- First check build or buy: low-code internal tool builders, spreadsheets with automation, or an existing SaaS product may be enough.
- If building: the web playbook, simplified. Company single sign-on, role-based access, audit trail if it touches money or personal data, and integration with existing systems.

### Mobile app
- Decide: mobile web or installed app; cross-platform or native; offline needs; push notifications; app store review and update strategy; backend.
- Candidates: a responsive web app or PWA when store presence and deep device features are not needed. Cross-platform: React Native with Expo (the New Architecture is now mandatory), or Flutter. Native Swift/SwiftUI and Kotlin/Jetpack Compose for heavy device integration or top-tier performance.
- Traps: building iOS, Android and web separately on a small team; underestimating app store review, signing and release management; forgetting how old app versions keep calling your API.

### Desktop app
- Decide: platforms; distribution (store, direct download, company deployment); auto-update; code signing; local versus cloud data.
- Candidates: Tauri 2 (small and fast, web UI with a Rust core; version 3 is still alpha); Electron (mature, larger footprint); .NET for Windows-centric business apps; native toolkits for platform-specific excellence. Embedded SQLite for local data.
- Traps: shipping without code signing or auto-update; adding a server the product does not need.

### Offline-first or local-first
- Decide: what must work offline; single device or sync across devices and users; conflict handling; local storage limits.
- Candidates: local SQLite (or IndexedDB in browsers) as the primary store. When records are mostly created and rarely edited by others, a simple design works: append-only records with unique IDs and timestamps, uploaded when a connection appears. When several people edit the same records, adopt a sync engine with proven production use on your platform (for example PowerSync or Zero; verify current status) rather than writing conflict resolution yourself.
- Traps: defaulting to a cloud-only web stack; building general-purpose sync and conflict resolution from scratch; forgetting that laptops get lost, so unsynced data needs its own backup and encryption.

### API, integration or automation
- Decide: triggers (schedule, webhook, queue); retries and idempotency; error alerts; secrets for the connected systems; rate limits.
- Candidates: the language with the best SDKs for the systems you connect to; a managed scheduler or durable workflow service for multi-step jobs; a queue when volume or retries require it.
- Traps: no retry or idempotency (duplicate charges or emails); failures nobody hears about.

### Product with AI features
- Read ai-features.md.

## Build or buy

Buy or use a managed service by default for: sign-in and identity, payments and billing, email and text delivery, error tracking, file storage, search beyond the database's built-in features, and video or maps.

Some integrations need outside approval with a lead time: business texting in the US (each sender registered with carriers, with a website, privacy policy and consent wording required; providers quote days, but reported waits run to several weeks, so check current guidance and plan for the long end), app store review, payment provider verification, and partner API programs. Research these early and put them on the roadmap's critical path. Build when the capability is the product's core differentiator, when no provider meets a hard requirement (data residency, offline use, cost at scale), or when the dependency risk is unacceptable. Write down the exit path for any provider that would be hard to replace.

## Evidence rules

- **Scale research to the tier.** Light: check only the few facts the decision hinges on (free-tier limits, the main framework's current version), about 5–10 lookups. Standard: a focused pass per one-way-door decision. Critical: thorough, with primary sources for anything compliance-related. When subagents are available, run the lookups in parallel in the background.
- **Verify, when you can browse:** the current stable or long-term-support version and its support window; recent release activity; license and any recent license change; pricing model and free-tier limits; known security problems; compatibility between the chosen parts.
- **Prefer primary sources:** official documentation, release notes, pricing pages, security advisories. Treat vendor benchmarks and marketing as claims.
- **Record** each source with the date you checked it in the ADR's Evidence section.
- **Cannot browse?** Say so. Write "Unverified — based on general knowledge as of [date]" in the ADR, and add a verification task to Milestone 0.
- **Never invent** prices, version numbers, benchmark results, compliance claims or compatibility.
- **State your confidence.** When uncertain, say so and say what would resolve it.

## Pushback

Raise a concern when the user proposes something, or asks to keep something, that weakens the project. Label the severity so the user knows how much it matters:

- **Blocker** — creates unacceptable security, legal or data-loss risk. Do not plan around it. Offer safe alternatives; if the user insists, record that this part is blocked and why.
- **Material risk** — likely to cost real money, time or reliability. Recommend the change; if the user keeps their choice, record it as an accepted risk (risks.md) with a mitigation, and note "decided against recommendation" in the ADR.
- **Tradeoff** — a reasonable choice with downsides. Note it in one line and follow the user's preference.

Do not confuse your preference with necessity. A familiar tool the team knows well often beats a "better" one they don't.

Protocol: name the concern · explain the likely consequences in their terms (money, time, risk) · say whether it bites now or later · say when their idea would be the right call · recommend the alternative · state the tradeoff · let them decide within acceptable risk.

When several parts of the user's proposal share one root cause (sized for a scale or team they don't have), put them on one card with a short comparison table instead of one card each, and merge the card into the architecture package.

When the user objects instead of choosing ("but will it scale?"), answer the objection once, directly, with numbers and a credible precedent, and offer a cheap way to prove the point (a load test at 10× peak, a spike), then ask again. If they still prefer their way after that, stop arguing: plan it their way within acceptable risk and record the accepted risk.

| Situation | Usually | Better default | When the user is right |
|---|---|---|---|
| Microservices for a small app or team | Material risk | Modular monolith with enforced boundaries | Independent teams, very different scaling needs, isolation requirements |
| Kubernetes or self-managed servers, nobody on operations | Material risk | Managed platform | Existing platform team, cost at large scale, hard on-premises requirement |
| Document database for relational data (orders, invoices, permissions) | Material risk | PostgreSQL, with JSON columns for flexible parts | Truly document-shaped data with few relations |
| Designing for millions of users on day one | Material risk | Design for 10× the realistic 12-month estimate | Confirmed launch audience at that scale |
| Multi-agent or heavy AI framework where one model call or plain code works | Material risk | Simplest AI pattern that meets the need (ai-features.md) | Demonstrated need that evaluations show simpler designs miss |
| Building custom sign-in, payments or email delivery | Material risk; Blocker if storing card data or raw passwords | Proven provider or library | Hard constraint no provider meets |
| Unmaintained, very new or license-incompatible technology | Material risk | Mature alternative | Clear benefit and an exit plan |
| Ignoring costs: AI usage, bandwidth, storage growth, backups, per-seat pricing | Material risk | Cost sketch with alerts | — |
| Permission checks only in the browser; no tenant isolation; shared admin accounts; secrets in code | Blocker | Server-side checks, isolation tests, individual accounts, secret store | — |
| iOS, Android, web and desktop all in version 1 on a small team | Material risk | One platform first, chosen by where users are | Funded team per platform |
| "No tests for now" on AI-written code | Material risk | Minimal tests on core flows from Milestone 1 | Throwaway prototype, labeled as such |

## Cost sketch

Required for Standard and Critical; a one-line estimate is enough for Light.

1. List every paid part: compute, database, storage, bandwidth, sign-in (often priced per monthly active user), email and texts, AI usage, monitoring, domains, app store fees.
2. Estimate usage at launch and at the 12-month target. If the user named a longer-term goal (2,000 companies in three years), add a rough figure for it too, labeled as rough.
3. Price each from current pricing pages, with the date checked. Without browsing, give a labeled rough range.
4. Report a range for both points, the biggest cost driver, and any cliffs (free-tier limits, per-seat jumps, minimums). When costs grow per customer (texts, seats, storage per tenant), also give the running cost per customer, because it sets the floor for pricing.
5. Recommend billing alerts on every paid service.

## Presenting the package

Present the architecture as one coherent package, not a string of separate questions. Parts depend on each other, and a non-engineer can judge a whole picture more easily than isolated choices. Use this shape (SKILL.md › Recommendation formats has the card versions):

| Part | Recommendation | Why, in plain words | Change later |
|---|---|---|---|
| (each part) | (choice) | (one reason tied to their needs) | Easy / Moderate / Hard |

Follow it with: expected monthly cost at launch and at the growth target, the main tradeoff, the main alternative and why it lost, and one approval question. Give a part its own decision card only when it is a real tradeoff the user owns (cost against convenience, control against lock-in, store app against web), when it is hard to reverse and your confidence is low, or when it contradicts something the user asked for.
