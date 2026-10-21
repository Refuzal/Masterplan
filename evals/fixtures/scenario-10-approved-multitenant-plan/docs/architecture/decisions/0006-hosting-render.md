# ADR-0006: Hosting on Render (Ohio) with a preview environment per pull request

- Status: Accepted
- Date: 2026-10-19 (workers, backup job and preview limits added the same day after the review panel)
- Decided by: Product owner, approving the recommended architecture package on 2026-10-19 after setting the criteria (Ravi is productive with it; it does not wake the founders at night). Ravi confirms in M0.
- Confidence: Medium
- Change later: Moderate

## Context
The app needs always-on web instances, a background worker (ADR-0005) and managed PostgreSQL with failover and point-in-time recovery (ADR-0002), to meet NFR-2, NFR-3 and NFR-7 (about $500 a month at launch). Nobody's job is operations. AI agents write much of the code, so every change should be checked by a human in a real environment before it reaches production. Customers are mostly in the US, some in Canada.

## Options considered
1. **Render** — push-to-deploy containers, background workers, managed PostgreSQL with high availability and 7-day point-in-time recovery, full-stack preview environments per pull request, infrastructure described in a `render.yaml` Blueprint / no Canadian region; regional incidents in 2026 (a 2 h 14 min critical web outage in Oregon on 2026-07-24).
2. **DigitalOcean App Platform with Managed PostgreSQL** — cheaper, a Toronto region, standby nodes and 7-day point-in-time recovery / per-pull-request previews come from a GitHub Action rather than the platform, and that documentation does not say how databases are handled in previews.
3. **Google Cloud Run with Cloud SQL** — strong reliability and Canadian regions, similar database cost (about $99 a month for a 1-vCPU high-availability instance) / networking, permissions, secrets and deployment pipelines are set up by hand, which takes Ravi weeks and adds things to watch.
Not considered further: Heroku (no longer adding features), AWS App Runner (closed to new customers), self-managed servers or Kubernetes (operations work).

## Decision
Render, Pro workspace, Ohio region:
- web service: 2 instances of 1 CPU / 2 GB behind Render's load balancer, with a health check and zero-downtime deploys;
- background workers (ADR-0005): two instances of 0.5 CPU / 512 MB for the `messages` queue, and one instance of 1 CPU / 2 GB for the `media` queue;
- a nightly cron job that runs the database backup as the owner role, with the only copy of the backup-bucket upload key;
- PostgreSQL per ADR-0002;
- a preview environment for every pull request, created from `render.yaml` with seed data only, sandboxed email and texts, the smallest instance sizes and expiry after 3 days without activity;
- production deploys automatically from `main` after CI passes and a human approves the pull request.
Oregon is avoided because it had the most incidents in the visible 2026 history. All infrastructure lives in `render.yaml`; changing it is a material change (AGENTS.md › Change control).

## Why
- Lowest operations work of the credible options: no servers, automatic restarts, managed failover and backups.
- Full-stack previews let the founders check each AI-written change in a real environment before it ships.
- Fits the budget (architecture.md › Cost). DigitalOcean lost on preview workflow maturity; Google Cloud lost on setup and operations work.

## Consequences
- Good: Ravi spends his time on the product; the infrastructure is reviewable code.
- Costs and tradeoffs: about $215–230 a month on Render at launch, including the database. No Canadian region (risks.md R-7). A regional Render outage takes the product down (risks.md R-6, R-8). Moving away later means re-creating the services elsewhere and moving the database: about 1–2 weeks, because the app is a standard container and standard PostgreSQL.
- Follow-up work: `render.yaml`, the health check and the preview seed script in M1.

## Evidence
- [Render pricing](https://render.com/pricing.md) (checked 2026-10-19) — Pro workspace $25 a month; 0.5 CPU / 512 MB service $7 and 1 CPU / 2 GB service $25 a month; cron jobs billed per minute; bandwidth overage $0.15/GB.
- [Render regions](https://render.com/docs/regions) (checked 2026-10-19) — Oregon, Ohio, Virginia, Frankfurt, Singapore; no Canadian region.
- [Render preview environments](https://render.com/docs/preview-environments) (checked 2026-10-19) — full-stack copy per pull request from the Blueprint, datastores start empty, Pro workspace required, billed by the second.
- [Render incident history](https://pingoru.io/providers/render/outage-history) (checked 2026-10-19) — 2026-07-24 critical Oregon web outage, 2 h 14 min; Oregon in six visible incidents.
- [DigitalOcean App Platform regions](https://docs.digitalocean.com/products/app-platform/details/availability/) and [pricing](https://www.digitalocean.com/pricing/app-platform) (checked 2026-10-19); [DigitalOcean PR previews via GitHub Actions](https://digitalocean.com/blog/github-actions-for-app-platform) (2024-09-26, checked 2026-10-19).
- [Cloud SQL pricing](https://cloud.google.com/sql/pricing) (checked 2026-10-19) — high availability doubles the per-vCPU and memory rates.

## Revisit when
- A customer requires Canadian data residency.
- Render incidents break NFR-2 in two months of any quarter.
- The Render bill passes $1,500 a month.
- A requirement for running in more than one region appears.
