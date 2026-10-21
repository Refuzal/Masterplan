#!/usr/bin/env python3
"""Masterplan foundation checker.

Deterministic checks for a Masterplan documentation foundation:
required files for the project's tier, leftover template placeholders,
broken relative links, secrets, ADR structure and status, instruction-file
size budgets, requirement and risk IDs referenced after their entry was
removed, unresolved items that block the readiness gate, and, once
building, milestone plans and build hygiene (commands defined, scratch
folder git-ignored, state.md tracking the build, acceptance tests unchanged
since the plan's 'Acceptance commit' apart from removed pending markers).

Usage:
    python3 check_foundation.py [PROJECT_ROOT] [--tier Light|Standard|Critical]
                                [--phase planning|ready|building|maintenance]
                                [--strict] [--json] [--verbose]

Tier and phase are read from docs/project/state.md unless given.
Exit code: 0 when nothing FAILs (with --strict, also no WARN), 1 otherwise,
2 for usage errors. Standard library only; Python 3.8+.

Paths in AGENTS.md/CLAUDE.md are checked only when written in backticks with a
folder and a doc/config extension (.md .json .jsonc .yaml .yml .toml .txt);
judgment checks (is an Assumed item really easy to reverse?) stay manual.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

TIERS = ("Light", "Standard", "Critical")
PHASES = ("planning", "ready", "building", "maintenance")

REQUIRED_FILES = {
    "Light": [
        "AGENTS.md",
        "docs/project/overview.md",
        "docs/project/state.md",
    ],
    "Standard": [
        "AGENTS.md",
        "docs/project/overview.md",
        "docs/project/state.md",
        "docs/project/requirements.md",
        "docs/architecture/architecture.md",
        "docs/project/roadmap.md",
        "docs/project/risks.md",
        "docs/engineering/standards.md",
    ],
}
REQUIRED_FILES["Critical"] = REQUIRED_FILES["Standard"] + [
    "docs/engineering/security.md",
    "docs/engineering/operations.md",
]

ADR_DIR = "docs/architecture/decisions"
ADR_NAME = re.compile(r"^(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
ADR_STATUSES = ("proposed", "accepted", "superseded", "deprecated", "rejected")
ADR_SECTIONS = {
    "Context": ("context", "context and problem statement"),
    "Options considered": ("options considered", "considered options", "alternatives",
                           "alternatives considered", "options"),
    "Decision": ("decision", "decision outcome"),
    "Consequences": ("consequences",),
    "Revisit when": ("revisit when", "revisit", "reconsider when", "review triggers",
                     "revisit triggers"),
}

AGENTS_SECTIONS = {
    "Commands": ("commands",),
    "Change control": ("change control",),
    "Never": ("never",),
    "Definition of done": ("definition of done",),
}

LABELS = ("Assumption", "Proposed", "Open", "Blocking")

PLACEHOLDER = re.compile(r"(?<![$%{])\{\{[^{}\n]{1,300}\}\}")  # not GitHub Actions ${{ }} or Jinja {%{{
LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
INLINE_CODE = re.compile(r"`([^`\n]+)`")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FIELD = r"^\s*[-*]?\s*\**{name}\**\s*:\s*\**\s*(.+?)\s*\**\s*$"

# (code, regex, level). Hard key formats FAIL; heuristics WARN.
SECRET_PATTERNS = [
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY-----"), "FAIL"),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), "FAIL"),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"), "FAIL"),
    ("github-pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}\b"), "FAIL"),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"), "FAIL"),
    ("stripe-live-key", re.compile(r"\b[sr]k_live_[A-Za-z0-9]{16,}\b"), "FAIL"),
    ("anthropic-key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b"), "FAIL"),
    ("openai-style-key", re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b"), "FAIL"),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"), "FAIL"),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"), "FAIL"),
    ("url-with-password", re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s:/@]+:[^\s@/]{6,}@[^\s)]+", re.I), "WARN"),
    ("assigned-secret", re.compile(
        r"(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret)\b"
        r"\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"), "WARN"),
]

SKIP_DIRS = {"node_modules", ".git", "__pycache__", ".venv", "venv", "dist", "build"}


class Report:
    def __init__(self):
        self.results = []

    def add(self, level, code, message, path=None, line=None):
        self.results.append({"level": level, "code": code, "message": message,
                             "path": path, "line": line})

    def count(self, level):
        return sum(1 for r in self.results if r["level"] == level)


def read(path):
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return ""


def rel(root, path):
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def prose_lines(text):
    """Yield (line_number, line) for lines outside fenced code blocks."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        marker = stripped[:3]
        if marker in ("```", "~~~"):
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            continue
        if fence is None:
            yield number, line


def headings(text):
    found = []
    for number, line in prose_lines(text):
        match = HEADING.match(line)
        if match:
            found.append((len(match.group(1)), match.group(2).strip(), number))
    return found


def has_heading(text, names):
    wanted = {n.lower() for n in names}
    for _, title, _ in headings(text):
        clean = re.sub(r"[*_`]", "", title).strip().lower()
        clean = re.sub(r"\s*\(.*?\)\s*$", "", clean)
        if clean in wanted:
            return True
    return False


def field(text, name):
    pattern = re.compile(FIELD.format(name=re.escape(name)), re.I)
    for _, line in prose_lines(text):
        match = pattern.match(line)
        if match:
            return match.group(1).strip()
    return None


def section_text(text, title):
    """Return the text under a level-2 heading with the given title (case-insensitive)."""
    lines = text.splitlines()
    out, inside = [], False
    for line in lines:
        match = HEADING.match(line)
        if match:
            level, heading = len(match.group(1)), match.group(2).strip().lower()
            if inside and level <= 2:
                break
            if level == 2 and heading.startswith(title.lower()):
                inside = True
                continue
        if inside:
            out.append(line)
    return "\n".join(out) if inside else None


def collect_docs(root):
    docs = []
    for name in ("AGENTS.md", "CLAUDE.md"):
        if (root / name).is_file():
            docs.append(root / name)
    docs_dir = root / "docs"
    if docs_dir.is_dir():
        for path in sorted(docs_dir.rglob("*.md")):
            if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
                continue
            docs.append(path)
    return docs


def detect(root, args, report):
    state = root / "docs/project/state.md"
    text = read(state) if state.is_file() else ""
    tier, phase = args.tier, args.phase
    if tier is None:
        value = field(text, "Tier") if text else None
        if value:
            for candidate in TIERS:
                if value.lower().startswith(candidate.lower()):
                    tier = candidate
        if tier is None:
            tier = "Standard"
            report.add("WARN", "tier-unknown",
                       "No 'Tier: Light|Standard|Critical' line in docs/project/state.md; assuming Standard.",
                       "docs/project/state.md")
    if phase is None:
        value = field(text, "Phase") if text else None
        if value:
            for candidate in PHASES:
                if value.lower().startswith(candidate):
                    phase = candidate
        if phase is None:
            phase = "planning"
            report.add("WARN", "phase-unknown",
                       "No 'Phase: planning|ready|building|maintenance' line in docs/project/state.md; assuming planning.",
                       "docs/project/state.md")
    return tier, phase


def scale_of(root):
    state = root / "docs/project/state.md"
    value = field(read(state), "Scale") if state.is_file() else None
    return value.split()[0].strip("*").capitalize() if value else None


def check_required(root, tier, report):
    required = list(REQUIRED_FILES[tier])
    if scale_of(root) == "Large":
        for name in ("docs/engineering/security.md", "docs/engineering/operations.md"):
            if name not in required:
                required.append(name)
    for name in required:
        if not (root / name).is_file():
            report.add("FAIL", "missing-file", f"Required for tier {tier}"
                       f"{' at Large scale' if name not in REQUIRED_FILES[tier] else ''}: {name}", name)
        else:
            report.add("PASS", "file-present", name, name)
    if not (root / "CLAUDE.md").is_file():
        report.add("WARN", "missing-claude-md",
                   "No CLAUDE.md. Older Claude Code versions ignore AGENTS.md; a CLAUDE.md whose first line is "
                   "'@AGENTS.md' works in every version.", "CLAUDE.md")
    if tier == "Light":
        overview = root / "docs/project/overview.md"
        if overview.is_file():
            text = read(overview)
            for section in ("Requirements", "Architecture", "Roadmap", "Risks"):
                if not has_heading(text, (section,)):
                    report.add("WARN", "light-overview-section",
                               f"Light tier keeps '{section}' inside overview.md, but no such heading was found.",
                               "docs/project/overview.md")


def check_placeholders(root, docs, phase, report):
    level = "WARN" if phase == "planning" else "FAIL"
    for path in docs:
        hits = []
        for number, line in prose_lines(read(path)):
            for match in PLACEHOLDER.finditer(line):
                hits.append((number, match.group(0)))
        if hits:
            first_line, sample = hits[0]
            sample = sample if len(sample) <= 70 else sample[:67] + "...}}"
            report.add(level, "placeholder",
                       f"{len(hits)} unfilled template placeholder(s), first: {sample}",
                       rel(root, path), first_line)


def check_links(root, docs, report):
    for path in docs:
        broken = []
        for number, line in prose_lines(read(path)):
            line_no_code = INLINE_CODE.sub("", line)
            for match in LINK.finditer(line_no_code):
                target = match.group(1).strip()
                if "{{" in target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
                    continue
                target = unquote(target.split("#", 1)[0].split("?", 1)[0])
                if not target:
                    continue
                base = root if target.startswith("/") else path.parent
                resolved = (base / target.lstrip("/")).resolve()
                if not resolved.exists():
                    broken.append((number, target))
        for number, target in broken:
            report.add("FAIL", "broken-link", f"Link target does not exist: {target}", rel(root, path), number)


def check_instruction_paths(root, phase, report):
    """Paths written in backticks inside AGENTS.md and CLAUDE.md, and @imports in CLAUDE.md."""
    for name in ("AGENTS.md", "CLAUDE.md"):
        path = root / name
        if not path.is_file():
            continue
        text = read(path)
        for number, line in prose_lines(text):
            for token in INLINE_CODE.findall(line):
                token = token.strip()
                if " " in token or "{{" in token or "/" not in token:
                    continue  # bare names like `state.md` are prose, not paths
                if re.search(r"[<>*?\[\]]", token):
                    continue  # patterns such as docs/plans/<milestone>.md or docs/**/*.md
                if re.match(r"^[a-z][a-z0-9+.-]*:", token, re.I) or token.startswith(("-", "$", "~")):
                    continue
                if token.endswith("/"):
                    if not (root / token).is_dir():
                        report.add("INFO", "missing-dir",
                                   f"Folder mentioned in {name} does not exist yet: {token}", name, number)
                elif re.search(r"\.(md|jsonc?|ya?ml|toml|txt)$", token):
                    if not (root / token).exists():
                        is_doc = token.startswith("docs/") or token in ("AGENTS.md", "CLAUDE.md")
                        if is_doc or phase in ("building", "maintenance"):
                            report.add("FAIL", "missing-referenced-file",
                                       f"File mentioned in {name} does not exist: {token}", name, number)
                        else:
                            report.add("INFO", "file-not-yet-created",
                                       f"{name} mentions {token}, which the build will create.", name, number)
        if name == "CLAUDE.md":
            imports = [t for t in re.findall(r"(?m)^\s*@(\S+)", text) if "/" in t or "." in t]
            for target in imports:
                if not (root / target).exists() and not (path.parent / target).exists():
                    report.add("FAIL", "broken-import", f"CLAUDE.md imports a missing file: @{target}", name)
            if (root / "AGENTS.md").is_file() and not re.search(r"(?m)^\s*@\.?/?AGENTS\.md\s*$", text):
                report.add("FAIL", "claude-md-no-agents",
                           "CLAUDE.md does not import AGENTS.md ('@AGENTS.md'). When CLAUDE.md exists, Claude Code "
                           "does not load AGENTS.md on its own, so the project rules would be skipped.", name)


def check_secrets(root, docs, report):
    for path in docs:
        for number, line in prose_lines(read(path)):
            for code, pattern, level in SECRET_PATTERNS:
                match = pattern.search(line)
                if match:
                    token = match.group(0)
                    masked = token[:6] + "..." if len(token) > 6 else "..."
                    report.add(level, "secret-" + code,
                               f"Possible secret ({code}): {masked} Remove it and rotate it if real.",
                               rel(root, path), number)


def check_sizes(root, report):
    budgets = [
        ("AGENTS.md", 100, 200),
        ("CLAUDE.md", 60, 150),
        ("docs/project/state.md", 80, 150),
    ]
    for name, warn_at, fail_at in budgets:
        path = root / name
        if not path.is_file():
            continue
        lines = len(read(path).splitlines())
        if lines > fail_at:
            report.add("FAIL", "too-long", f"{name} is {lines} lines (limit {fail_at}, target {warn_at}). "
                       "Move detail into linked docs.", name)
        elif lines > warn_at:
            report.add("WARN", "long", f"{name} is {lines} lines (target {warn_at}).", name)
    docs_dir = root / "docs"
    if docs_dir.is_dir():
        for path in docs_dir.rglob("*.md"):
            lines = len(read(path).splitlines())
            if lines > 500:
                report.add("WARN", "long-doc", f"{lines} lines; consider splitting by component or topic.",
                           rel(root, path))


def check_agents(root, phase, report):
    path = root / "AGENTS.md"
    if not path.is_file():
        return
    text = read(path)
    for section, names in AGENTS_SECTIONS.items():
        if not has_heading(text, names):
            report.add("WARN", "agents-section", f"AGENTS.md has no '{section}' section.", "AGENTS.md")
    if "docs/project/state.md" not in text:
        report.add("WARN", "agents-no-state",
                   "AGENTS.md does not point agents to docs/project/state.md.", "AGENTS.md")
    if phase in ("building", "maintenance"):
        commands = section_text(text, "Commands")
        if commands is not None and "`" not in commands:
            report.add("WARN", "agents-no-commands",
                       "Phase is past planning but AGENTS.md lists no runnable commands.", "AGENTS.md")
        elif commands is not None and re.search(r"(?i)defined in milestone 1|fill in when the project is created", commands):
            report.add("WARN", "agents-commands-placeholder",
                       "AGENTS.md still says commands will be defined later; replace it with the real commands.",
                       "AGENTS.md")


PLAN_SECTIONS = ("Global constraints", "Review focus", "Acceptance tests", "Tasks")


MARKER_LINE = re.compile(r"^\s*(?:test\.fail\(\s*\)\s*;?|@pytest\.mark\.xfail\b.*)\s*$")
MARKER_TOKEN = re.compile(r"\.(?:fails|failing)\b")


def check_acceptance_integrity(root, plan, text, report):
    """Since the plan's 'Acceptance commit', tests/acceptance may only lose pending markers."""
    m = re.search(r"(?im)^\**Acceptance commit:?\**\s*:?\s*`?([0-9a-f]{7,40})`?", text)
    if not m:
        return
    where = rel(root, plan)
    try:
        out = subprocess.run(["git", "-C", str(root), "diff", "-U0", "--no-color", m.group(1), "--",
                              "tests/acceptance"], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        report.add("WARN", "acceptance-unchecked", "Could not run git to check acceptance tests.", where)
        return
    if out.returncode != 0:
        report.add("WARN", "acceptance-unchecked",
                   f"Acceptance commit {m.group(1)} is not in this repository's history.", where)
        return
    removed, added = [], []
    for line in out.stdout.splitlines():
        if line.startswith(("---", "+++")):
            continue
        if line.startswith("-"):
            if not MARKER_LINE.match(line[1:]):
                removed.append(MARKER_TOKEN.sub("", line[1:]).strip())
        elif line.startswith("+"):
            added.append(line[1:].strip())
    if sorted(removed) != sorted(added):
        report.add("FAIL", "acceptance-tests-edited",
                   f"tests/acceptance changed since {m.group(1)} beyond removing pending markers. If a ruling "
                   "changed a test, commit that change alone and update 'Acceptance commit' in the plan.", where)


def check_build(root, phase, report):
    """Milestone plans and build hygiene. Plans are checked in every phase once they exist."""
    plans_dir = root / "docs" / "plans"
    plans = sorted(plans_dir.glob("*.md")) if plans_dir.is_dir() else []
    for plan in plans:
        text = read(plan)
        where = rel(root, plan)
        for section in PLAN_SECTIONS:
            if not has_heading(text, (section,)):
                report.add("WARN", "plan-section", f"Plan has no '{section}' section.", where)
        tasks = re.findall(r"(?m)^### Task \d+", text)
        if not tasks:
            report.add("WARN", "plan-no-tasks", "Plan has no '### Task N' entries.", where)
        elif not re.search(r"(?i)fail", text):
            report.add("WARN", "plan-no-red", "Plan never says to run a test and see it fail first.", where)
        if phase in ("building", "maintenance"):
            check_acceptance_integrity(root, plan, text, report)
    if phase not in ("building", "maintenance"):
        return
    gitignore = root / ".gitignore"
    if (root / ".masterplan").exists():
        ignored = gitignore.is_file() and re.search(r"(?m)^/?\.masterplan/?\s*$", read(gitignore))
        if not ignored:
            report.add("WARN", "scratch-not-ignored",
                       "The .masterplan/ build scratch folder is not listed in .gitignore.", ".gitignore")
    state = root / "docs/project/state.md"
    if state.is_file() and phase == "building":
        stext = read(state)
        if not re.search(r"(?im)^##\s*Build\b", stext):
            report.add("WARN", "state-no-build",
                       "Phase is building but state.md has no '## Build' section (current milestone, plan, ledger, last verified run).",
                       "docs/project/state.md")
        if not plans:
            report.add("WARN", "no-plans",
                       "Phase is building but docs/plans/ has no milestone plan.", "docs/plans")
    manifests = ("package.json", "pyproject.toml", "requirements.txt", "go.mod", "Cargo.toml", "Gemfile",
                 "pom.xml", "build.gradle", "build.gradle.kts", "composer.json", "pubspec.yaml", "Package.swift")
    if any((root / m).is_file() for m in manifests) and not any(
            (root / n).is_file() for n in ("README.md", "README", "README.txt", "readme.md")):
        report.add("WARN" if phase == "maintenance" else "INFO", "no-readme",
                   "No README for people: write how to install, start, stop and back up the app in plain words "
                   "(due with Milestone 1).", "README.md")


def parse_adrs(root, report):
    folder = root / ADR_DIR
    adrs = []
    if not folder.is_dir():
        return None
    for path in sorted(folder.glob("*.md")):
        if path.name.lower() in ("readme.md", "index.md") or "template" in path.name.lower():
            continue
        text = read(path)
        match = ADR_NAME.match(path.name)
        number = match.group(1) if match else None
        if not match:
            report.add("WARN", "adr-name", "ADR file name should look like 0001-short-title.md.", rel(root, path))
            title = re.search(r"ADR-(\d{4})", text)
            number = title.group(1) if title else None
        status = field(text, "Status")
        adrs.append({"path": path, "text": text, "number": number, "status": status})
    return adrs


def check_adrs(root, phase, report):
    adrs = parse_adrs(root, report)
    late = phase != "planning"
    if adrs is None:
        report.add("FAIL" if late else "WARN", "adr-dir-missing",
                   f"No {ADR_DIR}/ folder. Record material decisions as ADRs.", ADR_DIR)
        return
    if not adrs:
        report.add("FAIL" if late else "WARN", "adr-none", "No ADRs recorded yet.", ADR_DIR)
        return
    numbers = {}
    for adr in adrs:
        if adr["number"]:
            numbers.setdefault(adr["number"], []).append(adr)
    for number, group in numbers.items():
        if len(group) > 1:
            names = ", ".join(a["path"].name for a in group)
            report.add("FAIL", "adr-duplicate-number", f"ADR number {number} is used more than once: {names}", ADR_DIR)
    for adr in adrs:
        where = rel(root, adr["path"])
        text = adr["text"]
        title = re.search(r"(?m)^#\s+ADR-(\d{4})", text)
        if title and adr["number"] and title.group(1) != adr["number"]:
            report.add("WARN", "adr-number-mismatch",
                       f"Title says ADR-{title.group(1)} but the file name says {adr['number']}.", where)
        for section, names in ADR_SECTIONS.items():
            if not has_heading(text, names):
                report.add("FAIL", "adr-section", f"ADR is missing the '{section}' section.", where)
        if not has_heading(text, ("evidence", "more information", "sources")):
            report.add("WARN", "adr-evidence", "ADR has no 'Evidence' section.", where)
        status = adr["status"]
        if not status:
            report.add("FAIL", "adr-status", "ADR has no 'Status:' line.", where)
            continue
        if "{{" in status:
            continue  # reported as a placeholder
        word = status.split()[0].strip("*_:.,").lower() if status.split() else ""
        if word not in ADR_STATUSES:
            report.add("FAIL", "adr-status", f"Unknown ADR status '{status}'. Use one of: "
                       "Proposed, Accepted, Superseded by ADR-NNNN, Deprecated, Rejected.", where)
            continue
        if word == "superseded":
            successor = re.search(r"ADR-(\d{4})", status)
            if not successor:
                report.add("FAIL", "adr-superseded-target",
                           "Superseded ADR must name its successor, e.g. 'Superseded by ADR-0007'.", where)
            elif successor.group(1) not in numbers:
                report.add("FAIL", "adr-superseded-target",
                           f"Successor ADR-{successor.group(1)} does not exist.", where)
        if word == "accepted" and not field(text, "Decided by"):
            report.add("WARN", "adr-decided-by", "Accepted ADR does not say who decided ('Decided by:').", where)
        if word == "proposed":
            if phase == "ready":
                report.add("FAIL", "adr-proposed", "ADR is still Proposed; approve or reject it before handoff.", where)
            elif phase in ("building", "maintenance"):
                report.add("WARN", "adr-proposed", "ADR is awaiting approval.", where)
        supersedes = field(text, "Supersedes")
        if supersedes:
            for old in re.findall(r"ADR-(\d{4})", supersedes):
                targets = numbers.get(old, [])
                if not targets:
                    report.add("WARN", "adr-supersedes-missing", f"Supersedes ADR-{old}, which does not exist.", where)
                    continue
                old_status = (targets[0]["status"] or "").lower()
                if adr["number"] and ("superseded" not in old_status or adr["number"] not in old_status):
                    report.add("WARN", "adr-supersession-unlinked",
                               f"ADR-{old} should say 'Superseded by ADR-{adr['number']}'.",
                               rel(root, targets[0]["path"]))
    report.add("PASS", "adr-count", f"{len(adrs)} ADR(s) checked.", ADR_DIR)


def count_labels(root, docs):
    counts = {label: 0 for label in LABELS}
    where = {label: [] for label in LABELS}
    for path in docs:
        for number, line in prose_lines(read(path)):
            if line.lstrip().startswith(">"):
                continue  # legend and purpose lines
            line = INLINE_CODE.sub("", line)  # `[Blocking]` in code is a mention, not a tag
            line = re.sub(r"\[([^\]\n]*)\]\([^)\n]*\)", "", line)  # [Blocking issues](link) is link text
            for label in LABELS:
                hits = len(re.findall(r"\[" + label + r"(?:[:\s][^\]\n]*)?\]", line))
                if hits:
                    counts[label] += hits
                    where[label].append((rel(root, path), number))
    return counts, where


def check_readiness(root, docs, phase, report):
    counts, where = count_labels(root, docs)
    if counts["Blocking"]:
        if phase in ("ready", "building", "maintenance"):
            for path, number in where["Blocking"]:
                report.add("FAIL", "blocking-open", "A [Blocking] item is unresolved.", path, number)
        else:
            report.add("INFO", "blocking-open", f"{counts['Blocking']} [Blocking] item(s) still open.")
    state = root / "docs/project/state.md"
    if state.is_file():
        table = section_text(read(state), "Planning progress")
        if table is not None:
            open_rows, proposed_rows = [], []
            for line in table.splitlines():
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) < 2:
                    continue
                status = re.sub(r"[*_`]", "", cells[1]).strip().lower()
                if status.startswith("open"):
                    open_rows.append(cells[0])
                elif status.startswith("proposed") and "roadmap" not in cells[0].lower():
                    proposed_rows.append(cells[0])
            if phase == "ready" and proposed_rows:
                report.add("WARN", "planning-proposed",
                           "Planning areas still Proposed at handoff (get approval or record as Assumed): "
                           + ", ".join(proposed_rows), "docs/project/state.md")
            if phase == "ready" and open_rows:
                report.add("FAIL", "planning-open",
                           "Planning areas still Open at handoff: " + ", ".join(open_rows), "docs/project/state.md")
            elif phase in ("building", "maintenance"):
                report.add("WARN", "planning-table",
                           "Planning progress table is still in state.md; replace it with current build status.",
                           "docs/project/state.md")
            elif open_rows:
                report.add("INFO", "planning-open", f"{len(open_rows)} planning area(s) still Open.",
                           "docs/project/state.md")
    return counts


def check_requirements(root, tier, report):
    if tier == "Light":
        sources = [root / "docs/project/overview.md"]
    else:
        sources = [root / "docs/project/requirements.md"]
    text = "\n".join(read(p) for p in sources if p.is_file())
    if not text:
        return
    where = rel(root, sources[0])
    if not re.search(r"\bFR-\d+", text):
        report.add("WARN", "no-fr-ids", "No functional requirement IDs (FR-1, FR-2, ...) found.", where)
    if tier != "Light" and not re.search(r"\bNFR-\d+", text):
        report.add("WARN", "no-nfr-ids", "No measurable non-functional requirements (NFR-1, ...) found.", where)
    if not re.search(r"(?im)\bgiven\b.*\bwhen\b.*\bthen\b", text):
        report.add("WARN", "no-acceptance", "No Given/When/Then acceptance criteria found.", where)
    roadmap = root / ("docs/project/overview.md" if tier == "Light" else "docs/project/roadmap.md")
    if roadmap.is_file():
        rtext = read(roadmap)
        if not re.search(r"\bM1\b|Milestone 1", rtext):
            report.add("WARN", "no-m1", "No Milestone 1 (walking skeleton) found.", rel(root, roadmap))
        if not re.search(r"(?i)verification|verify", rtext):
            report.add("WARN", "no-verification", "Milestones do not say how they are verified.", rel(root, roadmap))


ID_REF = re.compile(r"(?<![\w-])(FR|NFR|Q|A|R)-(\d+)(?![\w-])")
ID_HOMES = {"FR": "requirements", "NFR": "requirements", "Q": "risks", "A": "risks", "R": "risks"}


def check_ids(root, tier, docs, report):
    """IDs (FR-, NFR-, Q-, A-, R-) referenced anywhere must still exist in their home document."""
    homes = {}
    for family, name in ID_HOMES.items():
        path = root / "docs/project" / ("overview.md" if tier == "Light" else f"{name}.md")
        if path.is_file():
            homes[family] = path
    defined = {}
    for family, path in homes.items():
        defined.setdefault(path, {m.group(0) for m in ID_REF.finditer(read(path))})
    seen = set()
    for path in docs:
        text = read(path)
        for number, line in prose_lines(text):
            if "{{" in line:
                continue
            for match in ID_REF.finditer(line):
                family, ident = match.group(1), match.group(0)
                home = homes.get(family)
                if home is None or path == home or ident in seen:
                    continue
                if ident not in defined[home]:
                    seen.add(ident)
                    report.add("WARN", "dangling-id",
                               f"{ident} is referenced but no longer exists in {rel(root, home)}; "
                               "point to where the answer now lives, or restore the entry.",
                               f"{rel(root, path)}:{number}")


def run(root, args):
    report = Report()
    tier, phase = detect(root, args, report)
    docs = collect_docs(root)
    check_required(root, tier, report)
    check_placeholders(root, docs, phase, report)
    check_links(root, docs, report)
    check_instruction_paths(root, phase, report)
    check_secrets(root, docs, report)
    check_sizes(root, report)
    check_agents(root, phase, report)
    check_adrs(root, phase, report)
    check_requirements(root, tier, report)
    check_ids(root, tier, docs, report)
    check_build(root, phase, report)
    labels = check_readiness(root, docs, phase, report)
    return report, tier, phase, labels


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check a Masterplan documentation foundation.")
    parser.add_argument("root", nargs="?", default=".", help="Project root (default: current folder)")
    parser.add_argument("--tier", choices=TIERS, help="Override the tier from state.md")
    parser.add_argument("--phase", choices=PHASES, help="Override the phase from state.md")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument("--verbose", action="store_true", help="Also print passing checks")
    args = parser.parse_args(argv)

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"Project root not found: {root}", file=sys.stderr)
        return 2

    report, tier, phase, labels = run(root, args)
    fails, warns = report.count("FAIL"), report.count("WARN")
    ok = fails == 0 and (warns == 0 or not args.strict)

    if args.json:
        print(json.dumps({"root": str(root), "tier": tier, "phase": phase, "ok": ok,
                          "summary": {"fail": fails, "warn": warns, "pass": report.count("PASS")},
                          "labels": labels, "results": report.results}, indent=2))
        return 0 if ok else 1

    print(f"Masterplan foundation check: {root}")
    print(f"Tier: {tier} | Phase: {phase}")
    order = {"FAIL": 0, "WARN": 1, "INFO": 2, "PASS": 3}
    shown = [r for r in report.results if args.verbose or r["level"] in ("FAIL", "WARN", "INFO")]
    for item in sorted(shown, key=lambda r: (order[r["level"]], r["path"] or "", r["line"] or 0)):
        location = item["path"] or ""
        if item["line"]:
            location += f":{item['line']}"
        print(f"  {item['level']:<4}  {item['code']:<26} {location}  {item['message']}".rstrip())
    label_text = ", ".join(f"{labels[k]} {k}" for k in LABELS)
    print(f"Summary: {fails} FAIL, {warns} WARN | Labels: {label_text}")
    if ok:
        print("Result: PASS" + (" (strict)" if args.strict else "") + " - deterministic checks only; "
              "the readiness gate also needs the judgment checks in lifecycle.md.")
    else:
        print("Result: FAIL - fix the items above" + (" (warnings count in strict mode)" if args.strict else "") + ".")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
