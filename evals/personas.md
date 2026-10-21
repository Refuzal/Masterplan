# Simulated users for the Masterplan evals

The evaluator plays these people. Reveal a fact only when the assistant's question calls for it. Answer in the persona's own voice, briefly, and pick the lettered option that fits; choose "I'm not sure — what do you recommend?" whenever the persona would not know. Never volunteer technical vocabulary the persona would not use.

## Eval 1 — Dana, dog-grooming booking app (non-technical founder)
- Former groomer, now building a product; no programming background; uses AI tools.
- Selling to independent groomers in the US, monthly subscription. Hopes for about 50 salons in year one, each with roughly 200 regular clients.
- Clients book from their phones. Groomers manage their calendar on a laptop or tablet at the salon.
- Reminders: text messages strongly preferred (clients ignore email). Email is fine as a backup.
- Data: client names, phone numbers, emails, dog names and breeds, vaccination notes. No payments in version 1 except groomers paying the subscription.
- Budget: wants running costs under about $200/month at first. Launch target: about 3 months.
- If it were down for an hour on a weekday: groomers would be annoyed and might lose a few bookings.
- Builds and maintains it herself with AI tools; might hire a freelancer later.
- Any question about technology choices, hosting, databases or security approach: "I'm not sure — what do you recommend?"
- Approves reasonable recommendations. If asked to choose between a phone app and a website for clients: prefers whatever is cheaper and faster to launch.

## Eval 2 — Mark, accounting-firm document tracker (over-engineered proposal)
- Operations manager at a 40-person accounting firm. Read a lot about "modern architecture"; uses the words but has never built anything.
- About 600 client businesses. Staff send document requests (bank statements, payroll reports, tax forms); clients upload via a secure link; staff see what is outstanding and send reminders.
- Data: client financial and tax documents. Firm uses Microsoft 365 for email and sign-in. US only.
- Hosting: the firm already has an AWS account managed by their one IT person; wants to stay on AWS (firm policy).
- Budget: $300–1,000/month is fine. Timeline: 4 months. Team: the IT person plus AI tools.
- Staff work on desktops; partners occasionally want to check status on their phones.
- First reaction to pushback: "But I want it to scale and be built properly." After a clear explanation with numbers, accepts the simpler architecture. Holds firm on AWS.
- On build vs buy: they tried two off-the-shelf portals; staff hated them and they don't fit the firm's workflow, so building custom is the goal.

## Eval 4 — Priya, property-management SaaS (multi-tenant)
- Product manager; co-founder Ravi is a backend developer with 8 years of Python and Django.
- Customers: small and mid-size property managers in the US and Canada. 20 pilot companies at launch; goal of 2,000 companies in 3 years. A typical customer has 5–50 buildings and 3–20 staff users.
- Users: company admins, property managers, maintenance coordinators; renters submit maintenance requests with photos from their phones (web is fine); vendors get work orders by email or text link and update status without an account.
- Data: renter names, contact details, unit numbers, photos inside homes. No rent collection in version 1; subscription billing for customers yes.
- Some larger customers will ask for single sign-on "eventually".
- Reliability: maintenance emergencies happen (water leaks), so an hour of downtime is serious for some customers.
- Budget: seed-funded; about $500/month running cost at launch is fine. Timeline: pilot in 4–5 months.
- Delegates infrastructure details: "Whatever Ravi will be productive with and won't wake us up at night."

## Eval 5 — Tom, wildlife field-data app (offline desktop)
- Research coordinator at a conservation NGO; not a programmer. One grad student (Lena) will build it with AI tools.
- 30 researchers, 3 field stations. Rugged Windows laptops; a few Android tablets would be nice later, not now.
- Offline for up to two weeks. Station Wi-Fi is slow and unreliable.
- Records: species, count, GPS, time, photos (several per sighting), notes. Researchers almost never edit each other's records; corrections happen rarely, by the original author.
- GPS points for endangered species must not leak (poaching risk). Only the team should see exact locations.
- Exports: CSV for R analysis; shapefile export would be nice later.
- Budget: grant-funded, about $100/month at most; minimal IT support. The NGO already uses Microsoft 365.
- Losing a laptop in the field happens about once a year.

## Eval 6 — Jess, houseplant swap app (uncertain user)
- No technical background. Wants to try the idea in her city (Austin) first. Free for users. Side project.
- Budget: as close to free as possible, under $30/month.
- To nearly every question, answers "I'm not sure — what do you recommend?" Exceptions she does know: it is a side project; free for users; start with Austin; people would arrange to meet up to swap plants; she would like people not to share exact home addresses publicly.
- If asked to approve a recommendation: "Sounds good."

## Eval 7 — Dana again (changing requirements)
- Same persona as eval 1, after the plan was approved.
- The vans: 12 vans, groomers use company Android phones; signal drops for hours in rural areas. Groomers need to see the day's schedule, client and dog notes, and mark appointments done while offline. Clients still book online when they have signal.
- Deposits: $25 card-on-file deposit at booking; charged only on no-show. Fine with using a payment provider.
- Approves the recommended approach after one clarifying exchange.

## Eval 8 — Sam, book-club page (small, cheap)
- 8 friends. Wants: list of nominated books, everyone votes once per round, meeting schedule. No sensitive data. Members all have email addresses.
- Wants it free. Will "maybe" put it on their own domain. Doesn't mind a simple shared password or email link sign-in.
- Built by Sam with AI tools over a weekend.
- On build vs buy: knows polls exist but wants a small custom page for fun and to learn.

## Eval 9 — Alex, team task tracker (plan and build)
- Leads a 6-person marketing team at a small company; not a programmer; uses Claude Code on a Mac.
- Wants: tasks with a title, owner (one of the six), due date and status (To do, Doing, Done); a board everyone can see; filter by owner. Nice to have: comments. Not needed: time tracking, projects, notifications.
- Data: task titles and first names; nothing sensitive. Fine with a shared team password at first.
- Budget: free or a few dollars a month. Would like it online for the team eventually, but is happy to see it working on their own computer first; has no hosting accounts yet.
- Time: wants something usable within a couple of weeks; checks in once a day.
- On build vs buy: knows Trello exists; the team found it cluttered and wants something very simple that they own.
- Approves reasonable recommendations. At each milestone demo: accepts and says to continue, unless the report says something does not work.

## Eval 10 — Priya and Ravi, property-maintenance SaaS (build from an approved plan)
- Same project as eval 4. The plan in the fixture was approved and building M0–M1 was authorized.
- Ravi (the developer) has no hosting, texting or payment accounts set up yet and is travelling this week; build locally and list what he needs to do.
- Approves the milestone if the report shows the isolation tests passing; asks one follow-up question about how the second lock works.

## Eval 11 — Alex again (bug report)
- Reports the symptom in the prompt; can describe steps but not causes. Answers "yes, every time" if asked whether it is reproducible.
