# Architecture

> Purpose: the current, approved structure of the system. Binding for all changes. Update in the same change that alters it. Owner: {{lead engineer}}, with human approval for material changes.

## Summary
{{One paragraph: the architecture style and its main parts, and why this shape fits the requirements.}}

```mermaid
flowchart LR
  user[{{Users}}] --> app[{{App}}]
  app --> db[({{Database}})]
  app --> ext[{{External service}}]
```

## Components and boundaries
| Component | Responsibility | Owns data | May call | Must not |
|---|---|---|---|---|
| {{Component}} | {{What it does}} | {{Tables or stores}} | {{Allowed dependencies}} | {{Forbidden shortcuts}} |

{{How these boundaries are enforced automatically, e.g. an import-boundary lint rule or structural test.}}

## Code layout
{{The folder layout by feature (references/codebase-design.md › Skeletons in the Masterplan skill): where features, shared platform code, adapters for external services, and tests live; which imports are forbidden.}}

## Data model
{{Main entities, relationships, and the tenancy rule if multi-tenant (e.g. "every table has organization_id; every query is scoped by it").}}

## Key flows
1. {{The two or three flows that matter most, step by step.}}

## Security model
- Sign-in: {{identity provider and methods}}
- Permissions: {{roles and where checks happen}}
- Tenant isolation: {{mechanism and how it is tested, or "single-tenant"}}
- Secrets: {{where they live; who can read them}}
- Top threats and mitigations: {{3–5 lines}}

## Environments and deployment
| Environment | Purpose | Data | Who can deploy |
|---|---|---|---|
| Local | Development | Fake or seed data only | Developers and agents |
| {{Preview / staging}} | {{Review each change}} | {{Seed or branch data}} | {{CI}} |
| Production | Real users | Real data; agents have no access | {{CI after human approval}} |

## Operations
- Monitoring and alerts: {{errors, uptime, key metrics; who is notified}}
- Backups and restore: {{frequency, retention, location, last tested}}
- Releases and rollback: {{how a bad release is undone}}

## Cost
{{Monthly estimate at launch and at the growth target, the assumptions, the biggest cost driver, free-tier cliffs, and the date prices were checked.}}

## Scaling path
{{What would change at 10× and the trigger to act. Do not build it now.}}

## Binding decisions
| ADR | Decision | Status |
|---|---|---|
| [ADR-0001](decisions/0001-{{slug}}.md) | {{Decision}} | Accepted |

## Review log
| Date | Finding (source) | Resolution |
|---|---|---|
| {{YYYY-MM-DD}} | {{Finding and which review raised it}} | {{Changed / rejected because / accepted risk}} |
