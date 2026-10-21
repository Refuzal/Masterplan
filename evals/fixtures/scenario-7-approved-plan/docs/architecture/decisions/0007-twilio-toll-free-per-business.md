# ADR-0007: Text messages through Twilio, one registered toll-free number per business

- Status: Accepted
- Date: 2026-10-19
- Decided by: Owner (approved the architecture package on 2026-10-19)
- Confidence: Medium (registration acceptance and timing until the M2 spike)
- Change later: Moderate

## Context
Text reminders are the core of the product (FR-7). US carriers deliver application texts only from registered senders, and a platform texting for its customers must register each customer with that customer's own details (requirements.md › Compliance obligations). Many groomers are sole proprietors without an EIN or a website. About 50 businesses join in year one, roughly one a week (NFR-7). A busy salon sends and receives about 600 texts a month [Assumption, A-3].

## Options considered
1. **Twilio, toll-free number per business with toll-free verification** — no registration or campaign fees; sole proprietors supported without a registration number; console, API or Twilio's embeddable onboarding form for software vendors; $2.15 per number per month; $0.0083 per text segment plus carrier fees / an 8xx number looks less local; carrier approval typically takes 1–3 weeks.
2. **Twilio, local number per business with A2P 10DLC registration** — familiar local area code / one-time brand and vetting fees ($4.50 + $15 or more), monthly campaign fees ($1.50–$10), sole proprietors must confirm a code on their personal mobile within 30 days; campaign vetting adds delay.
3. **Telnyx, toll-free per business** — cheaper texts ($0.0055 per toll-free segment plus carrier fees) / less documentation and fewer examples for AI tools; no equivalent we verified of Twilio's embeddable onboarding form.
4. **One shared platform number for all businesses** — simplest / contrary to the registration rules for platforms, and one STOP would silence every business for that client. Rejected.

## Decision
Twilio, with a separate toll-free number for each business, verified with that business's details. All texting code sits behind one `TextMessenger` interface with a fake implementation for local, preview and test environments, so no real text is ever sent outside production.

Texting setup at launch: the app collects the business details (FR-8) and shows the status; the platform admin submits the verification in Twilio's console and links the approved number to the business in the admin page. Automation through Twilio's Compliance Embeddable follows when sign-ups pass about two a week (roadmap › Later).

Messages are kept short by one message-builder module with tests: plain characters only (no emoji or curly quotes); each business sets a short texting name of at most 25 characters; dog names are shortened to 15 characters; every text fits one segment (160 characters) except the first text to a client, which carries the STOP and HELP line and may use two. The builder's tests cover the longest allowed names.

Opt-outs: our consent record for the business and phone number is authoritative and checked at send time; STOP from a number that is not yet a client is still recorded; a provider error saying the recipient has opted out is recorded as an opt-out. Twilio's own opt-out blocking is a second safety layer, not the source of truth.

A business's toll-free number is bought only when its registration is submitted.

## Why
- Per-business registration is required; toll-free verification is the cheapest and simplest path for sole proprietors and needs no per-business campaign fees.
- Per-business numbers keep opt-outs, costs and reputation separate between businesses.
- Twilio's documentation, its ISV guidance and its familiarity to AI tools reduce build risk; the price difference to Telnyx (about $1.70 per salon per month) does not outweigh that at 50 salons.
- Manual submission at launch avoids building a registration integration before it pays off.

## Consequences
- Good: compliant from day one; one provider; cheap fixed cost per business.
- Costs and tradeoffs: about $10 per salon per month in texts and number fees at the assumed volume; each new business waits for carrier approval, covered by email reminders (FR-8); about 20–30 minutes of the owner's time per new business at launch [Assumption].
- Follow-up work: the owner's Twilio account (paid, not trial) and its business profile as a software vendor are set up in M0, because they must be approved before any customer can be submitted; the first pilot groomer's verification is submitted in M2 (about week 4) as a spike that proves the booking page is accepted as the business's website.

## Evidence
- Twilio US SMS pricing: $0.0083 per segment (long code and toll-free); toll-free number $2.15/month; carrier fees $0.0035–$0.005 per segment — https://www.twilio.com/en-us/sms/pricing/us (checked 2026-10-19)
- Twilio toll-free verification: "Twilio reviews TFV requests within three business days"; registration number not required for SOLE_PROPRIETOR — https://www.twilio.com/docs/messaging/compliance/toll-free/api-onboarding (checked 2026-10-19)
- Twilio toll-free verification for ISVs: "the expectation is to identify and register the number for your customer" — https://support.twilio.com/hc/en-us/articles/13263383206299-Toll-Free-Verification-for-ISVs (checked 2026-10-19)
- Typical approval time 5–15 business days, up to 3–4 weeks at busy times; no separate Twilio fee for verification (third-party estimate, 2026-06-20) — https://www.telphiconsulting.com/blog/twilio-toll-free-verification-cost (checked 2026-10-19)
- A2P 10DLC fees: brand $4.50 (sole proprietor and low-volume standard), $46 standard; campaign vetting $15; monthly campaign $1.50–$10 — https://support.twilio.com/hc/en-us/articles/1260803965530 (checked 2026-10-19)
- Sole proprietor 10DLC rules: one campaign, one number, OTP within 30 days — https://twilio.com/docs/sms/a2p-10dlc/isv-starter-api (checked 2026-10-19)
- Compliance Embeddable: requires prior access approval and an approved ISV primary profile — https://www.twilio.com/docs/messaging/compliance/toll-free/compliance-embeddable-onboarding (checked 2026-10-19)
- Telnyx messaging pricing: toll-free $0.0055 per part plus carrier fees — https://telnyx.com/pricing/messaging (checked 2026-10-19)

## Revisit when
- Any business's verification is rejected twice, or approvals routinely take longer than 3 weeks.
- Groomers ask for texts from a local number, or from their existing business number.
- The monthly text bill passes $500, or the product passes 100 businesses (compare Telnyx again).
- Sign-ups exceed about two a week (automate registration).
