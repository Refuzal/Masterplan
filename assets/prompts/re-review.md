# Scoped re-review prompt

After each fix round, review only the fix. Build the review package from the commit the previous review saw (FIX_BASE) to the new HEAD.

```
You are checking whether a fix addressed specific review findings, in the repository at [repo path]. Read-only; do not start other agents.

Findings to check: [findings list, verbatim]
Task brief: [brief file]
Implementer's fix report: [report file], last section
Fix diff: [review package file]

For each finding, answer ADDRESSED or NOT ADDRESSED with file:line evidence. Then list any new Critical or Important problem introduced by the fix diff itself. Anything you notice outside the fix diff goes under "Out of scope" and does not change the verdict.

Output:
[finding] — ADDRESSED | NOT ADDRESSED — [evidence]
New problems in the fix: [none | list]
Out of scope: [none | list]
Verdict: all addressed | [N] open
```
