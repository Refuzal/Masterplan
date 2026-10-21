# Roadmap

> Purpose: what gets built in what order, and how each milestone is accepted. Each milestone gets an implementation plan in `docs/plans/` when it starts. Update when a milestone finishes or scope moves. Owner: {{product owner}} with {{lead engineer}}.

## M0 — Safe to build
Goal: make it safe for AI agents and people to change this repository. Light projects keep this short (an hour or two).
- [ ] Code in a private repository; secrets are git-ignored and live in {{secret store}}, never in code or docs
- [ ] Agents cannot reach production credentials or production data; backups or an undo exist outside the agent's reach
- [ ] Billing alerts on every paid service (free-only setups: no payment method on file)
- [ ] One command runs every check (format, lint, typecheck, boundary rules, tests); its fast part runs before each commit (a git hook) and the whole command before every merge and before anything goes live: {{Light: the deploy command runs it first · Standard and Critical: CI on every pull request also runs the dependency audit and secret scanning, and main is protected}}
- [ ] Project skeleton with the folder layout from architecture.md, boundary rules enforced by a lint step, and one passing test
- [ ] {{With a relational database: a migration linter in the check command (for example Squawk on the generated SQL for PostgreSQL)}}
- [ ] Guardrails tested: a planted boundary violation prints its fix text; variants of each blocked agent command were tried and what is and is not stopped is recorded
- [ ] {{Unverified facts from the ADRs re-checked, if any}}
Owner tasks: {{accounts and settings only the owner can create, as a plain checklist, or "None"}}
Verification: {{e.g. a deliberately broken change fails to go live; a planted fake secret is blocked}}

## M1 — Walking skeleton
Goal: the thinnest end-to-end slice through every layer, deployed through the real pipeline (or, until the owner's accounts exist, run locally through the same checks). It proves the stack early, when changing it is cheap, and gives agents a working pattern to copy.
Scope: {{e.g. sign in → page that reads and writes one record → deployed to a preview environment}}
Acceptance criteria:
- Given {{situation}}, when {{action}}, then {{result}}.
Verification: {{commands, checks, what a human looks at}}
Demo: {{what the owner will try, and how}}
Also delivers: a plain-language `README.md` (what it is; install, start, stop, back up; who to ask), which the owner follows for the demo
Depends on: M0

## M2 — {{First real capability}}
Scope: {{FR-1, FR-2}}
Acceptance criteria: see {{requirements.md FR-1, FR-2}}
Verification: {{how we know it works}}
Demo: {{what the owner will try, and how}}
Depends on: M1

## Later
- {{Deferred capabilities, in rough priority order}}

## Decision map (Large scale or multi-team projects; delete otherwise)
- Decided: {{decision → link to ADR or requirement}}
- Not yet specified: {{questions you can see coming but cannot answer yet, and the milestone that needs each}}
- Out of scope: {{what this product will not do}}
- Workstreams: {{name → owner → branch → which milestones}}
