# Requirements

> Purpose: what the system must do and how well. Update when scope, targets or obligations change. Owner: {{product owner}}; engineers keep IDs stable.
> Priority: Must (version 1) · Should · Could · Won't (now). Untagged = confirmed; [Assumption] [Proposed] [Open] [Blocking] mark the rest.

## Functional requirements

### FR-1 {{Capability}} — Must
{{One sentence from the user's point of view.}}
Acceptance criteria:
- Given {{situation}}, when {{action}}, then {{observable result}}.
- Given {{situation}}, when {{edge case}}, then {{result}}.

## Non-functional requirements
Each target must be measurable and checked somewhere.

| ID | Quality | Target | How we check |
|---|---|---|---|
| NFR-1 | Performance | {{e.g. key pages respond in under 1 s for 95% of requests}} | {{e.g. monitoring dashboard, load test before launch}} |
| NFR-2 | Availability | {{e.g. 99.5% per month}} | {{uptime monitor}} |
| NFR-3 | Data loss and recovery | {{e.g. Standard: lose at most 24 h of data; restore within a day}} | {{e.g. one tested restore before launch}} |
| NFR-4 | Security and privacy | {{e.g. every request authorized server-side; personal data encrypted at rest}} | {{authorization tests in CI}} |
| NFR-5 | Accessibility | {{e.g. WCAG 2.2 AA on public pages}} | {{automated checks in CI + manual pass}} |
| NFR-6 | Scale horizon | {{e.g. 10× the 12-month estimate without re-architecture}} | {{load test at milestone N}} |
| NFR-7 | Running cost | {{e.g. under $150/month at launch}} | {{billing alerts}} |

## Data
| Data | Sensitivity | Kept for | Notes |
|---|---|---|---|
| {{e.g. customer contact details}} | {{Personal}} | {{e.g. while account active + 30 days}} | {{deletion on request}} |

## Integrations
| System | Why | Direction | Notes |
|---|---|---|---|
| {{e.g. Stripe}} | {{payments}} | {{outbound + webhooks}} | {{hosted checkout; no card data stored}} |

## Compliance obligations
{{Only obligations that apply, each with a source link and access date. Write "None identified" if none.}}
