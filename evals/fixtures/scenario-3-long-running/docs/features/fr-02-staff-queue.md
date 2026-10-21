# Feature: Staff request queue with filters by building, status and urgency

- Status: Built
- Requirements: FR-2 · Milestone: M2
- Material change? No

## Goal
Staff request queue with filters by building, status and urgency.

## Acceptance criteria
See requirements.md › FR-2. All criteria pass in CI (`uv run pytest -k fr2`).

## Test plan
- Unit and integration tests in the owning app; isolation test for every company-scoped view.
