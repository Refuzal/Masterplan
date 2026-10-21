# Feature: Roles and two-step verification for company admins

- Status: Approved — in progress (part 1 merged in PR #61)
- Requirements: FR-5 · Milestone: M3
- Material change? No (uses django-allauth MFA, already chosen in ADR-0004)

## Goal
Company admins manage staff, billing and settings; property managers and coordinators do all maintenance work. Admins must use two-step verification because they control billing and staff access.

## Behavior
1. Part 1 (done): two roles, `company_admin` and `staff`; every staff view checks permissions on the server through `accounts.permissions`.
2. Part 2 (next): a company admin without two-step verification is sent to set it up (authenticator app) on next sign-in and cannot reach any page until done; ten single-use recovery codes are shown once; a founder can reset an admin's two-step verification from the founders' page after an identity check by phone.

## Acceptance criteria
- Given a company admin without two-step verification, when they sign in, then every page redirects to setup until it is complete.
- Given a company admin with two-step verification, when they sign in with password only, then they are asked for a code and cannot proceed without a valid one or a recovery code.
- Given a staff member (not admin), when they sign in, then two-step verification is offered but not required.
- Given a used recovery code, when it is entered again, then it is rejected.

## Test plan
- `accounts/tests/test_two_step.py`: one test per acceptance criterion (write these first, they should fail).
- Isolation test: an admin of company A cannot reset or view two-step status for company B's users.

## Out of scope
- Passkeys (cut item 1 in risks.md R-11).
- Two-step verification required for all staff.
