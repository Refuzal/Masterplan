"""Run check_foundation.py against fixtures and assert on the result codes."""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
CHECKER = Path(__file__).resolve().parent.parent / "scripts" / "check_foundation.py"


def run(name, *extra):
    proc = subprocess.run([sys.executable, str(CHECKER), str(HERE / "checker-fixtures" / name), "--json", *extra],
                          capture_output=True, text=True)
    data = json.loads(proc.stdout)
    return proc.returncode, data


def codes(data, level=None):
    return {r["code"] for r in data["results"] if level is None or r["level"] == level}


failures = []


def expect(cond, message):
    if not cond:
        failures.append(message)
    print(("ok   " if cond else "FAIL ") + message)


# 1. Complete Standard project at handoff passes cleanly.
rc, data = run("good-standard")
expect(rc == 0, "good-standard exits 0")
expect(data["tier"] == "Standard" and data["phase"] == "ready", "good-standard tier/phase detected")
expect(not codes(data, "FAIL"), f"good-standard has no FAIL (got {codes(data, 'FAIL')})")
expect(not codes(data, "WARN"), f"good-standard has no WARN (got {codes(data, 'WARN')})")
expect(data["labels"]["Assumption"] == 1 and data["labels"]["Open"] == 1,
       f"label counts ignore legend lines (got {data['labels']})")

# 2. Light project passes with only overview + state + ADRs.
rc, data = run("good-light")
expect(rc == 0, f"good-light exits 0 (FAIL: {codes(data, 'FAIL')})")
expect(data["tier"] == "Light", "good-light tier detected")
expect("light-overview-section" not in codes(data), "good-light overview has required sections")

# 3. During planning, placeholders and blocking items are warnings/info, not failures.
rc, data = run("planning-partial")
expect(codes(data, "FAIL") == {"missing-file", "missing-referenced-file", "broken-link"},
       f"planning-partial fails only on missing files and links (FAIL: {codes(data, 'FAIL')})")
expect("placeholder" in codes(data, "WARN"), "planning placeholders are WARN")
expect("blocking-open" in codes(data, "INFO"), "planning blocking items are INFO")
rc_ready, data_ready = run("planning-partial", "--phase", "ready")
expect("placeholder" in codes(data_ready, "FAIL") and "blocking-open" in codes(data_ready, "FAIL"),
       "--phase ready turns placeholders and blocking items into FAIL")
rc_strict, _ = run("planning-partial", "--strict")
expect(rc_strict == 1, "strict mode fails on warnings")

# 4. Broken project catches every planted defect.
rc, data = run("broken")
fails = codes(data, "FAIL")
expect(rc == 1, "broken exits 1")
for code in ("missing-file", "placeholder", "broken-link", "broken-import", "secret-aws-access-key",
             "too-long", "adr-section", "adr-status", "adr-duplicate-number", "adr-superseded-target",
             "blocking-open", "planning-open"):
    expect(code in fails, f"broken: detects {code}")

# 5. Overrides work.
rc, data = run("good-standard", "--tier", "Critical")
expect(rc == 1 and "missing-file" in codes(data, "FAIL"), "Critical override requires security/operations docs")
rc, data = run("good-standard", "--phase", "building")
expect("planning-table" in codes(data, "WARN"), "building phase warns about leftover planning table")

# 5b. Files the build will create are INFO, missing docs still FAIL.
import shutil
src = HERE / "checker-fixtures" / "good-standard"
dst = HERE / "checker-fixtures" / "future-files"
if dst.exists(): shutil.rmtree(dst)
shutil.copytree(src, dst)
agents = (dst / "AGENTS.md").read_text().replace("## Commands", "## Commands\nAgent settings live in `.claude/settings.json` and `config/app.yaml`.")
(dst / "AGENTS.md").write_text(agents)
rc, data = run("future-files")
expect(rc == 0 and "file-not-yet-created" in codes(data, "INFO"), "files the build creates are INFO at handoff")
rc, data = run("future-files", "--phase", "building")
expect("missing-referenced-file" in codes(data, "FAIL"), "the same files FAIL once building")

# 5c. CI expressions such as ${{ github.sha }} are not template placeholders.
dst2 = HERE / "checker-fixtures" / "ci-expressions"
if dst2.exists(): shutil.rmtree(dst2)
shutil.copytree(src, dst2)
std = dst2 / "docs" / "engineering" / "standards.md"
std.write_text(std.read_text() + "\nDeploy tag: `app:${{ github.sha }}`\n")
rc, data = run("ci-expressions")
expect(rc == 0 and "placeholder" not in codes(data), "GitHub Actions ${{ }} expressions are not placeholders")

# 5d. Build phase: plans are checked, scratch must be ignored, commands must be real.
dst3 = HERE / "checker-fixtures" / "building"
if dst3.exists(): shutil.rmtree(dst3)
shutil.copytree(src, dst3)
st = dst3 / "docs" / "project" / "state.md"
st.write_text(re.sub(r"(?m)^Phase: .*$", "Phase: building", st.read_text()))
(dst3 / ".masterplan" / "m1").mkdir(parents=True)
rc, data = run("building")
expect("no-plans" in codes(data, "WARN") and "scratch-not-ignored" in codes(data, "WARN"),
       "building without plans or ignored scratch is flagged")
(dst3 / ".gitignore").write_text("node_modules/\n.masterplan/\n")
(dst3 / "docs" / "plans").mkdir(parents=True)
(dst3 / "docs" / "plans" / "m1.md").write_text(
    "# Plan: M1\n\n## Global constraints\n- x\n\n## Review focus\n1. y\n\n## Acceptance tests\n- z\n\n## Tasks\n\n"
    "### Task 1: thing\n- [ ] Write the failing test\n- [ ] Run it and see it fail\n")
rc, data = run("building")
expect(not ({"no-plans", "scratch-not-ignored", "plan-section", "plan-no-tasks", "plan-no-red"} & codes(data)),
       f"a building project with a proper plan and ignored scratch passes build checks (got {codes(data)})")
(dst3 / "docs" / "plans" / "m2.md").write_text("# Plan: M2\n\nSome notes.\n")
rc, data = run("building")
expect({"plan-section", "plan-no-tasks"} <= codes(data, "WARN"), "a plan without sections or tasks is flagged")

# 5e. IDs referenced after their entry was deleted are flagged.
dst4 = HERE / "checker-fixtures" / "dangling"
if dst4.exists(): shutil.rmtree(dst4)
shutil.copytree(src, dst4)
arch = dst4 / "docs" / "architecture" / "architecture.md"
arch.write_text(arch.read_text() + "\nReview log: resolved Q-99 and FR-1.\n")
rc, data = run("dangling")
dangling = [r for r in data["results"] if r["code"] == "dangling-id"]
expect(len(dangling) == 1 and "Q-99" in dangling[0]["message"],
       f"a reference to a deleted question is flagged, an existing requirement is not (got {dangling})")

# 5f. Tag names in link text or inline code, path patterns and non-path @lines are not defects.
dst5 = HERE / "checker-fixtures" / "mentions"
if dst5.exists(): shutil.rmtree(dst5)
shutil.copytree(src, dst5)
ag = dst5 / "AGENTS.md"
ag.write_text(ag.read_text() + "\nSee [Blocking issues](docs/project/risks.md) and `[Blocking]` tags.\nPlans: `docs/plans/<milestone>.md`\n")
cl = dst5 / "CLAUDE.md"
cl.write_text(cl.read_text() + "\n@mention-style note, not an import\n")
rc, data = run("mentions", "--phase", "ready")
expect(rc == 0 and data["labels"]["Blocking"] == 0,
       f"mentions of tags, path patterns and @notes pass at handoff (got {codes(data, 'FAIL')}, {data['labels']})")

# 5g. Large scale requires the security and operations documents at any tier.
dst6 = HERE / "checker-fixtures" / "large"
if dst6.exists(): shutil.rmtree(dst6)
shutil.copytree(src, dst6)
st6 = dst6 / "docs" / "project" / "state.md"
st6.write_text(re.sub(r"(?m)^(Tier: .*)$", r"\1\nScale: Large", st6.read_text()))
rc, data = run("large")
missing = {r["path"] for r in data["results"] if r["code"] == "missing-file"}
expect(rc == 1 and {"docs/engineering/security.md", "docs/engineering/operations.md"} <= missing,
       f"a Large-scale Standard project must have security.md and operations.md (got {missing})")

# 5h. Acceptance tests may only lose their pending markers after the plan's acceptance commit.
dst7 = HERE / "checker-fixtures" / "acceptance"
if dst7.exists(): shutil.rmtree(dst7)
shutil.copytree(dst3, dst7)
(dst7 / "tests" / "acceptance").mkdir(parents=True)
acc = dst7 / "tests" / "acceptance" / "board.test.ts"
acc.write_text("test.fails('adds a task', async () => {\n  expect(count).toBe(1)\n})\n")
git = lambda *a: subprocess.run(["git", "-C", str(dst7), "-c", "user.name=t", "-c", "user.email=t@example.invalid", *a],
                                capture_output=True, text=True)
git("init", "-q"); git("add", "-A"); git("commit", "-qm", "acceptance tests")
sha = git("rev-parse", "--short", "HEAD").stdout.strip()
plan = dst7 / "docs" / "plans" / "m1.md"
plan.write_text(plan.read_text().replace("## Acceptance tests\n", f"## Acceptance tests\nAcceptance commit: {sha}\n"))
acc.write_text("test('adds a task', async () => {\n  expect(count).toBe(1)\n})\n")
rc, data = run("acceptance")
expect("acceptance-tests-edited" not in codes(data), "removing a pending marker is allowed")
acc.write_text("test('adds a task', async () => {\n  expect(count).toBe(0)\n})\n")
rc, data = run("acceptance")
expect("acceptance-tests-edited" in codes(data, "FAIL"), "editing an acceptance assertion fails the check")

# 6. Human-readable mode runs and prints a result line.
proc = subprocess.run([sys.executable, str(CHECKER), str(HERE / "checker-fixtures" / "broken")],
                      capture_output=True, text=True)
expect("Result: FAIL" in proc.stdout, "text output prints a result line")
print()
print(proc.stdout)

print(f"{len(failures)} failure(s)")
sys.exit(1 if failures else 0)
