# Risks, assumptions and open questions

> Purpose: everything uncertain, in one place. Update whenever a risk, assumption or question appears or is resolved; delete resolved rows once the answer is recorded in its home document; IDs are never reused, so gaps mean resolved items. Owner: Ravi (backend co-founder, lead engineer).

## Open questions
| ID | Question | Status | Needed by | Who answers |
|---|---|---|---|---|
| Q-6 | How should price track cost? A single-family home billed as one building costs the same as a 300-unit building, while texts (the main running cost) grow with units and requests (review panel, 2026-10-19). | [Open] | M4 (billing, FR-7) | Product owner |

## Assumptions
| ID | Assumption | Based on | How and when we check |
|---|---|---|---|
| A-1 | [Assumption] Staff and vendors use the same phone-friendly website as renters; no app-store apps in version 1 | Owner confirmed a website is fine for renters; vendors use links | Pilot feedback |
| A-2 | [Assumption] AI coding agents write much of the code, reviewed by Ravi | Two-person team, 4–5 month timeline | Confirmed with the architecture package |
| A-3 | [Assumption] A typical pilot company manages roughly 100–500 units; about 200 companies use the product a year after launch | Owner: pilot companies are mostly smaller ones on spreadsheets and email; 20 in the pilot, thousands eventually | Measured at pilot onboarding; revisit at 6 months |
| A-4 | [Assumption] A renter who loses their renter link gets a new one by entering their phone number or email; the old link stops working | Renter links have no password (approved 2026-10-19), so renters need a way back in | Pilot feedback |
| A-5 | [Assumption] No AI features inside the product in version 1 | Not in the approved version 1 list; positioning is simplicity | Revisit after the pilot |
| A-7 | [Assumption] The pilot lasts about three months from go-live, and adoption is measured as in overview.md › Goals | Owner chose adoption and revenue as the success measures; the thresholds are proposed defaults | Agree thresholds with pilot companies at signup |
| A-8 | [Assumption] Vendors see the renter's first name and phone number to arrange access (FR-4) | Common practice; vendors must reach renters | Pilot feedback; make it a company setting if companies object |
| A-9 | [Assumption] Each staff member belongs to one company in version 1 (the data model allows more) | Small companies; no shared staff mentioned | Pilot feedback |

## Risks
| ID | Risk | Likelihood | Impact | Mitigation | Trigger to act |
|---|---|---|---|---|---|
| R-1 | Established products already cover this workflow, so pilot companies may see no reason to switch. Property Meld does maintenance coordination and connects to AppFolio, Buildium, Rent Manager, Propertyware, Yardi and Rentvine ([FAQ](https://propertymeld.com/frequently-asked-questions), checked 2026-10-19); AppFolio and Buildium include maintenance requests and vendor work orders ([AppFolio](https://www.appfolio.com/property-manager/maintenance), [Buildium](https://www.buildium.com/features/resident-center/), checked 2026-10-19) | Med | High | Compete on focus and simplicity: maintenance only, no vendor accounts, renters use a link (overview.md); first target smaller companies without such software; the pilot measures adoption | Pilot companies keep using their old tool or phone calls |
| R-2 | The Buildium sync (FR-8) may reach few companies: Buildium's Open API is included only in its Premium plan, from $400/month ([pricing](https://www.buildium.com/pricing/), checked 2026-10-19) | Med | Low | Spreadsheet upload works for every company; check pilot companies' Buildium plans before building FR-8 | Planning FR-8 |
| R-3 | Each company's renter and vendor texts need a verified sender number: about 3–5 business days, and requests can be rejected. Unverified numbers are blocked | High | Med | Start verification at company signup; renter and vendor messages go by email until approved; urgent staff alerts use our own number, so they are unaffected; Twilio confirms the setup in writing before M3 | A company waits more than 10 business days |
| R-4 | Text messages are the running cost that grows fastest: about $0.012 per text segment plus $2.15 a month per company number (US prices, [Twilio](https://www.twilio.com/en-us/sms/pricing/us), checked 2026-10-19); the launch estimate ($410–560) tops the $500 budget only if texting is heavy | High | Med | Per-company daily caps; track texts per company; use email where texts add little; settle Q-6 before billing | Texts exceed 30% of the running cost |
| R-5 | Legal and tax groundwork (customer contract with data processing terms, privacy notice, sales tax registration) is not done by the pilot | Med | High | Lawyer and accountant engaged in M0; templates for software companies keep it affordable | First pilot contract ready to sign |
| R-6 | A maintenance emergency (such as a water leak) during an outage harms a renter or a building | Low | High | Emergencies never depend on the app: the emergency line is shown on every renter page and message (FR-11); urgent requests alert the on-call contact | Any outage longer than 15 minutes |
| R-7 | A Canadian customer requires its data to be stored in Canada; Render has no Canadian region (ADR-0006) | Low | Med | US storage is allowed with notice and contract terms (requirements.md › Compliance obligations); the app is a standard container and standard PostgreSQL, so a move takes about 1–2 weeks | A prospect makes Canadian hosting a condition |
| R-8 | A regional Render outage takes the product down for hours (a 2 h 14 min critical outage hit Render's Oregon region on 2026-07-24) | Med | Med | Ohio region; emergency line on every renter page (R-6); public status page; managed failover for the database | NFR-2 missed in any month |
| R-9 | AI agents know Procrastinate and row-level security patterns less well than mainstream defaults, so they write subtly wrong job or tenancy code | Med | High | M1 builds the reference pattern for both; isolation and schema tests in CI; Ravi reviews the guarded modules (standards.md › AI-agent guardrails) | An isolation test or a review catches a tenancy mistake twice |
| R-10 | Ravi has not yet confirmed the stack personally; if his Python experience is mainly in another framework, Django costs some ramp-up | Low | Med | Ravi confirms ADR-0001 to ADR-0009 in M0; a change goes through `/masterplan change` | Ravi raises an objection in M0 |
| R-11 | The milestones fill 18 of the roughly 18–21 weeks before the pilot, and the lawyer, accountant and Twilio approvals can slip | Med | High | Start outside approvals in M0; two buffer weeks; if late, keep the pilot date and cut in this order (approved by the product owner 2026-10-19): passkeys, Excel uploads (CSV stays), self-serve company sign-up (founders set up pilot companies) | M2 not done by week 10 |

## Accepted risks
| ID | Risk accepted | Accepted by | Date | Reason |
|---|---|---|---|---|
| — | None yet | — | — | — |
