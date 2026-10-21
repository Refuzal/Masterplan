# Risks, assumptions and open questions

> Purpose: everything uncertain, in one place. Update whenever a risk, assumption or question appears or is resolved; delete resolved rows once the answer is recorded in its home document. Owner: lead engineer (currently the planning agent; the founder approves).

## Open questions
| ID | Question | Status | Needed by | Who answers |
|---|---|---|---|---|
| Q-4 | Subscription price (per salon or per groomer), free-trial length (texting approval can take 1–3 weeks of it), and how many texts a month the price includes | [Open] | M4 | Owner |
| Q-5 | Does the owner's Twilio software-vendor profile need a registered business and an EIN? If so, getting an EIN is the first M0 task (the IRS issues them free online [Assumption: general knowledge, check irs.gov]) | [Open] | M0 | Owner, with Twilio support |
| Q-6 | Must the subscription charge sales tax in the owner's state? | [Open] | M4 | Owner, with an accountant |
| Q-7 | Terms of service, privacy policy and text-message terms: template service or lawyer? They must be live before the first texting registration | [Open] | M2 (week 4) | Owner |

## Assumptions
| ID | Assumption | Based on | How and when we check |
|---|---|---|---|
| A-1 | [Assumption] No AI features inside the product in version 1 (AI tools are used only to build it). | Product description | Owner may raise it at any time |
| A-3 | [Assumption] A salon with about 200 regular clients sends and receives about 600 text segments a month (about 145 appointments; confirmation, reminder, the client's reply and its acknowledgement). | Owner's year-one goal; typical 4–8 week grooming cycle | Measure per business during the M5 pilot |
| A-6 | [Assumption] Submitting one business's texting registration by hand takes the owner about 20–30 minutes. | Twilio console steps (ADR-0007) | Time the first three in M3 and M5 |
| A-7 | [Assumption] Carriers accept a business's booking page as its website for verification. | Twilio requires a working website related to the business name, with privacy policy and terms | M2 spike with the first pilot groomer (about week 4) |

## Risks
| ID | Risk | Likelihood | Impact | Mitigation | Trigger to act |
|---|---|---|---|---|---|
| R-1 | Established products already sell online booking and reminders from $29/month, so groomers may not switch | High | High | Stay simpler and cheaper for independent groomers and small salons; put the product in front of real groomers early (M5 pilot) | Fewer trial groomers convert than the year-one goal needs |
| R-2 | A sellable version in about 3 months, built by a non-programmer with AI tools, is tight, and per-groomer calendars add about a week | Medium | High | Lean scope; walking skeleton first; automated checks catch AI mistakes; texting approvals started early | M1 not in production by the end of week 3 |
| R-3 | Carriers must approve each business before the app can text its clients; approval typically takes 1–3 weeks (up to 4) and can be rejected | High | High | Owner's Twilio profile in M0; first pilot registration in M2 (about week 4); email reminders until approval, and launch goes ahead on email if approvals are pending (owner decision 2026-10-19); status visible to owner and admin; booking page doubles as the website with privacy policy, terms and the opt-in | Any approval takes longer than 3 weeks, or any rejection |
| R-4 | Texts (about $10 per salon per month) eat into a low subscription price | Medium | Medium | Price covers about $13–14 of running cost per salon (Q-4); messages kept to one segment; per-business caps and usage tracking | Text cost above 30% of a business's subscription |
| R-5 | AI-written code contains security flaws (Veracode's 2026 tests found AI-generated code passing security checks only about 56% of the time; [source](https://www.veracode.com/news/llms-are-getting-smarter-but-not-safer-veracode-2026-genai-code-security-report-finds-ai-generated-code-security-has-stalled-at-56%25-pass-rate/), cited by the planning method) | High | High | CI gates (types, tests, isolation tests, Semgrep, secret scanning); owner approves every merge after trying the preview; a paid review of sign-in, isolation and webhooks by a qualified developer is a launch gate (owner decision 2026-10-19) | A security-relevant bug reaches production |
| R-6 | Real client data reaches previews, local machines or agents | Low | High | Separate Neon development project with seed data only; production secrets only in Vercel production (ADR-0004) | Any real record seen outside production |
| R-7 | Reminders silently stop (cron, provider or code failure) and no-shows rise | Medium | High | Health check fails on overdue or stuck messages; Sentry uptime and cron monitors alert the owner | Any alert; any groomer report of a missing reminder |
| R-8 | The owner is the only person who can fix production problems, and is not a programmer | High | Medium | Managed services only; phone push alerts; runbook with first steps (architecture.md › Operations); one-click rollback | An incident lasting more than 4 hours |
| R-9 | A database restore makes already-sent messages look unsent, and clients get duplicate texts | Low | High | Dispatcher pause switch and reconciliation steps (ADR-0008, runbook); practised in the restore drill | Any restore |

## Accepted risks
| ID | Risk accepted | Accepted by | Date | Reason |
|---|---|---|---|---|
| — | None yet | — | — | — |
