# Requirements

> Purpose: what the system must do and how well. Update when scope, targets or obligations change. Owner: product owner; engineers keep IDs stable.
> Priority: Must (version 1) · Should · Could · Won't (now). Untagged = confirmed; [Assumption] [Proposed] [Open] [Blocking] mark the rest.

## Functional requirements
Version 1 (the pilot) is every Must below, approved by the product owner on 2026-10-19.

### FR-1 Renters submit maintenance requests with photos — Must
As a renter, I report a problem from my phone through my renter link, with no password or app: a description, photos, permission to enter, and an urgent flag (FR-11).
- Given a renter opens their renter link on a phone, when they describe a problem, attach up to 10 photos (including iPhone HEIC photos) and submit, then the request appears in the company's request queue and the renter sees a confirmation with the request number and the company's emergency line.
- Given a renter allows entry when they are not home, when staff or the vendor view the request, then the permission is shown.
- Given a file that is not a photo or is larger than 15 MB, when the renter attaches it, then it is refused with a clear message and the rest of the form is kept.

### FR-2 Renters follow their requests — Must
As a renter, I see the status and progress of my own maintenance requests through my renter link.
- Given a renter with two requests, when they open their renter link, then they see both with their current status and latest update, and nothing belonging to any other renter.
- Given a vendor has scheduled a visit, when the renter opens their link, then they see the scheduled time.
- [Assumption] Given a renter enters their phone number or email on the "get a new link" page, when it matches an active renter, then a new link is sent, and the old one stops working once the new one is opened; when it does not match, the page shows the same neutral message, so nobody can learn who is a renter (risks.md A-4).
- Given the same phone number or email asks for a new link more than once in 10 minutes or three times in a day, then no further link is sent that day and staff see a warning.
- Given a renter link unused for 180 days, when it is opened, then it shows how to get a new link and the emergency line, and nothing else.

### FR-3 Staff turn requests into vendor work orders — Must
As a maintenance coordinator, I create a work order from a maintenance request, pick a vendor, add instructions and set a priority.
- Given an open maintenance request, when staff create a work order for a vendor, then the vendor is sent a vendor link and the request shows "Work order sent".
- Given a vendor declines, when staff open the request, then it is marked for reassignment and staff can send a new work order to another vendor.

### FR-4 Vendors update work orders from a vendor link — Must
As a vendor, I receive a work order by email or text and, through the vendor link and without an account, accept or decline it, set a scheduled time, add notes and photos, and mark it done.
- Given a vendor opens their vendor link, then it shows the address and unit, the problem and its photos, permission to enter, and [Assumption] the renter's first name and phone number to arrange access; it shows nothing about other work orders or renters.
- Given a vendor accepts and sets a scheduled time, then staff and the renter see the time and are notified.
- Given a vendor marks the work order done with notes and photos, then the maintenance request shows "Completed" and the renter is notified.
- Given a work order closed more than 30 days ago, or a link staff revoked, when the vendor opens the link, then it says the link has expired and shows no details.

### FR-5 Staff accounts and roles — Must
As a company admin, I give company admins, property managers and maintenance coordinators their own sign-in. Company admins manage staff, billing and company settings; property managers and maintenance coordinators do all maintenance work across all the company's buildings.
- Given a company admin invites a staff member with a role, when the invitee accepts, then they can sign in and do only what that role allows.
- Given a property manager or maintenance coordinator, when they try to open billing, staff management or company settings, by page or by direct address, then the server refuses.
- Given a company admin without two-step verification, when they sign in, then they must set it up before continuing.

### FR-6 Buildings, units and renters — Must
As staff, I add the company's buildings, units and renters by typing them in or uploading a spreadsheet, and keep them up to date.
- Given a spreadsheet in the provided template (CSV or Excel), when staff upload it, then they see a preview listing problems row by row before anything is saved, and confirming saves every valid row.
- Given imported renters with a phone number or email, when staff choose "send renter links", then each renter receives their renter link.
- Given a building is archived, then it no longer counts toward the subscription.

### FR-7 Subscription billing per building — Must
As a company admin, I pay a subscription priced per building per month by card through a payment provider. Pilot companies get free months.
- Given a company admin starts the subscription, when they pay, then the card is entered on the payment provider's page and no card details reach our servers.
- Given the number of active buildings changes, when the next invoice is made, then it charges for the new number.
- [Assumption] Given a payment fails, then the company admin is emailed; renter and vendor links keep working; after 30 days unpaid, staff access becomes read-only until payment.
- [Open] Whether a single-family home counts as one building, and how price tracks texting cost (risks.md Q-6); decided before M4.

### FR-8 Sync from Buildium — Should (after the pilot)
As a company on Buildium, my buildings, units and renters stay in step with Buildium without retyping them.

### FR-9 Single sign-on — Should (when a larger customer asks)
As a company admin at a larger company, my staff sign in through our own identity system (SAML or OpenID Connect single sign-on). Adding it must not require moving existing staff accounts.

### FR-10 Company setup and staff invitations — Must
As a company admin, I create the company, enter its emergency line and on-call contact, and invite staff by email.
- Given a new company, when the admin finishes setup, then renter links cannot be sent until an emergency line and an on-call contact are saved.
- Given an invitation older than 7 days, when someone uses it, then it is refused and the admin can send a new one.

### FR-11 Emergency line and urgent requests — Must
As a renter, I see the company's emergency line before and after I submit a request. As the company's on-call contact, I get a text immediately when a request is flagged urgent.
- Given any renter page or message to a renter, then the company's emergency line is shown.
- Given a renter flags a request as urgent, when it is submitted, then the on-call contact gets a text within 1 minute, sent from our own staff-alert number so it works from the company's first day, and the renter is told to call the emergency line if anyone is in danger or water is leaking.
- Urgent alerts are a best-effort convenience, not an emergency service: renter pages, renter messages and the customer terms say so, and point to the emergency line.
- Given an urgent alert cannot be delivered after retrying for 5 minutes, then staff see a warning on the request and the founders' monitoring raises an alert.

### FR-12 Staff log requests for renters — Must
As staff, I record a maintenance request that a renter reported by phone or email, so all maintenance lives in one place.
- Given a renter phones in a problem, when staff log it for that renter, then it appears in the queue marked "logged by staff" and the renter gets the usual updates.

### FR-13 Request queue — Must
As staff, I see all open maintenance requests and work orders, filtered by building, status, urgency and vendor.
- Given open requests, when staff open the queue, then urgent requests are listed first.
- Given 500 open requests, when staff apply any filter, then results show in under 1 second.

### FR-14 Notifications — Must
Renters, vendors and staff get email or text messages at key steps: request received, work order sent, scheduled, done. Texts to renters and vendors come from the company's own verified number; texts to staff come from our staff-alert number (ADR-0008).
- Given a status change, when it happens, then each affected renter, vendor and staff member is sent a message within 1 minute: by text if the right number is approved and the person has not opted out, otherwise by email.
- Given someone replies STOP, then they get no more texts from that company's number, and later messages go by email when an address is known.
- Given any text, then it names the company and contains no marketing.

### FR-15 Vendor list — Must
As staff, I keep the company's vendors with their trade, phone and email.
- Given staff add a vendor, then the vendor can be chosen when creating a work order.

### FR-16 Activity history — Must
As staff, I see who did what and when on each maintenance request and work order.
- Given any change to a request or work order, then the history shows who made it (a named staff member, "renter via link", "vendor via link" or "system") and when.
- Given any staff member, when they view the history, then they cannot edit or delete it.

### FR-17 Staff limited to their own buildings — Should
### FR-18 Costs, vendor invoices and owner approval on work orders — Should
### FR-19 Recurring maintenance, such as annual inspections — Could
### FR-20 Reports on response times and vendor performance — Should
### FR-21 French language — Should; Must before selling in Quebec
See Compliance obligations › Quebec. All user-facing text is written so it can be translated from day one.

### FR-22 Company data export and deletion — Must
As a company admin, I can get all my company's data exported, and have it deleted when we leave. In the pilot the team runs this on request. Required by customer contracts (Compliance obligations).
- Given a company asks for its data, when the team runs the export, then the company receives its records as CSV files and its photos within 30 days.
- Given a departing company confirms deletion, then its data is deleted from the live database and storage, and backups holding it expire within 30 days.

### FR-23 Pilot metrics for the founders — Must
As a founder, I see how each pilot company uses the product, to judge the pilot (overview.md › Goals).
- Given a founder opens the pilot metrics page, then they see for each company: staff active per week, maintenance requests per unit per month, median time from request to work order sent, and subscription status.
- Given anyone who is not a founder, when they open the page, then access is refused.

## Non-functional requirements
Each target must be measurable and checked somewhere. Targets approved with the architecture package on 2026-10-19.

| ID | Quality | Target | How we check |
|---|---|---|---|
| NFR-1 | Performance | Staff pages respond in under 1 s for 95% of requests; a renter can submit a request with 3 phone photos in under 15 s on a typical 4G connection | Monitoring; a timed test on real phones before the pilot |
| NFR-2 | Availability | 99.9% per month (about 43 minutes of downtime) as an internal objective; no uptime promise in customer contracts during the pilot | Uptime monitor |
| NFR-3 | Data loss and recovery | Lose at most 15 minutes of data; restore within 2 hours | Restore drill before the pilot and every quarter |
| NFR-4 | Company data isolation | No staff member, renter link or vendor link can read or change another company's data | Cross-company isolation tests on every pull request |
| NFR-5 | Accessibility | WCAG 2.2 AA on all pages | Automated checks in CI plus a manual pass before the pilot |
| NFR-6 | Scale horizon | 2,000 companies and 200,000 maintenance requests a month without re-architecture (10× the year-one estimate, risks.md A-3) | Load test before general launch |
| NFR-7 | Running cost | About $500 a month at pilot launch (estimate $400–550, architecture.md › Cost) | Billing alerts on every paid service; monthly review |
| NFR-8 | Link security | Renter and vendor links cannot be guessed, can be revoked by staff, and open only their own renter's requests or their own work order | Security tests in CI |
| NFR-9 | Message delivery | Emails and texts leave within 1 minute of the event that triggers them, for 95% of messages | Job queue monitoring |

## Data
| Data | Sensitivity | Kept for | Notes |
|---|---|---|---|
| Renter names, phone numbers, email addresses and units | Personal | [Assumption] While the company's account is active, plus 30 days | Belongs to the company that manages the unit |
| Maintenance request text and photos taken inside homes | Personal | [Assumption] As above | Photos can show people, belongings and location data; strip location data on upload |
| Staff accounts | Personal | [Assumption] As above | |
| Vendor contact details and work order history | Business contact data | [Assumption] As above | |
| Activity history | Personal | [Assumption] As above | |
| Subscription and invoices | Business | As tax law requires | Card details stay with the payment provider; never stored here |
| Backups and logs | Mixed | [Assumption] 30 days | |

## Integrations
| System | Why | Direction | Notes |
|---|---|---|---|
| Stripe Billing (ADR-0009) | Subscription billing per building | Outbound + webhooks | Hosted checkout and customer portal; no card data stored |
| Amazon SES (ADR-0008) | Renter and vendor links, notifications, staff sign-in | Outbound + delivery webhooks | Transactional stream only; SPF, DKIM and DMARC on the sending domain |
| Twilio texts (ADR-0008) | Renter and vendor links, notifications, urgent alerts | Outbound + replies (STOP, HELP) + delivery webhooks | One verified toll-free number per company; verification is free and takes about 3–5 business days, and unverified numbers are blocked ([Twilio](https://support.twilio.com/hc/en-us/articles/360038172934-Best-Practices-for-Using-Toll-Free-SMS-and-MMS-in-the-US-and-Canada), checked 2026-10-19). Platforms must register each customer business, not themselves ([Twilio ISV guide](https://support.twilio.com/hc/en-us/articles/13263383206299-Toll-Free-Verification-for-ISVs), checked 2026-10-19) |
| Cloudflare R2 (ADR-0007) | Photo storage | Direct browser uploads + app reads | Private bucket; short-lived signed links |
| Buildium (after the pilot, FR-8) | Building, unit and renter records | Inbound sync | Buildium's Open API comes only with its Premium plan ([pricing](https://www.buildium.com/pricing/), checked 2026-10-19); see risks.md R-2. Other systems later; AppFolio's API needs the customer's Plus or Max plan, and its marketplace partnership takes 3+ months to contract ([Propexo guide](https://docs.propexo.com/pms-guidance/appfolio/integration-and-partnership), checked 2026-10-19) |

## Compliance obligations
Researched 2026-10-19 from secondary legal sources; not legal advice. A lawyer reviews the customer contract and privacy notice before the first pilot contract is signed (risks.md R-5).

Each company controls its renters' data; this product processes it on the company's behalf as a service provider.

- **Canada, PIPEDA (and similar laws in Alberta and British Columbia):** a company stays accountable for data it sends to a service provider, including one in another country. It must be open about outsourcing and the provider must give comparable protection, by contract and safeguards ([BLG on the Privacy Commissioner's position](https://www.blg.com/en/insights/2020/08/opc-affirms-requirements-for-transferring-personal-information-across-borders-for-processing), checked 2026-10-19). We provide: a data processing agreement, a privacy notice saying where data is stored, and a short security summary.
- **Quebec, Law 25:** before sending personal information outside Quebec, the company must assess the transfer, and its contract with the service provider must cover confidentiality measures, use limited to the mandate, no keeping data after the contract ends, notice of breaches without delay, and verification rights ([BLG](https://www.blg.com/en/insights/2022/12/cross-border-transfers-of-personal-information-outside-quebec), checked 2026-10-19). No pilot company is in Quebec; the data processing agreement includes these clauses before the first Quebec sale. FR-22 supports the end-of-contract duty.
- **Quebec, Charter of the French Language:** businesses must serve customers in French; standard-form contracts and websites must be available in French; workplace software must be offered in French when a French version exists ([Miller Thomson](https://www.millerthomson.com/en/insights/publications/special-considerations-doing-business-in-quebec-civil-law-language-compliance/), checked 2026-10-19). Hence FR-21 before selling in Quebec.
- **Canada, anti-spam law (CASL):** maintenance notifications are not marketing; we still identify the sender and offer an opt-out in every message, and never send marketing to renters or vendors ([MoEngage summary](https://moengage.com/docs/user-guide/campaigns-and-channels/sms-mms-and-rcs/compliance-and-deliverability/messaging-regulations-for-canada), checked 2026-10-19).
- **United States, texting:** each company's sender number is verified, every text names the company, and STOP and HELP replies are honored (Integrations above).
- **United States and Canada, breach notification:** we tell affected companies promptly about any breach of their data, so they can meet their own notification duties.
- **Accessibility:** customer-facing pages meet WCAG 2.2 AA (NFR-5).
- **Sales tax on the subscription:** some US states and Canada (GST/HST) tax software subscriptions. [Open] An accountant confirms where we must register before billing starts (risks.md R-5).
