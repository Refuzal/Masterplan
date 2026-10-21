"""Build fixture projects for testing check_foundation.py."""
import shutil
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "checker-fixtures"


def write(root, files):
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.lstrip("\n"), encoding="utf-8")


AGENTS = """
# AGENTS.md — PawBook

Online booking and reminders for independent dog groomers, sold as a subscription.

Start every session by reading `docs/project/state.md`.

## Map
- Product, users, scope, glossary: `docs/project/overview.md`
- Requirements: `docs/project/requirements.md`
- Architecture: `docs/architecture/architecture.md`
- Decisions: `docs/architecture/decisions/`
- Roadmap: `docs/project/roadmap.md` · Risks: `docs/project/risks.md`
- Engineering standards: `docs/engineering/standards.md`

## Stack
TypeScript (strict) · Next.js · PostgreSQL via Drizzle · Vercel + Neon ([ADR-0001](docs/architecture/decisions/0001-stack.md))

## Commands
Defined in Milestone 1 — fill in when the project is created.

## Binding rules
1. Every table has `salon_id`; every query is scoped by it through `src/server/db/scoped.ts`.
2. UI components never import from `src/server/db`.

## How to work
1. Read the relevant docs, then the code.
2. Small changes, tests first.

## Change control
Material changes need an ADR with status Proposed and human approval.

## Never
- Commit secrets or use production data.

## Definition of done
Acceptance criteria met · tests passing · docs and state updated
"""

CLAUDE = """
@AGENTS.md

# Claude Code notes
- Use plan mode for material changes.
"""

OVERVIEW = """
# PawBook — Overview

> Purpose: what we are building and why. Tags: [Assumption] [Proposed] [Open] [Blocking].

## Problem
Independent groomers lose bookings to phone tag and no-shows.

## Users and roles
| Role | Who | Needs |
|---|---|---|
| Groomer | Salon owner | Manage calendar |
| Client | Dog owner | Book and get reminders |

## Scope
**Version 1 (Must):** FR-1 booking, FR-2 reminders.

**Non-goals:** payments in version 1.

## Glossary
| Term | Meaning |
|---|---|
| Salon | One groomer business (the tenant) |
"""

REQUIREMENTS = """
# Requirements

> Purpose: what the system must do.

## Functional requirements

### FR-1 Online booking — Must
Acceptance criteria:
- Given an open slot, when a client books it, then the groomer sees it within 5 seconds.

### FR-2 Reminders — Must
Acceptance criteria:
- Given a booking tomorrow, when it is 6 pm today, then the client gets an SMS reminder.

## Non-functional requirements
| ID | Quality | Target | How we check |
|---|---|---|---|
| NFR-1 | Availability | 99.5% monthly | Uptime monitor |
| NFR-2 | Data loss | At most 24 h | Restore drill |

- [Assumption] Most clients book from phones.
"""

ARCHITECTURE = """
# Architecture

> Purpose: the current structure.

## Summary
A modular monolith on managed hosting.

```mermaid
flowchart LR
  user[Clients] --> app[Next.js app]
  app --> db[(Postgres)]
```

## Binding decisions
| ADR | Decision | Status |
|---|---|---|
| [ADR-0001](decisions/0001-stack.md) | Stack | Accepted |
| [ADR-0002](decisions/0002-hosting.md) | Hosting | Superseded |
| [ADR-0003](decisions/0003-hosting-render.md) | Hosting | Accepted |
"""

ROADMAP = """
# Roadmap

## M0 — Safe to build
Verification: a trivial pull request passes every check.

## M1 — Walking skeleton
Acceptance criteria:
- Given a groomer account, when they sign in, then they see an empty calendar.
Verification: end-to-end test in CI.
"""

RISKS = """
# Risks, assumptions and open questions

## Open questions
| ID | Question | Status |
|---|---|---|
| Q-1 | Which SMS provider? | [Open] |
"""

STANDARDS = """
# Engineering standards

## AI-agent guardrails
- Agents have no production credentials.
"""

STATE_READY = """
# Project state

Phase: ready
Tier: Standard
Last updated: 2026-10-19 by Masterplan

## Now
- Milestone: M0

## Next actions
1. Create the repository.

## Planning progress
| Area | Status | Recorded in |
|---|---|---|
| Problem, users, success criteria | Confirmed | overview.md |
| Architecture and stack | Delegated | ADRs |
| Scale and growth | Assumed | requirements.md |
"""

ADR1 = """
# ADR-0001: Stack

- Status: Accepted
- Date: 2026-10-19
- Decided by: Delegated — owner chose "I'm not sure", AI recommendation adopted
- Confidence: High

## Context
Small team, web first.

## Options considered
1. **Next.js** — typed, mainstream.
2. **Rails** — productive, less familiar to the owner.

## Decision
TypeScript with Next.js.

## Consequences
- Good: one language.

## Evidence
- Next.js docs (checked 2026-10-19).

## Revisit when
- A native mobile app is required.
"""

ADR2 = """
# ADR-0002: Hosting on Vercel

- Status: Superseded by ADR-0003
- Date: 2026-10-19
- Decided by: Owner

## Context
Need hosting.

## Options considered
1. Vercel
2. Render

## Decision
Vercel.

## Consequences
- Simple deploys.

## Evidence
- Pricing page (checked 2026-10-19).

## Revisit when
- Long-running jobs are needed.
"""

ADR3 = """
# ADR-0003: Hosting on Render

- Status: Accepted
- Date: 2026-10-20
- Decided by: Owner
- Supersedes: ADR-0002

## Context
Reminders need a long-running worker.

## Options considered
1. Vercel plus a job service
2. Render web service plus worker

## Decision
Render.

## Consequences
- One platform for web and worker.

## Evidence
- Render docs (checked 2026-10-20).

## Revisit when
- Traffic exceeds one instance.
"""


def good_standard():
    root = OUT / "good-standard"
    write(root, {
        "AGENTS.md": AGENTS, "CLAUDE.md": CLAUDE,
        "docs/project/overview.md": OVERVIEW,
        "docs/project/requirements.md": REQUIREMENTS,
        "docs/architecture/architecture.md": ARCHITECTURE,
        "docs/project/roadmap.md": ROADMAP,
        "docs/project/risks.md": RISKS,
        "docs/engineering/standards.md": STANDARDS,
        "docs/project/state.md": STATE_READY,
        "docs/architecture/decisions/0001-stack.md": ADR1,
        "docs/architecture/decisions/0002-hosting.md": ADR2,
        "docs/architecture/decisions/0003-hosting-render.md": ADR3,
    })


def good_light():
    root = OUT / "good-light"
    agents = AGENTS.replace(
        "- Requirements: `docs/project/requirements.md`\n- Architecture: `docs/architecture/architecture.md`\n", ""
    ).replace("- Roadmap: `docs/project/roadmap.md` · Risks: `docs/project/risks.md`\n", "").replace(
        "- Engineering standards: `docs/engineering/standards.md`\n", "")
    overview = OVERVIEW + """
## Requirements
### FR-1 Booking — Must
- Given an open slot, when I book it, then it appears in the calendar.

## Architecture
A single Next.js app with SQLite.

## Roadmap
### M1 — Walking skeleton
Verification: I can book a slot locally.

## Risks
- [Assumption] Only one groomer uses it.
"""
    state = STATE_READY.replace("Tier: Standard", "Tier: Light")
    write(root, {
        "AGENTS.md": agents, "CLAUDE.md": CLAUDE,
        "docs/project/overview.md": overview,
        "docs/project/state.md": state,
        "docs/architecture/decisions/0001-stack.md": ADR1,
    })


def planning_partial():
    root = OUT / "planning-partial"
    state = STATE_READY.replace("Phase: ready", "Phase: planning").replace(
        "| Scale and growth | Assumed |", "| Scale and growth | Open |")
    write(root, {
        "AGENTS.md": AGENTS.replace("Online booking", "{{One sentence: what this is}} Online booking"),
        "CLAUDE.md": CLAUDE,
        "docs/project/overview.md": OVERVIEW + "\n- [Blocking] Who pays for SMS?\n",
        "docs/project/state.md": state,
    })


def broken():
    root = OUT / "broken"
    long_agents = AGENTS + "\n".join(f"- filler rule {i}" for i in range(220))
    bad_adr = """
# ADR-0001: Database

- Status: Approved-ish
- Date: 2026-10-19

## Decision
Postgres.
"""
    dup_adr = ADR1.replace("# ADR-0001: Stack", "# ADR-0001: Duplicate")
    orphan = ADR2.replace("Superseded by ADR-0003", "Superseded by ADR-0009")
    state = STATE_READY.replace("| Scale and growth | Assumed |", "| Scale and growth | Open |")
    write(root, {
        "AGENTS.md": long_agents,
        "CLAUDE.md": "@AGENTS.md\n@docs/missing-rules.md\n",
        "docs/project/overview.md": OVERVIEW + "\n- [Blocking] Who pays for SMS?\n"
            + "\nSee [the old plan](plans/old-plan.md).\n",
        "docs/project/state.md": state,
        "docs/architecture/architecture.md": ARCHITECTURE + "\n{{Monthly estimate at launch}}\n"
            + "\nDeploy key: AKIAIOSFODNN7EXAMPLE\n",
        "docs/project/roadmap.md": ROADMAP,
        "docs/project/risks.md": RISKS,
        "docs/engineering/standards.md": STANDARDS,
        "docs/architecture/decisions/0001-database.md": bad_adr,
        "docs/architecture/decisions/0001-stack.md": dup_adr,
        "docs/architecture/decisions/0002-hosting.md": orphan,
    })
    # requirements.md deliberately missing


if __name__ == "__main__":
    if OUT.exists():
        shutil.rmtree(OUT)
    good_standard()
    good_light()
    planning_partial()
    broken()
    print("fixtures written to", OUT)
