# Feature: Vendor accepts, schedules, adds notes and photos, and completes through a link

- Status: Built
- Requirements: FR-4 · Milestone: M2
- Material change? No

## Goal
Vendor accepts, schedules, adds notes and photos, and completes through a link.

## Acceptance criteria
See requirements.md › FR-4. All criteria pass in CI (`uv run pytest -k fr4`).

## Test plan
- Unit and integration tests in the owning app; isolation test for every company-scoped view.
