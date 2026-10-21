"""Regression tests for scripts/task_brief.py and scripts/review_package.py. Run: python3 test_scripts.py"""
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
failures = []


def expect(cond, message):
    if not cond:
        failures.append(message)
    print(("ok   " if cond else "FAIL ") + message)


def run(*args, cwd=None):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, cwd=cwd)


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    plan = tmp / "plan.md"
    plan.write_text(
        "# Plan: M1\n\n**Goal:** g\n\n## Global constraints\n- gc\n\n## Review focus\n1. rf\n\n"
        "## Acceptance tests\nAcceptance commit: abc1234\n- c -> pending until Task 10\n\n## File map\n- `a.ts` - a\n\n"
        "## Tasks\n\n### Task 1: one\n- [ ] step one\n```md\n## Not a heading\n### Task 10: fake\n```\n\n"
        "### Task 10: ten\n- [ ] step ten\n")
    out = tmp / "brief.md"
    r = run(SCRIPTS / "task_brief.py", plan, 1, out)
    text = out.read_text() if out.exists() else ""
    expect(r.returncode == 0 and "step one" in text and "step ten" not in text, "task 1 brief has task 1 only")
    expect("## Not a heading" in text, "headings inside code fences stay inside the task")
    expect(all(h in text for h in ("Global constraints", "Review focus", "Acceptance tests", "File map")),
           "brief carries the plan's shared sections")
    r = run(SCRIPTS / "task_brief.py", plan, 10, out)
    expect(r.returncode == 0 and "step ten" in out.read_text(), "task 10 is not confused with task 1")
    r = run(SCRIPTS / "task_brief.py", plan, 3, out)
    expect(r.returncode == 1, "a missing task exits 1")
    r = run(SCRIPTS / "task_brief.py", tmp / "nope.md", 1, out)
    expect(r.returncode == 1 and "Traceback" not in r.stderr, "a missing plan gives a clean error")

    repo = tmp / "repo"
    repo.mkdir()
    git = lambda *a: subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.invalid", *a],
                                    capture_output=True, text=True)
    git("init", "-q")
    git("commit", "-q", "--allow-empty", "-m", "base")
    (repo / "doc.md").write_text("# Doc\n\n```js\ncode\n```\n")
    (repo / "package-lock.json").write_text('{"lockfileVersion": 3}\n')
    git("add", "-A")
    git("commit", "-q", "-m", "add doc")
    pkg = tmp / "review.md"
    r = run(SCRIPTS / "review_package.py", "HEAD~1", "HEAD", pkg, "--repo", repo)
    body = pkg.read_text() if pkg.exists() else ""
    expect(r.returncode == 0 and "````diff" in body, "diff fence is longer than any fence in the diff")
    expect("package-lock.json" in body.split("## Diff")[0] and "lockfileVersion" not in body,
           "lockfiles are listed in the stat but left out of the diff")
    r = run(SCRIPTS / "review_package.py", "HEAD", "HEAD", pkg, "--repo", repo)
    expect(r.returncode != 0, "base equal to head is refused")

print(f"{len(failures)} failure(s)")
sys.exit(1 if failures else 0)
