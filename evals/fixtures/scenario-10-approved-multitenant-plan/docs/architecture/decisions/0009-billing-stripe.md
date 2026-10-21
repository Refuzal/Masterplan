# ADR-0009: Subscription billing with Stripe Billing

- Status: Accepted
- Date: 2026-10-19
- Decided by: Product owner, approving the recommended architecture package on 2026-10-19.
- Confidence: High
- Change later: Moderate

## Context
Companies pay a subscription priced per building per month (FR-7); pilot companies get free months. Card details must never reach our servers. Customers are in the US and Canada, where software subscriptions can be taxable (requirements.md › Compliance obligations).

## Options considered
1. **Stripe Billing** — quantity-based subscriptions, hosted checkout, a customer portal for cards and invoices, automatic payment retries, and optional Stripe Tax / Stripe charges 0.7% of billing volume on top of card fees.
2. **A merchant of record such as Paddle** — handles sales tax collection and filing for us / higher fees (unverified) and less control over the billing experience.
3. **Manual invoices** — rejected: does not scale and makes per-building counts error-prone.

## Decision
Stripe Billing with one product, "Building", priced per month; each company's subscription quantity equals its number of active buildings and is updated when buildings are added or archived. Companies sign up through Stripe Checkout and manage cards and invoices in Stripe's customer portal. Pilot companies get a trial period. Stripe webhooks are checked for a valid signature, processed once (by event ID) in a background job, and update the company's subscription status. Stripe Tax is switched on once an accountant confirms where we must register (risks.md R-5). Only the `billing` app calls Stripe.

## Why
- The standard way to charge per unit per month, with very little code.
- No card data touches our servers, so the product stays out of most payment-card compliance work.

## Consequences
- Good: retries, receipts and card updates handled by Stripe.
- Costs and tradeoffs: 0.7% of billing volume, plus 2.9% + 30¢ per US card charge (ACH debit 0.8%, capped at $5, is an option for larger customers); Stripe Tax adds 0.5% per transaction where registered.
- Follow-up work: billing in M4; payment-failure behavior per FR-7.

## Evidence
- [Stripe Billing pricing](https://stripe.com/billing/pricing) (checked 2026-10-19) — 0.7% of billing volume, pay as you go; US cards 2.9% + 30¢; ACH Direct Debit 0.8% capped at $5.
- [Stripe Tax pricing](https://stripe.com/tax/pricing) (checked 2026-10-19) — 0.5% per transaction where registered, for Billing integrations.

## Revisit when
- Sales tax registrations in many places make a merchant of record cheaper overall.
- Larger customers need annual contracts or invoicing outside Stripe.
- The pricing model changes (for example to per unit).
