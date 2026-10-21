# ADR-0001: Python and Django modular monolith with server-rendered pages

- Status: Accepted
- Date: 2026-10-19 (Python version rule added the same day after the review panel)
- Decided by: Product owner, approving the recommended architecture package on 2026-10-19. The owner set the criteria (Ravi is productive with it; low operations work) and left the technical details to the recommendation. Ravi confirms in M0.
- Confidence: High
- Change later: Hard

## Context
Two founders build version 1 (requirements.md FR-1 to FR-23) in 4–5 months: a product owner and Ravi, a backend developer fluent in Python. AI coding agents write much of the code (risks.md A-2). Renters and vendors use phones (NFR-1); every page must meet WCAG 2.2 AA (NFR-5); the design must reach 2,000 companies without a rewrite (NFR-6). The screens are forms, lists, status pages and photo uploads.

## Options considered
1. **Python with Django, server-rendered templates and htmx** — the team already knows Python; Django includes accounts, an admin, an ORM with migrations, forms, translations and protections against common web attacks; very widely used, so AI agents know it well / Python type checking is opt-in; very rich client-side interactions need extra JavaScript.
2. **Python with FastAPI for an API, plus a React front end** — typed API and a modern client / two codebases and two languages; sign-in, admin screens, migrations and forms must be assembled from separate libraries; slower for two people.
3. **TypeScript with Next.js** — strict types help AI agents; large ecosystem / Ravi's fluency is Python, so switching costs time; sign-in, admin and background jobs are assembled from libraries.

## Decision
Build one Django 6.1 application on Python 3.14 (or Python 3.13 if the M0 compatibility check finds any pinned dependency without 3.14 support; nothing in the design needs 3.14), organized as a modular monolith with the apps listed in architecture.md › Components and boundaries. Pages are server-rendered Django templates with htmx 2.x for partial updates and a small amount of plain JavaScript where needed (direct photo uploads). Styling uses Tailwind CSS v4 through its standalone command-line tool, so no Node.js toolchain is needed. Upgrade to Django 6.2 LTS after it is released (expected April 2027).

## Why
- Ravi's Python fluency is the strongest productivity factor for a two-person team; switching stacks is a cost, not a free upgrade.
- Django provides most of version 1's plumbing (accounts, admin, migrations, forms, translations for FR-21, security middleware), which leaves the team's time for the maintenance workflow.
- Mainstream frameworks get better and safer AI-generated code; Django is among the most widely used backend frameworks.
- Server-rendered pages keep one codebase in one language and are fast on low-end phones. Option 2 lost because a second codebase doubles the work and the places agents can go wrong; option 3 lost on switching cost.

## Consequences
- Good: one deployable and one language; built-in admin for founder support; translation-ready from day one.
- Costs and tradeoffs: type safety depends on mypy with django-stubs in strict mode, enforced in CI (standards.md). htmx 4.0 is released but not yet the default npm version, so the project stays on htmx 2.x until 4.x is the default. A rich drag-and-drop interface (for example a dispatch calendar) would need a targeted JavaScript component.
- Follow-up work: pin versions in `uv.lock`; plan the Django 6.2 LTS upgrade after the pilot starts; run the M0 compatibility check for Python 3.14.
- Not chosen after review: starting on Django 5.2 LTS. Its mainstream support ended in December 2025, and moving from 6.1 to 6.2 LTS is a small step, while moving from 5.2 crosses three releases.

## Evidence
- [Django downloads](https://www.djangoproject.com/download/) (checked 2026-10-19) — latest 6.1.2; 6.1 supported until December 2027; 5.2 LTS security support until April 2028.
- [Django 6.1 release notes](https://docs.djangoproject.com/en/6.1/releases/6.1/) (checked 2026-10-19) — released 2026-08-05; Python 3.12–3.14; PostgreSQL 15 and later.
- [htmx.org](https://htmx.org/) (checked 2026-10-19) — 4.0 released but not marked `latest` on npm; examples use 2.0.11.
- [Mündler et al. 2025](https://arxiv.org/abs/2504.09246) — most compile errors in LLM-generated code are type errors, which a type checker catches.
- [BaxBench, ICML 2025](https://proceedings.mlr.press/v267/vero25a.html) — models produce worse and less secure code on less widely used backend frameworks.

## Revisit when
- A planned feature needs a rich client-side interface that htmx cannot reasonably support.
- A second team needs to release part of the system independently.
- Django 6.2 LTS is released (upgrade, not redesign).
