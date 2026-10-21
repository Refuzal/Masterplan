# ADR-0003: Host on Vercel (Pro plan) with a preview for every change

- Status: Accepted
- Date: 2026-10-19
- Decided by: Owner (approved the architecture package on 2026-10-19)
- Confidence: High
- Change later: Moderate

## Context
The app is a commercial product, so free hobby plans that forbid commercial use are out. Reminders must go out within 15 minutes of their scheduled time (NFR-9), so the host needs a reliable scheduler that runs at least every few minutes. The owner reviews changes by trying them, not by reading code, so every change should get its own private test link. Nobody's job is operations, so the host must be fully managed with simple rollback. Traffic is small (NFR-7).

## Options considered
1. **Vercel Pro** — made by the Next.js team; a preview deployment for every pull request; instant rollback; cron jobs down to once per minute with per-minute precision on Pro; bot protection (BotID Basic) free / $20 per developer seat per month; usage-based beyond the included $20 credit; vendor features tie in somewhat.
2. **Render** — always-on web service plus cron jobs and managed PostgreSQL in one place / preview environments need a paid team workspace; slower deploys; we would run more of the plumbing ourselves.
3. **Netlify or Cloudflare Workers** — capable and cheap / Next.js support goes through adapters, and scheduled functions have tighter limits; less well-trodden for this stack.

## Decision
Deploy the Next.js app to Vercel on the Pro plan, region US East (close to the database). Production deploys only from the main branch after CI passes and the owner approves the pull request; every pull request gets a preview deployment. Vercel Cron triggers the message dispatcher every minute (ADR-0008).

## Why
- Preview links per change let a non-programmer check each AI-made change before it reaches groomers.
- Per-minute cron covers reminders without another service.
- Render lost on preview-environment cost and more operations work; Netlify and Cloudflare on adapter complexity for Next.js.

## Consequences
- Good: zero server management; one-click rollback; previews; free basic bot protection.
- Costs and tradeoffs: $20 per month per developer seat (one seat: the owner); usage beyond the included credit is billed, so a spend alert is required; moving hosts later means replacing cron, previews and environment setup.
- Follow-up work: set a spend alert; protect the cron endpoint with a secret; keep production environment variables out of local and preview environments.

## Evidence
- Vercel pricing: "Our Hobby plan is for personal, non-commercial use"; Pro $20/month per developer seat with $20 of included usage credit — https://vercel.com/pricing (checked 2026-10-19)
- Vercel cron limits: Pro minimum interval once per minute, per-minute precision; Hobby once per day — https://vercel.com/docs/cron-jobs/usage-and-pricing (checked 2026-10-19)
- Vercel BotID: Basic mode free on all plans — https://vercel.com/docs/botid (checked 2026-10-19)

## Revisit when
- The Vercel bill exceeds $150 per month, or its pricing model changes materially.
- Work appears that runs longer than a function may run (for example large exports), or needs always-on connections.
- Two or more Vercel incidents in a quarter cause missed reminders.
