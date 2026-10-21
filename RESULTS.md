# Masterplan test results

I tested Masterplan against Claude with no skill, and against grill-me and Superpowers. A separate model played each user from a fixed script, and another model graded each run. Each setup ran once, with a simulated user. More runs with real people would make the numbers firmer.

## Planning: with and without the skill

| Scenario | | Checks passed | Questions you answer | Plan quality (avg of 4, out of 5) |
|---|---|---|---|---|
| Non-technical founder, booking app | No skill | 1 / 12 | 21 | 3.3 |
| | **Masterplan** | **12 / 12** | **8** | **4.5** |
| Over-engineered proposal, accounting firm | No skill | 5 / 10 | 12 | 3.5 |
| | **Masterplan** | **10 / 10** | 14 | **4.5** |
| User who isn't sure about anything | No skill | 6 / 9 | 8 | 3.3 |
| | **Masterplan** | **8 / 9** | 7 | **4.5** |

Quality is the average of four grades: completeness, technical soundness, effort asked of the user, and whether a fresh agent could start building from the docs. About half the checks look for Masterplan's own outputs, such as decision records, so the quality grade is the fairer comparison. In the booking-app test, the founder answered 62% fewer questions and got a plan that was ready to build.

## Planning: against other skills

| Scenario | Skill | Questions you answer | Times you reply | Files written |
|---|---|---|---|---|
| Booking app | **Masterplan** | **9** | **6** | 17 |
| | grill-me | 30 | 4 | 0 |
| | Superpowers | 10 | 15 | 2 |
| Book-club site | **Masterplan** | **4** | **4** | 7 |
| | grill-me | 31 | 4 | 0 |
| | Superpowers | 6 | 10 | 2 |

grill-me asked about 3 times as many questions. Superpowers needed more than twice as many replies. Neither left a plan in the repo.

## Building: a task tracker, planned and built end to end

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

## Building a multi-tenant SaaS

From an approved plan, Masterplan built the first two milestones of a property-maintenance SaaS in Django with PostgreSQL. A separate grader reran everything on its own database: 675 tests and 6 phone journeys pass. Every company table is protected at the database level, and the tests try to read and write each record as another company. An early experiment found a data leak in the approved design before any feature code was written. Reviews caught previews that would have run migrations against production, and a sign-in limit that one attacker could have used to lock out every customer. It took about 7.5 hours, a lot of it in review loops on deployment config that couldn't be tested locally. The skill now cuts those loops short and hands the leftovers to the owner's first-deploy checklist.

## Fixing a bug

The same planted bug went to Masterplan and to Superpowers. Both found the root cause, made the same one-line fix and added tests that fail without it. Masterplan kept the fix off the owner's working copy until it was reviewed, and told the owner in plain words how to check it. Superpowers was about 4 minutes faster and slightly more rigorous about writing down its guesses.

## Does it switch on at the right times?

23 test prompts, 3 runs each: correct every time. It started for "plan a SaaS for dental clinics" and similar requests. It stayed out of "add a dark mode toggle", "fix this failing test" and "write a kitchen remodel plan".

The scenarios, user scripts and grading notes are all in [`evals/`](evals/), so you can rerun the tests yourself. The validation record with every run, including what is still unverified, is [`evals/README.md`](evals/README.md).
