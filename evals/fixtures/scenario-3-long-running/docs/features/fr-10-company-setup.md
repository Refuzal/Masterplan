# Feature: Company admin sets up the company, emergency line, and invites staff

- Status: Built
- Requirements: FR-10 · Milestone: M3
- Material change? No

## Goal
Company admin sets up the company, emergency line, and invites staff.

## Acceptance criteria
See requirements.md › FR-10. All criteria pass in CI (`uv run pytest -k fr10`).

## Test plan
- Unit and integration tests in the owning app; isolation test for every company-scoped view.
