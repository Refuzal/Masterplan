#!/usr/bin/env python3
"""Extract one task from a Masterplan milestone plan into its own brief file.

Usage:
    python3 task_brief.py <plan-file> <task-number> <output-file>

The brief contains the plan's header (title, goal, approach) and its Global constraints,
Review focus, Acceptance tests and File map sections, plus the full text of the one task, so an
implementer or reviewer gets exactly its requirements without reading the whole plan.
Headings inside fenced code blocks are ignored. Standard library only.
"""
import re
import sys
from pathlib import Path

HEADER_SECTIONS = ("Global constraints", "Review focus", "Acceptance tests", "File map")


def blocks(lines):
    """Yield (level, title, start, end) for every '## ' and '### ' heading outside code fences."""
    heads, fence = [], False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{2,3}) (.+?)\s*$", line)
        if m:
            heads.append((len(m.group(1)), m.group(2), i))
    for idx, (level, title, start) in enumerate(heads):
        end = len(lines)
        for nlevel, _, nstart in heads[idx + 1:]:
            if nlevel <= level:
                end = nstart
                break
        yield level, title, start, end


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    plan_path, number, out_path = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    if not plan_path.is_file():
        sys.exit(f"plan file not found: {plan_path}")
    lines = plan_path.read_text().splitlines()
    found = list(blocks(lines))

    first = found[0][2] if found else len(lines)
    parts = ["\n".join(lines[:first]).rstrip(), ""]
    for level, title, start, end in found:
        if level == 2 and title in HEADER_SECTIONS:
            parts += ["\n".join(lines[start:end]).rstrip(), ""]

    task = next((b for b in found if b[0] == 3 and re.match(rf"Task {re.escape(number)}\b", b[1])), None)
    if not task:
        sys.exit(f"Task {number} not found in {plan_path}")
    parts += ["## Your task", "", "\n".join(lines[task[2]:task[3]]).rstrip(), ""]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(parts))
    print(out_path.resolve())


if __name__ == "__main__":
    main()
