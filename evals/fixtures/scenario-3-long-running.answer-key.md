# Scenario 3 answer key (long-running project, cold start)

A fresh agent with no conversation history, reading only the repository, must get these right.
Each item is graded PASS / PARTIAL / FAIL with the file it cited.

| # | Question | Ground truth | Trap |
|---|---|---|---|
| K1 | What are we building, for whom | Multi-tenant maintenance-request SaaS for small/mid property-management companies; renters, staff, vendors | — |
| K2 | Binding decisions | ADR-0001–0007, 0009, 0010 Accepted; **ADR-0008 Superseded by ADR-0010** | Citing Postmark as the email provider = FAIL |
| K3 | Email provider | Amazon SES, sent only from `notifications` via the `messages` queue | Postmark |
| K4 | What is implemented | M0, M1, M2 done; M3: FR-10 done, FR-5 part 1 (roles, permissions) merged in PR #61 | Saying M3 not started, or FR-5 done |
| K5 | Exact next task | FR-5 part 2: enforce two-step verification for company admins at sign-in (django-allauth MFA) with recovery codes; start by writing the failing tests in `accounts/tests/test_two_step.py` per the FR-5 spec | Starting FR-6 or FR-14 |
| K6 | Validation commands | `uv sync --frozen`, `docker compose up -d db`, `uv run pytest`, ruff check, ruff format --check, mypy, lint-imports; isolation tests `-m isolation` | Inventing npm/other commands |
| K7 | Definition of done | Per AGENTS.md › Definition of done (tests incl. isolation test for company-scoped views, checks pass, docs/state updated) | — |
| K8 | Change control | Recognizes that changing tenancy/sign-in/provider etc. is material and needs an ADR; two-step via allauth MFA is NOT a material change (spec says so) | Proposing a new auth library without an ADR |
| K9 | Blockers | Twilio written confirmation blocks FR-14 going live, not development; Q-6 pricing vs texting cost before M4 | — |
| K10 | Build authorization | Authorized 2026-10-20 for M0–M4; agent may proceed with FR-5 | Refusing to build because "planning" |

Pass bar: K2–K5 and K10 must be PASS (they are the ones that cause real damage if wrong); at most two PARTIAL elsewhere.
