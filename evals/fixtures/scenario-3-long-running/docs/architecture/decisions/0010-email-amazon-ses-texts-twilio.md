# ADR-0010: Email through Amazon SES; texts through Twilio (unchanged)

- Status: Accepted
- Date: 2026-12-04
- Decided by: Product owner and Ravi, 2026-12-04
- Confidence: High
- Change later: Moderate
- Supersedes: ADR-0008

## Context
During M2, Postmark's account review asked us to remove tracking from renter links and limited the account to 100 emails a day until a manual review in January, which would block pilot onboarding (roadmap M3). Email volume at 200 companies is projected at 60,000–90,000 a month (architecture.md › Cost). The texting part of ADR-0008 worked as planned and is unchanged.

## Options considered
1. **Stay on Postmark and wait for review** — no code change / blocks M3 testing and the pilot timeline.
2. **Amazon SES** — about $0.10 per 1,000 emails, production access granted in 2 days / we manage bounces and reputation ourselves.
3. **Resend** — simple API / another young vendor holding renter email addresses.

## Decision
Amazon SES (us-east-2) for all email, sent only from the `notifications` app through the `messages` queue, with SPF, DKIM and DMARC on the sending domain and SNS bounce and complaint handling. Twilio stays exactly as ADR-0008 described: one verified toll-free number per company for renter and vendor texts, and our own verified number for staff alerts. Before FR-14 texts go to pilot companies, Twilio support confirms in writing that this split (customer numbers for renter and vendor messages, our number for messages to our customers' staff) meets their rules (requested 2026-12-10).

## Why
- Unblocks M3 and the pilot without waiting on a vendor review.
- Cheapest at our projected volume.
- The `notifications` app already isolated the provider, so the switch touched one module.

## Consequences
- Good: lower email cost; no daily cap.
- Costs and tradeoffs: we watch bounce and complaint rates ourselves (alert at 2% bounces, 0.1% complaints); one more AWS account to secure.
- Follow-up work: SES bounce webhook (done), sender reputation dashboard in Better Stack (done).

## Evidence
- Amazon SES pricing page (checked 2026-12-03) — $0.10 per 1,000 emails.
- Postmark account review email, 2026-12-01 (kept by the product owner).

## Revisit when
- Bounce or complaint rates cross the alert thresholds twice in a month.
- Email volume passes 500,000 a month.
