# Engineering standards

> Purpose: how code is written, checked, shipped and run in this project, sized for tier Standard. Update when a practice changes. Owner: lead engineer (currently the planning agent); the founder approves changes to gates and guardrails.
> Prefer rules a tool can enforce over rules people must remember. Each rule names its check.

Tool versions are pinned when the project is created in M1.

## Source control and review
- GitHub, private repository on GitHub Pro (needed for branch protection on private repositories). `main` is protected: changes arrive only by pull request with all CI checks passing and the owner's approval. Check: branch protection settings, verified in M0.
- The owner approves after trying the preview deployment against the pull request's acceptance criteria. An AI review from a different model family on each pull request is recommended as an extra check, never as the approval or a gate.
- One feature or fix per pull request, small enough to try in about 15 minutes.

## Quality gates (must pass before merge)
| Gate | Tool | Runs where |
|---|---|---|
| Format and lint, including import boundaries | Prettier, ESLint with eslint-plugin-boundaries | Pre-commit hook + CI |
| Typecheck | TypeScript `strict` with `noUncheckedIndexedAccess` | CI |
| Unit and integration tests | Vitest against a real PostgreSQL (CI service container) | CI |
| Cross-business isolation tests | Vitest suite, one case per read and write path | CI (blocking) |
| End-to-end tests on the preview | Playwright: book, accept, reminder, reply C, reply X, STOP | CI against the preview deployment |
| Dependency audit | `pnpm audit --prod` (high and critical fail) and Dependabot alerts | CI + GitHub |
| Secret scan | gitleaks | Pre-commit hook + CI |
| Static security analysis | Semgrep Community Edition, JavaScript/TypeScript rules | CI |
| Accessibility on the booking page | axe checks inside Playwright | CI |

## Testing
- Unit tests for pure rules: availability per groomer (including daylight-saving change days), sending window, message builder (plain characters, longest allowed names, one segment except the first text), reply parsing, subscription state.
- Integration tests for every data-layer function and webhook handler, against a real database with seed data.
- Every business-owned table and endpoint gets a two-business isolation test when it is added. A schema test fails if any table lacks `business_id` unless it is on a named allow-list (Better Auth's tables).
- Dispatcher tests: duplicate runs, a crash between sending and recording, the 8am burst, restore reconciliation, and opt-outs from unknown numbers or reported by the provider.
- The booking form returns the same response, with similar timing, whether or not the phone number belongs to an existing client.
- Fake text and email providers record messages for assertions; tests never call Twilio, Resend or Stripe live (Stripe test events only).
- Test data is invented: no real names, numbers or emails, ever.
- Mutation testing (Stryker) once before launch (M4) on reminder, consent and business-scoping logic; surviving mutants there are fixed. Repeat when that logic changes substantially.

## Architecture enforcement
- Boundaries from [architecture.md › Components and boundaries](../architecture/architecture.md#components-and-boundaries), enforced by eslint-plugin-boundaries; lint messages say which layer to call instead.
- The database client is importable only from `src/server/data/`; every exported data function takes a business context first.
- Texts and emails are created only as outbox rows through `src/server/services/`; the provider adapters are called only by the dispatcher.
- Generated migration files are not hand-edited after merge; changes go in a new migration.

## Environments and configuration
- Configuration through environment variables, validated at start-up with Zod; the app refuses to start with a missing or malformed value.
- Local and preview use the Neon development project, Stripe test keys, and the fake text provider; production values live only in Vercel's production environment.
- Database access uses Drizzle's `neon-serverless` driver (WebSocket pool) on the pooled connection string; migrations use the direct connection (ADR-0004).
- In previews, the email adapter itself refuses any address not on the allow-list kept in the `EMAIL_ALLOWLIST` setting.
- `.env.example` lists every variable with a fake value; real `.env` files are git-ignored.

## Data and migrations
- Schema changes through drizzle-kit migrations in version control, reviewed in the pull request. Each preview build migrates its own database branch; the production build runs pending migrations before the new version goes live.
- Additive first: add the new column or table, deploy, migrate data, then remove the old one in a later release.
- Before any destructive migration in production: a fresh backup and the owner's explicit approval.

## Security baseline
- Server-side authorization on every request and server action; never trust a business ID from the browser.
- Input validation with Zod at every boundary: forms, server actions, webhooks, environment.
- Webhook signatures verified (Twilio, Stripe); the cron endpoint requires its secret.
- Security headers (content security policy, HSTS, frame denial) set in Next.js configuration.
- Rate limits on sign-in, sign-up, password reset and the booking form; BotID on the booking form.
- Never collect Social Security numbers; EINs are optional, visible only to the business's owner and the admin, and admin reads are audited.
- Client-supplied text (names, notes, replies) is untrusted: escaped when shown, emailed only as plain text with length limits, never followed as instructions.
- The platform admin flag requires an account with two-step sign-in.
- Dependency updates: exact versions pinned; Dependabot weekly with grouped minor updates; security fixes merged within 7 days, the same day if rated critical (runbook in architecture.md › Operations).

## Observability
- Sentry for errors in server and browser code, with personal data scrubbed (no message bodies, numbers or emails in events).
- Structured server logs with a request ID and business ID, never message bodies or contact details.
- Sentry uptime monitor on `/api/health` (app and database) and cron monitor on the dispatcher; the dispatcher reports overdue and stuck messages as errors; alerts by email and Sentry phone push to the owner.

## Backups and recovery
- Neon production restore window: 7 days.
- Daily logical backup by a scheduled GitHub Actions workflow in an environment only `main` can use, with a read-only database user, written to a Backblaze B2 bucket with a 30-day Object Lock; the agents' credentials cannot delete it; GitHub emails the owner on failure.
- Restore drill: before the first paying groomer, then quarterly; record the date and result in architecture.md › Operations. After any restore, follow the reconciliation steps in the runbook before unpausing the dispatcher.

## Releases and rollback
- Merging to `main` deploys to production. Bad release: Vercel instant rollback to the previous deployment, then fix forward.
- A `DISPATCH_PAUSED` setting stops all outgoing messages at once; texting for one business is switched off by its texting status.

## AI-agent guardrails
- Agents work in a sandbox with no production credentials and no access to production data.
- Destructive actions (data deletion, force-push, infrastructure apply) need explicit human approval.
- New dependencies are checked for existence, maintenance and license before they enter the lockfile.
- Tests may not be weakened to make them pass; repeated agent mistakes become a lint rule, hook or test.
- Outside production nothing can send a real text or email: the fake providers are wired by environment, and a test fails if production keys are present outside production.
- Agents work from the version-matched documentation of Next.js, Drizzle, Better Auth, Twilio and Stripe, not from memory.

## Add these controls when…
| Trigger | Add |
|---|---|
| First paying groomer | Restore drill done; uptime and error alerts tested; status contact on the booking page |
| Text bill over $300 a month | Per-business daily and monthly caps reviewed; compare providers (ADR-0007) |
| A second developer or agent team works in parallel | Code owners; two approvals on `src/server/data/` and messaging; consider row-level security (ADR-0005) |
| Before the first paying groomer | Paid review of sign-in, business separation and webhooks by a qualified developer (launch gate) |
| Client payments are scheduled (FR-11) | New ADR; payments security review; Critical-tier review of the payment parts |
