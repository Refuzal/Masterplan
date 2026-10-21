# Discovery

How to learn what matters with as few questions as possible.

Contents: Fork questions · Tiers · Scale · Decision ledger · Question filter · Facts are yours · Rounds · Fast path · Writing a good question · Stress-test with scenarios · The "I'm not sure" protocol · Product and business · Estimating unknowns · Question bank · Requirements quality

## Fork questions

A handful of answers change the architecture more than everything else combined. Settle them first. Skip any the user already answered, and any that is obvious from the description (a book-club page holds nothing sensitive); state each such inference in your playback so the user can correct it. With a structured question tool, the first three can go out together as one quick round of clicks. When the build-or-buy check applies, it takes the place of the least urgent fork in that round, which stays at three questions.

| # | Ask (plain words) | Options | Drives |
|---|---|---|---|
| F1 | Who is it for? | Me, my team or one business (mine or a client's) · Members of the public or a community, free or paid · Many companies, each with its own private space (a product sold to businesses) · I'm not sure — what do you recommend? | Tenancy, sign-in, billing, trust and safety, tier |
| F2 | Where will people use it? (multi-select) | Web browser, on a computer or phone · Installed phone app · Desktop app, or must work without internet · I'm not sure — what do you recommend? (Free text covers "no screen: runs in the background or connects systems".) | Platform and archetype |
| F3 | What's at stake with the data? | Nothing sensitive · Personal details or payments · Health, financial, legal, children's or government data · I'm not sure — what do you recommend? | Security level, tier, compliance |
| F4 | What stage is this? | Try an idea quickly · First version for real users · Replace or run something business-critical · I'm not sure — what do you recommend? | Rigor and roadmap shape |
| F5 | Money, time and team | Monthly running budget band, first-release date, who will build and run it, and roughly how much of their week they have for it (ask only what is not implied) | Hosting, build vs buy, scope, how much operational machinery is realistic |
| F6 | Who makes the technical choices? | You decide and explain them; I'll approve the overall plan · We have preferences or skills you should build around (I'll list them) · I'm not sure — what do you recommend? | How many technical decisions become questions; team-fluency weighting |
| F7 | Where are the users? Ask only if the product messages the public (texts, emails), holds personal data or takes payments | One country (which?) · Europe or the UK · Several countries · I'm not sure — what do you recommend? | Consent and messaging rules, carrier registration, privacy law, data location |

F6 is the delegation question. Ask it early, phrased for the user's level; for a non-technical owner it can merge with "who builds it" ("I don't write code, so you pick the tools"). If the user hands technical choices to you, present them as one package to approve and do not ask about individual technologies. If the user or their team owns some choices (a language they know, a cloud account they already pay for), treat those as constraints and push back only with a labeled severity.

Build vs buy check: if the description matches an existing product category (scheduling, CRM, forms, e-commerce storefront, helpdesk, community groups, polls), say so once before designing: name one or two existing products as examples (from general knowledge, without prices, if you have not researched yet), plus the low-code route when the organization already has a platform that could do it (Microsoft 365 or Google Workspace forms, lists and automations; Airtable; Notion), and ask whether building custom is still the goal and why. The why often reveals the real requirements. Accept the answer and move on. Create project files only once building is the decision. If the user is building a product to sell into a category that already has products (booking software for groomers), ask instead: "What will make customers choose yours over [named products]?" The answer shapes version 1.

## Tiers

Set the tier right after the forks. The highest signal present wins.

| Tier | Signals | What it changes |
|---|---|---|
| **Light** | Personal or small-team tool, private group, prototype or experiment; no payments; no sensitive personal data (first names or contact details shared within a private group of people who know each other are fine); downtime is an annoyance | Four short files (the overview holds requirements, architecture, roadmap and risks) plus two to four short ADRs; self-review; about 2–6 questions |
| **Standard** | Real external users, or a tool a business depends on; user accounts; personal data; payments through a provider; sold to many customers; growth expected | Full file set; three-reviewer panel; cold-start test; about 6–12 questions |
| **Critical** | Stores health records, financial or tax documents, legal files, children's or government data; regulated industry; the product itself holding, routing or paying out money (wallets, escrow, payouts, lending); safety or legal consequences; contractual uptime; AI that takes consequential actions. (Tracking only that such documents exist, without storing them, is usually Standard. So are payments where a provider such as Stripe holds the cards and the money goes straight to the merchant: subscriptions, checkout, card on file; give the payment code an extra review instead of raising the tier.) | Standard plus security and operations docs, threat model, compliance mapping, checker in strict mode, second review round on blockers, and a recommendation for qualified human review of regulated parts; about 12–20 questions |

Tell the user the tier in one sentence and what it means for them ("I'll keep this light: a few questions and a handful of short documents"). They may raise it freely. Lowering it means accepting specific risks, which you record in risks.md. A Critical signal that involves regulated data or money cannot be waived: keep the Critical safeguards and recommend a qualified professional for the regulated parts.

## Scale

The tier sets rigor from risk. Scale sets operational machinery from size, so a large product without sensitive data still gets what running it at size needs. Set it with the tier, from the growth answer and fork F5, for the 12–24-month horizon, and record `Scale:` in state.md.

| Scale | Signals | Adds to the tier |
|---|---|---|
| **Small** | One team, community or business; up to about a thousand active users; one builder | Nothing |
| **Medium** | Thousands of users or dozens of paying customers; a second engineer; usage-based costs (texts, AI, storage) | The Medium rung of codebase-design.md › The scale ladder: job queue and outbox, preview environments, uptime checks with alerts, rate limits, feature flags, cost alerts per service |
| **Large** | Hundreds of tenants or tens of thousands of users; several teams or workstreams; customers who pay for uptime | `docs/engineering/operations.md` (service objectives, alerts, runbooks, who is on call) and `docs/engineering/security.md` with a threat model, whatever the tier; a load test at expected peak before launch; staged rollouts; per-tenant observability, quotas and cost tracking; the decision map and workstreams (build-loop.md › Large projects); the B2B questions below when sold to businesses |

Tell the owner the scale in the same sentence as the tier when it is above Small. Scale moves up only on evidence (a growth plan, signed customers, measured load), never "in case".

## Decision ledger

The ledger is how you know what to ask next and when to stop. Keep it in `docs/project/state.md` under "Planning progress" (area, status, where recorded); keep detail in the home documents, not the ledger.

| Area | Owner | Blocking for |
|---|---|---|
| Problem, users, success criteria | User | All tiers |
| Version 1 scope and non-goals | User; you propose | All |
| Key screens and journeys | User; you propose (mockups) | All with a user interface (Light: one sketch of the main screen) |
| Platforms and connectivity | User | All |
| Data and sensitivity | User | All |
| Scale and growth | User, or delegated | Standard, Critical (Light: assume) |
| Trust and safety | You, user approves | Public or community apps where strangers interact or meet (technology-selection.md › Community and marketplace apps) |
| Budget, timeline, team, lifespan | User | All |
| Product and business viability | User; you propose | Products sold to customers or relying on adoption by strangers (Light: one line) |
| Existing data and cutover | User | When it replaces a tool, spreadsheet or paper process that holds data |
| Reliability and recovery | User, or delegated | Standard, Critical |
| Compliance and accessibility | User facts + your research | When F3 or the audience suggests obligations |
| AI inside the product | User | When the product uses AI |
| Architecture and stack | You, user approves | All |
| Sign-in, permissions, tenancy | You, user approves | When there are accounts |
| Hosting and environments | You, user approves | All |
| Security baseline | You | Standard, Critical |
| Testing and agent guardrails | You | All (Light: minimal) |
| Operations and cost | You | Standard, Critical (Light: cost only) |
| Roadmap and Milestone 1 | You, user approves | All |

Statuses:
- **Open** — not yet known.
- **Assumed** — you picked a safe, easy-to-change default and told the user. Tag it [Assumption] where it is recorded.
- **Proposed** — you recommended it; waiting for the user.
- **Confirmed** — the user decided or approved it, including as part of an approved package (the engineering details inside an approved setup count as Confirmed).
- **N/A** — the area does not apply to this project, or does not block this tier (AI in a product without AI; security baseline for Light).
- **Delegated** — the user chose "I'm not sure — what do you recommend?" and accepted your recommendation. Treat as decided; record "Decided by: Delegated" in the ADR so future agents know the owner did not weigh alternatives.

Only easy-to-reverse items may stay Assumed at handoff. Anything hard to reverse must be Confirmed or Delegated. A blocking area may still be Assumed when the question filter shows that every plausible answer leads to the same design (100, 1,000 or 10,000 members of a one-city pilot); record the assumption and its revisit trigger.

Areas marked "User" can be delegated too. When the user hands you their own goals or differentiator, recommend one, and pair it with a cheap way to test it early (a three-month success measure, a few customer conversations).

Stop asking when no user-owned blocking area for the tier is Open or Proposed; the areas you own are settled by the architecture package and the roadmap, which the user approves in one step each. Do not keep asking because more could be known.

## Question filter

Run this before every question. Ask only if all three hold:

1. The answer moves a blocking area for this tier.
2. You cannot get it from what the user already said, the repository, research, or a safe default.
3. Plausible answers would lead to different decisions.

Then ask the open question with the highest impact multiplied by difficulty of reversal. When a safe default exists and the decision is easy to change later, do not ask: assume it, tag it [Assumption], and mention it in your next progress line ("I've assumed reminders go by email; say if you need SMS").

Before asking, check the ledger and conversation: never re-ask something already answered and still valid. If a new answer contradicts an earlier one, point out the conflict and ask which holds.

Question counts (questions, not one-click confirmations of your recommendations). Typical in this skill's test runs: Light 2–6, Standard 6–12, Critical 12–20. In your opening message give a rough range from your first read of the idea, and adjust it once the tier is set. Soft ceilings: Light 10, Standard 20, Critical 35. Going over usually means you are asking things you should decide yourself.

When research or the repository settles a question you had planned to ask, drop the question and record the fact, or the risk it reveals, instead.

Two signals end discovery early:
- **Prediction test.** If you could confidently predict the user's answers to your next three questions, stop asking. Write those answers down as assumptions and show them in the next summary for correction.
- **Fatigue.** Answers getting shorter, "just pick", or repeated "I'm not sure" mean the user wants you to drive. Switch to the fast path.

## Facts are yours

Never ask the user for something you can find out. Read the repository, the files they attached, and their existing tools' exports; research prices, regulations, competitors and technical limits yourself. When a question depends on a fact that takes time to find, start the lookup in the background (a subagent when you have one) and ask the other questions in the meantime; only the questions downstream of that fact wait. Ask the user for decisions, preferences, and facts only they hold (their customers, their budget, what went wrong last time).

## Rounds

Think of the open decisions as a tree: each decision unlocks the ones that depend on it. A round asks questions whose prerequisites are already settled, never one whose answer depends on another question in the same round.

- **Default (most users):** up to three questions per round, plain words, the recommended option marked on each.
- **Expert users** (they use technical vocabulary, name a stack, or ask to see everything): ask the whole settled frontier in one round, up to about eight questions, each with your recommended answer in one line.
- End every round with: "Reply **yes** to take every recommendation, or answer any by number." One word then settles the round.
- Recompute the frontier after each round; settled answers unlock the next questions.
- A question that needs real thought (who pays and why, what success looks like, a tradeoff the owner must weigh) goes alone, or with only quick factual ones beside it.
- **Show, don't describe.** For how something should look or behave, show a rough mockup or a tiny clickable prototype instead of asking in words: a single self-contained HTML file in the scratch folder (or an artifact, where the surface has them) that the owner opens, with your recommended layout and one alternative. Record what they settle in the requirements; the mockup itself is throwaway.
- **Research shapes the next round.** Right after the forks, run a background scan of comparable products (their core features, typical workflows, common complaints) and of the domain's usual edge cases. Use it to draft the version 1 list, the mockups and the scenario questions, so the owner reacts to informed proposals instead of a blank page.
- Keep to the question count you gave the owner, counting the review's escalations. Before a round that would go past it, either fold the lowest-value questions into recommendations they can change in the package, or say in one line how many more and why. Products sold to businesses usually need a few more questions (pricing, pilots, edge cases); include them in the first estimate rather than discovering them later.

## Fast path

For users who would rather react to a draft than answer questions. Offer it in your opening line ("or say 'fast' and I'll fill in sensible defaults and show you a draft to correct"), and switch to it when you see fatigue.

1. Settle only the fork questions (F6 is the delegation question).
2. Fill every other area with a stated default, tagged [Assumption], sized for the tier.
3. Present the architecture package together with a short list of the assumptions that matter most, and ask for corrections in one round.
4. Hard-to-reverse items in the package still need explicit approval, which the package's approval question provides.

The fast path changes how many questions you ask, not the quality bar: the tier's documents, review and readiness gate still apply.

## Writing a good question

- Ask about situations and outcomes, not technology. "Will people use this somewhere without signal, like a basement or a farm?" not "Do you need offline-first sync?"
- Every choice question carries your recommendation: mark the recommended option "(recommended)" with a one-line reason, or "(my guess)" when it is a guess about a fact of their situation. Put it first. Confirming is easier than choosing.
- Offer 2–3 options that cover the realistic answers, each with a short consequence when it helps the user choose, then the uncertainty option last (SKILL.md › Asking questions has the format rules).
- Ask a question only once the answers it depends on are settled.
- Ranges, not precise numbers, for things nobody can know yet.
- Unpack vague goals before designing for them. "It must scale", "built properly", "secure" and "fast" each hide a different requirement. Ask which outcome they mean (more users, busier peaks, more features without a rebuild, selling to other companies), because each leads to a different design.
- Add a one-clause "why this matters" when the relevance is not obvious.
- When the user corrects one of your announced assumptions, treat it like a revised answer: update the record and run the ripple map. When an approval comes with a new fact ("approved, and most salons have two groomers"), treat it as an approval plus a change.
- If later research shows something you told the user was wrong, correct it in one line at the top of your next message.

## Stress-test with scenarios

When scope or a domain rule is being settled, invent two or three concrete scenarios at the edges and ask what should happen: "A client books the 2pm slot, cancels ten minutes later, and books it again — what should the groomer see?" Scenarios turn vague rules into precise requirements (and acceptance criteria), and expose terms that mean different things to different people; record the resolved terms in the glossary. Answer them yourself as recommendations when the user has delegated; ask only the ones whose answer is genuinely theirs.

## The "I'm not sure" protocol

When the user picks **I'm not sure — what do you recommend?**:

1. **Check you can recommend.** If one critical fact is missing, ask one easier, concrete question instead of the original. Replace "How many users?" with "Is this for your team, a few business customers, or the general public?"
2. **Estimate.** Use the facts you have, comparable products and the heuristics below. Research when current facts matter (prices, regulations, typical usage).
3. **Recommend one answer**, sized for now with a stated trigger for later: "Plan for about 500 users; design so 5,000 needs no rewrite."
4. **Name the assumption and its main risk** in one line.
5. **Confirm in one click:** approve or adjust (options: approve, adjust, I'm not sure — what do you recommend?).
6. If the user is still unsure, adopt your recommendation, mark it **Delegated**, and move on. Never hand the decision back, and never repeat the same question.

When several questions in one round come back "I'm not sure", answer them together: one message with a short recommendation for each and a single approval question. A related proposal (such as the version 1 scope) can share that approval if the message stays readable.

On a recommendation card the same option means "decide for me": adopt the recommendation, mark it Delegated, give one line on when to revisit, and continue.

## Product and business

For a product sold to customers, or one that only works if strangers adopt it, an experienced team checks that it can work as a business before building much. Cover it briefly, recommending answers the user can confirm, and research the market facts yourself:

- **Customer and problem:** who exactly, and the moment the problem costs them (time, money, embarrassment).
- **Alternatives:** what they use today, including doing nothing, and what yours does better (from the build-or-buy check).
- **Price and unit cost:** a pricing hypothesis, the running cost per customer (texts, AI, storage, payment fees), and the margin between them.
- **First customers:** how the first ten will be found, and how the next hundred would be.
- **Demand test:** the cheapest check before most of the building (five to ten conversations, a pilot with friendly customers, a waiting list), placed in the roadmap beside Milestone 1, with a pass mark.
- **Business basics:** what must exist before charging money (a business entity and bank account for payouts, terms and privacy policy, tax registration where needed), stated as owner tasks with a note that this is not legal or tax advice.

Record these in the overview's Goals and risks.md (Light: one line each in the overview). A weak answer is a risk to record and test early, not a reason to stop planning.

## Estimating unknowns

Defaults for when the user cannot say. Label each as an assumption and give its revisit trigger.

- **Users in year one.** Own team: headcount. Business tool sold to companies: customers × seats (for example 30 × 10 = 300). New consumer app: plan for 1,000 to 10,000 and design for 10× that without a rewrite. Do not design for 1000×.
- **Peak simultaneous users.** Roughly 5–10% of daily active users for business apps; spikier for event-driven or consumer apps. A heuristic, not a law.
- **Data volume.** Records per user per month × users × 24 months; add file storage separately (photos and documents dominate).
- **Reliability.** Light: best effort, daily backups. Standard: 99.5% monthly (about 3.6 hours of downtime), daily backups, lose at most 24 hours, restore within a day. Critical: 99.9% (about 43 minutes), point-in-time recovery, lose at most 15 minutes, restore within an hour.
- **Budget.** Start on the smallest tier of managed services that meets the requirements, show the cost at launch and at the growth target, and recommend billing alerts.
- **Data retention.** Keep while the account is active plus 30 days after deletion; backups 30 days; logs 30 days. Then check jurisdiction-specific rules before treating this as settled.
- **Accessibility.** Public or customer-facing UI: WCAG 2.2 AA. Internal tools: keyboard-usable and readable; full AA when required by policy or law.

## Question bank

Plain-language starting points by area. Adapt the wording to the user's own words and domain.

**Problem and success**
- "In a sentence or two: what should be different for people once this exists?"
- "How will you know it's working after three months?" Options: people use it regularly · it saves measurable time or money · it brings in revenue · I'm not sure — what do you recommend?

**Users and roles**
- "Do different people need to see or do different things?" Options: everyone can do the same things · a few roles, such as admin and regular user · each customer has their own private space with their own users · I'm not sure — what do you recommend?

**Version 1 scope**
- Propose the version 1 list yourself from what you heard, sorted Must / Later / Not building, and ask the user to move items. A proposal is far easier to react to than a blank page.
- Keep it to one screen: about 6–12 Must items in plain words (one line each), a short Later line, a short Not-building line, and two or three measurable success criteria. Record it in the home document tagged [Proposed] while it awaits approval, then remove the tag once approved.

**Key screens and journeys** (any product with a screen)
- After the version 1 list, show rough mockups of the two or three screens people will use most, with your recommended layout, and ask what is wrong or missing (Rounds › "Show, don't describe"). Low fidelity: boxes, real labels and sample data, no styling decisions.
- "Walk me through the one thing people will do most, step by step." Use the answer to check the mockups and to write the main journey as acceptance criteria.

**Scale**
- "Roughly how many people will use it in the first year?" Options: under 100 · 100 to 10,000 · more than 10,000 · I'm not sure — what do you recommend? (Use plain text if you need finer bands.)

**Reliability and recovery**
- "If it were down for an hour on a weekday, what would happen?" Options: minor annoyance · lost sales or people can't work · serious harm, broken contracts or safety issues · I'm not sure — what do you recommend?
- "If the last day of data vanished, how bad would that be?" Same pattern; this sets backup frequency.

**Integrations**
- "Does it need to connect to anything, like payments, email or texts, calendars, or a system you already use?" Options: no, it stands alone · yes, I'll list them · I'm not sure — what do you recommend? Follow a "yes" with a free-text request for the list.

**Budget, time, team**
- "What's a comfortable monthly amount to keep it running in the first year?" Options: under $50 · $50–500 · more than $500 · I'm not sure — what do you recommend?
- "Who will build and look after it?" Options: me with AI tools · me plus a developer or two · an engineering team · I'm not sure — what do you recommend?
- "Can that person read and review code, and in which language?" Ask when it is not clear. Someone has to review what AI tools write, so their fluency weighs heavily in the stack decision.
- "Which AI tools will you build with?" Options: a coding assistant working on code in a folder (such as Claude Code, Codex or Cursor) · an all-in-one app builder (such as Lovable, Bolt or Replit) · not chosen yet · I'm not sure — what do you recommend? App builders largely dictate the stack and hosting, so the plan must fit them, or recommend exporting the code to a repository early.
- "Do you or your team already know a programming language, or have a cloud account you want to keep using?" Ask only when it could change the stack. Team fluency is a real reason to prefer a technology.

**Compliance and location** (only when personal or sensitive data is involved)
- Where the users are is fork F7. Then research the obligations yourself; do not ask the user to name regulations.
- Go as far as identifying which obligations likely apply and what they require of the design, with sources. Say plainly that applicability is your reading, not legal advice, and recommend a qualified professional confirm it for Critical-tier projects. Facts about the user's own situation (whether they prepare tax returns, already run multi-factor sign-in) are questions; obligations are research.
- Not every question fits the multiple-choice shape. Free-text facts ("which state?") and questions about past experience ("what went wrong with the tools you tried?") can be plain questions; the uncertainty option is for choices.

**AI in the product**
- "Should the app use AI to do something for people?" If yes: "What should it do?" (free text) and "If the AI gets it wrong, what happens?" Options: a minor annoyance · someone wastes time or money · real harm, such as a wrong medical, legal or financial outcome · I'm not sure — what do you recommend?

**Existing data and cutover**
- "Is there data that has to come across, like a spreadsheet, another app or a paper book, and does the old way need to keep running for a while?" Options: no, starting fresh · yes, some records to bring over · yes, and the old system must keep running during the switch · I'm not sure — what do you recommend? A yes adds an import and switch-over step to the roadmap.

**Product and business** (products sold to customers)
- "Who will pay, and what are they doing about this problem today?" Recommend from what you heard and the alternatives you researched.
- "What price feels right to you?" Options: a recommended price with the per-customer cost beside it · a cheaper entry price · a premium price · I'm not sure — what do you recommend?
- "How will you find your first ten customers?" Options: people I already know · a community or group they gather in · paid ads or marketplaces · I'm not sure — what do you recommend?

**Selling to businesses** (Large scale, or customers that are companies) — research what is normal for the category first, then confirm only what changes the design:
- Plans and limits: what differs between price tiers (seats, usage, features), and what happens at a limit.
- Integration: do customers expect an API, webhooks, an export, or single sign-on, now or "eventually"?
- Data location and assurances: will customers ask where data lives, for a security questionnaire, or for a certification such as SOC 2?
- Onboarding and support: how a new customer gets set up and brings data in, and whether your support staff may view a customer's account (and how that is logged).
- Languages and regions: any customers outside one language or currency?

**Lifespan**
- "How long should this last?" Options: a few months · a few years · a long-term core part of the business · I'm not sure — what do you recommend?

## Requirements quality

- **Functional requirements** get stable IDs (FR-1, FR-2), a priority (Must, Should, Could, Won't-now), a one-line statement from the user's point of view, and acceptance criteria written as Given / When / Then.
- **Non-functional requirements** get IDs (NFR-1) and a measurable target plus how it will be checked. "Fast" is not a requirement; "key pages respond in under one second for 95% of requests, checked by monitoring" is.
- **Non-goals** are explicit, so agents do not build them.
- **Glossary**: domain terms with one-line meanings. Use them consistently in docs, code, database names and UI; it stops agents from inventing synonyms.
- Anything not confirmed carries a tag: [Assumption], [Proposed], [Open], or [Blocking].
