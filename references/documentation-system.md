# Documentation system

The repository, not the conversation, is the project's memory. These rules keep it small, current and trustworthy for any agent.

Contents: Files by tier · Rules for every document · Tags · AGENTS.md and CLAUDE.md · ADRs · Glossary · state.md · Writing during discovery · Keeping docs true during the build · Growing the docs · Never store

## Files by tier

Templates live in this skill's `assets/templates/` folder. Copy the shape, fill it with project facts, and delete guidance text; anything left in `{{double braces}}` is flagged by the checker.

| File | Purpose | Light | Standard | Critical | Template |
|---|---|---|---|---|---|
| `AGENTS.md` | Short, agent-independent instructions and map | ✓ | ✓ | ✓ | AGENTS.template.md |
| `CLAUDE.md` | Imports AGENTS.md for Claude Code; Claude-only notes | ✓ | ✓ | ✓ | CLAUDE.template.md |
| `docs/project/overview.md` | Problem, users, scope, non-goals, constraints, glossary | ✓ + requirements, architecture, roadmap, risks sections | ✓ | ✓ | overview.template.md |
| `docs/project/state.md` | Where things stand; next actions | ✓ | ✓ | ✓ | state.template.md |
| `docs/architecture/decisions/NNNN-title.md` | One ADR per material decision | ✓ (usually 2–4) | ✓ | ✓ | adr.template.md |
| `docs/project/requirements.md` | Functional and measurable non-functional requirements, data, integrations, obligations | in overview | ✓ | ✓ | requirements.template.md |
| `docs/architecture/architecture.md` | Current approved structure, security model, environments, operations, cost, review log | in overview | ✓ | ✓ | architecture.template.md |
| `docs/project/roadmap.md` | Milestones with acceptance criteria and verification | in overview | ✓ | ✓ | roadmap.template.md |
| `docs/project/risks.md` | Open questions, assumptions, risks, accepted risks | in overview | ✓ | ✓ | risks.template.md |
| `docs/engineering/standards.md` | Quality gates, testing, security baseline, agent guardrails | in AGENTS.md | ✓ | ✓ | standards.template.md |
| `docs/engineering/security.md` | Data classification, threat model, controls, compliance mapping | — | Large scale | ✓ | security.template.md |
| `docs/engineering/operations.md` | Service objectives, alerts, runbooks, on-call | — | Large scale | ✓ | operations.template.md |
| `README.md` | For people: what the app is, and in plain words how to install, start, stop, back up and restore it, reset a password, and where to get help. Written in Milestone 1, kept current each milestone; the owner should be able to run the app from it alone | ✓ | ✓ | ✓ | — |
| `docs/plans/<milestone>.md` | The milestone's implementation plan, written at the start of each milestone | ✓ (short) | ✓ | ✓ | plan.template.md |
| `docs/features/<name>.md` | A feature spec, when a feature needs more than its plan and requirements say | as needed | as needed | as needed | feature-spec.template.md |
| `.masterplan/<milestone>/` | Git-ignored scratch for the build: ledger, task briefs, reports, review packages | build | build | build | — |

Light keeps one overview file with `## Requirements`, `## Architecture`, `## Roadmap` and `## Risks` sections, shaped like the matching templates but shorter. The Light target is four core files (AGENTS.md, CLAUDE.md, overview.md, state.md) plus two to four short ADRs.

## Rules for every document

1. **Purpose first.** The first lines say what the document is for, when to update it, and who owns it.
2. **One home per fact.** Say it once; link to it elsewhere. Duplicated facts drift apart and agents follow the stale copy.
3. **Current state, not history.** Documents describe the system as it is now. History lives in git and in superseded ADRs.
4. **Tag what is not confirmed** (below).
5. **Short.** AGENTS.md about 100 lines at most; CLAUDE.md a few lines; state.md under about 60; other documents under about 300. Past that, split by component or topic. The checker warns at 100 (AGENTS.md), 60 (CLAUDE.md), 80 (state.md) and 500 (other documents). For the whole foundation, stay under about 5,000 words for Light, 15,000 for Standard and 20,000 for Critical; when it runs long, cut repetition first (rule 2).
6. **Dates as YYYY-MM-DD.** Sources get the date they were checked.
7. **Written for a capable newcomer.** Plain words, the glossary's terms, no chat references ("as discussed above").

## Tags

Untagged statements are confirmed. Tag everything else inline:
- `[Assumption]` — a default you chose; reversible; the user has been told.
- `[Proposed]` — recommended, waiting for approval.
- `[Open]` — unknown, not blocking the next milestone.
- `[Blocking]` — unknown and must be resolved before handoff (use [Open] for anything that can wait until a later milestone, and name that milestone).

Never turn a guess into an untagged statement. When a tagged item is resolved, remove the tag and update the text in the same edit. A tag may carry a short note (`[Assumption: owner to confirm]`); the checker counts those too.

## AGENTS.md and CLAUDE.md

AGENTS.md is loaded into every agent session, so every line costs attention in every future task. Include only what an agent cannot quickly discover and must not get wrong:
- one-line purpose and a pointer to state.md;
- a map of the docs;
- the stack in one line, linked to ADRs;
- exact commands (or a note that Milestone 1 defines them);
- 3–7 binding, project-specific rules, including hard constraints agents must not loosen on their own (budget ceiling, where data may live, compliance duties, non-goals);
- how to work, change control, a Never list, and the definition of done.

Write it from the project's decisions, not by summarizing the repository. Leave out generic advice ("write clean code"), anything a linter or formatter enforces, and long explanations: link to the document instead. Research on context files found that broad repository overviews do not improve agent success while adding cost ([arXiv 2602.11988](https://arxiv.org/abs/2602.11988v1)); project-specific, non-obvious rules are what help.

CLAUDE.md exists for Claude Code: recent versions read AGENTS.md only when no CLAUDE.md is present, and older versions not at all. A CLAUDE.md whose first line imports AGENTS.md (`@AGENTS.md`) works in every version and leaves room for Claude-only notes below it. Never duplicate AGENTS.md content into it. Other agents differ too (Gemini CLI, for example, must be configured to read AGENTS.md); if the team uses one, add that agent's pointer file or setting rather than copying the rules.

If the repository already has either file: read it, keep its valid rules, propose the merged version to the user, and apply it only after they agree.

## ADRs

- One file per material decision in `docs/architecture/decisions/`, named `NNNN-short-title.md` with numbers that never repeat.
- Required: Status, Date, Decided by, Context, Options considered, Decision, Why, Consequences, Evidence, Revisit when.
- Status is one of Proposed, Accepted, Superseded by ADR-NNNN, Deprecated, Rejected. Only Accepted ADRs bind.
- "Decided by" records whether the owner decided, approved it as part of the package, delegated ("I'm not sure"), left it as an engineering default they never saw, or found it pre-existing in the codebase. Name the owner only for choices they actually saw.
- To change a decision, write a new ADR that says "Supersedes: ADR-NNNN", and set the old ADR's status to "Superseded by ADR-MMMM". Leave the old ADR's text alone otherwise; it is the history. Update architecture.md so it shows only the current decision.
- Exception while planning (before any building): review findings that refine an Accepted ADR without reversing it may be edited in place; log each edit in the Review log. If only a fact in an ADR's Context goes stale while the decision stands, add a dated "Updated:" line rather than superseding it.
- What deserves an ADR: a decision that is hard to reverse, would surprise a future reader without its reasons, and came from a real tradeoff. Typically language and framework, data store, tenancy model, sign-in provider, hosting, AI architecture, major integrations, and deliberate departures from the obvious path. Not: library choices a five-minute change could swap, or the obvious default with no real alternative; record those in one line in architecture.md (Light: the overview's Architecture section).

## Glossary

The glossary (in overview.md; one section per module, or one file per module, in large systems) holds the project's domain terms, one or two sentences each, with the synonyms to avoid:

> **Client**: a pet owner who books appointments with a groomer. _Avoid_: customer, user (a user is anyone who signs in).

Only terms specific to this project; never implementation details. When the user's words are vague or overloaded ("account" meaning both a company and a person), propose one precise term and record it. Code, database names, API names and UI text use these terms exactly.

## state.md

The first file any agent reads. Keep it under about 60 lines and current:
- `Phase:` planning, ready, building or maintenance; `Tier:` Light, Standard or Critical; `Last updated:` date and by whom. The checker reads these lines.
- Now: current milestone and what is in progress.
- Next actions: at most five, in order, each small enough to start immediately.
- Recently done: the last five or so, with dates.
- Blockers and open questions, linked to risks.md.
- During planning only: the Planning progress table (the decision ledger). At handoff, set every row to its final status. When building starts, replace the table with the Build section: current milestone, its plan file, its ledger path, and the last verified test run (command, result, date).
- When several agents work in parallel, give each its own line under "In progress" and have each edit only its own lines in small edits; one coordinator (a person or a lead agent) owns Next actions. This keeps parallel updates from overwriting each other.

## Writing during discovery

Persist as you go, so nothing depends on the conversation surviving.

1. Once the idea, users and tier are clear (usually after three to five answers), create the core files: AGENTS.md, CLAUDE.md, overview.md and state.md. Create each of the tier's other files when its first real content arrives, rather than as empty stubs.
2. After each answer, make one small edit: record the answer in its home document and update its ledger row in state.md. That alone means nothing is lost if the session ends, and it keeps each turn quick.
3. At four checkpoints, do the full consistency pass: write or update the ADRs, then follow the ripple map (lifecycle.md) to fix every dependent document. The checkpoints are when the forks are settled, when the architecture package is approved, before the review, and after the review. Never append a contradicting line; rewrite the outdated one. For every fact that changed (a number, a provider, a limit, a rule), search all the documents for the old value and fix each occurrence; stale copies of numbers are the most common inconsistency.
4. Keep edits focused. Never overwrite unrelated existing files. During planning, checker warnings about sections not yet written are expected; only FAILs need fixing before handoff.
5. Tell the user what you recorded in one line, not the file contents.

## Keeping docs true during the build

- The milestone plan is committed and its checkboxes ticked as tasks finish; the git-ignored ledger holds the working detail.
- At the end of each milestone (build-loop.md › Record and integrate): update state.md and the roadmap, replace AGENTS.md placeholders with the real commands, update architecture.md and the glossary for anything the code changed, and turn rulings that changed a decision into ADRs.
- When code and docs disagree, the code is the truth about what exists and the Accepted ADRs are the truth about what should exist: fix the doc, or fix the code that broke a decision.

## Growing the docs

- When a component becomes complex, give it `docs/architecture/components/<name>.md` and link it from architecture.md.
- For rules that apply to one part of the code: put a short AGENTS.md in that folder, and keep anything critical in the root AGENTS.md as well, because support for nested files varies (Cursor and Copilot read them; Codex reads only those between the repository root and its working folder). For Claude Code, add a CLAUDE.md in that folder that imports the nested AGENTS.md (it loads when Claude works on files there), or a rule file under `.claude/rules/` with a `paths:` list.
- Split engineering standards by topic once they pass about 300 lines.
- Delete documents that are no longer true rather than letting them rot. Superseded ADRs are the exception: they stay, clearly marked.

## Never store

Secrets, credentials, tokens or private keys; real personal or customer data; chat transcripts or transient observations; unapproved ideas presented as decisions. The checker scans for common secret formats, but it is a safety net, not permission.
