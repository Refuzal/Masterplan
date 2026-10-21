# ADR-0010: Supporting services — Resend for email, Sentry for errors and uptime, Vercel BotID for the booking form

- Status: Accepted
- Date: 2026-10-19
- Decided by: Owner (approved the architecture package on 2026-10-19)
- Confidence: High
- Change later: Easy

## Context
The app sends email for sign-in, groomer notifications and client messages before texting is approved (FR-1, FR-4, FR-8). Someone must hear about errors, downtime and stalled reminders (NFR-3, NFR-9), and the owner is the only person on call. The public booking form must resist junk submissions (FR-3). Running cost should stay low (owner preference: cheaper and faster).

## Options considered
1. **Email: Resend** — simple API, free for 3,000 emails a month (100 a day), $20 for 50,000 / young company. **Postmark** — excellent deliverability, from $15 a month / no free tier for production volume.
2. **Errors and uptime: Sentry Developer plan** — free: 5,000 errors, one uptime monitor, one cron monitor / one user only. **Better Stack** — good uptime and logs / another account.
3. **Bot protection: Vercel BotID Basic** — free on all plans, invisible to clients / basic mode stops simpler bots only. **Cloudflare Turnstile** — free, visible widget sometimes / another vendor.

## Decision
Resend for all email, behind an `EmailSender` interface with a fake implementation outside production. Sentry for error tracking, one uptime monitor on the health endpoint and one cron monitor on the dispatcher, alerting the owner by email. Vercel BotID (Basic) plus rate limits on the booking form and sign-in.

## Why
- Cheapest options that meet the needs, each easy to swap behind a small interface.
- One monitoring tool covers errors, downtime and stalled reminders.

## Consequences
- Good: $0 at launch for all three.
- Costs and tradeoffs: Resend's 100-a-day free limit is passed at roughly 15 active salons; budget $20 a month from then. Sentry's free plan allows one user only.
- Follow-up work: sending domain verification (SPF, DKIM, DMARC) in M0; Sentry wiring in M1.

## Evidence
- Resend pricing: free 3,000 emails/month, 100/day, 3 domains; Pro $20/month for 50,000 — https://resend.com/pricing (checked 2026-10-19)
- Sentry pricing: Developer plan 5k errors, one user, one uptime monitor, one cron monitor; Team $29/month — https://sentry.io/pricing/ (checked 2026-10-19)
- Vercel BotID: Basic free on all plans — https://vercel.com/docs/botid (checked 2026-10-19)

## Revisit when
- Email deliverability problems (bounces or spam-folder reports) appear.
- More than one person needs alerts, or errors pass 5,000 a month.
- Junk bookings get through BotID Basic.
