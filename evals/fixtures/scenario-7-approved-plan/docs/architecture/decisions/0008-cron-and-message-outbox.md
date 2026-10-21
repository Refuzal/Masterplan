# ADR-0008: Scheduled work through a database outbox and a per-minute cron

- Status: Accepted
- Date: 2026-10-19
- Decided by: Owner (approved the architecture package on 2026-10-19)
- Confidence: High
- Change later: Moderate

## Context
Reminders must go out within 15 minutes of their scheduled time, never twice, and never after an opt-out or a cancellation (FR-7, NFR-9). Booking confirmations, declines and expiries also send messages (FR-4). Volume is small: about 30,000 messages a month at the year-one goal, with a burst at 8am local time when reminders held back overnight are released. Hosting runs short-lived functions (ADR-0003); Vercel cron calls are not retried when they fail and can occasionally arrive twice.

## Options considered
1. **Database outbox plus Vercel Cron every minute** — every message is a row with a send time and a status; a cron-triggered function claims due rows and sends them / we own the retry and claiming logic (small, testable).
2. **A managed workflow service (Inngest, Trigger.dev, Upstash QStash)** — retries and delayed jobs handled for us / another vendor, account and failure mode; scheduled state lives outside our database, so cancelling or moving an appointment means finding and cancelling remote jobs.
3. **Sending inside the web request, plus scheduled jobs on a separate worker server** — always-on server / more infrastructure for a small app.

## Decision
A `message` table is the outbox for every text and email. Creating, moving or cancelling an appointment updates its scheduled messages in the same database transaction. Vercel Cron calls the dispatcher every minute (protected by a secret). Each run:
1. stops at once if the dispatcher pause switch is on (used after a database restore and in emergencies);
2. claims up to 200 due rows atomically in one statement (status `scheduled` to `sending`, skipping rows another run holds), so overlapping or duplicate runs are safe and a missed run is simply caught by the next one;
3. re-checks each row at send time: appointment still booked, client still opted in (the consent record for that business and number is authoritative), business active, texting approved, and local time inside the sending window (8am–8pm in the business's time zone) [Assumption];
4. sends through the provider with a status-callback address that carries the message ID, then records the provider's message ID and status `sent`;
5. stops claiming new rows after 40 seconds and leaves the rest for the next run.

A row stuck in `sending` for more than 10 minutes is never resent automatically. If the provider's status callback for it arrives, the row is updated to `sent` or `delivered`; if none arrives, it becomes `stuck`, is reported to Sentry as an error, and the admin decides. Missing one reminder is better than texting a client twice. If the provider reports the recipient has opted out, the opt-out is recorded.

## Why
- Keeps all scheduling state in one place, so moving or cancelling an appointment is a simple update in the same transaction.
- No additional vendor; easy to test end to end with the fake text provider.
- Managed workflow services lost because they add a second source of truth for scheduled messages at this small volume.

## Consequences
- Good: transparent, testable, cheap; message history doubles as text-usage records (FR-10).
- Costs and tradeoffs: the per-minute job keeps the database awake (ADR-0004); about 200 messages a minute per run is the ceiling, enough to clear an 8am burst of thousands within minutes.
- Restoring the database to an earlier moment turns already-sent messages back into `scheduled`. After any restore the dispatcher stays paused until every message due before the restore was finished is marked `cancelled` or `stuck` and checked against the provider's log (runbook in architecture.md › Operations).
- Follow-up work: dispatcher, claim logic and tests in M3: duplicate runs, a crash between sending and recording, the overnight burst, and restore reconciliation. The dispatcher reports overdue and stuck messages to Sentry (NFR-9).

## Evidence
- Vercel cron: per-minute minimum interval and precision on Pro — https://vercel.com/docs/cron-jobs/usage-and-pricing (checked 2026-10-19)
- Vercel cron management: failed invocations are not retried; events can be delivered more than once (reported by the independent review, citing https://vercel.com/docs/cron-jobs/manage-cron-jobs, 2026-10-19)
- Planning method default: request/response first; add a queue or schedule when work must retry or run later; no message broker until measured (technology-selection reference).

## Revisit when
- Messages exceed about 2,000 an hour at peak, or a dispatcher run regularly hits its 40-second budget.
- Multi-step workflows appear (for example payment retries with several stages), which may justify a managed workflow service.
