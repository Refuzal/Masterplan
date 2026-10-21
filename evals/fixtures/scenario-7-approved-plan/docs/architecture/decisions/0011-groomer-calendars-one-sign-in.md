# ADR-0011: Each groomer has a calendar; one sign-in per business in version 1

- Status: Accepted
- Date: 2026-10-19
- Decided by: Owner (approved the recommendation on 2026-10-19)
- Confidence: High
- Change later: Moderate

## Context
The version 1 scope first assumed one calendar per business. The owner then confirmed that most target salons have one or two groomers. With one calendar, a two-groomer salon's booking page could offer only one dog at a time, showing about half its real openings (FR-2, FR-3, FR-5). No code exists yet, so changing the data model now costs only planning and about a week of building.

## Options considered
1. **Groomers as calendars, one sign-in per business** — each groomer has working hours and time off; every appointment belongs to one groomer; clients pick a groomer or "anyone available"; the owner manages all calendars / staff cannot sign in separately yet.
2. **Groomers as calendars with separate staff sign-ins and permissions** — closest to what larger salons want / adds roles, invitations and permission tests to version 1; too much for the January target.
3. **One calendar per business (original scope)** — least work / poor fit for most target salons; appointment records would need reshaping later.

## Decision
Option 1. A `groomer` record belongs to a business and has its own working hours and time off; every appointment has a groomer. Availability is computed per groomer. When a client chooses "anyone available", the request goes to the first free groomer in the order the owner set [Assumption]. Only the owner signs in (membership role `owner`, ADR-0005); separate staff sign-ins remain FR-13.

## Why
- Fits most target salons and shows clients the real openings.
- Avoids a data migration on live appointments later.
- Staff sign-ins lost on schedule risk; the model leaves room for them (a groomer can later be linked to a user).

## Consequences
- Good: two-groomer salons are served from launch; no later reshaping of appointments.
- Costs and tradeoffs: about one more week in M2; the calendar needs a per-groomer day view; text costs unchanged (they follow appointments).
- Follow-up work: requirements FR-2, FR-3, FR-5 updated; data model updated in architecture.md; isolation tests cover groomers.

## Evidence
- Owner's statement during planning (2026-10-19): "Most salons have one or two groomers."

## Revisit when
- Salons ask for staff to sign in separately, or a salon has more than three groomers.
- The owner decides to price per groomer rather than per salon (Q-4).
