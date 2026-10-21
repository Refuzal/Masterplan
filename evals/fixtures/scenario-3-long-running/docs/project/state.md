# Project state

Phase: building
Tier: Standard
Last updated: 2027-01-08 by Claude Code (session: FR-5 roles, part 1)
Build authorization: 2026-10-20 by the product owner — plan as of 2026-10-19, building M0–M4

> Purpose: where things stand right now, for whoever picks this up next. Keep it under 60 lines. Update at the end of every work session. History belongs in git, not here.

## Now
- Milestone: [M3 — Onboarding and texts](roadmap.md#m3--onboarding-and-texts-weeks-1114--in-progress), week 12 of 20.
- In progress: FR-5 roles and two-step verification for company admins. Roles and server-side permission checks are merged (PR #61); two-step verification enforcement is not started. Spec: [docs/features/fr-05-roles-and-two-step.md](../features/fr-05-roles-and-two-step.md).

## Next actions
1. FR-5: enforce two-step verification for company admins at sign-in (django-allauth MFA), with recovery codes; acceptance criteria in the FR-5 spec. Start by writing the failing tests listed under "Test plan" in the spec.
2. FR-6: spreadsheet import (CSV first; Excel is cut item 2 in risks.md R-11 if we slip). Write the spec in `docs/features/` first.
3. FR-14 texts: Twilio toll-free number purchase and verification per company, STOP handling, email fallback.
4. Ask Twilio support again for the written confirmation required by ADR-0010 before FR-14 texts go to pilot companies (requested 2026-12-10, no answer yet).

## Recently done
- 2027-01-07 — FR-5 part 1: company admin and staff roles; every staff view checks `accounts.permissions` (PR #61).
- 2026-12-30 — FR-10 company setup and staff invitations (PRs #52–#58); isolation tests added for invitations.
- 2026-12-18 — M2 done: renter → staff → vendor loop, urgent alerts, email notifications.
- 2026-12-04 — Email moved from Postmark to Amazon SES (ADR-0010 supersedes ADR-0008).
- 2026-11-23 — M1 done; restore drill took 38 minutes (NFR-3 target: 2 hours).

## Blockers and open questions
- Twilio's written confirmation of the staff-alert number split (see Next actions 4) — blocks FR-14 going live, not development.
- Q-6 in [risks.md](risks.md): how price tracks texting cost; needed before M4.
