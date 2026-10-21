# Build loop

How an authorized plan becomes working, reviewed, verified software, one milestone at a time. The same loop serves a weekend task tracker and a large multi-tenant system; the tier and the project's size change how much ceremony each step gets, not the steps.

Contents: Before the first milestone · The milestone loop · 1 Prepare · 2 Slice · 3 Write the task plan · 4 Execute · 5 Review and fix · 6 Verify · 7 Demo and accept · 8 Record and integrate · Execution modes · Rulings and stops · Owner tasks · Large projects · Efficiency

## Before the first milestone

- Building needs a recorded authorization in `docs/project/state.md` (lifecycle.md › Handoff). "I'm not sure" or silence is not authorization.
- Set `Phase: building` when the first Milestone 0 task starts.
- Read AGENTS.md, state.md, the roadmap entry for the milestone, the ADRs it touches, and engineering standards. Read references/testing.md and references/codebase-design.md once per session before writing code.

## The milestone loop

| Step | Output | Light | Standard | Critical |
|---|---|---|---|---|
| 1 Prepare | Branch or worktree, green baseline | ✓ | ✓ | ✓ |
| 2 Slice | Tasks with blocking edges, in the plan | ✓ | ✓ | ✓ |
| 3 Task plan | `docs/plans/<milestone>.md` and acceptance tests | short | full | full + threat notes per task |
| 4 Execute | Commits, test evidence | inline | subagent per task | subagent per task |
| 5 Review | Findings fixed or ruled | one review at milestone end | per-task review + milestone review | + second security reviewer on sensitive diffs |
| 6 Verify | Fresh evidence for every claim | ✓ | ✓ | ✓ + checker `--strict` |
| 7 Demo and accept | Owner sees it working | ✓ | ✓ | ✓ |
| 8 Record and integrate | State, roadmap, docs, merge | ✓ | ✓ | ✓ |

## 1 Prepare

1. Work on a branch named for the milestone (`m2-booking`), or in an isolated worktree when the environment offers one; never on the main branch without the owner's consent.
2. Install dependencies from the lockfile and run the full test suite, lint and typecheck. A red baseline is reported before any work starts; never build on top of it silently. Do the same at the start of every session that resumes a build.
3. Create the milestone's scratch folder `.masterplan/<milestone>/` (git-ignored) for the ledger, task briefs, reports and review packages. Add `.masterplan/` to `.gitignore` if it is missing.
4. Start the ledger `.masterplan/<milestone>/ledger.md` with its first line `# Ledger — <milestone> — plan: docs/plans/<milestone>.md`. The ledger survives context compaction; your memory does not. After any interruption, trust the ledger and `git log` over recollection, and never redo a task the ledger marks complete. Write ledger lines in fixed forms so a fresh session can resume from them: `Base: <sha>` · `Task N dispatched (<model>) — base <sha>` · `Task N DONE — RED: <command → failure> — GREEN: <command → result>` · `Task N review: approved | <k> findings` · `Task N fix round K — <what changed>` · `Task N COMPLETE` · `Ruling: <what> — <why> — <cost if wrong>` · `Milestone review: <verdict>` · `<milestone> COMPLETE`.
5. Keep a short **Lessons** list at the top of the ledger: any review finding that could recur in later tasks (a missed isolation test for jobs, a test not seen failing first, a copy rule) in one line each. Every later task brief's context includes it.

## 2 Slice

Break the milestone into **tracer-bullet tasks**: each one a thin, complete path through every layer it needs (data, logic, interface, tests), demoable or testable on its own, and small enough for one fresh agent context.

- Give each task its **blocking edges**: the tasks that must finish first. The tasks with no unfinished blockers are the frontier.
- Put enabling refactors first ("make the change easy, then make the easy change").
- A change whose blast radius spans the codebase (rename a column used everywhere, change a shared type) is not a vertical slice. Sequence it **expand → migrate in batches → contract**: add the new form beside the old, move callers over in batches that each keep the build green, then delete the old form.
- Right-size: fold setup, configuration and docs into the task whose result needs them. Split a task that would create more than one new module, change more than about ten files, or mix code that runs here with configuration that can only be checked on the real platform; oversized tasks draw long review loops. Split only where a reviewer could reject one part and approve the other.
- Light projects often have 3–6 tasks per milestone; a large milestone may have 20. More than about 25 means the milestone should be split.

## 3 Write the task plan

The plan records the decisions an implementer cannot make alone; the implementer writes the code. Write it to `docs/plans/<milestone>.md` from `assets/templates/plan.template.md`.

**Header:** goal (one sentence), approach (two or three sentences), the requirements and ADRs it implements (by ID), and:
- **Global constraints:** the binding rules for every task, copied verbatim from AGENTS.md, ADRs and requirements (versions, tenant scoping, naming, limits, copy text).
- **Review focus:** the five inputs or conditions most likely to break this milestone for a real person that no requirement spells out (empty states, duplicates, time zones, concurrent edits, a second tenant, slow networks, permission edges). Each gets a test in the task that owns the code.
- **File map:** files to create or change and each one's single responsibility, organized by feature (codebase-design.md).

**Each task:** title; blocked by; files; **interfaces** it consumes and produces (exact names, parameters and return types, so neighbouring tasks agree); the test seams; the **existing tests that cover the files it changes** (so the implementer knows what it could break); then steps, each one action with a checkable result:
1. Write the failing test (its name and assertions with the exact values from the requirements).
2. Run it and see it fail for the expected reason (command and the expected failure).
3. Implement the minimal code (signature and file; a body only when the signature and test do not determine it).
4. Run the focused test, then the fast check and the task's acceptance tests (commands and what passing looks like).
5. Commit with a message naming the requirement.

**Acceptance tests (all tiers).** Before the first task, one test per acceptance criterion from the roadmap, through the outermost seam (end-to-end or the public API), is written and committed under `tests/acceptance/` by the plan's named **acceptance-test author**: the coordinator or a fresh agent that implements no task (in inline mode, the one agent, before any task code). Each starts **pending**: marked with the test runner's strict expected-failure marker (`test.fails` in Vitest, `test.failing` in Jest, `test.fail()` in Playwright, `@pytest.mark.xfail(strict=True)` in pytest), so the suite stays green while the behavior is missing and fails if a pending test passes early. The plan names the task that turns each one green; that task's last step removes the marker, and that removal is the only edit an implementer may make under `tests/acceptance/`. Any other change there is a Critical finding unless a ledgered ruling says the test itself was wrong. This keeps the agent that writes the code from also writing the test that judges it: agents reliably build to whatever is checked and, when a test and the specification conflict, often change the test ([ImpossibleBench, 2025](https://arxiv.org/abs/2510.20270)). Keep them few and behavioral: one per criterion, a handful per milestone (Light: about six at most). A criterion that already holds when the tests are written gets an ordinary guard test with no marker. Record the commit that adds them as `Acceptance commit: <sha>` in the plan; `check_foundation.py` then fails the build if anything under `tests/acceptance/` changed since that commit other than removed markers. When a ruling changes a test, commit that change alone and move the `Acceptance commit` line to it. At milestone end none may still be pending. Milestone 0 has no user-facing behavior; its roadmap verification checks (a broken change is refused, a planted secret is blocked) serve instead.

**Self-review before executing:** every requirement in scope maps to a task; every step decides exactly one thing (no "handle edge cases", no "add validation"); names and types agree across tasks; every review-focus line has a test; the plan is shorter than the code it describes. Fix gaps inline.

The owner does not review the plan's code. Tell them in two or three plain lines what the milestone will deliver and how they will see it working. Bring them only a decision that is genuinely theirs (scope, cost, risk, wording they own).

## 4 Execute

Pick the execution mode (Execution modes, below). Whatever the mode, every task follows the same contract:

- **Test first at the agreed seams** (testing.md). No production code without a failing test that was seen to fail, except configuration, generated code and throwaway spikes.
- **Build only the task.** No speculative options, no unrelated refactors, no new dependencies the plan did not name. A dependency the plan did not name needs a ledgered ruling after checking that it exists in the registry, is maintained, is not brand new, and comes from the expected publisher; it is pinned in the lockfile. Only a dependency with a cost, a restrictive license or access to user data goes to the owner.
- **Follow the plan's file map and the codebase's existing patterns.** If a file grows past its single responsibility, stop and report it rather than restructuring on your own.
- **Run the focused test while iterating; the fast check (lint, typecheck, unit and integration tests) and the task's own acceptance tests before committing.** The full check, with every browser and acceptance test, runs once at milestone verification and before any merge, not after every task.
- **Stopping is a valid result.** When the task cannot be done as written, or a test and the spec disagree, the implementer reports BLOCKED with the conflict instead of bending the code or the test. In ImpossibleBench, offering an explicit way out cut one model's test-gaming from 54% to 9% ([2025](https://arxiv.org/abs/2510.20270)).
- **Report** in a file: what was built, the RED and GREEN evidence (commands and output), files changed, self-review findings, concerns. Return only a short status: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED, with commits and a one-line test summary.

Handle the status: answer NEEDS_CONTEXT and re-dispatch; for BLOCKED, add context, use a more capable model, split the task, or rule on a plan correction (Rulings and stops). Never make a stuck implementer retry unchanged. Treat DONE as a claim: the review and your own run of the task's focused and acceptance tests confirm it, not the report. Don't rerun the whole suite after each task; the milestone verification does that once. Before marking a task complete, resolve every item the reviewer listed as "cannot verify from this diff": check it yourself in the code, or carry it to the milestone review's checklist in the ledger.

## 5 Review and fix

**Per task (Standard and Critical).** A fresh reviewer gets the task brief, the implementer's report and a review package (`python3 <skill>/scripts/review_package.py <base> <head> <out-file>`: commit list, stat and full diff with context). Record the base commit before dispatching the implementer; never use `HEAD~1`, which drops earlier commits of a multi-commit task. The reviewer returns two separate verdicts (assets/prompts/task-reviewer.md):
- **Spec:** anything missing, extra or misunderstood against the task and global constraints.
- **Standards:** code quality, tests that really test, structure, security, and the project's standards and binding rules.

Findings are Critical, Important or Minor. Minor findings go to the ledger for the milestone review and never block. Critical or Important findings, or a spec failure, start the **fix loop**: resume the same implementer with the findings (rounds 1–2), then a fresh implementer on a more capable model (round 3); each round ends with a scoped re-review of only the fix diff (assets/prompts/re-review.md). After round 3, stop the loop: adjudicate each open finding yourself and ledger a ruling, or, when the finding shows the plan is wrong, correct the plan and re-dispatch the task from scratch. The cap of three is a heuristic: no study sets the best number, but Anthropic's guidance is to start fresh after two failed corrections in one context ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)), and long review loops drift toward over-engineering. Never fix findings in the coordinating context. Critical, security-sensitive and spec findings always get the scoped re-review; for other Important and Minor fixes, you may instead confirm the fix yourself with the targeted test and a read of the fix diff, since the milestone review sees everything again. Work that cannot be run here (deployment configuration, a provider's behavior) gets at most two fix rounds: whatever is still uncertain goes on the owner's first-preview checklist, marked unverified, instead of more review loops.

**Per milestone (all tiers).** A fresh reviewer on the most capable model reviews the whole milestone diff against the milestone's requirements and acceptance criteria, the ledger's deferred minors and rulings, and the architecture (assets/prompts/milestone-reviewer.md). Light uses this as its only review. Fix its findings in one batch, with one scoped re-review.

**Security-sensitive changes** (sign-in, permissions, tenant isolation, payments, file upload, anything touching secrets) get an additional security pass in the milestone review; Critical tier runs it as a separate reviewer, on a different model when one is available.

**Receiving findings:** reviewers asked to find problems usually report some, even on sound work ([Claude Code best practices](https://code.claude.com/docs/en/best-practices)), which pushes code toward over-engineering. Verify each finding against the code before acting; push back with evidence when a finding is wrong for this codebase; check "do it properly" suggestions against real usage before adding anything (YAGNI). Never weaken or delete a test to make a finding go away.

## 6 Verify

No claim of "done", "fixed" or "passing" without fresh evidence from this turn: run the command, read the full output and exit code, then state the result with the evidence. Before marking a milestone done:

1. Full test suite, lint, typecheck and build pass on the milestone branch, run fresh.
2. Each acceptance criterion in the roadmap is checked one by one against the running software: its acceptance test passes, and where the criterion has a visible result you also exercised it yourself (a browser run, a request, a scripted check). Passing unit tests are not acceptance.
3. **Coverage audit:** list every requirement in the milestone's scope and the test that proves it. A requirement with no test is either given one or reported as unverified; never report it as done. Check also that binding decisions were really followed (the chosen library, service or pattern is in use, not quietly reimplemented).
4. The app starts locally (and in the preview or staging environment when one exists) and the milestone's main path works.
5. `python3 <skill>/scripts/check_foundation.py <root> --phase building` reports no FAIL.
6. Every claim in the milestone report is backed by an output you saw. "Should work" is not evidence; an agent's report of success is not evidence until the diff and test output confirm it.

## 7 Demo and accept

Show the owner the milestone working, in their terms: what they can now do, exactly how to try it (a link, or the README steps plus what to click), what was verified and how, what is not done yet, and any rulings that affect them. Say what the evidence means ("the board loads instantly with 200 tasks"), not raw figures; timings, test counts and tool output stay in the ledger and the plan. Ask them to try it and accept or say what is wrong, and whether to continue to the next milestone; that yes extends the build authorization (lifecycle.md › Handoff). Their acceptance is the milestone gate. A non-technical owner is never asked to read code.

## 8 Record and integrate

1. Update `docs/project/state.md` (done, next, blockers), tick the milestone in the roadmap, and move rulings that change a decision into an ADR (superseding when needed) or the owner's risk list.
2. Fix docs the milestone made stale: README.md (for people), AGENTS.md commands, architecture.md, requirements status, glossary.
3. Integration is the owner's decision when it has outside effects: merging to main, pushing, opening a pull request, deploying to production, running a production migration, spending money. Offer it in plain words with a recommendation, for example: "Add this milestone to the main version on your computer (recommended; I rerun every check on the result first)" · "Also send it to GitHub for safekeeping" (when an account exists) · "Keep it separate for now". Production deploys and data migrations need explicit approval each time unless the owner has given a standing approval for that environment.
4. Collect every `Ruling:` line from the ledger into the milestone report, then the scratch folder can go; git history is the record.
5. When the last authorized milestone is accepted and running where its users reach it, or the owner says the project is done for now, set `Phase: maintenance` in state.md; later work arrives through Fix, Change and Review (lifecycle.md).
6. Run a short retro after each milestone: any mistake an automated check could have caught becomes a check (lint rule, test, CI step), not a new paragraph in AGENTS.md. Keep AGENTS.md short.

## Execution modes

| Mode | When | How |
|---|---|---|
| **Subagent per task** | Standard and Critical, when subagents or headless sessions are available (Light stays inline whatever its task count) | Coordinator dispatches a fresh implementer per task (assets/prompts/implementer.md) with the task brief file, never the whole plan or the conversation; then a fresh task reviewer. One implementer at a time unless tasks are on the frontier and touch disjoint files. |
| **Headless sessions** | No subagent tool, but an agent CLI is available (for example `claude -p`) | Same as above, each role a separate headless session with only the files it needs; implementers get write and shell tools, reviewers read-only tools. |
| **Inline** | Light tier, very small milestones, or no way to start fresh sessions | You implement each task yourself, still test-first, then a fresh milestone reviewer (or, with no way to start one, a structured self-review that you label as such). |
| **Parallel waves** | Large milestones whose frontier holds several tasks with disjoint file maps and interfaces already fixed by the plan | Each implementer works in its own worktree on its own branch based on the milestone branch, with its own environment setup (dependencies, `.env`, database); the coordinator merges each finished task, reruns the tests, and dispatches the next frontier. Never let two implementers touch the same files. |

Default to one writer at a time. Parallel writers on overlapping code conflict often (41.7% of replayed merges between different agents' pull requests, [Xu et al., 2026](https://arxiv.org/abs/2607.04697)), multi-agent work uses many times the tokens ([Anthropic, 2025](https://www.anthropic.com/engineering/multi-agent-research-system)), and parallel output multiplies review load, which is already the bottleneck; parallelize only where the plan proves the tasks independent. Read-only work (research, review, test runs) parallelizes safely.

Make task briefs with `python3 <skill>/scripts/task_brief.py docs/plans/<milestone>.md <N> <out-file>`; hand every artifact to a subagent as a file path, not pasted text.

## Rulings and stops

Inside an authorized milestone, technical ambiguities, plan defects and reviewer conflicts are yours to decide: the requirements and ADRs are binding, the plan argues from them, and your judgment settles what neither answers. Record each decision in the ledger as `Ruling: <what> — <why> — <cost if wrong>` and keep going. Stop and ask only for:
1. anything irreversible or destructive (deleting data, dropping tables, force-pushing, rewriting history);
2. a security-sensitive action (credentials, permissions, production access);
3. an effect outside the workspace (push, merge to main, deploy, publish, send messages to real people, spend money);
4. a decision the owner owns (scope, budget, risk, anything contradicting an Accepted ADR or the approved scope), which is a change (lifecycle.md › Change);
5. a plan so broken that every path forward is a guess.

## Owner tasks

Some steps only the owner can do: create accounts, enter payment details, verify a domain, submit a carrier or app-store registration, copy a secret. Give them a numbered checklist in plain words: the page to open, what to click, what to copy, where it goes (a secret goes into the platform's secret settings or a local `.env` that is git-ignored, never into the chat or the repository), how long approval takes, and how they will know it worked. For a long or repeated setup, write a small script that walks them through the steps one at a time and writes values where they belong. Start long-lead tasks (registrations, approvals) as early as the roadmap allows, and keep building on local fakes while they wait.

## Large projects

When the work spans many milestones, teams or sessions:
- Keep a **decision map** in the roadmap: decided (with links), not yet specified (questions you can see coming but cannot phrase yet), and out of scope. Resolve one open architectural question per session, by research, a spike or the owner's decision, before the milestones that depend on it.
- Split a big milestone into **workstreams** with their own branches, plans and ledgers, joined on an integration branch with its own review.
- Give each domain module its own section of the glossary or its own glossary when the language diverges (codebase-design.md › Large systems).
- Re-run the architecture review panel when a milestone changes a binding decision or the scale assumptions.

## Efficiency

- Use the least capable model that does each role well: cheap models for mechanical tasks whose plan fixes the code, standard models for integration work, the most capable model for architecture, the milestone review and fix-loop escalations. Always name the model when dispatching.
- Batch small, same-shaped edits (the same one-line change across ten files) into one task and one review.
- Keep dispatches small: the task brief, the interfaces it touches and the global constraints. Never paste earlier tasks' history.
- **Light tier:** stay inline (no session per task) and write the acceptance tests yourself before any task code, protected by the agent's deny rules and the acceptance-commit check; the acceptance tests are the walkthrough; run them in the check command (with a real browser where one is available) instead of a separate scripted walk-through per milestone, re-run only what a fix touches during the fix loop, and keep to two or three demos before go-live.
- Keep tool output short: test runners print a summary line and failures in full, long logs go to files, and error lines are easy to search. Agents lose time and context reading noise.
- While subagents work, keep doing useful coordination; when idle, wait in bounded stretches and check for finished or stuck workers.
