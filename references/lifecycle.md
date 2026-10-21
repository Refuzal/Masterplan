# Lifecycle

Modes beyond a fresh plan, the readiness gate, the handoff, and how the project stays healthy for years.

Contents: Resume · Build · Fix · Change · Review · Brownfield · Ripple map · Readiness gate · Handoff · Ordering the roadmap · Plan on a page · Reconsideration triggers

## Resume
For a plan interrupted mid-discovery (state.md says `Phase: planning`).
1. Read state.md, then the documents its ledger points to. Do not rely on any earlier conversation.
2. Tell the user in two or three lines what is settled, what was assumed, and what is next.
3. Continue the stages from the first Open or Proposed blocking area. If none is left, resume at the first unfinished stage: checker, then review (the Review log is empty), then handoff. Never re-ask answered questions.

## Build
For continuing or starting the build (`/masterplan build`, "start Milestone 0", "next milestone", or `Phase: building` with no other request).
1. Read state.md, the current milestone's plan in `docs/plans/`, and its ledger in `.masterplan/<milestone>/` if one exists. Check that the build authorization covers this milestone; if it does not, show what the next milestone delivers and ask for a clear yes.
2. Resume at the first task the ledger does not mark complete (a task whose last ledger line is a fix round resumes that loop). Never redo completed tasks; confirm against `git log`.
3. Follow references/build-loop.md from the current step.

## Fix
For a reported bug or failing behavior on a project with Masterplan documents.
1. Restate the symptom in one line; ask only for what you cannot reproduce or find yourself.
2. Follow references/debugging.md: feedback loop, reproduce, hypotheses, root cause, regression test, fix, verify.
3. If the cause is a gap in the requirements or a decision, the fix is a change: handle it with Change below.
4. Have the fix reviewed by a fresh reviewer (assets/prompts/task-reviewer.md, with the symptom, root cause and fix report as the brief; Light may use one milestone-style review of the fix). Keep the fix on its own branch until it is reviewed and verified; never leave an unreviewed change live in the copy the owner runs.
5. Report in plain words: what was wrong, what you changed, what now guards it, the evidence, and exactly how the owner can see it fixed. Update state.md.
6. Integration: merging a verified fix into the owner's local main is covered by the build authorization's integration rules (build-loop.md › Record and integrate). Ask once, the first time, whether verified fixes may be merged locally without asking each time; record the answer in state.md and follow it. Pushing and deploying always need the owner's approval unless they gave a standing approval for that environment.

## Change
For a new or changed requirement after decisions exist ("we now need offline use", "budget halved", "customers want single sign-on"). When the user revises an earlier answer mid-planning, run only steps 1–3, then update the documents directly: ADRs that are not yet Accepted are simply edited.
1. Restate the change in one sentence and confirm it if ambiguous.
2. Classify it. **Minor:** no Accepted ADR or binding rule is affected; update the documents and move on. **Material:** it affects an ADR, the data model, sign-in, permissions, tenancy, hosting, cost or a binding rule (AGENTS.md › Change control has the list).
3. For a material change, run the ripple map below and list every affected requirement, ADR, architecture section, roadmap item, cost line, risk, and any existing code or data.
4. Evaluate the options, including "keep the current design and work around it". Recommend one, and spell out the migration: data to move or transform, rework (rough relative size), cost difference, new risks, and the order of work. If code already exists, say what must change and what can stay.
5. Present the change as a delta the user can approve in one look: requirements added, modified and removed; ADRs to be superseded and their replacements; roadmap items added or moved; cost before and after.
6. After approval: write a new ADR that supersedes the old one, restating any part of the old decision that still holds so nothing binding lives only in a superseded record; rewrite every affected document so it describes the new current state (never append contradictions); update the roadmap and state.md; run the checker.
7. Summarize for the user: what changed in the plan, what new work it creates, and what it costs.

## Review
For checking an existing plan or project (`/masterplan review`), or periodically during the build.
1. Run the checker and fix what it finds.
2. Compare documents with the code: stack and versions in manifests, folder structure against the boundaries, environment and infrastructure files, test setup. Code wins; update docs, or flag code that violates an Accepted ADR.
3. Check reconsideration triggers against current reality (usage, cost, incidents, new requirements, vendor changes, end-of-life versions).
4. Run the review panel for Standard and Critical (architecture-review.md) when anything material changed since the last review.
5. When code exists, check its health: boundary rules still enforced and passing; test suite green, with no skipped, weakened or quarantined-and-forgotten tests; dependencies current, with no known vulnerabilities or end-of-life versions; files and modules that have outgrown one responsibility; docs that no longer match the code.
6. Turn repeated mistakes into automated checks (a lint rule, a test, a CI step) rather than more instructions in AGENTS.md.
7. Report: drift found and fixed, decisions to revisit, outdated dependencies and accumulating debt, recommended next steps. Update state.md.

## Brownfield
For a repository that already has code but no Masterplan documents.
1. Inventory before asking anything: README and docs, existing AGENTS.md or CLAUDE.md or other agent rules, manifests and lockfiles, framework config, folder structure, database schema and migrations, CI, infrastructure files, test suites, environment examples (never open real secret files).
2. Write down the as-is architecture. Record each de-facto decision as an ADR with status Accepted and "Decided by: Pre-existing (documented from the codebase)".
3. Present a short as-is summary to the user and confirm it. Then run discovery only for the gaps: goals, users, scope, non-functional requirements, and anything the code does not reveal.
4. Treat existing choices as constraints unless they create a Blocker or a Material risk. Prefer incremental improvement to rewrites, and say what would justify a bigger change.
5. Never overwrite existing instruction files or documents. Propose merged versions, keep the user's rules, and apply changes after agreement.

## Ripple map
When a decision changes, re-check the documents in its row, in the same pass.

| If this changes | Re-check |
|---|---|
| Users, roles or who it is for | Tenancy and permissions ADRs, security model, data model, requirements, glossary, cost |
| Platforms or offline needs | Stack ADR, architecture, sync and storage, roadmap, testing, cost |
| Scale or growth | Hosting ADR, database, scaling path, cost, NFR targets, load testing |
| Data sensitivity or jurisdiction | Tier, compliance obligations, security model, hosting region, retention, backups, AI provider |
| Budget | Hosting and provider ADRs, build-or-buy decisions, cost sketch, roadmap scope |
| Timeline or team | Roadmap, scope, build-or-buy decisions, stack (team fluency) |
| Reliability targets | Hosting, backups and recovery, operations, monitoring, cost |
| Stack, framework or language | AGENTS.md stack line and commands, standards, testing tools, boundary enforcement, hiring and fluency risks |
| Hosting | Environments, deployment, secrets, cost, operations, background jobs |
| Sign-in or tenancy | Security model, data model, isolation tests, every permission rule |
| AI features | AI architecture ADR, cost, privacy, security, evaluation plan |
| Existing data or cutover | Data model, import and switch-over steps in the roadmap, migration risks, requirements |

## Readiness gate
Run before handoff. Every item either passes or is explicitly accepted by the user as a recorded risk. A Blocker cannot be accepted as a risk: tag it [Blocking] and keep the affected work out of Milestones 0 and 1 until it is resolved.

1. Objectives are clear and success is measurable.
2. Version 1 scope and non-goals are written down.
3. Every blocking ledger area for the tier is Confirmed, Delegated, or (if easy to reverse) Assumed. The exception is "Roadmap and Milestone 1": it may be Proposed, because the authorization question at handoff approves it.
4. Major technology choices have ADRs with options considered, evidence and revisit triggers; none is still Proposed.
5. Security and data handling were considered at the tier's depth: sign-in, permissions, tenant isolation if any, secrets, backups.
6. Development, testing and deployment are defined well enough for Milestones 0 and 1.
7. Risks and assumptions are visible in risks.md (Light: the overview's Risks section), with owners or triggers.
8. Milestone 1 has acceptance criteria and a verification method.
9. The next step is concrete enough that an agent could start it immediately.
10. Deterministic checks pass: `check_foundation.py <root> --phase ready` reports no FAIL (Critical: also `--strict`).
11. Standard and Critical: the review panel ran and its findings were resolved; the cold-start test passed. Light: the self-review ran.

## Handoff
1. Set `Phase: ready` in state.md, finalize the decision ledger (Planning progress), and fill Next actions with Milestone 0's first steps.
2. Show the plan on a page (below) and list the files created.
3. If the project is in a git repository, offer to commit the foundation as one commit. If not, offer to initialize one now (otherwise Milestone 0 creates it). Do not push.
4. If there was no writable project folder, deliver the documents as files or a zip and explain that they belong at the root of the code repository.
5. Ask for explicit authorization to start implementation, offering: start building now (Milestones 0 and 1, then I show you each milestone working before going on) · review the documents first · change something · I'm not sure — what do you recommend? Then stop. Planning documents being complete is not permission to build, and neither is "I'm not sure": give your recommendation and ask again for a clear yes.
6. When the user authorizes, replace the "Build authorization: not yet given" line in state.md with exactly what was approved: `Build authorization: YYYY-MM-DD by [owner] — plan as of [commit or date], building M0–M1`. Future agents can then tell an approved plan from a draft. When the owner accepts a milestone and says to continue, extend the line to the next milestone (`… extended to M2 on YYYY-MM-DD`); an owner may also authorize the whole roadmap at once. The agent that starts the first Milestone 0 task sets `Phase: building`.
7. Mention how to continue later: any agent can resume from AGENTS.md and state.md; with this skill installed, `/masterplan build` continues the build, `/masterplan change …` handles new requirements, `/masterplan fix …` handles bugs and `/masterplan review` checks for drift.

### Ordering the roadmap
- Milestone 0 makes it safe to build; Milestone 1 is the walking skeleton.
- After that, put the riskiest assumption first: the feature or technical question most likely to sink the project (a doubtful integration, a performance unknown, whether users will actually do the core action) gets built and checked earliest, while changing course is cheap.
- Low-confidence, hard-to-reverse decisions get a time-boxed spike before the work that depends on them.
- For a product to sell, unless the user already has paying demand, put a demand check (conversations with five to ten target customers, or a pilot with willing ones) and a written pricing hypothesis alongside Milestone 1, before the bulk of the features.

## Plan on a page
Plain language, short, no file contents. With the review summary (at most five bullets), the file list and the authorization question, the whole handoff message should still read in about two minutes.

- **What we're building:** one sentence.
- **For whom and why:** one or two sentences, plus how success is measured.
- **Version 1 includes / doesn't include:** short lists.
- **How it's built:** each part in one line, with why.
- **What it will cost to run:** at launch and at the growth target, with the date prices were checked.
- **What you'll look after:** the accounts the owner must create and keep, and any recurring chores (checking a backup alert, renewing a domain), so the ongoing burden is visible and can be pushed back on.
- **Biggest risks and how we handle them:** two or three lines.
- **Decisions you delegated to me:** list them, with when to revisit.
- **First milestones:** Milestone 0 and Milestone 1 in one line each, with how we'll know they're done.
- **Next step:** the authorization question.

## Reconsideration triggers
Write concrete triggers in each ADR's "Revisit when", and check them during reviews. Typical triggers:
- Usage, concurrency or data volume well past the planned horizon (for example 10× the 12-month estimate).
- A large change in budget, hosting cost or pricing of a key provider.
- New regulatory, security or customer requirements (single sign-on, data residency, audits).
- Changed data access patterns (heavy reporting, search, real-time features).
- New platforms: mobile, desktop or offline.
- Repeated incidents tracing back to the same design choice.
- A vendor or framework reaching end of life, changing license, or being acquired or discontinued.

Without a trigger, do not redesign. The goal is controlled evolution, not perpetual re-engineering.
