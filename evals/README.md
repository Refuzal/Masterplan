# Masterplan evals and validation record

Not loaded by the skill at run time. This folder is for testing the skill and re-running the tests after changes.

## Contents

| File | What it is |
|---|---|
| `evals.json` | 8 planning scenarios plus 3 build scenarios (9 task tracker plan + build, 10 multi-tenant build from an approved plan, 11 bug fix), each with a prompt, expected output and gradable assertions |
| `personas.md` | The simulated user for each scenario (what they know, how they answer) |
| `fixtures/scenario-3-long-running/` | A Masterplan project hand-advanced to week 12 of 20 (M0–M2 done, a provider swapped by a superseding ADR, feature specs, code stubs), for the cold-start test |
| `fixtures/scenario-3-long-running.answer-key.md` | What a fresh agent must get right from that repository |
| `fixtures/scenario-10-approved-multitenant-plan/` | An approved Standard-tier multi-tenant plan with build authorization for M0–M1, the starting point for `/masterplan build` |
| `fixtures/scenario-7-approved-plan/` | An approved, unbuilt Standard-tier plan (dog-grooming booking app), the starting point for `/masterplan change …` |
| `trigger_evals.json` | 11 prompts that should trigger the skill and 12 near-misses that should not |
| `run_trigger_evals.py` | Trigger runner that gives every run its own project folder (needs Anthropic's skill-creator skill; point the `SC` environment variable at its folder) |
| `test_checker.py`, `make_checker_fixtures.py` | Regression tests for `scripts/check_foundation.py` (run `make_checker_fixtures.py`, then `test_checker.py`) |
| `test_scripts.py` | Regression tests for `scripts/task_brief.py` and `scripts/review_package.py` |

## How the scenarios were run

Each run was a fresh agent with no access to the authoring conversation, told only that the skill was installed and what the user typed. A simulated user answered in character from `personas.md`, and only revealed facts when asked. Runs were graded by separate grader agents against the assertions, plus a quality score (completeness, soundness, user burden, agent readiness, each 1–5) and, from iteration 4, a proportionality verdict (vendor accounts and chores against who builds and runs the project). Every produced project was also checked with `check_foundation.py --phase ready`.

Iteration numbers below are successive versions of the skill during development; each run used a frozen copy of the version it names.

Limits of this method: one run per configuration (no variance estimate); simulated users, not real ones; graders are models, not human reviewers; subagents could not spawn subagents, so "independent reviewers" ran as headless `claude -p` sessions with read-only tools.

## Version 2 results (October 2026)

Version 2 merges the build workflow (task plans, a fresh implementer per task, two-axis review, test-first, systematic debugging, verification before claims) into the planning skill, adds a scale axis (Small/Medium/Large), screen mockups before scope approval, a B2B question set, and pending acceptance tests. Assertions added after a run were not graded on that run.

| Scenario | Run | Pass | Notes |
|---|---|---|---|
| 1 Non-technical founder (planning) | iteration 7 | 12/12 (3 newer assertions ungraded) | Quality 5/4/4/5; 13 questions (v1: 8); 7 accounts, "somewhat heavy" |
| 4 Multi-tenant SaaS (planning, large end) | iteration 10 | 10/10 (4 newer assertions ungraded) | Quality 5/4/3/5; 14 questions; Large scale, security and operations docs, mockups; 8 accounts, "right-sized"; first hosting proposal too heavy until the owner's ops experience was known (fixed in the skill since) |
| 9 Task tracker, plan + build | iteration 7 | 11/11 (2 newer assertions ungraded) | 185/185 tests, lint and typecheck pass, app works; 110.7 working minutes; no README (fixed since) |
| 9 Task tracker, Superpowers | iteration 7 | 3/11 | 148/148 tests, app works, no lint or typecheck; 75.2 minutes; most failed assertions check Masterplan-specific files |
| 9 Task tracker, plan + build | iteration 9 | 13/13 | 214/214 tests (24 browser acceptance tests, unchanged since written before code), app works, README; quality equal or better than iteration 7; 183.5 working minutes (session per task on a Light project, separate acceptance-test writer, full suite after every task). The skill now keeps Light inline, runs the full suite once per milestone and caps Light acceptance tests; the effect on time is not yet measured |
| 10 Multi-tenant build M0–M1 | iteration 7 | 10/10 | Grader reran `scripts/check` on its own PostgreSQL 18: 675 tests and 6 phone journeys pass; every company table under row-level security, isolation tests as the app role on reused connections; spike found an RLS leak before feature code; reviews caught production migrations from previews, a proxy-wide sign-in limit and session-bound photo IDs; about 450 working minutes, about 40% in per-task fix rounds and re-reviews (the skill now caps loops on unverifiable config and lets the coordinator confirm non-security fixes) |
| 11 Bug fix | iteration 11 (final skill) | 9/9 by the coordinator's own check | Ranked hypotheses tested with tagged probes, then removed; both new tests verified failing with the bug restored and passing with the fix (157/157); fix isolated on a branch and reviewed; the one-time standing merge approval asked and recorded; about 9 minutes; flagged the missing README unprompted |
| 11 Bug fix | iteration 8 | 6/6 (3 newer assertions ungraded) | Superpowers also 6/6; Masterplan safer (fix isolated on a branch, throwaway data), Superpowers slightly more rigorous; 12.9 vs 9.0 minutes |

Trigger test (v2): 23 prompts × 3 runs, 23/23 correct.

Independent audit of v2: no Blockers; 4 Major findings (UX/mockups, scale axis, acceptance-test contradiction, this validation record), all addressed; most Minor findings fixed.

Unverified: the pending acceptance-test mechanism and the scale axis have been followed by runs only partly (iteration 9 used the version before the pending markers); no eval yet covers Critical-tier builds.

## Version 1 results (October 2026)

Pass = assertions passed. Quality scores are completeness / soundness / user burden / agent readiness.

| Scenario | Version | Pass | Quality | Questions + approvals | Checker |
|---|---|---|---|---|---|
| 1 Non-technical founder | iteration 1 | 11/12 | 5/4/5/5 | 8 + 4 | 0 FAIL |
| | iteration 2 | 12/12 | 5/4/5/5 | 6 + 3 | 0 FAIL |
| | iteration 4 | 11/12 | 5/4/4/5 | 9 + 3 | 0 FAIL |
| | iteration 6 (final) | 12/12 | 5/4/4/5 | 8 + 3 | 0 FAIL |
| | no skill (baseline) | 1/12 | 3/3/3/4 | 21 + 0 | 9 FAIL |
| 2 Over-engineered proposal | iteration 1 (Critical) | 10/10 | 5/4/4/5 | 14 + 4 | 0 FAIL, strict |
| | iteration 2 (Critical) | 10/10 | 5/4/4/5 | 14 + 4 | 0 FAIL, strict |
| | no skill (baseline) | 5/10 | 4/4/3/3 | 12 + 3 | 9 FAIL |
| 3 Long-running cold start | fixture + fresh agent, no skill | 9/10 key facts, 1 partial (fixed in the AGENTS template) | — | — | 0 FAIL (building) |
| 4 Multi-tenant SaaS | iteration 1 | 9/10 | 5/4/4/5 | 8 + 4 | 0 FAIL |
| 5 Offline desktop field app | iteration 1 | 8/8 | 5/4/4/5 | 8 + 4 | 0 FAIL |
| 6 Uncertain user | iteration 1 | 8/9 | 5/4/4/5 | 4 + 5 | 0 FAIL |
| | iteration 4 | 8/9 | 5/4/4/5 | 7 + 5 | 0 FAIL |
| | iteration 6 (final) | 8/9 | 5/4/4/5 | 7 + 5 | 0 FAIL |
| | no skill (baseline) | 6/9 | 3/4/3/3 | 8 + 1 | 9 FAIL |
| 7 Changing requirements | iteration 3 | 8/8 | 5/4/5/5 | 3 + 2 | 0 FAIL, strict |
| 8 Small cheap app | iteration 1 | 8/8 | 5/4/5/5 | 2 + 3 | 0 FAIL |
| | iteration 2 | 8/8 | 5/4/5/5 | 2 + 3 | 0 FAIL |
| | iteration 4 | 8/8 | 5/5/5/5 | 4 + 3 | 0 FAIL |

The one assertion scenario 6 misses ("swaps a hard question for an easier one") is not triggered by its persona, which only says "I'm not sure" to choices the assistant can safely make.

Proportionality (iteration 4 → 6): scenario 1 went from 9 to 8 vendor accounts, with the owner's chores now listed in the plan on a page (still "somewhat heavy"); scenario 6 went from 7 to 4 accounts ("right-sized"); scenario 8 stayed at 2 ("right-sized").

## Head-to-head with grill-me (v1.3.1) and Superpowers (v7.0.0)

Same simulated users, same harness, no transcript-writing overhead (iterations 4 and 5). Working minutes are the agent's total working time across the conversation; user replies counts how many times the user had to answer.

| Scenario | Skill | Pass | Quality | Questions | User replies | Working minutes | Longest single wait | Files written |
|---|---|---|---|---|---|---|---|---|
| 1 Founder | Masterplan | 11/12 | 5/4/4/5 | 9 | 6 | 27.6 | 10.8 | 17 |
| | grill-me | 2/12 | 3/4/2/1 | 30 | 4 | 9.7 | 3.4 | 0 |
| | Superpowers | 5/12 | 4/3/3/4 | 10 | 15 | 22.8 | 13.8 | 2 |
| 8 Book club | Masterplan | 8/8 | 5/5/5/5 | 4 | 4 | 12.6 | 5.2 | 7 |
| | grill-me | 3/8 | 4/5/2/1 | 31 | 4 | 4.5 | 1.6 | 0 |
| | Superpowers | 3/8 | 4/4/4/4 | 6 | 10 | 12.1 | 7.0 | 2 |

About half the assertions check Masterplan's own formats (tiers, ADRs, the checker), so pass rates overstate the gap; the quality scores are the fairer comparison. What the competitors did better: grill-me produced the strongest business plan (pricing, LLC, pilot pass mark, interview script); Superpowers produced the most detailed, executable task plan. Version 1 handed task-level planning to the user's build workflow; version 2 builds it in (see above).

## Pacing

Discovery turns: about 1–3 minutes each in the final version (iteration 2: 6–13 minutes). The two slow turns are the architecture package (about 9–11 minutes, includes current-price research) and the review (about 11–16 minutes for Standard, with three reviewers and a cold-start test; about 5 minutes for Light). The skill now tells the user how long these take before starting them.

## Trigger test

16 prompts × 3 runs each, every run in its own project folder: 16/16 correct (48/48 runs). All 8 planning requests triggered; none of the 8 near-misses (a dark-mode toggle, a failing test, a database question, a kitchen-remodel plan, CI setup, monolith vs microservices, a marketing plan, a refactor) did. The stock runner shares one commands folder across parallel workers, which made the same set score 8/16; `run_trigger_evals.py` fixes that.

## Changes the testing caused

- Iteration 1 → 2: lighter discovery turns, research deferred to the package, rounds of up to three questions, "who builds and runs it" as a fork, vague goals unpacked, checker bug in the AGENTS template.
- Iterations 2–4: cost at the long-term target, searching all docs for stale values after a change, keeping what the user explicitly said, never writing an authorization early, effort fit for the builder, fewest moving parts for first-time builders, "Engineering default" ADR value, demand check and pricing hypothesis, low-code in build-vs-buy, headless reviewers, ADR amendment rules, honest question counts, checking reviewer-added controls against the builder, counting vendor accounts, provider-held payments stay Standard, builder's weekly time, material-change wording, superseded ADRs restate what still holds, "I'm not sure" is never authorization.
- Iterations 4–6: "What you'll look after" in the plan on a page, reviewer additions tied to growth triggers, the uncertainty option on every lettered question, word budgets for the docs.
- Independent audit: a Status mode for approved plans, N/A ledger status, a stopping rule for user-owned areas, the build-authorization gate in the AGENTS template, existing data and cutover, aligned size budgets and recovery targets, a checker fix for `${{ }}` expressions.
