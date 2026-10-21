# ADR-0005: Background jobs with Procrastinate, a PostgreSQL-based queue

- Status: Accepted
- Date: 2026-10-19 (queues, payload rules and the transaction spike added the same day after the review panel, before any code)
- Decided by: Product owner, approving the recommended architecture package on 2026-10-19. Ravi confirms in M0.
- Confidence: Medium
- Change later: Moderate

## Context
Work that is slow, must retry or runs on a schedule cannot run inside a web request: sending emails and texts (FR-14, NFR-9: within 1 minute), urgent alerts (FR-11), photo processing (FR-1, FR-4), spreadsheet imports (FR-6), Stripe webhooks (FR-7), nightly backups and cleanup. A job must never be lost when its data is saved, nor sent when the data was rolled back. The owner wants nothing extra to watch at night.

## Options considered
1. **Procrastinate** — jobs stored in the same PostgreSQL database, so a job is saved in the same transaction as the data; retries, periodic tasks, locks and Django integration; actively maintained / less familiar to AI agents than Celery.
2. **Celery with Valkey (Render Key Value, from $10 a month)** — the most familiar Python queue / a second data store to run and watch; enqueueing is not part of the database transaction unless deferred carefully.
3. **Django's Tasks framework** — a first-party interface / Django ships no production backend or worker, and the reference package removed its database backend in 0.12.0.

## Decision
Use Procrastinate with its Django integration. All job code goes through `core.jobs`, a thin wrapper, so the queue could be swapped later.
- Two queues on separate Render workers: `messages` (emails, texts, urgent alerts, webhooks, cleanup) on two small instances, so one failure does not stop urgent alerts; and `media` (photo processing, spreadsheet imports) on one instance that holds no email, text or Stripe credentials, because it opens untrusted files.
- Jobs are deferred inside the same transaction as the data they act on. Whether Procrastinate's Django integration joins the Django transaction is verified by an M0 spike (a deferred job must disappear when the transaction rolls back); if it does not, jobs are deferred with `transaction.on_commit` instead.
- Job payloads hold IDs only, never message text, names, phone numbers or email addresses, because Procrastinate's tables are not company-scoped. Every payload carries `company_id`, and the job sets the company context before touching data.
- Payload changes stay backward compatible for one release, so old and new workers can run side by side during a deploy.
- Sends use idempotency keys so a retry never double-sends. Periodic tasks handle link expiry, data retention, cleanup of finished jobs and a heartbeat per queue.
- Workers connect directly to PostgreSQL (no external connection pooler), because Procrastinate's workers use LISTEN/NOTIFY.

## Why
- No extra service: the queue shares the database's backups, failover and monitoring.
- Saving a job in the same transaction as the data removes a whole class of lost or phantom notifications.
- Expected volume (thousands to tens of thousands of jobs a day) is well within what a PostgreSQL queue handles.
- Option 2 lost on operations work; option 3 is not production-ready yet.

## Consequences
- Good: one data store; simple recovery; job history queryable with SQL.
- Costs and tradeoffs: agents know Procrastinate less well than Celery, so the first job (M1) becomes the documented pattern to copy. The job table needs periodic cleanup. Confidence is Medium because the library is less widely used.
- Follow-up work: M0 spike on transactional deferral and on Django 6.1 / Python 3.14 support; build `core.jobs`, both queues and their heartbeats in M1.

## Evidence
- [Procrastinate on PyPI](https://pypi.org/project/procrastinate/) (checked 2026-10-19) — version 3.10.0 released 2026-09-23; PostgreSQL 13+; Django integration, retries and periodic tasks.
- [Procrastinate pyproject.toml](https://github.com/procrastinate-org/procrastinate/blob/main/pyproject.toml) (checked 2026-10-19) — Django extra requires Django 2.2 or later.
- [Loopwerk review of Django 6.0 Tasks](https://www.loopwerk.io/articles/2026/django-tasks-review/) (checked 2026-10-19) — no worker and no production backend in Django.
- [django-tasks on PyPI](https://pypi.org/project/django-tasks/) (checked 2026-10-19) — 0.12.0 (2026-02-06) ships only the dummy and immediate backends.
- [Render pricing](https://render.com/pricing.md) (checked 2026-10-19) — Key Value from $10 a month.

## Revisit when
- Queue delay breaks NFR-9 or job volume passes about 50 jobs per second.
- Django ships a production-ready database task backend (consider moving to the `django.tasks` interface).
- Procrastinate's maintenance stalls (no release for 12 months).
