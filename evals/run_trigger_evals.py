"""Trigger eval with one isolated project root per run (the stock runner shares one
.claude/commands folder across parallel workers, so each query sees several copies of the
skill and is only credited when it picks its own copy)."""
import json, sys, tempfile, os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
sys.path.insert(0, os.environ["SC"])
from scripts.run_eval import run_single_query
from scripts.utils import parse_skill_md

def one(args):
    q, name, desc = args
    root = tempfile.mkdtemp(prefix="trig-", dir=os.path.join(tempfile.gettempdir(), "masterplan-trigger-roots"))
    os.makedirs(os.path.join(root, ".claude"), exist_ok=True)
    try:
        return run_single_query(q, name, desc, 120, root)
    except Exception as e:
        return None

if __name__ == "__main__":
    eval_set = json.load(open(sys.argv[1])); runs = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    name, desc, _ = parse_skill_md(Path(sys.argv[2]))
    if len(sys.argv) > 4: desc = open(sys.argv[4]).read().strip()
    os.makedirs(os.path.join(tempfile.gettempdir(), "masterplan-trigger-roots"), exist_ok=True)
    jobs = [(it["query"], name, desc) for it in eval_set for _ in range(runs)]
    with ProcessPoolExecutor(8) as ex:
        res = list(ex.map(one, jobs))
    out = []; passed = 0
    for i, it in enumerate(eval_set):
        r = res[i*runs:(i+1)*runs]; errors = sum(1 for x in r if x is None)
        valid = runs - errors; trig = sum(1 for x in r if x)
        # Errored runs are excluded rather than counted as non-triggers; a query with no valid run is not scored.
        ok = None if valid == 0 else ((trig / valid) >= 0.5) == it["should_trigger"]
        passed += bool(ok)
        out.append({"query": it["query"], "should_trigger": it["should_trigger"], "triggers": trig, "runs": runs, "errors": errors, "pass": ok})
        label = "ERROR" if ok is None else ("PASS" if ok else "FAIL")
        print(f"[{label}] {trig}/{valid} expected={it['should_trigger']}: {it['query'][:70]}", file=sys.stderr)
    scored = sum(1 for o in out if o["pass"] is not None)
    print(json.dumps({"summary": {"total": len(eval_set), "scored": scored, "passed": passed,
                                  "errored_runs": sum(o["errors"] for o in out)},
                      "description": desc, "results": out}, indent=2))
