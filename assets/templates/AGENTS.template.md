# AGENTS.md — {{Project name}}

{{One sentence: what this is and who it is for.}}

Start every session by reading `docs/project/state.md`. It says what is done, what is next, and what is blocked. If it says `Build authorization: not yet given`, the plan is a draft: write no application code until a human approves it.

## Map
- Product, users, scope, glossary: `docs/project/overview.md`
- Requirements and acceptance criteria: `docs/project/requirements.md`
- Architecture (current and binding): `docs/architecture/architecture.md`
- Decisions: `docs/architecture/decisions/` (Accepted ADRs are binding; Superseded ones are history only)
- Roadmap: `docs/project/roadmap.md` · Risks, assumptions, open questions: `docs/project/risks.md`
- Engineering standards: `docs/engineering/standards.md`
{{Light tier: replace the lines above with the files that exist (overview.md holds requirements, architecture, roadmap and risks).}}

## Stack
{{One line, e.g. "TypeScript (strict) · Next.js · PostgreSQL via Drizzle · Vercel + Neon". Link the ADR for each part.}}

## Commands
{{install · dev · test · lint + typecheck · build. Before scaffolding, write: "Defined in Milestone 1 — fill in when the project is created."}}

## Binding rules
{{3–7 project-specific rules a capable engineer would not guess: module boundaries, where business logic lives, tenant scoping on every query, naming from the glossary, generated files not to edit.}}

## How to work
1. Read the docs relevant to your task, then the code. If they disagree, trust the code, say so, and fix the doc.
2. Work from the current milestone's plan in `docs/plans/`. For anything bigger than a small fix that no plan covers, write the plan (or a short spec in `docs/features/`) with acceptance criteria before coding.
3. Keep changes small: one task per session (the plan's tasks are sized for that), one milestone per branch.
4. Test first: write the failing test, run it and see it fail, then write the least code that passes. Run the full test suite, lint and typecheck before saying you are done, and quote the fresh output; "should work" is not done.
5. Build only what the roadmap and requirements ask for. Suggest new ideas; do not add them.
6. Before finishing: update `docs/project/state.md` (done, next, blockers) and any doc your change made stale.
7. When a decision changes, write a new ADR that supersedes the old one rather than editing history. Flag outdated or end-of-life dependencies and growing technical debt in `docs/project/risks.md` when you notice them.

## Change control
A change is **material** if it adds or replaces a service, datastore, framework or external provider; changes sign-in, permissions, tenant isolation or the shape of existing data; changes hosting or adds recurring cost; or contradicts an Accepted ADR. Building what the roadmap, an approved feature spec and the Accepted ADRs already describe is not a material change; departing from them is.
For a material change: stop, explain the consequences, draft an ADR with status Proposed in `docs/architecture/decisions/`, and wait for human approval. Everything else is a normal change.

## Never
- Commit secrets, or put credentials or real personal data in code, docs, tests or logs.
- Use production credentials or data, or run destructive commands (deleting data, force-pushing, applying infrastructure changes) without explicit human approval.
- Weaken, skip or delete a test to make it pass, or mock this project's own modules in tests. If a test and the requirements disagree, stop and say so.
- Edit anything under `tests/acceptance/`, except: the plan's named acceptance-test author writes them before a milestone's first task, and the task that delivers a behavior removes its test's expected-failure marker.
- Add a dependency without checking that it exists, is maintained, and is pinned in the lockfile.
- Rewrite large areas when a smaller change meets the goal.

## Definition of done
Acceptance criteria met and checked against the running software · new tests added and all existing tests passing, from a fresh run · lint, typecheck and boundary checks clean · reviewed by a fresh agent · docs and `docs/project/state.md` updated{{ · tier extras, e.g. "security review for auth changes"}}
