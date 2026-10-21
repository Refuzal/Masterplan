# Plan: {{Milestone ID and name}}

> Purpose: the implementation plan for one milestone, written before coding and executed task by task (references/build-loop.md in the Masterplan skill). It records decisions; implementers write the code. Tick steps as they finish.

**Goal:** {{one sentence: what works for users when this milestone is done}}
**Approach:** {{two or three sentences}}
**Implements:** {{FR and NFR IDs}} · **Binding decisions:** {{ADR links}} · **Roadmap:** {{link to the milestone}}

## Global constraints
{{Binding rules for every task, copied verbatim from AGENTS.md, ADRs and requirements: versions, tenant scoping, naming, limits, exact copy text. One line each. Multi-tenant: "every tenant-owned table has tenant_id, row-level security and composite (tenant_id, id) foreign keys".}}

## Review focus
{{The five inputs or conditions most likely to break this for a real person that no requirement spells out. One line each: the condition and the behavior a reasonable user expects. Each line's test is added to the task that owns the code.}}
1. {{e.g. two clients book the same slot at the same moment → one succeeds, the other sees the slot is taken}}

## Acceptance tests
**Author:** {{coordinator | a fresh agent that implements no task | inline: written before any task code}}
Acceptance commit: {{short SHA of the commit that adds them}}
{{One per acceptance criterion, committed under tests/acceptance/ before Task 1, each pending (strict expected-failure marker) until its task removes the marker. Milestone 0: "The roadmap's verification checks serve instead."}}
- {{criterion}} → `{{test file and name}}` → pending until Task {{N}}

## File map
{{Files to create or change, each with its one responsibility, grouped by feature.}}
- `{{path}}` — {{responsibility}}

## Tasks

### Task 1: {{title}}
**Blocked by:** {{none | Task N}}
**Files:** create `{{path}}` · change `{{path}}` · test `{{path}}`
**Interfaces:**
- Consumes: {{exact names and types from earlier tasks, or "none"}}
- Produces: {{exact names, parameters and return types later tasks rely on}}
**Test seams:** {{the public interfaces these tests drive}}
**Covered by existing tests:** {{tests that already exercise the files this task changes, or "none"}}

- [ ] **Write the failing test** `{{test name}}`: {{assertions with the exact values}}
```{{language}}
{{test code, or its name and assertions when the shape is obvious}}
```
- [ ] **Run it and see it fail:** `{{command}}` → fails because {{expected reason}}
- [ ] **Implement** `{{signature}}` in `{{path}}`. {{One line on the approach only when the signature and test leave a real choice.}}
- [ ] **Run focused test, then the fast check and this task's acceptance tests:** `{{commands}}` → all pass, output clean
- [ ] **Commit:** `{{type}}: {{message}} ({{FR-ID}})`

## Verification for the milestone
- [ ] Full suite, lint, typecheck and build pass: `{{commands}}`
- [ ] Acceptance tests all pass with no pending markers left, unchanged since they were committed apart from marker removals (or by a recorded ruling)
- [ ] Each acceptance criterion also exercised on the running app: {{criterion → what was done and seen}}
- [ ] Coverage audit: every requirement in scope maps to a passing test; any that does not is listed as unverified
- [ ] App starts and the main path works: `{{command}}`, then {{what to do}}
- [ ] `check_foundation.py --phase building` reports no FAIL
- [ ] Milestone review done; findings fixed or ruled

## Owner tasks
{{Steps only the owner can do for this milestone, as a numbered plain-language checklist, or "None".}}
