# Architecture review

Independent stress-testing of the plan before anyone builds it.

Contents: When · Self-review (Light) · Review panel (Standard and Critical) · Synthesis · Cold-start test

## When
Run the review after the draft foundation exists: overview, requirements, architecture, ADRs and risks. Reviewers read files, so the docs must be written first. That is deliberate: if a reviewer who never saw the conversation cannot follow the plan, the docs are not good enough yet.

## Self-review (Light, or when subagents are unavailable)
Run each lens yourself and write down what you find. Tell the user it was a single-agent self-review, not independent reviewers.

- **Fit:** does every part trace to a requirement? Anything unjustified?
- **Simplicity:** what could be removed without breaking a requirement?
- **Security:** sign-in, permissions, data exposure, secrets, dependencies.
- **Data:** what happens if the database is lost? Is restore possible and tested?
- **Cost:** monthly at launch and at the growth target; the biggest driver.
- **Operations:** how will anyone know it is broken, and who fixes it?
- **AI-readiness:** could a fresh agent build Milestone 1 from the docs alone?
- **Pre-mortem:** it is twelve months later and the project failed. What are the three most likely reasons, and what in the plan prevents each?

## Review panel (Standard and Critical)
Spawn three subagents in parallel, in the same turn, with whatever subagent tool the environment provides (for example the Agent or Task tool, general-purpose type). Give each only the project root path and its brief. Do not pass the conversation or your own conclusions; independence is the point. If the environment lets you choose a different model for one reviewer, do it for the security reviewer: different models have different blind spots (a reasonable inference, not a proven effect). Record in the Review log how each reviewer ran (subagent or headless session, and the model if you set one); claim a different model only when you set one.

If you have no subagent tool but a `claude` command-line tool is available, separate headless sessions restricted to read-only tools work as independent reviewers.

Common instructions for every reviewer (include them in each prompt):

> You are reviewing a software plan before any code is written. Read AGENTS.md and everything under docs/ in [project root]. Do not modify any files. Use web search to check facts that may have changed (versions, maintenance status, pricing, licensing) where it matters.
> Report at most 12 findings, most important first, each as:
> `[Blocker | Material | Minor] [area] Finding — why it matters (evidence or reasoning, with links where you checked) — recommended change — confidence High/Medium/Low`
> Then: up to 3 things that are right and should not change, and up to 3 questions only the product owner can answer.
> Also report anything you could not understand from the docs alone; that is itself a finding.
> Keep the whole report under 600 words.

**Reviewer 1 — Technology and architecture.** Do the language, frameworks, data design and integrations fit the requirements? Are they current, maintained, licensed compatibly and compatible with each other? Is anything immature or unnecessary? Were credible alternatives considered? Are boundaries clear enough that coding agents will keep them? Is the stack well suited to AI-assisted development (types, mainstream conventions, fast tests)?

**Reviewer 2 — Infrastructure, operations, scale and cost.** Will hosting and deployment meet the non-functional requirements? Check the cost estimate against current pricing and find cost cliffs. Are backups, restore, monitoring, alerting and rollback adequate for the tier? What breaks first at 10× load? Is the operational burden realistic for the team named in the overview?

**Reviewer 3 — Security, maintainability and critical review.** Model the threats: who could misuse what, and how (sign-in, permissions, tenant isolation, data exposure, secrets, supply chain, AI-specific risks such as prompt injection). Look for over-engineering, unsupported assumptions, contradictions between documents, and technical debt the plan creates. Run a pre-mortem: assume the project failed within a year and give the three most likely causes.

Critical tier: if any Blocker was found, fix the docs and run Reviewer 3 again on the revised version.

## Synthesis
1. Merge duplicate findings. Weigh evidence and severity, not the number of reviewers who said it.
2. For each finding choose one: **accept** (change the docs), **reject** (record why), or **escalate** to the user (only for a tradeoff they own or a Blocker that needs their decision). Findings in areas the decision ledger gives to you (security baseline, testing, operations, architecture inside the approved package) are yours to settle: list them under "what the review changed" so the owner can object, rather than asking.
3. When reviewers disagree, decide explicitly which evidence wins and say why.
4. Reviewers tend to add controls. Before accepting a finding that adds a service, vendor account, tool or recurring chore, check it against who builds and runs the project (overview, fork F5): accept it when it closes a real risk at this tier and that person can run it; otherwise record it in risks.md with an "add when…" trigger tied to growth ("at 20 paying customers", "when someone else gets admin access"). Prefer the platform's built-in feature (its backups, logs, alerts, code scanning) over a new vendor, or an account the owner already has. Size the control to the tier's row in engineering-standards.md: a Critical-tier control (quarterly restore drills, custom encrypted backup schedules) in a Standard project needs a named risk it closes at the current stage.
5. When a finding changes something the owner already approved (a monthly cost, an account, a recurring chore, a date), list it under "what the review changed" as old → new. Never let an approved number change silently.
6. Update the affected docs so they describe the corrected plan, searching every document for each changed fact's old value and every reference to an ID you removed (the checker flags dangling IDs). Log each material finding and its resolution in architecture.md › Review log (Light: in the overview's Risks section).
7. Tell the user, in at most five bullets, what changed because of the review, then ask the escalated questions (up to three in one round). If you downgrade a reviewer's Blocker, record why in the Review log.

## Cold-start test
Proves that a new agent can pick up the project from the repository alone. Required for Standard and Critical before handoff; optional for Light.

For Light, cover it inside the self-review's AI-readiness lens instead of a separate test.

Spawn one fresh subagent with only the project root and this prompt:

> You are joining this project with no other context. Using only the files in [project root], and without asking questions, answer each item in two or three sentences and cite the file each answer came from:
> 1. What are we building, and for whom?
> 2. Why: what does success look like?
> 3. How is it structured: the main parts and their boundaries?
> 4. Which decisions are binding?
> 5. What is implemented so far?
> 6. What remains, in order?
> 7. What exactly should you work on next, and what is the first step?
> 8. How do you validate a change: commands, tests, and the definition of done?
> Then list anything that was missing, ambiguous or contradictory.
> Finally, as the engineer who will build Milestone 1, list every question you would need answered before you could start it with confidence.

Compare the answers with what you intended. Every wrong, missing or hedged answer points to a doc that needs fixing. Fix it, then re-run the test if the gap was serious.

Then handle the builder's questions: answer each one you can from research or sound defaults, and write the answer into the right document. Bring only the questions the user must own to the user, in a single round. Without subagents, do the same exercise yourself by reading only the files, and say you did it that way.
