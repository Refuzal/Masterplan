# Requirements

> Purpose: what the system must do and how well. Update when scope, targets or obligations change. Owner: the founder (product owner); engineers keep IDs stable.
> Priority: Must (version 1) · Should · Could · Won't (now). Untagged = confirmed; [Assumption] [Proposed] [Open] [Blocking] mark the rest.

Terms follow the glossary in [overview.md](overview.md#glossary). Version 1 scope was confirmed by the owner on 2026-10-19, including a calendar for each groomer ([ADR-0011](../architecture/decisions/0011-groomer-calendars-one-sign-in.md)). In version 1 only the owner of a business signs in; groomers are calendars the owner manages.

## Functional requirements

### FR-1 Owner sign-up and subscription — Must
An owner can create an account for their business, try the product free, then pay a monthly subscription by card through the payment provider's hosted pages.
Acceptance criteria:
- Given a new owner, when they sign up, then a business is created for them and its free trial starts.
- Given a business in its trial, when the owner subscribes on the payment provider's hosted checkout, then the subscription becomes active and the app never receives or stores the card number.
- Given an active business, when the owner opens billing settings, then they can update the card or cancel on the provider's hosted billing page.
- Given a business whose trial ended unpaid or whose payment failed after the provider's retries, when that happens, then the business is paused: the booking page stops taking requests, no reminders are sent, and the owner can still sign in, see the data and pay. [Assumption]

### FR-2 Business setup — Must
The owner sets up the business: name, address, phone, time zone, services (name, typical length, price), the groomers who work there (each with their own working hours), and how far ahead and how late clients may book.
Acceptance criteria:
- Given an owner finishing sign-up, when they add at least one service and at least one groomer with working hours, then the booking page goes live at its own link.
- Given a service with a typical length of 90 minutes, when a client looks for open times, then only start times when some groomer has 90 free minutes inside their working hours are offered.
- Given a business with two groomers, when both are free at 10:00, then 10:00 is offered and two clients can each book it, one with each groomer.

### FR-3 Booking page — Must
A client can request an appointment from a phone without creating an account. The booking page doubles as the business's simple website.
Acceptance criteria:
- Given a client on a phone, when they choose a service, a groomer or "anyone available", and an open time, and enter their name, mobile number and their dog's name, breed and size, then a booking request is created and they see that it was sent.
- Given "anyone available", when the request is created, then it is assigned to the first free groomer in the order the owner set. [Assumption]
- Given the text-consent box, when the client ticks it, then the consent wording, time and page are stored with the client; when they leave it unticked, then the request is still accepted and that client is never texted.
- Given anyone who opens a booking page, when it loads, then it shows the business name and contact details, its services and groomers, the text-consent wording, and links to the terms and privacy policy.
- Given a mobile number that matches an existing client of that business, when a request arrives, then it is linked to that client for the owner to review; the booking page never shows any stored client or pet details and responds the same way whether or not the number was known.

### FR-4 Booking requests — Must
The owner accepts or declines each online booking request.
Acceptance criteria:
- Given a new booking request, when it arrives, then the owner is notified by email and it shows as pending on that groomer's calendar.
- Given a pending request, when the owner accepts it (optionally moving it to another groomer), then it becomes an appointment and the client receives a confirmation.
- Given a pending request, when the owner declines it, then the client is told and the time is freed.
- Given a request not answered within 48 hours or before its start time, whichever is sooner, when that time passes, then it expires and the client is told. [Assumption]

### FR-5 Calendar — Must
The owner sees and manages every groomer's appointments in day and week views, on a laptop or tablet.
Acceptance criteria:
- Given the owner opens the calendar, when it loads, then appointments and pending requests appear in the business's time zone, side by side per groomer in the day view, and the week view can show one groomer or all.
- Given a phone booking, when the owner adds an appointment for a client, dog and groomer, then it appears on that groomer's calendar and gets reminders like an online booking.
- Given an appointment, when the owner moves it (to another time or groomer) or cancels it, then the client is told and the reminder is rescheduled or cancelled.
- Given a new appointment that overlaps another for the same groomer, when the owner saves it, then they are warned and may still save it.
- Given time off blocked for a groomer (a break, a holiday), when clients look for open times, then no time inside the block is offered for that groomer.

### FR-6 Client and pet records — Must
The owner keeps records of clients and their dogs.
Acceptance criteria:
- Given a client, when the owner opens the record, then it shows contact details, text-consent status, their dogs (name, breed, size, notes such as temperament) and past and upcoming appointments with their groomers.
- Given an owner of one business, when they search or open any record, then they can only ever reach their own business's clients, pets, groomers and appointments.

### FR-7 Text reminders — Must
Clients who agreed to texts get an automatic reminder before each appointment and can confirm or cancel by replying.
Acceptance criteria:
- Given an appointment for a client who agreed to texts, when the reminder time arrives (24 hours before by default; the owner can change it), then the client receives one text naming the business, the dog and the time, with "Reply C to confirm or X to cancel".
- Given a reminder, when the client replies C, then the appointment shows as confirmed; when they reply X, then it is cancelled, the time is freed and the owner is notified.
- Given any number, client or not, when it replies STOP or another clear opt-out, then that business never texts that number again unless it opts back in, the opt-out is recorded, and one confirmation text is sent. An opt-out reported by the text provider is recorded the same way.
- Given the first text a business sends to a client, when it is built, then it names the business and adds "Reply STOP to opt out, HELP for help" (this text may use two segments; all others fit one); a HELP reply gets the business's name and phone number.
- Given any other reply, when it arrives, then it is shown as plain text on the client's record and emailed to the owner as plain text.
- Given a reminder that falls before 8am or after 8pm in the business's time zone, when it is due, then it is sent at the next allowed time. [Assumption]
- Given a restart, retry or duplicate job, when reminders are processed, then no client ever receives the same reminder twice.

### FR-8 Texting setup — Must
Each business completes a carrier registration before the app texts its clients.
Acceptance criteria:
- Given a new owner, when they complete the texting setup form (business details, EIN if they have one, contact person), then the details are saved, the platform admin sees the business in the texting queue, and the status (waiting to submit, pending, approved, rejected) is shown to the owner and the admin. At launch the admin submits the registration by hand in the text provider's console (ADR-0007).
- Given the form, when an owner has no EIN, then they can still complete it as a sole proprietor, and the form never asks for a Social Security number.
- Given a business whose texting is not approved, when a reminder or confirmation is due, then it goes by email if the client gave one, and the owner can see which clients will get nothing.
- Given a rejected registration, when the owner views the status, then they see the reason and can correct and resubmit.

### FR-9 No-show tracking — Must
Acceptance criteria:
- Given a past appointment, when the owner marks it as a no-show, then it counts toward that month's no-shows.
- Given any month, when the owner opens the summary, then they see appointments, text confirmations, cancellations and no-shows for that month, for the business and per groomer.

### FR-10 Platform admin page — Must
Acceptance criteria:
- Given the founder signed in as platform admin, when they open the admin page, then they see each business's subscription status, texting setup status and texts sent this month, but no client or pet details.
- Given any user who is not a platform admin, when they request any admin page or action, then the server refuses it.

### Later (no acceptance criteria until scheduled)
- FR-11 Deposits, cards on file and no-show fees — Won't (now)
- FR-12 Instant booking for returning clients — Should
- FR-13 Separate sign-ins and permissions for staff groomers — Should
- FR-14 Repeat bookings and "time for the next groom" texts — Should
- FR-15 Vaccination record uploads — Could
- FR-16 Google or Apple calendar sync — Could
- FR-17 Two-way chat and marketing texts — Won't (now)

## Non-functional requirements
Each target must be measurable and checked somewhere.

| ID | Quality | Target | How we check |
|---|---|---|---|
| NFR-1 | Platforms | Clients can book from a phone's web browser; owners can work from a laptop or tablet browser. No app-store apps in version 1. | Manual check on current iPhone, Android, iPad and laptop browsers before each release |
| NFR-2 | Performance | The booking page is usable within 2 seconds on a typical 4G phone for 95% of visits; owner screens respond within 1 second for 95% of actions | Page-speed check in CI on the booking page; hosting analytics |
| NFR-3 | Availability | Target 99.5% per month (about 3.6 hours of downtime); the hosting plans carry no uptime guarantee | Sentry uptime monitor on `/api/health` |
| NFR-4 | Data loss and recovery | Lose at most a few minutes of data (restore to any moment in the last 7 days); restore within 4 hours; an independent daily backup kept 30 days | Restore drill before launch and each quarter |
| NFR-5 | Security and privacy | Every request is authorized on the server; a business can never read or change another business's data | Cross-business isolation tests in CI |
| NFR-6 | Accessibility | WCAG 2.2 AA on the booking page; owner screens usable by keyboard and readable | Automated accessibility checks in CI plus a manual pass before launch |
| NFR-7 | Scale horizon | Year one: about 50 businesses with about 200 regular clients each (about 10,000 clients, about 7,000 appointments and 30,000 text segments a month). Design for 500 businesses without re-architecture | Load test of the booking page at 10× expected traffic before launch |
| NFR-8 | Running cost | About $50 a month before any business joins; about $670 a month at 50 businesses, mostly texts (see architecture.md › Cost) | Billing alerts on every paid service; monthly review |
| NFR-9 | Message reliability | Reminders go out within 15 minutes of their scheduled time, never twice; opt-outs take effect immediately | Automated dispatcher tests; the dispatcher reports overdue and stuck messages to Sentry |

## Data
| Data | Sensitivity | Kept for | Notes |
|---|---|---|---|
| Owner account, business and groomer details | Personal | While the account is active, plus 30 days after cancellation [Assumption] | Then deleted |
| Client names, mobile numbers, optional emails | Personal | As long as the business keeps them, plus 30 days after the business cancels [Assumption] | The owner can delete a client |
| Text consent and opt-out records (wording agreed to, when, where) | Personal; compliance evidence | 5 years [Assumption: covers the four-year limitation period generally applied to TCPA claims; verify in M4] | Kept even after the client is deleted, reduced to number, business, event and time |
| Pet details and grooming notes | Personal (linked to a client) | With the client | |
| Appointments and booking requests | Personal (linked to a client) | With the client | |
| Message log (outbox) | Personal (contains numbers and text) | 13 months [Assumption] | Usage records (counts and cost) kept longer without contact details |
| Texting registration details (EIN, contact person) | Business confidential | While the account is active | Shared only with the text-message provider |
| Card details | Not stored | — | Owners pay through the payment provider's hosted pages; clients pay nothing in version 1 |
| Social Security numbers | Never collected | — | Sole proprietors register without one |

## Integrations
| System | Why | Direction | Notes |
|---|---|---|---|
| Stripe Billing ([ADR-0009](../architecture/decisions/0009-stripe-billing.md)) | Businesses' monthly subscriptions (FR-1) | Outbound + webhooks | Hosted checkout and billing pages; the product never sees card numbers |
| Twilio ([ADR-0007](../architecture/decisions/0007-twilio-toll-free-per-business.md)) | Reminders, booking texts, replies, STOP (FR-4, FR-7, FR-8) | Outbound + inbound replies and status callbacks | One verified toll-free number per business (Compliance obligations) |
| Resend ([ADR-0010](../architecture/decisions/0010-supporting-services.md)) | Sign-in, owner notifications, client emails before texting is approved | Outbound | |

## Compliance obligations
Researched 2026-10-19 for US groomers and their clients. Not legal advice; see [risks.md](risks.md) R-3.

1. **Carrier registration for business texting.** US carriers require every business that sends application-generated texts to be registered: A2P 10DLC brand and campaign for local numbers, or toll-free verification for toll-free numbers. A software platform texting for its customers must register each customer with that customer's own details. Sole proprietors without a tax ID have a lighter path. The registration needs a working business website related to the business name, with a privacy policy and terms, and evidence of how clients opt in.
   Sources (checked 2026-10-19): [Twilio A2P 10DLC](https://www.twilio.com/docs/messaging/compliance/a2p-10dlc); [Twilio ISV registration](https://www.twilio.com/docs/sms/a2p-10dlc/isv-api-registration-overview); [Twilio toll-free verification](https://www.twilio.com/docs/messaging/compliance/toll-free) ("Twilio reviews TFV requests within three business days"); [Twilio business information for registration](https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/collect-business-info).
2. **Consent before reminder texts.** Appointment reminders are informational messages: the client must agree to receive them (for example on the booking form), consent cannot be a condition of booking, and the opt-in must name the business, say how often texts come, include "Msg & data rates may apply", explain STOP and HELP, and link the terms and privacy policy. Marketing texts need separate, written consent and are out of scope for version 1.
   Source (checked 2026-10-19): [Infobip US SMS compliance guide](https://www.infobip.com/docs/essentials/usa-and-canada-compliance/us-sms-compliance-guide).
3. **Opt-out.** STOP and other clear requests to stop must be honored, within at most ten business days under the FCC rule effective 2025-04-11; one confirmation text without marketing is allowed. The product honors opt-outs immediately (FR-7).
   Source (checked 2026-10-19): [Kelley Drye on the FCC revocation rules](https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/fcc-sets-effective-date-for-tcpa-reasonable-consent-revocation-rules).
4. **State privacy laws.** The comprehensive state privacy laws apply above thresholds the product will not reach in year one; for example the CCPA applies from $26.625 million annual revenue or 100,000 California residents' data bought, sold or shared. The product never sells or shares client data. In practice each business controls its clients' data and the product processes it for them, which the terms of service should say. Revisit at 50,000 client records.
   Source (checked 2026-10-19): [California Privacy Protection Agency FAQ](https://cppa.ca.gov/faq.html).
5. **Accessibility.** Clients of public-facing businesses book through the booking page, so it targets WCAG 2.2 AA (NFR-6), the benchmark US accessibility claims are usually measured against [Assumption: general knowledge as of 2026-10-19, not legal advice].
6. **Legal documents.** Terms of service, a privacy policy and text-message terms must be published before texting registration (carriers check them) and before launch. [Open] Q-7.
