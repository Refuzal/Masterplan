# Property maintenance platform (working name) — Overview

> Purpose: what we are building, for whom, and why. Update when goals, users or scope change. Owner: product owner (co-founder, product manager).
> Untagged statements are confirmed. Tags mark everything else: [Assumption] [Proposed] [Open] [Blocking].

## Problem
Property management companies manage buildings, renters, maintenance requests and vendor work orders. This product gives each company one web app where renters report problems with photos from their phones and follow their progress, staff turn requests into vendor work orders, and vendors update those work orders from a link.

**First customers:** smaller property management companies in the United States and Canada that run maintenance on spreadsheets, email and phone calls today. A few pilot companies use Buildium.

**Why they will choose it:** it does maintenance only and is much simpler than full property management software. Vendors need no account, and renters just use a link.

## Users and roles
| Role | Who they are | What they need to do |
|---|---|---|
| Company admin | Staff member who runs the company's account | Set up the company, its buildings and staff; manage the subscription |
| Property manager | Staff member responsible for a set of buildings and their renters | Follow maintenance in their buildings; keep renters informed |
| Maintenance coordinator | Staff member who runs maintenance day to day | Triage requests, create work orders, assign vendors, track jobs to completion |
| Renter | Person living in a unit | Submit maintenance requests with photos from a phone; follow their progress. Uses a renter link, with no password or app (risks.md A-4) |
| Vendor | Outside contractor, such as a plumber or electrician | Receive work orders by email or text link; update their status without an account |

Permissions: company admins manage staff, billing and company settings; property managers and maintenance coordinators do all maintenance work across all the company's buildings (requirements.md FR-5). Limiting staff to their own buildings comes later (FR-17).

## Goals and success criteria
The pilot (about 20 companies, about three months from go-live [Assumption]) succeeds when both hold:
- **Adoption:** most pilot companies run nearly all their maintenance through the app by the end of the pilot. [Assumption] Measured as at least 15 of 20 companies with staff active every week in the pilot's last month, each logging at least one maintenance request per 10 units that month (FR-23).
- **Revenue:** at least half the pilot companies (10 of 20) agree to pay when the pilot ends.

## Scope
**Version 1 (Must):** FR-1 to FR-7, FR-10 to FR-16, FR-22 and FR-23 in requirements.md. Approved by the product owner on 2026-10-19.

**Later (Should / Could):** Buildium sync (FR-8), single sign-on for larger customers (FR-9), staff limited to their own buildings (FR-17), costs, invoices and owner approval on work orders (FR-18), recurring maintenance (FR-19), reports (FR-20), French (FR-21).

**Non-goals for version 1:**
- Rent collection, or any payment between renters, companies and vendors. The only payments are companies paying their own subscription through a payment provider.
- Renter screening: credit or background checks, ID documents, bank details.
- App-store apps. Renters use a phone-friendly website. [Assumption] Staff and vendors use the website too.
- Leases, accounting and other property management features beyond maintenance.

## Constraints
- Budget: about $500 a month to run at launch; seed-funded.
- Timeline: pilot with about 20 companies in 4–5 months (February–March 2027).
- Team: two founders: a product manager (the product owner) and Ravi, a backend developer fluent in Python. [Assumption] AI coding agents write much of the code; Ravi reviews it.
- Infrastructure: chosen by two tests the owner set: Ravi is productive with it, and it does not wake the founders at night (low operations work).
- Platforms: one web app that works well on phones. Renters and vendors mostly use phones; staff use computers and phones.
- Data and compliance: renter contact details, units, maintenance requests and photos taken inside homes. No rent, payment card or screening data. Customers and renters are mostly in the United States, some in Canada; no pilot company is in Quebec. Obligations are in requirements.md › Compliance obligations.
- Reliability: an hour of downtime on a weekday is serious for some customers, because maintenance emergencies such as water leaks happen. Targets are in requirements.md (NFR-2, NFR-3).
- Scale: about 20 companies in the pilot; thousands of companies is the long-term goal. [Assumption] A typical pilot company manages roughly 100–500 units (risks.md A-3).

## Glossary
Use these terms, exactly, in docs, code, database names and UI.

| Term | Meaning |
|---|---|
| Company | A property management company that subscribes to the product; the customer account. Its data is private to it. |
| Staff | People who work for a company and sign in: company admins, property managers and maintenance coordinators. |
| Building | A property a company manages. The subscription is priced per building per month. |
| Unit | A home inside a building (an apartment, or the whole house for a single-family property) where renters live. |
| Renter | A person who lives in a unit. Never called "tenant" in the product or the code. |
| Maintenance request | A problem reported by a renter, or by staff on a renter's behalf, with a description and photos. |
| Urgent request | A maintenance request the renter or staff flags as urgent; it alerts the company's on-call contact immediately. |
| Emergency line | The company's own after-hours phone number, shown to renters on every page and message so emergencies never depend on the app. |
| On-call contact | The person (name, phone, email) a company names to receive urgent-request alerts. |
| Work order | A job sent to a vendor to resolve a maintenance request. |
| Vendor | An outside contractor who receives work orders by email or text and updates them through a vendor link, without an account. |
| Vendor link | A secure link, sent by email or text, that lets a vendor view and update one work order. |
| Renter link | A secure personal link, sent by email or text, that lets a renter submit and follow their own maintenance requests. |
| Subscription | The company's paid plan, billed per building per month. |
