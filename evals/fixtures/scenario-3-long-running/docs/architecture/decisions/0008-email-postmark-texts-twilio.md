# ADR-0008: Email through Postmark; texts through Twilio with one verified toll-free number per company

- Status: Superseded by ADR-0010
- Date: 2026-10-19 (staff-alert number added the same day after the review panel)
- Decided by: Product owner, approving the recommended architecture package on 2026-10-19.
- Confidence: Medium
- Change later: Moderate

## Context
Renters, vendors and staff get links and updates by email or text (FR-11, FR-14; NFR-9: within 1 minute). Recipients are in the US and Canada. Carriers require a software platform to register each customer business that sends texts, not the platform itself. Canada's anti-spam law and US carrier rules require sender identification and opt-out. Texts are the fastest-growing cost (risks.md R-4).

## Options considered
Email:
1. **Postmark** — built for transactional email with strong delivery; $15 a month for 10,000 emails / not the cheapest at volume.
2. **Amazon SES** — cheapest / more setup and reputation management for the team.

Texts, provider:
1. **Twilio** — the most widely used, with a Python SDK and APIs for toll-free verification on behalf of customers / not the cheapest per message.
2. **Telnyx or Plivo** — cheaper per message / less familiar to agents and the team.

Texts, sender type:
1. **One toll-free number per company** — verification is free, takes about 3–5 business days, and covers US and Canadian recipients; $2.15 a month per number.
2. **One 10DLC local number per company** — US only; brand and campaign registration fees ($4.50–$46 per brand, $15 vetting, $1.50–$10 a month per campaign).
3. **One shared number for all companies** — not allowed: verification must name the end business.

## Decision
- Postmark's transactional stream for all email, with SPF, DKIM and DMARC set on the sending domain.
- Twilio for texts to renters and vendors, with one toll-free number per company, bought and submitted for verification through the API during company setup (FR-10). Until a company's number is approved, its renter and vendor messages go by email (FR-14).
- Texts to a company's own staff (urgent alerts to the on-call contact, staff notifications) come from one toll-free number verified for our own business, so urgent alerts work by text from a company's first day.
- Before M3, Twilio support confirms in writing that this split (customer numbers for renter and vendor messages, our number for messages to our customers' staff) meets their rules.
- Twilio's opt-out handling answers STOP and HELP; opt-outs are mirrored in our database so the app falls back to email.
- Every text names the company and contains no marketing. Each company has a daily sending cap to stop runaway jobs.
- Only the `notifications` app calls Postmark or Twilio. Delivery-status webhooks are checked for a valid signature.

## Why
- Mainstream providers with good delivery and documentation lower the risk of messages silently failing, which matters for urgent alerts (FR-11).
- Toll-free per company is the cheapest compliant route that also covers Canada.

## Consequences
- Good: compliant texting from day one; email works immediately for every company.
- Costs and tradeoffs: about $0.012 per text segment in the US including carrier fees, plus $2.15 a month per company (architecture.md › Cost). Verification can be rejected and resubmitted (risks.md R-3). Switching providers means new numbers and verification, so it is a moderate change.
- Follow-up work: our own business profile and our staff-alert number with Twilio in M0; Twilio's written confirmation before M3; verification flow in M3. Canadian per-message rates are not yet checked (M0).

## Evidence
- [Twilio US SMS pricing](https://www.twilio.com/en-us/sms/pricing/us) (checked 2026-10-19) — $0.0083 per segment; toll-free number $2.15 a month; carrier fees $0.0035–$0.005 per outbound segment.
- [Twilio toll-free best practices for the US and Canada](https://support.twilio.com/hc/en-us/articles/360038172934-Best-Practices-for-Using-Toll-Free-SMS-and-MMS-in-the-US-and-Canada) (checked 2026-10-19) — unverified numbers are blocked; verification is free and takes about 3–5 business days.
- [Twilio toll-free verification for ISVs](https://support.twilio.com/hc/en-us/articles/13263383206299-Toll-Free-Verification-for-ISVs) (checked 2026-10-19) — submissions must name the end business, not the platform.
- [Twilio A2P 10DLC fees](https://support.twilio.com/hc/en-us/articles/1260803965530) (checked 2026-10-19) — brand $4.50 or $46; vetting $15; campaign $1.50–$10 a month.
- [Postmark pricing](https://postmarkapp.com/pricing) (checked 2026-10-19) — Basic $15 a month for 10,000 emails; $1.80 per extra 1,000.

## Revisit when
- Texts pass 30% of running cost (compare cheaper providers, or send fewer texts).
- A company's verification is rejected twice.
- Two-way texting (replies that reach staff) becomes a requirement.
