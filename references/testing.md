# Testing

Tests are how an AI-built codebase stays correct when nobody reads every line. These rules make tests catch real breaks instead of decorating the code.

Contents: The rule · Seams · Vertical slices · Acceptance tests · A good test · Mocks · The test mix · Special cases · Never · Keep the suite fast · Flaky tests · Checklist

## The rule

Write the test first, run it, and watch it fail for the reason you expect. Then write the least code that makes it pass, run it again, then clean up while it stays green.

- If you did not see the test fail, you do not know it can catch anything.
- A test that passes on first run is testing behavior that already exists or is testing nothing; fix the test.
- A missing module or an import error is not a red test: it fails for the wrong reason. Create the empty function or export first, then watch the assertion fail.
- Code written before its test is deleted and rewritten from the test, not kept "as reference". When that is impractical (a large change already reviewed), put the bug back that the test is meant to catch, record the test failing, then restore the code; note it in the ledger as a deviation.
- Exceptions, which the plan names explicitly: configuration, generated code, and throwaway spikes. A spike's lessons come back into tested code.
- Bug fixes start with a failing test that reproduces the bug (debugging.md).

## Seams

A **seam** is the public interface where a test observes behavior: a module's exported functions, an HTTP endpoint, a page a user drives. Tests live at seams, never against private internals.

- The task plan names the seams before any test is written. Prefer the highest seam that still gives a fast, precise signal; fewer seams across the codebase is better.
- When a module is hard to test at its interface, the interface is the problem: make it deeper and simpler (codebase-design.md) rather than reaching inside.
- Tests at the interface survive refactors. If a test must change whenever the implementation changes but behavior does not, it is testing past the interface.

## Vertical slices

One test, then the code for it, then the next test. Writing all the tests first and then all the code (horizontal slicing) tests imagined behavior and locks in structure before you understand it. Each cycle is a tracer bullet that teaches the next one.

## Acceptance tests

Agents build to whatever is checked, and when a test and the specification disagree they often change the test. So the tests that decide whether a milestone is done are not written by the agents that write its code.

- Before a milestone's first task, the plan's acceptance-test author writes one acceptance test per acceptance criterion through the outermost seam (end-to-end for a user journey, the public API otherwise) and commits them under `tests/acceptance/` (build-loop.md › Write the task plan).
- They start **pending**, under the runner's strict expected-failure marker, so the suite stays green and a test that passes too early fails it. The task that delivers the behavior removes the marker as its last step; that is the only edit implementers make there. Any other change takes a ruling that the test itself is wrong.
- They are few and behavioral. The implementer's own test-first tests carry the detail.
- They run in the full check (before every merge, before each demo, and in CI), driving a real browser where the machine has one, so every later change re-proves every accepted criterion. The pre-commit hook may run only the fast checks when browser tests make it slow.
- At verification, every requirement in scope is traced to a test. A requirement no test proves is reported as unverified, not done.

## A good test

- **Names the break it catches.** Before writing the body, name the production change that would make it fail: a wrong branch, a missing side effect, a boundary, a broken rule. If you cannot name one, redesign the test around observable behavior.
- **Uses independent expected values.** Literals, hand-checked fixtures and worked examples from the requirements. An expected value computed the way the code computes it passes no matter what the code does.
- **Describes behavior, not mechanism.** "a member of another company cannot see this request" rather than "calls repository.find with company_id".
- **One behavior per test**, with a name that reads like a requirement.
- **Tests your contract, not the framework.** Do not test that the router calls a handler; test what your endpoint returns.
- **Passes the mutation check.** Imagine a wrong constant, a flipped condition, a missing state change, an empty return, or missing validation for empty, zero, unauthorized or malformed input. At least one test should fail for each realistic mutation.

## Mocks

Mock only at system boundaries you do not control or cannot run fast: third-party APIs (payments, email, texts, AI providers), time, randomness, and sometimes the file system. Never mock your own modules or internal collaborators.

- Put each external service behind a small adapter with a fake for tests (codebase-design.md › Ports and adapters). The fake mirrors the real response shape completely.
- Prefer real dependencies you can run locally: a real PostgreSQL test database (a local instance, a container, or an in-process build such as PGlite), a real file system in a temp folder.
- Never assert on a mock's existence or call count unless the call itself is the contract (a payment must be charged exactly once).
- Test-only helpers live in test utilities, never as methods on production code.
- When mock setup outgrows the test, switch to an integration test with real components.

## The test mix

Most value comes from tests at module interfaces that run against real local dependencies.

| Kind | What | How many |
|---|---|---|
| Integration at module interfaces | Behavior of each feature through its public interface, with a real test database | The bulk |
| Unit | Pure logic with many cases: pricing, scheduling, permissions rules, parsers | Where logic is dense; table-driven with literal expectations |
| End-to-end and acceptance | The critical user journeys and each milestone's acceptance criteria, driven through the real UI or API (Playwright for web) | One per acceptance criterion, plus sign-in, the core action and payment if any |
| Contract | Each external adapter against the provider's sandbox, run on a schedule or before release | One small suite per provider |
| Property-based | Core rules that must hold for all inputs (no double booking, totals never negative) | Critical tier, and any rule with many edge cases |

Light projects: integration tests for the core flow plus unit tests for dense logic, one or two end-to-end checks. Standard: the full mix except property tests where not needed. Critical: everything, plus mutation testing on core logic.

## Special cases

- **Tenant isolation and permissions:** for every new table, endpoint, job or file path, a test proves that a user of one tenant (or role) cannot read or change another's data, including through search, exports, background jobs and direct links. Database-level isolation tests connect as the application's own role (a test container's default superuser bypasses row-level security, so the test would prove nothing) and run on a reused connection as well as a fresh one. Include rows with empty values in the columns that lookups match on, and a test that the tenant setting does not survive past the end of its transaction.
- **Time:** inject a clock; test time zones, daylight-saving changes and month ends when dates matter.
- **Concurrency:** when two users can act on the same thing, test the race (two bookings for the same slot) at the database level.
- **Migrations:** a test or CI step runs migrations forward on a copy with realistic data; destructive changes follow expand–contract.
- **Money:** integer minor units, rounding rules from the requirements, idempotency for every charge.
- **AI features:** an evaluation set with pass thresholds (ai-features.md), not exact-text assertions.

## Never

- Weaken, skip, delete or rewrite a test to make it pass. If a test is wrong, say why in the report and change it as its own reviewed step.
- Commit with failing tests, or with test output full of warnings.
- Write tests only to raise coverage; a test that checks no outcome costs maintenance and catches nothing.
- Leave debugging prints or focused/skipped test markers (`.only`, `skip`) in committed code. A strict expected-failure marker on a pending acceptance test is not a skip: it fails the suite when the test starts passing, and it is removed by the task that delivers the behavior. Enforce it with a check, not a reminder: Playwright's `forbidOnly` in CI and the test linter's no-focused and no-disabled rules. A tool that "heals" a failing end-to-end test by skipping it needs a human's approval.
- Wrap assertions in try/catch, or in a condition, so a failing check cannot fail the test.
- Edit an acceptance test to make it pass.

## Keep the suite fast

Agents wait for every run, so test time is build time. Run browser tests in parallel workers, sign in once per file (or reuse a saved signed-in state) instead of per test, give each worker its own database, and keep the pre-commit hook to the fast checks. During a task, run only the tests it touches; run everything at milestone verification.

## Flaky tests

A flaky test is a bug report. Quarantine it in a named list with an owner and a date, find the cause (shared state, real time, network, ordering, async waits), and replace sleeps with waiting on the actual condition. Never retry a test in a loop until it passes.

## Checklist before a task is done

- Each new behavior has a test that was seen failing first, for the expected reason.
- Expected values are literals or hand-checked fixtures.
- No mocks of internal code; external services faked behind adapters.
- Edge cases from the plan's review focus have tests.
- Full suite green, output clean; lint and typecheck clean.
