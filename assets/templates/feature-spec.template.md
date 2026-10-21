# Feature: {{Name}}

- Status: {{Draft | Approved | Built | Dropped}}
- Requirements: {{FR IDs}} · Milestone: {{Mn}}
- Material change? {{No | Yes — ADR-NNNN}}

## Goal
{{What the user can do after this ships, and why it matters.}}

## Behavior
{{What the user sees and does, step by step. Use glossary terms.}}

## Acceptance criteria
- Given {{situation}}, when {{action}}, then {{observable result}}.
- Given {{error or edge case}}, when {{action}}, then {{result}}.

## Design
- Components and files affected: {{list}}
- Data changes: {{new fields or tables, migrations, backfill}}
- Permissions: {{who may do this; how it is enforced}}

## Out of scope
- {{What this feature deliberately does not do}}

## Test plan
- {{Unit, integration and end-to-end tests that prove the acceptance criteria}}

## Risks
- {{What could go wrong and how we would notice}}
