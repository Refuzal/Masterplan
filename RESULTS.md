# Masterplan: test results and background

A Claude skill that plans and builds software the way a good engineering team would. You can use it with no technical background.

You describe what you want. Masterplan asks you a handful of plain-English questions, works out the stack, hosting and monthly cost, and has the plan checked by independent reviewers. It writes everything into your repo, then builds it one milestone at a time. You see each milestone working before it moves on.

It works the same way for a weekend task tracker and for a multi-tenant SaaS with thousands of customers. Only the amount of process changes.

## Why I built it

AI coding tools are good at writing code and bad at everything around it. They start building before anyone has decided who the users are, what the data is worth, or what it will cost to run. They pick whatever stack they saw most in training. They say "done" when the tests pass, sometimes after quietly editing the tests.

The popular skills each fix part of this. grill-me asks great questions but leaves you with a conversation, not a plan. Superpowers has an excellent build loop, but it assumes you can review code and answer technical questions. I wanted one skill that does both, for people who can't read code as well as people who can.

## What it does

**Plans**
- Asks only questions that change the plan, three at a time. Every question comes with a recommended answer, so replying "yes" accepts them all.
- "I'm not sure, what do you recommend?" is always an option, and you get a real recommendation back.
- Looks up facts itself (prices, regulations, what competitors charge) instead of asking you.
- Shows rough sketches of the main screens before you agree on scope.
- Proposes one setup with plain-English reasons, a monthly cost and what you'll have to look after. It pushes back if your idea will cost you later.
- Three reviewers, each in a fresh session, stress-test the plan. A fourth fresh session checks that a new developer could pick it up from the docs alone.

**Builds** (only after you say go)
- Writes a plan for each milestone, then gives each task to a fresh agent.
- Acceptance tests are written before the code, by an agent that doesn't write the code, and the builders can't edit them.
- Tests are written before the code they test. Every task gets an independent review, and nothing is called done without fresh test output.
- Organises code by feature, with boundaries enforced by a lint check.
- Ends every milestone with a plain-language demo: what you can do now and how to try it.

**Maintains**
- `/masterplan fix` reproduces a bug before touching code and adds a test that fails without the fix.
- `/masterplan change` handles new requirements: it shows what changes, what it costs and what moves, then updates every affected document.
- `/masterplan review` checks the code and docs for drift.

Everything lives in your repo as plain Markdown: `AGENTS.md`, requirements, decision records, a roadmap and a state file. Any coding agent can pick the project up later, with or without this skill.

## How much process you get

The skill sets two dials at the start and tells you what they mean.

**Risk tier**, from what's at stake:
- **Light:** a personal or small-team tool. About 2–6 questions and four short docs.
- **Standard:** real users, personal data or payments. Gets the full doc set and independent review.
- **Critical:** health, financial or regulated data. Adds a threat model, compliance mapping and stricter checks.

**Scale**, from size:
- **Small:** no extra machinery.
- **Medium:** adds job queues, preview environments and rate limits.
- **Large:** adds on-call runbooks, load tests, staged rollouts and per-customer cost tracking.

## Test results

I tested the skill against Claude with no skill, grill-me and Superpowers. A separate model played each user from a fixed script, and a separate model graded each run. Each configuration ran once, and the users were simulated, not real. Read these as strong signals, not proof.

### Planning: with and without the skill

| Scenario | | Checks passed | Questions you answer | Plan quality (avg of 4, out of 5) |
|---|---|---|---|---|
| Non-technical founder, booking app | No skill | 1 / 12 | 21 | 3.3 |
| | **Masterplan** | **12 / 12** | **8** | **4.5** |
| Over-engineered proposal, accounting firm | No skill | 5 / 10 | 12 | 3.5 |
| | **Masterplan** | **10 / 10** | 14 | **4.5** |
| User who isn't sure about anything | No skill | 6 / 9 | 8 | 3.3 |
| | **Masterplan** | **8 / 9** | 7 | **4.5** |

Quality is the average of four grades: completeness, technical soundness, effort asked of the user, and whether a fresh agent could start building from the docs. About half the checks look for Masterplan's own outputs, such as decision records, so the quality grade is the fairer comparison. In the booking-app test, the founder answered 62% fewer questions and got a plan that was ready to build.

### Planning: against other skills

| Scenario | Skill | Questions you answer | Times you reply | Files written |
|---|---|---|---|---|
| Booking app | **Masterplan** | **9** | **6** | 17 |
| | grill-me | 30 | 4 |
| | Superpowers | 10 | 15 |
| Book-club site | **Masterplan** | **4** | **4** | 7 |
| | grill-me | 31 | 4 |
| | Superpowers | 6 | 10 |

grill-me asked about 3 times as many questions. Superpowers needed more than twice as many replies. Neither left a plan in the repo.

### Building: a task tracker, planned and built end to end

| | Masterplan | Superpowers |
|---|---|---|
| Automated tests passing | 185 / 185 | 148 / 148 |
| Lint and type checks | Pass | None set up |
| App works when tested by hand | Yes | Yes |
| Code organisation (out of 5) | **5** | 3 |
| Test quality (out of 5) | **5** | 4 |
| Correctness (out of 5) | **5** | 4 |
| Owner experience (out of 5) | **4** | 3 |
| Times the owner had to reply | **6** | 8 |
| Working time | 111 min | **75 min** |

Masterplan was slower. The extra time went into independent reviews and a demo at each milestone. Those reviews caught a race condition in the login lockout and a daylight-saving bug before the owner saw either one. A later build with stricter acceptance testing scored as well or better but took 184 minutes, mostly from rerunning the whole test suite after every task. The skill now runs the full suite once per milestone instead; I haven't re-timed it yet.

### Building a multi-tenant SaaS

From an approved plan, Masterplan built the first two milestones of a property-maintenance SaaS in Django with PostgreSQL. A separate grader reran everything on its own database: 675 tests and 6 phone journeys pass. Every company table is protected at the database level, and the tests try to read and write each record as another company. An early experiment found a data leak in the approved design before any feature code was written. Reviews caught previews that would have run migrations against production, and a sign-in limit that one attacker could have used to lock out every customer. It took about 7.5 hours, a lot of it in review loops on deployment config that couldn't be tested locally. The skill now cuts those loops short and hands the leftovers to the owner's first-deploy checklist.

### Fixing a bug

The same planted bug went to Masterplan and to Superpowers. Both found the root cause, made the same one-line fix and added tests that fail without it. Masterplan kept the fix off the owner's working copy until it was reviewed, and told the owner in plain words how to check it. Superpowers was about 4 minutes faster and slightly more rigorous about writing down its guesses.

### Does it switch on at the right times?

23 test prompts, 3 runs each: correct every time. It started for "plan a SaaS for dental clinics" and similar requests. It stayed out of "add a dark mode toggle", "fix this failing test" and "write a kitchen remodel plan".

The scenarios, user scripts and grading notes are all in [`evals/`](evals/), so you can rerun the tests yourself. The validation record with every run, including what is still unverified, is [`evals/README.md`](evals/README.md).


## Credits

The build workflow borrows ideas from [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent, and the questioning style borrows from [Matt Pocock's skills](https://github.com/mattpocock/skills). Both are MIT-licensed. The ideas were rewritten, not copied. See [CREDITS.md](CREDITS.md).
