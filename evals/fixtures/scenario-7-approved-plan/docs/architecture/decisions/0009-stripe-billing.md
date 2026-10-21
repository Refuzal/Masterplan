# ADR-0009: Groomer subscriptions through Stripe Billing and Stripe-hosted pages

- Status: Accepted
- Date: 2026-10-19
- Decided by: Owner (approved the architecture package on 2026-10-19)
- Confidence: High
- Change later: Moderate

## Context
Groomers pay a monthly subscription with a free trial (FR-1). Clients pay nothing through the app in version 1. Storing or handling card numbers is out of the question for a solo founder. The price and trial length are not decided yet (risks.md Q-4) and must be changeable without code.

## Options considered
1. **Stripe Billing with Stripe Checkout and the Stripe customer portal** — hosted payment and card-update pages; trials, retries of failed payments and receipts built in; 2.9% + 30¢ per card payment plus 0.7% of billing volume / sales tax is not handled unless Stripe Tax is added (0.5% per transaction where registered).
2. **A merchant of record (for example Paddle)** — also handles sales tax in every state / higher fees per payment; less control over the customer relationship.

## Decision
Stripe Billing. The app creates a Checkout session for the subscription and links to the customer portal for card changes and cancellation; it never sees card numbers. Stripe webhooks (signature-checked) update the business's subscription status, which drives pausing (FR-1). Prices and the trial length live in Stripe, not in code. Stripe test mode is used everywhere except production.

## Why
- The most widely used and documented subscription system; agents know it well.
- Hosted pages keep card data entirely outside the app.
- A merchant of record lost on cost at this size; revisit if sales tax becomes a burden.

## Consequences
- Good: no card data; failed payments, receipts and cancellations handled by Stripe.
- Costs and tradeoffs: about $1.34 per $29 payment (4.6%); whether to charge sales tax is an open question for the owner and an accountant (Q-6).
- Follow-up work: billing in M4; webhook handling tested with Stripe's test events.

## Evidence
- Stripe pricing: 2.9% + 30¢ per successful domestic card transaction; Billing pay-as-you-go 0.7% of billing volume; Stripe Tax 0.5% per transaction where registered — https://stripe.com/pricing (checked 2026-10-19)

## Revisit when
- Sales-tax registration is needed in several states.
- Groomers ask to pay by bank transfer or annual invoice.
- Client payments (deposits, no-show fees, FR-11) are scheduled, which needs Stripe Connect and a new ADR.
