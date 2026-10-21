#!/usr/bin/env python3
"""Write a review package for a reviewer agent: commit list, change summary and full diff.

Usage:
    python3 review_package.py <base-commit> <head-commit> <output-file> [--repo PATH] [--context N]

The reviewer reads one file instead of re-deriving the diff with git commands, and the
diff never has to pass through the coordinating agent's context. Record <base-commit>
(git rev-parse HEAD) before the implementer starts; HEAD~1 drops earlier commits of a
multi-commit task. Standard library only.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path


LOCKFILES = ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb", "uv.lock", "poetry.lock",
             "Pipfile.lock", "Cargo.lock", "Gemfile.lock", "composer.lock", "go.sum")


def git(repo, *args):
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def main():
    parser = argparse.ArgumentParser(description="Write a review package (commits, stat, diff) to a file.")
    parser.add_argument("base")
    parser.add_argument("head")
    parser.add_argument("output")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--context", type=int, default=10, help="lines of context around each change (default 10)")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    base = git(repo, "rev-parse", "--verify", args.base + "^{commit}").strip()
    head = git(repo, "rev-parse", "--verify", args.head + "^{commit}").strip()
    if base == head:
        sys.exit("base and head are the same commit: nothing to review")

    log = git(repo, "log", "--oneline", f"{base}..{head}")
    stat = git(repo, "diff", "--stat", f"{base}..{head}")
    # Lockfiles and build output stay in the stat summary but out of the full diff, so the package stays readable.
    excluded = [f":(exclude,glob)**/{name}" for name in LOCKFILES] + [":(exclude,glob)**/dist/**"]
    diff = git(repo, "diff", f"-U{args.context}", f"{base}..{head}", "--", ".", *excluded)

    # A fence longer than any backtick run in the diff, so Markdown in the diff cannot close it early.
    longest = max((len(run) for run in re.findall(r"`+", diff)), default=0)
    fence = "`" * max(3, longest + 1)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"# Review package\n\nRepository: {repo}\nBase: {base}\nHead: {head}\n\n"
        f"## Commits\n\n```\n{log}```\n\n## Changed files\n\n```\n{stat}```\n\n"
        f"## Diff\n\n{fence}diff\n{diff}{fence}\n"
    )
    print(out.resolve())


if __name__ == "__main__":
    main()
