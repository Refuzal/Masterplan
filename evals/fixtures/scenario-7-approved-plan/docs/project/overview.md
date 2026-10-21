# Dog Groomer Booking App — Overview

> Purpose: what we are building, for whom, and why. Update when goals, users or scope change. Owner: the founder (product owner).
> Untagged statements are confirmed. Tags mark everything else: [Assumption] [Proposed] [Open] [Blocking].

Working name: "Dog Groomer Booking App" [Assumption]. The product name is not decided; renaming is a text change.

## Problem
Independent dog groomers lose money when clients miss appointments (no-shows), and taking bookings by phone or text eats into grooming time. This product lets a groomer's clients book appointments online and sends them automatic text reminders, so fewer appointments are missed. It is sold to groomers as a monthly subscription.

**Why groomers will choose it:** simpler and cheaper than existing groomer software. It is made for independent groomers and small salons with one or two groomers, and does a few things very well: online booking, text reminders, and client and pet records. Text reminders matter most, because clients ignore email.

## Users and roles
| Role | Who they are | What they need to do |
|---|---|---|
| Owner | Runs an independent grooming business (a solo groomer or a salon with one or two groomers), signs in and pays the subscription. Works on a laptop or tablet at the salon. | Set up services, groomers and hours, accept bookings, manage every groomer's calendar, keep client and pet records |
| Groomer | A person who grooms dogs at the business. Has a calendar and working hours; does not sign in in version 1 ([ADR-0011](../architecture/decisions/0011-groomer-calendars-one-sign-in.md)) | Appear on the booking page; be booked |
| Client | A pet owner who is a business's customer. Uses a phone. | Book an appointment online, receive text reminders, confirm or cancel by replying |
| Platform admin | The founder, running the product | Help groomers, check subscriptions and texting approval [Assumption] |

## Goals and success criteria
- About 50 paying salons within the first year after launch (launch target mid-January 2027), each with about 200 regular clients. Most salons have one or two groomers, and each groomer has a calendar in version 1.
- A version groomers can buy by mid-January 2027. If a salon's texting approval is still pending at launch, it starts on email reminders and switches to texts when approved; launch does not wait for carriers.
- Groomers can see the app working: a monthly count of text confirmations and no-shows for their business (FR-9).

## Scope
Confirmed by the owner on 2026-10-19. Details and acceptance criteria: [requirements.md](requirements.md).

**Version 1 (Must):**
1. Groomer sign-up with a free trial, then a monthly subscription paid by card through a payment provider (FR-1).
2. Business setup: services with typical length and price, and each groomer with their own working hours (FR-2).
3. Booking page, designed for phones, that doubles as the business's simple website (texting approval requires one, with a privacy policy and terms): the client picks a service, a groomer or "anyone available" and an open time, enters their own and their dog's details, and may agree to text reminders (FR-3).
4. Booking requests: the owner accepts or declines each online booking (dog size and coat change how long a groom takes); the client is told either way (FR-4).
5. Calendar: a calendar per groomer, shown side by side; day and week views; add, move or cancel appointments, including bookings taken by phone; block time off (FR-5).
6. Client and pet records: contact details; dogs with breed, size and notes such as temperament; past and upcoming visits (FR-6).
7. Text reminders: an automatic reminder before each appointment with "reply C to confirm or X to cancel"; replies update the calendar; STOP always works (FR-7).
8. Texting setup: each business completes a short form so carriers approve its texts; reminders go by email until approval (FR-8).
9. No-show tracking: the owner marks no-shows and sees a simple monthly count (FR-9).
10. A simple admin page for the founder: businesses, subscription status, texting approval and text usage (FR-10).

**Later (Should / Could):** deposits, cards on file and no-show fees; instant booking for returning clients; separate sign-ins for staff groomers; repeat bookings ("every 6 weeks") and "time for the next groom" texts; vaccination record uploads; two-way chat and marketing texts; Google or Apple calendar sync (FR-11 to FR-17).

**Non-goals:** App Store or Google Play apps (see [ADR-0001](../architecture/decisions/0001-web-app-no-app-store.md)); taking client payments of any kind in version 1; payments at the salon, tips, payroll or inventory; mobile (van) grooming routes; boarding and daycare; a marketplace where pet owners find groomers; AI features inside the app; countries outside the US.

## Constraints
- Budget: the owner prefers the cheaper and faster option wherever it does not hurt the product. Approved running cost: about $50 a month before groomers join and about $670 a month at 50 salons (updated after review), mostly texts ([architecture.md › Cost](../architecture/architecture.md#cost)).
- Lifespan: a long-term subscription business [Assumption].
- Timeline: a first version groomers can buy in about 3 months (target: mid-January 2027).
- Team: the founder, who is not a programmer, building with AI coding tools for 20 or more hours a week. A coding agent working in this repository, such as Claude Code, rather than a hosted app builder.
- Platforms: a web app. Clients book from their phones' web browsers; owners use a laptop or tablet. No App Store or Google Play apps in version 1 ([ADR-0001](../architecture/decisions/0001-web-app-no-app-store.md)).
- Market: groomers in the United States first.
- Payments: owners pay the subscription through a payment provider. Clients pay nothing through the app in version 1, so the app never handles client payments.
- Data and compliance: contact details of owners and their clients, groomers' names, and pet details. US carrier registration and consent rules apply to text reminders (see [requirements.md › Compliance obligations](requirements.md#compliance-obligations)).

## Market context
Groomers can already buy booking software with online booking and reminders, for example DaySmart Pet (from $29/month with 500 texts a month and online deposits; [pricing](https://www.daysmart.com/pet/pricing/)) and MoeGo ($49/month for mobile groomers, $79/month for salons; [Capterra](https://www.capterra.com/p/165732/MoeGo/pricing/)). Both checked 2026-10-19.

## Glossary
Use these terms, exactly, in docs, code, database names and UI.

| Term | Meaning |
|---|---|
| Owner | The person who runs a business, signs in and pays the subscription; usually also a groomer |
| Groomer | A person who grooms dogs at a business; has a calendar and working hours |
| Business | An independent grooming business ("salon"): the account that owns its groomers, services, hours, clients, pets and appointments. Each business's data is private to it |
| Client | A pet owner who is a customer of a business and books appointments |
| Pet | A client's dog, with name, breed, size and notes |
| Service | Something a business offers, with a typical length and a price (for example full groom, bath and brush, nail trim) |
| Booking page | A business's public web page where its clients book |
| Booking request | An online booking waiting for the owner to accept or decline |
| Appointment | A service booked for a pet with a groomer at a set time, once accepted |
| Reminder | An automatic text (or email, before texting is approved) sent to a client before an appointment |
| Texting setup | The carrier registration each business completes before the app can text its clients |
| No-show | A client who misses an appointment without cancelling |
| Subscription | The monthly plan an owner pays for the product, per business |
