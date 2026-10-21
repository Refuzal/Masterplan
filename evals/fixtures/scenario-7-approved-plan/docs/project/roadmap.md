# Roadmap

> Purpose: what gets built in what order, and how each milestone is accepted. Update when a milestone finishes or scope moves. Owner: the founder (product owner) with the lead engineer.

Target: a first version groomers can buy by mid-January 2027, about 13 weeks from 2026-10-20, with the owner building 20 or more hours a week. Week numbers are targets, not promises; the critical path is carrier approval for texting (ADR-0007), which is why the owner's Twilio setup starts in M0 and the first pilot groomer's registration in M2.

## M0 — Safe to build (week 1)
Goal: make it safe for AI agents and the owner to change this repository, and start the slow approvals early.
Owner tasks (only the owner can do these):
- [ ] Domain name bought; business email address on it.
- [ ] GitHub account on GitHub Pro; private repository created from this folder.
- [ ] Accounts with two-step sign-in: Vercel (Pro), Neon, Twilio (paid, not trial), Stripe, Resend, Sentry.
- [ ] Twilio business profile for the owner's company as a software vendor (ISV) submitted; it must be approved before any groomer's texting can be submitted. [Open] Q-5: whether this needs a registered business and an EIN.
- [ ] Start recruiting 3–5 pilot groomers; at least one must agree by week 3 to be the first texting registration.
- [ ] Choose how to get terms of service, a privacy policy and text-message terms (Q-7); they must be live by week 4.
Agent tasks:
- [ ] Branch protection on `main`: pull requests only, CI must pass, owner approval required.
- [ ] CI runs format, lint, typecheck, tests, dependency audit, gitleaks and Semgrep on every pull request; pre-commit hook runs format, lint and gitleaks.
- [ ] Neon production and development projects created (ADR-0004); Vercel previews connected to the development project only.
- [ ] Production secrets only in Vercel's production environment; `.env.example` with fake values.
- [ ] Billing alerts set on Vercel, Neon, Twilio and Resend.
- [ ] Email sending domain verified (SPF, DKIM, DMARC).
- [ ] Re-check and pin exact versions (Next.js, Better Auth, Drizzle); confirm GitHub Pro's price, that Neon production can run without scaling to zero, and Backblaze B2 Object Lock pricing.
- [ ] Backup workflow to Backblaze B2 set up in a GitHub environment only `main` can use; one test run succeeds.
Verification: a trivial pull request shows every check passing and produces a preview link; a pull request containing a planted fake secret is blocked; a preview deployment shows only seed data; the owner confirms the Twilio profile is submitted.

## M1 — Walking skeleton (weeks 1–2)
Goal: the thinnest end-to-end slice through every layer, deployed to production through the real pipeline. It proves the stack early, when changing it is cheap, and gives agents a working pattern to copy.
Scope: an owner signs up and signs in → creates a business with one service and one groomer with working hours → the public booking page at `/b/<slug>` shows the service and open times → a client submits a booking request → the request appears in the owner's list → an outbox message is dispatched by the per-minute cron and the owner receives a "new booking request" email (fake provider in previews, Resend in production) → errors reach Sentry.
Acceptance criteria:
- Given a new owner in production, when they sign up and add a service and a groomer with hours, then the booking page is reachable at its link from a phone.
- Given a booking request on that page, when it is submitted, then it appears in the owner's list and the owner receives an email within 2 minutes.
- Given two businesses in the test database, when the isolation suite runs, then neither can read or change the other's business, groomer, service or appointment.
- Given a pull request, when it is opened, then CI runs every gate and a preview deployment with seed data is created.
Verification: the owner does the scenario on a phone and a laptop in production with a test business; CI is green on `main`; Sentry shows a deliberately triggered test error. AGENTS.md › Commands is filled in.
Depends on: M0

## M2 — Booking and calendar (weeks 3–6)
Scope: FR-2, FR-3, FR-4, FR-5, FR-6 including a calendar per groomer (ADR-0011), with email notices to clients (texts arrive in M3). Terms, privacy policy and text-message terms published and linked from every booking page.
Spike (about week 4, critical path): submit toll-free verification for the first pilot groomer using their production booking page as the business website; record how long approval takes and any rejection reason in ADR-0007's Evidence.
Acceptance criteria: see [requirements.md](requirements.md) FR-2 to FR-6.
Verification: Playwright journeys for booking (a named groomer and "anyone available"), accepting, declining, expiry, moving between groomers and cancelling pass on the preview; isolation tests cover every new table and endpoint; the owner runs the journeys on a phone and a tablet.
Depends on: M1

## M3 — Text reminders and texting setup (weeks 6–9)
Scope: FR-7, FR-8; outbox dispatcher with send-time checks and the pause switch (ADR-0008); Twilio adapter and inbound webhook; consent records; overdue and stuck messages reported to Sentry; the admin texting queue with two-step sign-in for the admin (first part of FR-10).
Acceptance criteria: see requirements.md FR-7 and FR-8; plus: given a duplicate cron call, when due messages are processed, then each is sent once; given a crash after sending but before recording, when the next run happens, then the message is not sent again.
Verification: end-to-end tests with the fake provider (reminder, C, X, STOP, HELP, unknown reply, sending window); in production, the owner's own phone receives a reminder from the approved pilot business and the C and X replies update the calendar.
Depends on: M2; the owner's Twilio profile approved (M0)

## M4 — Subscriptions, admin and launch readiness (weeks 9–11)
Scope: FR-1 billing (Stripe Checkout, customer portal, webhooks, pausing), FR-9, the rest of FR-10.
Launch checks (each a gate before the first paying groomer): restore drill from the independent backup, including message reconciliation; accessibility pass on the booking page (WCAG 2.2 AA); mutation testing on reminder, consent and business-scoping logic; a short load test at 10× expected traffic of the booking page, the Twilio webhook and an 8am reminder burst; review of sign-in, business separation, Stripe and Twilio webhook code by a qualified developer, paid for a few hours (owner decision 2026-10-19), with every serious finding fixed.
Acceptance criteria: see requirements.md FR-1, FR-9, FR-10.
Verification: Stripe test-mode subscription, failed payment and cancellation scenarios pass; restore drill result recorded in architecture.md; checks above recorded in state.md.
Depends on: M3

## M5 — Pilot and launch (weeks 11–13)
Scope: 3–5 pilot groomers use the app for real bookings; fix what they find; then open sign-ups by mid-January. A salon whose texting approval is still pending uses email reminders and switches to texts when approved; launch does not wait for carriers (owner decision 2026-10-19).
Acceptance criteria:
- Given the pilot groomers, when they have used the app for two weeks, then every reminder due was sent on time (health check history) and no cross-business or duplicate-text incident occurred.
- Given a new owner, when they sign up without help, then they reach a live booking page in under 20 minutes.
Verification: dispatcher and health-check history in Sentry; pilot feedback notes in `docs/project/`; the owner decides to open sign-ups.
Depends on: M4

## Later
In rough priority order: automate texting registration with Twilio's Compliance Embeddable (when sign-ups pass about two a week); repeat bookings and "time for the next groom" texts (FR-14); instant booking for returning clients (FR-12); staff sign-ins (FR-13); vaccination records (FR-15); calendar sync (FR-16); deposits and no-show fees (FR-11, new ADR and higher review tier).
