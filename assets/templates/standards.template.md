# Engineering standards

> Purpose: how code is written, checked, shipped and run in this project, sized for tier {{Tier}}. Update when a practice changes. Owner: {{lead engineer}}.
> Prefer rules a tool can enforce over rules people must remember. Each rule names its check.

## Source control and review
- {{e.g. main is protected; every change arrives by pull request with passing CI and one human approval}}

## Quality gates (must pass before merge)
| Gate | Tool | Runs where |
|---|---|---|
| Format and lint | {{tool}} | {{pre-commit hook + CI}} |
| Typecheck | {{tool, strict mode}} | CI |
| Tests | {{tool}} | CI |
| Dependency audit and secret scan | {{tool}} | CI |
| {{Standard+: static security analysis · Critical: duplication limit, mutation score on changed core logic}} | {{tool}} | CI |

## Testing
- {{What gets unit, integration and end-to-end tests; where tests live; test data rules (no real personal data)}}

## Architecture enforcement
- {{The boundary rules from architecture.md and the tool that enforces them}}

## Environments and configuration
- {{Environments, configuration via environment variables, how secrets reach each environment}}

## Data and migrations
- {{Migrations in version control and reviewed; forward-only; backup before destructive changes}}

## Security baseline
- {{Server-side authorization on every request; input validation at boundaries; dependency updates; security headers}}

## Observability
- {{Error tracking, structured logs, uptime checks, what alerts and who receives them}}

## Backups and recovery
- {{Schedule, retention, storage location out of agent reach, restore drill frequency}}

## Releases and rollback
- {{How releases go out, feature flags if used, how to roll back}}

## AI-agent guardrails
- Agents work in a sandbox with no production credentials and no access to production data.
- Destructive actions (data deletion, force-push, infrastructure apply) need explicit human approval.
- New dependencies are checked for existence, maintenance and license before they enter the lockfile.
- Tests may not be weakened to make them pass; repeated agent mistakes become a lint rule, hook or test.
- {{Tier-specific additions, e.g. a second model reviews every pull request}}

## Add these controls when…
| Trigger | Add |
|---|---|
| {{e.g. first paying customer}} | {{e.g. tested restore, uptime alerts, on-call contact}} |
