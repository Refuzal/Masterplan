# Debugging

For any bug, failing test, broken build or unexpected behavior, during the build or after release. Find the root cause before changing code; a fix without a cause is a guess.

Contents: 1 Build a feedback loop · 2 Reproduce and minimise · 3 Hypothesise · 4 Instrument · 5 Fix with a regression test · 6 Clean up · When fixes keep failing · Production incidents

## 1 Build a feedback loop

This is most of the work. Get one command that goes red on this exact bug and green when it is fixed, then everything else consumes that signal.

Try, roughly in this order: a failing test at the seam that reaches the bug; an HTTP call against the running app; the CLI with a fixture input; a headless browser script (Playwright); replaying a captured request or event; a small harness that calls the failing code path directly; a loop over many random inputs for intermittent bugs; `git bisect run` with a check script when the bug appeared between two known versions.

The loop is ready when it:
- drives the real code path and checks the user's exact symptom (not just "no crash");
- gives the same verdict every run (for intermittent bugs, a high, stable reproduction rate);
- runs in seconds;
- runs without a person in the loop.

If you cannot build one, say so, list what you tried, and ask for access to the failing environment, a captured artifact (logs, a request, a screen recording with timestamps), or permission for temporary instrumentation. Do not start theorizing without a loop.

Redact secrets in everything you show: commands, logs and captured requests.

## 2 Reproduce and minimise

Run the loop and confirm it fails the way the user described, not some nearby failure. Then shrink the scenario one element at a time (inputs, data, steps, configuration), keeping only what is needed for the failure. The minimal case shrinks the list of suspects and becomes the regression test.

## 3 Hypothesise

Write three to five ranked hypotheses down (in the ledger or fix report) before testing any, even when one looks obvious; an obvious first guess is the one most worth checking against alternatives. Each must predict something checkable: "if X is the cause, then changing Y makes the bug disappear." Read the full error and stack trace, check what changed recently (`git log`, dependency updates, configuration), and compare with similar code that works. Share the ranked list when the owner or user might know something that re-ranks it, without blocking on them.

## 4 Instrument

Test one hypothesis at a time, changing one variable at a time. Prefer a debugger or REPL; otherwise targeted logs at the boundaries that separate hypotheses. Tag every temporary log with a unique prefix (`[DBG-4f2a]`) so removal is a single search. For multi-part systems, log what enters and leaves each part once to find where it breaks, then investigate that part. For slowness, measure a baseline first (timings, profiler, query plan), then change.

## 5 Fix with a regression test

1. Turn the minimal case into a failing test at a seam that exercises the real bug pattern. If no such seam exists, record that as a design finding.
2. Watch it fail, for the reason the bug predicts.
3. Fix the root cause, not the symptom: one change, no unrelated improvements.
4. Watch the test pass, rerun the original loop, then the full suite.
5. Prove every new test guards the bug: put the bug back (revert only the production change), watch each new test fail, then restore the fix. A test that passes with the bug present is not a regression test; fix it or drop it. Only then write "seen failing" in the report.
6. Where the bug came from bad data crossing a boundary, add validation at that boundary too.

## 6 Clean up

Before calling it fixed: the original loop is green; the regression test passes; tagged debug logs and throwaway harnesses are gone; the commit message states the root cause, so the next person learns from it. Update state.md if the bug was on the blockers list.

Reproduce on a throwaway copy of the data (a temporary database or folder), never on the data the owner uses, and keep the fix on a branch until it is integrated (lifecycle.md › Fix).

## When fixes keep failing

After three fixes that did not hold, stop fixing. Repeated failures that each reveal a new problem elsewhere point to the design, not the last line changed. Write down what the attempts showed, and raise it as a design question: in a build milestone, a ruling or a change (lifecycle.md › Change) if it affects an Accepted decision; outside one, a short note to the owner with options.

## Production incidents

Stabilize first: roll back the last deploy or turn off the feature flag if that stops the harm, and tell the owner what users are affected. Then debug with the same steps on a copy, never by experimenting on production data. Afterwards, write a short incident note in `docs/project/risks.md` or `operations.md`: what happened, the root cause, the fix, and the check that now prevents it.
