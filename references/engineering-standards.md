# Engineering standards

A proportionate baseline for how the project is built, checked, shipped and run. Fill `docs/engineering/standards.md` from this (Light: put the essentials in AGENTS.md instead). Prefer rules a tool enforces over rules people must remember. How code is organized is in codebase-design.md, how it is tested in testing.md, and how each milestone is built and reviewed in build-loop.md.

Contents: Baseline by tier · AI-agent harness · Make the architecture enforceable · Add controls when

## Baseline by tier

| Area | Light | Standard | Critical (adds to Standard) |
|---|---|---|---|
| Source control | Git in a private repository; commit often; the deploy command runs the tests first; a secret scanner (for example gitleaks) in the pre-commit hook | Protected main; pull requests; CI must pass; one human approval | Two approvals on security-sensitive paths; signed commits if policy requires |
| Quality gates | Formatter, linter, and a strict typecheck where the language has one (a plain-JavaScript learner project may skip it; record why in an ADR); the folder layout from the architecture with its main boundary rule checked by a lint rule or a short script | + tests, dependency audit, secret scanning, static security analysis; prefer the platform's built-in scanners (for example GitHub's Dependabot, secret scanning and CodeQL default setup) over separate tools | + duplication and coverage limits on new code; mutation score on core logic; license check |
| Testing | Tests for core logic and the main flow | Unit tests for logic; integration tests against a real database; end-to-end tests for key journeys; authorization tests per role | + cross-tenant isolation tests; property-based tests for core rules; regular restore and failover tests |
| Environments | Local + production | Local, preview per pull request, production; seed data only outside production | + staging that mirrors production; production access audited |
| Secrets and access | Environment variables, never in the repo | Platform secret store; least privilege; no shared accounts | + rotation schedule; access reviews; separate admin identities |
| Data and migrations | Migrations in version control | Reviewed migrations; backup before destructive changes; rollback plan | + data classification; encryption beyond provider defaults where required; retention enforcement |
| Security baseline | Server-side permission checks; validated inputs; dependency updates | + security headers, rate limits, audit of sign-in and admin actions | + threat model, penetration test before launch, incident response plan |
| Observability | Error tracking | + structured logs, uptime checks, alerts to a named person | + service objectives, dashboards, on-call |
| Backups and recovery | Provider backups on | Daily backups kept 30 days, stored where agents cannot reach; one tested restore before launch | Point-in-time recovery; quarterly restore drills; documented recovery time |
| Releases | Deploy from main | Preview first; feature flags for risky changes; one-step rollback | + staged rollouts; change records |
| Accessibility and performance | Readable, keyboard-usable | WCAG 2.2 AA for public UI; performance budget on key pages | + accessibility audit; load test at expected peak |
| Cost | Billing alert, or no payment method on file for free-only setups | Alerts on every paid service; monthly review | + per-tenant or per-feature cost tracking |

Scale adds to the tier (discovery.md › Scale): a Large project takes the Critical column's observability, releases, performance and backup rows, plus per-tenant cost tracking, whatever its data; a Medium project takes the Medium rung of codebase-design.md › The scale ladder.

Fit the baseline to whoever builds and runs the project (fork F5). Every control should be something that person can set up in Milestone 0 and keep running; when one is not, choose a managed or simpler equivalent, or drop it and record the risk. A weekend builder's Milestone 0 takes an hour or two.

## AI-agent harness

The documented failures of AI-built software come from the environment around the agent more than from the agent's code. The widely reported agent incidents share the same causes: over-broad credentials, no separation between test and production, backups within the agent's reach, and no outside approval for destructive actions. Examples: an agent that deleted a startup's production volume and its backups in one call ([OECD incident record](https://oecd.ai/en/incidents/2026-04-27-6153)), the Replit agent that deleted a production database during a declared code freeze ([CIO](https://www.cio.com/article/4230232/the-replit-case-an-agent-a-written-order-and-a-deleted-database.html)), and a reported 13-hour AWS outage involving its Kiro agent, which AWS attributes to a misconfigured role rather than the AI ([Computing, 2026](https://www.computing.co.uk/news/2026/ai/aws-blames-user-error-not-ai)). Model quality does not fix this: AI-generated code has passed security tests only about 56% of the time in Veracode's 2025 and 2026 benchmarks, unchanged across model sizes ([Veracode 2026](https://www.veracode.com/news/llms-are-getting-smarter-but-not-safer-veracode-2026-genai-code-security-report-finds-ai-generated-code-security-has-stalled-at-56%25-pass-rate/)).

So the harness goes in before the features (roadmap Milestone 0):

1. **Contain the blast radius.** Agents run in a sandbox with file and network limits; production credentials and data are unreachable from it (separate credentials per environment, and no agent ever holds production write access); backups live off the production volume, where the agent's credentials cannot delete them, and one restore has been tested; destructive commands are blocked by the agent's deny rules or hooks and need human approval outside the agent. Instructions are not controls: in the recorded incidents the agent had been told not to. Deny rules and git hooks are pattern matches, not a security boundary (`git commit --no-verify`, `git -c core.hooksPath=…` or a shell wrapper slip past them), so back every rule that must hold with something the agent cannot change: a required CI status and protected main, credentials it does not have, or a deploy script that refuses on a failed check. In Milestone 0, try variants of each blocked command and record what is and is not stopped; never describe the settings as blocking more than they do.
2. **Deterministic gates.** One check command runs formatting, typecheck, lint, boundary rules and all tests, including acceptance and browser tests. A pre-commit hook runs the fast part of it (everything except slow browser tests, when they make commits sluggish), so a broken commit never lands even before CI exists; the full command runs before every merge and demo, and CI runs it plus the dependency audit, secret scanning and static security analysis on every pull request. A gate the agent cannot argue with beats an instruction it might ignore.
3. **Supply chain.** Install only from the committed lockfile (`npm ci`, `pnpm install --frozen-lockfile`, `uv sync --locked`); check that new packages exist, are maintained and come from the expected publisher, and record each new dependency as a reviewed decision (build-loop.md › Execute; the owner approves only those with a cost, a restrictive license or access to user data); where the package manager supports it, refuse versions published in the last day or so (pnpm's `minimumReleaseAge`, for example), which blocks most hijacked releases before anyone installs them. Models invent package names a few percent of the time, and attackers register them ([arXiv 2605.17062](https://arxiv.org/abs/2605.17062)). Turn on the host's secret push protection for the repository; it is not on by default for private repositories.
4. **Tests that bite.** Agent-written pull requests often change code without updating its tests ([arXiv 2607.18057](https://arxiv.org/abs/2607.18057)). Require tests with every change and forbid weakening tests to pass; for Critical, add mutation testing on core logic, which Thoughtworks recommends specifically for AI-written tests ([Technology Radar](https://www.thoughtworks.com/radar/techniques/mutation-testing)).
5. **Small, reviewed changes.** One task per agent session, one milestone per branch, and pull requests small enough to review; a human approves merges for Standard and Critical (a non-technical owner approves after trying the change in a preview, with the independent AI reviews as the code check). An AI reviewer from a different model family is a useful extra check, not a replacement.
6. **Learn from mistakes.** When an agent repeats a mistake, turn it into a lint rule, hook or test rather than another paragraph of instructions.

## Make the architecture enforceable

Agents copy the patterns they find, and drift where nothing stops them. Write the important boundaries as automated checks:
- Import-boundary rules (for example an ESLint boundaries rule, dependency-cruiser, or import-linter for Python) for "UI must not touch the database" style rules.
- A single data-access module that applies tenant scoping, plus a test that fails if a query bypasses it.
- Strict type settings and schema validation at every boundary (requests, webhooks, AI outputs).
- Generated files and migrations marked so agents do not hand-edit them (for example `linguist-generated` in `.gitattributes`, and a CI step that regenerates and fails on a difference).
- A migration linter in CI where one exists for the database (Squawk for PostgreSQL, or Atlas's analyzers), so locking or destructive migrations are caught before they run.
- Lint error messages that say how to fix the problem, so the agent can correct itself.

## Add controls when

| Trigger | Add |
|---|---|
| First real users | Error tracking alerts, uptime check, tested restore |
| First paying customer | Rate limits, audit of admin actions, status page or contact route, billing failure handling |
| Personal data | Privacy notice, data export and deletion, retention rules, access logging |
| First business customer | Role-based access, audit log, security questionnaire answers, single sign-on plan |
| Second engineer or second agent working in parallel | Code owners, branch protection with required reviews, shared conventions in AGENTS.md |
| Regulated data or contractual uptime | Move to the Critical tier: threat model, operations runbooks, professional review |
| Hundreds of tenants, tens of thousands of users, or customers paying for uptime | Move to Large scale: operations.md with service objectives and on-call, threat model, load test at expected peak, staged rollouts, per-tenant quotas and cost tracking |
| A second team, or work split into parallel workstreams | Module owners, contract tests between modules, an integration branch with its own review (build-loop.md › Large projects) |
| AI features in production | Evaluation set in CI, spend caps, output logging with redaction |
