#!/usr/bin/env python3
"""Workflow integration tests for the derive-and-enforce MCP server.

Every test runs in a fresh temporary project directory with real files under
specs/<feature>/ — the server derives state from them and persists nothing.

Run:  python3 spec-kit-mcp-server/test_workflow.py
"""

import anyio, json, os, sys, tempfile, shutil, subprocess
from pathlib import Path

from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession

SERVER_SCRIPT = Path(__file__).resolve().parent / "server.py"
failures = 0


def check(label, ok, detail=""):
    global failures
    if ok:
        print(f"  ✓ {label}")
    else:
        print(f"  ✗ {label}  {detail}")
        failures += 1


async def call(s, tool, args=None):
    r = await s.call_tool(tool, args or {})
    return json.loads(r.content[0].text)


def write(root, feature, name, text="# x\n"):
    p = Path(root) / "specs" / feature / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


BUGS = """# Bug Report

## Bug Log

### BUG-001: first
- **Status**: {s1}
- **Evidence**: {e1}
- **Verified-by**: {v1}

### BUG-002: second
- **Status**: {s2}
- **Evidence**: [output:/probe: files]
- **Verified-by**: [user / ci:<run-id> / review:<other-agent>]

---

## Summary

| Bug ID | Severity | Area | Status | Needs Clarification |
|--------|----------|------|--------|---------------------|
| BUG-001 | minor | x | {s1} | no |
| BUG-002 | minor | x | {s2} | no |

**Total Bugs**: 2
"""

TASKS = """# Tasks
- [{a}] T001 first task — src/a.py
- [{b}] T002 second task — src/b.py
- [ ] BF-001 fix — src/c.py
"""


# ── Tests ──────────────────────────────────────────────────────────────────


async def test_derivation(s, root):
    print("\n═══ Phase derivation from files ═══")
    d = await call(s, "get_feature_state", {"feature": "nope"})
    check("missing feature → error", "error" in d)

    d = await call(s, "init_feature", {"feature": "f1", "name": "Feature one"})
    check("init_feature creates the directory", d["success"] and (Path(root) / "specs/f1/history.md").exists())
    check("  new feature is phase 1 / new", d["state"]["current_phase"] == 1 and d["state"]["status"] == "new")
    d = await call(s, "init_feature", {"feature": "f1"})
    check("duplicate init → already exists", "already exists" in d.get("error", ""))

    write(root, "f1", "spec.md");                      d = await call(s, "get_feature_state", {"feature": "f1"})
    check("spec.md → phase 2 (plan)", d["state"]["current_phase"] == 2)
    write(root, "f1", "plan.md");                      d = await call(s, "get_feature_state", {"feature": "f1"})
    check("plan.md → phase 3 (tasks)", d["state"]["current_phase"] == 3)
    write(root, "f1", "tasks.md", TASKS.format(a=" ", b=" ")); d = await call(s, "get_feature_state", {"feature": "f1"})
    check("tasks.md pending → phase 4 (implement)", d["state"]["current_phase"] == 4)
    check("  task counts derived", d["state"]["tasks"] == {"total": 3, "done": 0, "bugfix": 1})
    check("  phase card present (10 lines)", d["phase_card"].count("\n") == 9 and "PHASE CARD" in d["phase_card"])
    write(root, "f1", "bugs.md", BUGS.format(s1="open", e1="x", v1="x", s2="claimed")); d = await call(s, "get_feature_state", {"feature": "f1"})
    check("bugs.md → phase 5 (test)", d["state"]["current_phase"] == 5)
    check("  bug counts: 1 open, 1 claimed", d["state"]["bugs"]["open"] == 1 and d["state"]["bugs"]["claimed"] == 1)
    write(root, "f1", "close.md");                     d = await call(s, "get_feature_state", {"feature": "f1"})
    check("close.md + open bug → reopened at phase 5", d["state"]["status"] == "reopened" and d["state"]["current_phase"] == 5)
    write(root, "f1", "bugs.md", BUGS.format(s1="verified", e1="output:e/a.txt", v1="ci:816", s2="superseded")); d = await call(s, "get_feature_state", {"feature": "f1"})
    check("close.md + no open bugs → closed at phase 6", d["state"]["status"] == "closed" and d["state"]["current_phase"] == 6)

    check("no state file was written", not (Path(root) / "specs/.spec-kit").exists())


async def test_advance_validation(s, root):
    print("\n═══ advance_phase validates, never writes ═══")
    write(root, "f2", "spec.md")
    d = await call(s, "advance_phase", {"feature": "f2", "from_phase": 1, "artifacts_created": ["spec.md"]})
    check("advance 1→2 with spec.md on disk", d["success"] and d["to_phase"] == 2)
    d = await call(s, "advance_phase", {"feature": "f2", "from_phase": 1, "artifacts_created": ["plan.md"]})
    check("artifact claimed but not on disk → error", "not on disk" in d.get("error", ""))
    d = await call(s, "advance_phase", {"feature": "f2", "from_phase": 3})
    check("wrong from_phase → Phase mismatch", "Phase mismatch" in d.get("error", ""))
    d = await call(s, "advance_phase", {"feature": "f2", "from_phase": 0})
    check("phase 0 → project-level error", "project-level" in d.get("error", ""))
    write(root, "f2", "plan.md"); write(root, "f2", "tasks.md", TASKS.format(a="x", b="x"))
    write(root, "f2", "bugs.md", BUGS.format(s1="open", e1="x", v1="x", s2="open"))
    d = await call(s, "advance_phase", {"feature": "f2", "from_phase": 5})
    check("5→6 blocked by open bugs", "open bugs" in d.get("error", ""))
    d = await call(s, "get_next_actions", {"feature": "f2"})
    acts = [a["action"] for a in d["available_actions"]]
    check("next actions: bugfix offered, close blocked", "bugfix" in acts and any(a.get("blocked") for a in d["available_actions"] if a["action"] == "advance_to_close"))
    write(root, "f2", "close.md")
    d = await call(s, "advance_phase", {"feature": "f2", "from_phase": 5})
    check("reopened feature (close doc + open bugs) still blocked by open bugs", "open bugs" in d.get("error", ""))
    write(root, "f2", "bugs.md", BUGS.format(s1="verified", e1="output:x", v1="user", s2="superseded"))
    d = await call(s, "advance_phase", {"feature": "f2", "from_phase": 5})
    check("closed feature → use reopen", "closed" in d.get("error", ""))


async def test_close_and_reopen(s, root):
    print("\n═══ close_feature / reopen_feature ═══")
    write(root, "f3", "spec.md"); write(root, "f3", "plan.md"); write(root, "f3", "tasks.md", TASKS.format(a="x", b="x"))
    d = await call(s, "reopen_feature", {"feature": "f3"})
    check("reopen non-closed → error", "not closed" in d.get("error", ""))
    d = await call(s, "close_feature", {"feature": "f3"})
    check("close without close doc → error", "no close.md" in d.get("error", ""))
    write(root, "f3", "close.md")
    write(root, "f3", "bugs.md", BUGS.format(s1="verified", e1="output:x", v1="", s2="claimed"))
    d = await call(s, "close_feature", {"feature": "f3"})
    check("verified without Verified-by → error", "without a Verified-by" in d.get("error", ""))
    write(root, "f3", "bugs.md", BUGS.format(s1="verified", e1="output:x", v1="review:claude", s2="claimed"))
    d = await call(s, "close_feature", {"feature": "f3"})
    check("close ok, claimed bug reported as unverified", d.get("success") and d["claimed_unverified"] == ["BUG-002"])
    d = await call(s, "reopen_feature", {"feature": "f3"})
    check("reopen closed feature ok, writes nothing", d.get("success") and "bugs.md" in d["next"])
    d = await call(s, "list_features")
    f3 = [f for f in d["features"] if f["feature"] == "f3"][0]
    check("list_features derives closed/phase 6", f3["status"] == "closed" and f3["phase"] == 6 and f3["claimed_bugs"] == 1)


async def test_update_artifact(s, root):
    print("\n═══ update_artifact checks disk ═══")
    write(root, "f4", "spec.md")
    d = await call(s, "update_artifact", {"feature": "f4", "artifact": "spec.md", "status": "present"})
    check("present + on disk → ok", d.get("success"))
    d = await call(s, "update_artifact", {"feature": "f4", "artifact": "plan.md", "status": "present"})
    check("present + missing → error", "not on disk" in d.get("error", ""))
    d = await call(s, "update_artifact", {"feature": "f4", "artifact": "spec.md", "status": "absent"})
    check("absent + on disk → error", "exists on disk" in d.get("error", ""))


async def test_project_tools(s, root):
    print("\n═══ project_status / project_set_constitution ═══")
    d = await call(s, "project_status")
    check("version 3, constitution absent, no legacy state", d["version"] == 3 and d["constitution"] == "absent" and d["legacy_state_file"] is False)
    d = await call(s, "project_set_constitution", {"status": "present"})
    check("set present without file → error", "write the file first" in d.get("error", ""))
    (Path(root) / "specs/constitution.md").write_text("# C")
    d = await call(s, "project_set_constitution", {"status": "present", "principles": '{"testing": "A"}'})
    check("set present with file → ok, principles echoed", d.get("success") and d["principles"]["testing"] == "A")
    (Path(root) / "specs/.spec-kit").mkdir(); (Path(root) / "specs/.spec-kit/state.json").write_text("{}")
    d = await call(s, "auto_detect_features")
    check("auto_detect reports legacy state file", d["legacy_state_file"] is True and d["success"])


async def test_next_id_and_lint(s, root):
    print("\n═══ next_id / lint_artifacts ═══")
    write(root, "f5", "spec.md"); write(root, "f5", "plan.md")
    write(root, "f5", "tasks.md", TASKS.format(a="x", b=" "))
    write(root, "f5", "bugs.md", BUGS.format(s1="resolved", e1="x", v1="x", s2="verified"))
    d = await call(s, "next_id", {"feature": "f5", "kind": "BUG"})
    check("next BUG id is BUG-003", d["next_id"] == "BUG-003")
    d = await call(s, "next_id", {"feature": "f5", "kind": "T"})
    check("next T id is T003", d["next_id"] == "T003")
    d = await call(s, "next_id", {"feature": "f5", "kind": "BF"})
    check("next BF id is BF-002", d["next_id"] == "BF-002")
    d = await call(s, "next_id", {"feature": "f5", "kind": "X"})
    check("unknown kind → error", "error" in d)
    d = await call(s, "lint_artifacts", {"feature": "f5"})
    msgs = " | ".join(f["msg"] for f in d["findings"])
    check("lint flags legacy 'resolved' as warning", any(f["severity"] == "warning" and "resolved" in f["msg"] for f in d["findings"]))
    check("lint flags verified without Verified-by", "without Verified-by" in msgs)
    check("lint flags missing history.md", "history.md missing" in msgs)
    check("lint result not success (errors present)", d["success"] is False and d["errors"] >= 2)
    write(root, "f5", "history.md", "# Process History: f5\n")
    write(root, "f5", "bugs.md", BUGS.format(s1="claimed", e1="output:evidence/BF-001-green.txt", v1="", s2="verified").replace(
        "- **Verified-by**: [user / ci:<run-id> / review:<other-agent>]", "- **Verified-by**: user"))
    d = await call(s, "lint_artifacts", {"feature": "f5"})
    check("clean artifacts lint ok", d["success"] is True, json.dumps(d["findings"]))
    write(root, "f5", "close.md")
    d = await call(s, "lint_artifacts", {"feature": "f5"})
    check("closed feature without Current Design → warning", any("Current Design" in f["msg"] for f in d["findings"]) and d["success"] is True)
    write(root, "f5", "plan.md", "# plan\n\n## Current Design\n\nbuilt\n")
    d = await call(s, "lint_artifacts", {"feature": "f5"})
    check("  with Current Design → no warning", not any("Current Design" in f["msg"] for f in d["findings"]))
    write(root, "f5", "tasks.md", "# Tasks\n- [x] T001 [TEST] tests — t.py\n- [x] T002 [SEAM] rates — src/r.py\n- [ ] T003 later — src/l.py\n")
    d = await call(s, "lint_artifacts", {"feature": "f5"})
    msgs = " | ".join(f["msg"] for f in d["findings"])
    check("[SEAM] done without probe → warning", "T002 [SEAM]" in msgs)
    check("[TEST] done without red file → warning", "T001 [TEST]" in msgs)
    write(root, "f5", "evidence/T002-probe-rates.txt", "cmd\nresult\n")
    write(root, "f5", "evidence/core-red.txt", "cmd\nFAILED\n")
    d = await call(s, "lint_artifacts", {"feature": "f5"})
    msgs = " | ".join(f["msg"] for f in d["findings"])
    check("  with probe + red files → no warnings", "[SEAM]" not in msgs and "[TEST]" not in msgs, msgs)


async def test_timestamp_and_history_guard(s, root):
    print("\n═══ timestamp / history_guard ═══")
    d = await call(s, "timestamp")
    check("timestamp is UTC ISO", d["utc"].endswith("+00:00") and "T" in d["utc"])
    write(root, "f6", "spec.md")
    d = await call(s, "history_guard", {"feature": "f6", "phase": "Phase 1"})
    check("no history.md → not ok", d["ok"] is False)
    write(root, "f6", "history.md", "# Process History: f6\n\n## 2020-01-01T00:00:00+00:00 | Phase 1 | spec-kit-specify | claude\n- Artifacts: spec.md\n")
    d = await call(s, "history_guard", {"feature": "f6", "phase": "Phase 2"})
    check("entry for other phase → not ok", d["ok"] is False and "no history entry" in d["reason"])
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "init"], cwd=root, check=True)
    d = await call(s, "history_guard", {"feature": "f6", "phase": "Phase 1"})
    check("entry older than last commit → not ok", d["ok"] is False and "predates" in d["reason"])
    with open(Path(root) / "specs/f6/history.md", "a") as fh:
        fh.write("\n## 2999-01-01T00:00:00+00:00 | Phase 1 | spec-kit-specify | claude\n- Artifacts: spec.md\n")
    d = await call(s, "history_guard", {"feature": "f6", "phase": "Phase 1"})
    check("fresh entry → ok", d["ok"] is True)

    print("\n═══ append_history ═══")
    d = await call(s, "append_history", {"feature": "f6", "phase": "Phase 2", "skill": "spec-kit-plan", "agent": "claude",
                                         "artifacts": "plan.md", "commit": "spec(phase-2): f6 plan", "note": "short note"})
    check("append_history writes a stamped entry", d.get("success") and d["timestamp"].endswith("+00:00"))
    text = (Path(root) / "specs/f6/history.md").read_text()
    check("  entry has the fixed fields", "| Phase 2 | spec-kit-plan | claude" in text and "- Evidence: none — unverified" in text)
    d = await call(s, "history_guard", {"feature": "f6", "phase": "Phase 2"})
    check("  guard sees the new entry", d["ok"] is True)
    d = await call(s, "append_history", {"feature": "f6", "phase": "Phase 3", "skill": "s", "agent": "a", "note": " ".join(["w"] * 26)})
    check("note over 25 words → error", "max 25" in d.get("error", ""))
    d = await call(s, "append_history", {"feature": "f6", "phase": "Phase 3", "skill": "s", "agent": "a", "artifacts": " ".join(["f"] * 70)})
    check("entry over 60 words → error", "max 60" in d.get("error", ""))


# ── Runner ─────────────────────────────────────────────────────────────────


async def run_in_tmp(test_fn):
    root = tempfile.mkdtemp(prefix="spec-kit-test-")
    try:
        (Path(root) / "specs").mkdir()
        params = StdioServerParameters(command=sys.executable, args=[str(SERVER_SCRIPT)], cwd=root)
        async with stdio_client(params) as (read, write_):
            async with ClientSession(read, write_) as s:
                await s.initialize()
                await test_fn(s, root)
    finally:
        shutil.rmtree(root, ignore_errors=True)


async def main():
    print("═" * 55)
    print("  spec-kit MCP Server — Workflow Integration Tests (v3 derive-only)")
    print("═" * 55)
    for t in [test_derivation, test_advance_validation, test_close_and_reopen, test_update_artifact,
              test_project_tools, test_next_id_and_lint, test_timestamp_and_history_guard]:
        try:
            await run_in_tmp(t)
        except Exception as e:
            print(f"  ✗ {t.__name__} crashed: {e}")
            import traceback; traceback.print_exc()
            global failures
            failures += 1
    print(f"\n{'═' * 55}")
    print(f"  FAILURES: {failures} check(s) failed" if failures else "  All tests passed!")
    print(f"{'═' * 55}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(anyio.run(main))
