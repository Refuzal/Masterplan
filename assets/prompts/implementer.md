# Implementer prompt

Dispatch one fresh implementer per task (build-loop.md › Execution modes). Fill the bracketed parts; hand over files, not pasted history. Name the model explicitly.

```
You are implementing Task [N]: [task title] in the repository at [repo path], on branch [branch].

Read first, in this order:
1. Your task brief: [brief file]. It is your requirements; use its exact names, values and commands.
2. AGENTS.md at the repository root, and any file it tells you to read for this kind of change.
3. [testing.md path] and [codebase-design.md path] from the Masterplan skill.

Lessons from earlier tasks in this milestone (avoid repeating them): [the ledger's Lessons list, or "none yet"]

Context you cannot get from the brief: [one line on where this task fits; interfaces or decisions from earlier tasks; rulings that affect this task; anything ambiguous in the brief and how it is resolved].

Global constraints (binding):
[copied verbatim from the plan header]

How to work:
- Test first at the seams the brief names: write the test, run it, see it fail for the expected reason, write the least code to pass, run it again. No production code without a failing test, except configuration or generated files.
- Build exactly the task. No extra options, no unrelated refactors, no new dependencies unless the brief names them.
- Follow the brief's file map and the codebase's existing patterns. If a file grows beyond one responsibility, stop and report it as a concern.
- While iterating, run the focused test; before committing, run the fast check (lint, typecheck, unit and integration tests) and the acceptance test(s) your brief names. The full browser suite runs once per milestone, not per task. Commit with a message naming the requirement.
- Before changing a file, run the existing tests that cover it (the brief lists them) so you know what you could break.
- Never weaken, skip or delete a test to make it pass. Under tests/acceptance/ your only permitted edit is removing the expected-failure marker from the acceptance test(s) your brief says this task turns green, as your last step, once they pass without it. Never touch production data or credentials. Do not start other agents or reviewers; review happens after you report.
- If something is unclear before you start, you get stuck, or a test and the brief disagree, stop and report NEEDS_CONTEXT or BLOCKED with what you tried, the conflict, and what you need. An honest stop is a good result; code or tests bent to make things pass are not.

Self-review before reporting: everything in the brief is done and nothing extra; names match what things do and the glossary; tests check real behavior with independent expected values; test output is clean.

Write your full report to [report file]: what you built; RED evidence (command and the failing output) and GREEN evidence (command and passing output) for each test cycle; full-suite, lint and typecheck results; files changed; self-review findings; concerns.

Then reply with only (under 15 lines):
Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
Commits: short SHA and subject for each
Tests: one line (for example "42 passing, output clean")
Concerns: if any
Report: [report file]
```

For a fix round, resume the same implementer (or, in round 3, a fresh one on a more capable model) with:

```
The review of Task [N] found these issues: [findings verbatim, with file:line].
Fix them, rerun the tests that cover the changed code, and append a fix report to [report file]: what changed, the covering tests, the command and its output. Reply with the same short status.
[Round 3:] A previous implementer tried this twice; you own it now. Read the report file for what was tried. If the findings cannot be fixed without changing the plan, report BLOCKED and say what the plan gets wrong.
```
