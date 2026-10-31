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


FINAL = """
## Round {n} — 2026-10-26 — review:hermes

**Verdict**: {v}
**Reviewed-commit**: {c}
"""


def git(root, *args):
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", *args], cwd=root, check=True,
                   capture_output=True)


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
    d = await call(s, "close_feature", {"feature": "f3"})
    check("close without ADR section / final review → error",
          "Architecture Decisions" in d.get("error", "") and "review-final.md" in d.get("error", ""))
    write(root, "f3", "close.md", "# Close\n\n## Architecture Decisions\n\nnone met the ADR bar\n")
    write(root, "f3", "review-final.md", FINAL.format(n=1, v="NOT READY", c="abc1234"))
    d = await call(s, "close_feature", {"feature": "f3"})
    check("close with NOT READY verdict → error", "NOT READY" in d.get("error", ""))
    write(root, "f3", "review-final.md", FINAL.format(n=1, v="NOT READY", c="abc1234") + FINAL.format(n=2, v="AWAITING-OWNER", c="abc1234"))
    d = await call(s, "close_feature", {"feature": "f3"})
    check("close with AWAITING-OWNER → error naming the owner", "AWAITING-OWNER" in d.get("error", ""))
    write(root, "f3", "review-final.md", FINAL.format(n=1, v="NOT READY", c="abc1234") + FINAL.format(n=2, v="READY", c="abc1234"))
    d = await call(s, "close_feature", {"feature": "f3"})
    check("close without change-record.md → error", "change-record.md" in d.get("error", ""))
    write(root, "f3", "change-record.md", "# Change Record\n")
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
    write(root, "f5", "spec.md", "# Spec\n\n**Size**: S — tiny\n")
    d = await call(s, "lint_artifacts", {"feature": "f5"})
    check("  size S → RED file still required", "T001 [TEST]" in " | ".join(f["msg"] for f in d["findings"]))
    write(root, "f5", "spec.md")
    write(root, "f9", "spec.md"); write(root, "f9", "plan.md")
    write(root, "f9", "tasks.md", "# Tasks\n- T001 [X] [TEST] t — t.py\n- T002 [ ] code — c.py\n- BF-001 [X] fix — c.py\n")
    d = await call(s, "get_feature_state", {"feature": "f9"})
    check("id-first task lines ('- T001 [X] …') are parsed", d["state"]["tasks"] == {"total": 3, "done": 2, "bugfix": 1}, json.dumps(d["state"]["tasks"]))
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


async def test_size_final_review_adr_and_diff_scan(s, root):
    print("\n═══ size tier / final review gate / next_id ADR / diff_scan ═══")
    write(root, "f7", "spec.md", "# Spec\n\n**Size**: S\n")
    d = await call(s, "get_feature_state", {"feature": "f7"})
    check("size read from spec.md header", d["state"]["size"] == "S" and d["state"]["size_declared"] is True)
    check("phase card shows the size", "size: S" in d["phase_card"])
    write(root, "f8", "spec.md")
    d = await call(s, "get_feature_state", {"feature": "f8"})
    check("undeclared size → M, flagged", d["state"]["size"] == "M" and "undeclared" in d["phase_card"])
    d = await call(s, "lint_artifacts", {"feature": "f8"})
    check("lint warns on missing Size line", any("Size" in f["msg"] for f in d["findings"]))

    # a git repo with a base branch and a feature branch
    git(root, "init", "-q", "-b", "main")
    (Path(root) / "src").mkdir()
    (Path(root) / "src/app.py").write_text("x = 1\n")
    git(root, "add", "-A"); git(root, "commit", "-q", "-m", "base")
    git(root, "checkout", "-q", "-b", "feat/007")
    write(root, "f7", "plan.md", "# plan\n- src/app.py\n")
    write(root, "f7", "tasks.md", "# Tasks\n- [x] T001 change — src/app.py\n")
    (Path(root) / "src/app.py").write_text("x = 2  # TODO tidy\npassword = 'hunter2hunter2'\n")
    (Path(root) / "src/extra.py").write_text("<<<<<<< HEAD\n")
    (Path(root) / "cert.pfx").write_text("binary")
    git(root, "add", "-A"); git(root, "commit", "-q", "-m", "feat")
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=root, capture_output=True, text=True).stdout.strip()

    d = await call(s, "diff_scan", {"feature": "f7"})
    checks = {f["check"] for f in d["findings"]}
    check("diff_scan finds conflict marker, secret, todo, forbidden file",
          {"conflict-marker", "secret-assignment", "todo", "forbidden-file"} <= checks, str(checks))
    unplanned = [f for f in d["findings"] if f["check"] == "unplanned-change"]
    check("diff_scan lists unplanned files, not planned ones",
          unplanned and "src/extra.py" in unplanned[0]["files"] and "src/app.py" not in unplanned[0]["files"])
    check("diff_scan not success with errors", d["success"] is False and d["base"] == "main")
    d = await call(s, "diff_scan", {"feature": "f7", "base": "nope"})
    check("diff_scan unknown base → error", "merge-base" in d.get("error", ""))

    d = await call(s, "advance_phase", {"feature": "f7", "from_phase": 5})
    check("5→6 blocked without a final review", "review-final.md" in d.get("error", ""))
    d = await call(s, "get_next_actions", {"feature": "f7"})
    check("next actions offer the final review", any(a["action"] == "final_review" for a in d["available_actions"]))
    write(root, "f7", "review-final.md", FINAL.format(n=1, v="READY", c=head))
    d = await call(s, "advance_phase", {"feature": "f7", "from_phase": 5})
    check("5→6 ok with a fresh READY review", d.get("success"), json.dumps(d))
    d = await call(s, "get_feature_state", {"feature": "f7"})
    check("phase card shows the verdict", f"final review: READY @ {head}" in d["phase_card"])
    git(root, "add", "-A"); git(root, "commit", "-q", "-m", "spec only")
    d = await call(s, "advance_phase", {"feature": "f7", "from_phase": 5})
    check("  a specs/-only commit keeps the review fresh", d.get("success"), json.dumps(d))
    (Path(root) / "src/app.py").write_text("x = 3\n")
    git(root, "add", "-A"); git(root, "commit", "-q", "-m", "code after review")
    d = await call(s, "advance_phase", {"feature": "f7", "from_phase": 5})
    check("  a code commit after the review → stale", "re-run the final review" in d.get("error", ""))
    write(root, "f7", "review-final.md", "# Final review\n\n## Round 1 — x\n\nno verdict\n")
    d = await call(s, "lint_artifacts", {"feature": "f7"})
    msgs = " | ".join(f["msg"] for f in d["findings"])
    check("lint: round without verdict / commit → errors", "Verdict" in msgs and "Reviewed-commit" in msgs and d["success"] is False)

    d = await call(s, "next_id", {"feature": "f7", "kind": "ADR"})
    check("next_id ADR without an ADR dir → error", "ADR directory" in d.get("error", ""))
    (Path(root) / "docs/adr").mkdir(parents=True)
    (Path(root) / "docs/adr/0001-first.md").write_text("# 0001")
    (Path(root) / "docs/adr/0014-later.md").write_text("# 0014")
    d = await call(s, "next_id", {"feature": "f7", "kind": "ADR"})
    check("next_id ADR → 0015 in docs/adr", d.get("next_id") == "0015" and d["adr_dir"] == "docs/adr")
    (Path(root) / "specs/git-conventions.md").write_text("adr_dir: records\nbranch_source: main\n\n## Examples\nbranch_source: develop\nadr_dir: elsewhere\n")
    (Path(root) / "records").mkdir()
    d = await call(s, "next_id", {"feature": "f7", "kind": "ADR"})
    check("adr_dir from git-conventions wins", d.get("next_id") == "0001" and d["adr_dir"] == "records")
    d = await call(s, "diff_scan", {"feature": "f7"})
    check("branch_source: first occurrence wins over the Examples block", d.get("base") == "main", json.dumps(d)[:200])
    d = await call(s, "project_status")
    check("project_status reports adr_dir and merge checklist", d["adr_dir"] == "records" and d["merge_checklist"] == "absent")


ACC_SPEC = """# Spec

**Size**: M

- **FR-001**: System MUST save rules
- **FR-002**: System MUST flag overdue tasks
- **FR-003**: System MUST export

### User Story 1
- **AC-001** (FR-001) Given rules, When saved, Then stored — Verify: integration
- **AC-002** (FR-002) Given a late task, When listed, Then flagged — Verify: unit
- **AC-003** (FR-001, FR-002) Given the settings page, When saved, Then the grid updates — Verify: e2e (spans SPA + BFF + auth)
- **AC-004** (FR-002) Given the migration, When applied to an empty DB, Then it succeeds — Verify: command
- **AC-005** (FR-001) Given the card, When viewed, Then it matches the design — Verify: manual (visual)
"""

ACC_TASKS = """# Tasks
- [x] T001 [TEST] [AC-001] rules integration test — tests/RulesTests.cs
- [x] T002 [TEST] [AC-002] overdue unit test — tests/OverdueTests.cs
- [x] T003 [TEST] [AC-003] e2e — cypress/e2e/overdue.cy.ts
- [x] T004 rules handler — src/Rules.cs
"""

JUNIT = """<?xml version="1.0"?>
<testsuites><testsuite name="s">
  <testcase classname="OverdueTests" name="AC002_late_task_is_flagged"/>
  <testcase classname="OverdueTests" name="other test"{reg}</testcase>
</testsuite></testsuites>
"""

TRX = """<?xml version="1.0"?>
<TestRun xmlns="http://microsoft.com/schemas/VisualStudio/TeamTest/2010"><Results>
  <UnitTestResult testName="RulesTests.AC001_rules_are_stored" outcome="{o}"/>
</Results></TestRun>
"""


async def test_epics_and_design(s, root):
    print("\n═══ epics / design docs (optional dirs) ═══")
    for f in ("e1", "e2", "e3"):
        write(root, f, "spec.md", "# Spec\n\n**Size**: S — x\n**Epic**: rs-m\n")
        write(root, f, "history.md", "# Process History\n")
    d = await call(s, "project_status")
    check("3 specs naming an epic without epics_dir → hint", any("epic 'rs-m'" in h for h in d["hints"]), json.dumps(d["hints"]))
    d = await call(s, "lint_artifacts", {"feature": "e1"})
    check("lint: Epic line without epics_dir → warning", any("no epics_dir" in f["msg"] for f in d["findings"]) and d["success"])
    (Path(root) / "specs/git-conventions.md").write_text("epics_dir: specs/epics\ndesign_dir: docs/design\n")
    d = await call(s, "lint_artifacts", {"feature": "e1"})
    check("lint: epic file missing → warning", any("does not exist" in f["msg"] for f in d["findings"]))
    (Path(root) / "specs/epics").mkdir(parents=True); (Path(root) / "specs/epics/rs-m.md").write_text("# Epic\n| 1 | e2 | S | closed |\n")
    d = await call(s, "lint_artifacts", {"feature": "e1"})
    check("lint: epic file without the feature's row → warning", any("no row for e1" in f["msg"] for f in d["findings"]))
    d = await call(s, "lint_artifacts", {"feature": "e2"})
    check("  feature with a row → no epic warning", not any("epic" in f["msg"].lower() for f in d["findings"]))
    write(root, "e2", "plan.md", "# Plan\n\n**Modules**: reader, bff\n")
    d = await call(s, "lint_artifacts", {"feature": "e2"})
    check("lint: module without design doc → warning", sum("no docs/design/" in f["msg"] for f in d["findings"]) == 2)
    d = await call(s, "project_status")
    check("project_status reports the dirs, no hints once set", d["epics_dir"] == "specs/epics" and d["hints"] == [])


async def test_acceptance(s, root):
    print("\n═══ acceptance criteria: lint / next_id / freeze / status / gates ═══")
    git(root, "init", "-q", "-b", "main")
    write(root, "f10", "history.md", "# Process History: f10\n")
    write(root, "f10", "spec.md", ACC_SPEC.replace(" — Verify: e2e (spans SPA + BFF + auth)", " — Verify: e2e"))
    write(root, "f10", "plan.md")
    write(root, "f10", "tasks.md", ACC_TASKS.replace("- [x] T001 [TEST] [AC-001] rules integration test — tests/RulesTests.cs\n", "- [x] T001 [TEST] [AC-009] stray — tests/RulesTests.cs\n"))
    d = await call(s, "lint_artifacts", {"feature": "f10"})
    msgs = " | ".join(f["msg"] for f in d["findings"])
    check("lint: e2e without a reason → error", "AC-003: Verify: e2e needs a reason" in msgs, msgs)
    check("lint: automated AC without a [TEST] task → error", "AC-001 (Verify: integration) has no" in msgs)
    check("lint: task tagged with an unknown AC → error", "[AC-009] tagged on a task but not defined" in msgs)
    check("lint: FR without an AC → warning", "FR-003" in msgs)
    write(root, "f10", "spec.md", ACC_SPEC)
    write(root, "f10", "tasks.md", ACC_TASKS)
    d = await call(s, "next_id", {"feature": "f10", "kind": "AC"})
    check("next_id AC → AC-006", d.get("next_id") == "AC-006")

    d = await call(s, "acceptance_freeze", {"feature": "f10"})
    check("freeze before the tests exist → error", "write the tests" in d.get("error", ""))
    for f in ("tests/RulesTests.cs", "tests/OverdueTests.cs"):
        (Path(root) / f).parent.mkdir(parents=True, exist_ok=True)
        (Path(root) / f).write_text("// " + f + "\n")
    d = await call(s, "acceptance_freeze", {"feature": "f10"})
    check("freeze hashes the AC test files", d.get("success") and d["frozen"] == 2, json.dumps(d))
    (Path(root) / "cypress/e2e").mkdir(parents=True)
    (Path(root) / "cypress/e2e/overdue.cy.ts").write_text("it('AC-003')\n")
    d = await call(s, "acceptance_freeze", {"feature": "f10"})
    check("  later phase: freeze is additive", d.get("success") and d["added"] == ["cypress/e2e/overdue.cy.ts"] and d["frozen"] == 3)

    (Path(root) / "results").mkdir()
    (Path(root) / "results/unit.xml").write_text(JUNIT.format(reg=">"))
    (Path(root) / "results/int.trx").write_text(TRX.format(o="Failed"))
    d = await call(s, "acceptance_status", {"feature": "f10", "results": "results/*.xml,results/int.trx", "round": 1})
    m = {r["ac"]: r["outcome"] for r in d["matrix"]}
    check("status: TRX failure → fail, JUnit pass → pass", m["AC-001"] == "fail" and m["AC-002"] == "pass", json.dumps(m))
    check("status: e2e not run → deferred, manual → manual, command without evidence → missing",
          m["AC-003"] == "deferred" and m["AC-005"] == "manual" and m["AC-004"] == "missing")
    check("status: result FAIL", d["result"] == "FAIL")
    (Path(root) / "results/int.trx").write_text(TRX.format(o="Passed"))
    write(root, "f10", "evidence/acceptance-r1-AC-004.txt", "RESULT: PASS\ncmd: dotnet ef database update\n")
    d = await call(s, "acceptance_status", {"feature": "f10", "results": "results/*.xml,results/int.trx", "round": 1})
    check("status: all automated pass → PASS", d["result"] == "PASS" and d["counts"]["pass"] == 3, json.dumps(d["counts"]))
    (Path(root) / "results/unit.xml").write_text(JUNIT.format(reg="><failure/>"))
    d = await call(s, "acceptance_status", {"feature": "f10", "results": "results/*.xml,results/int.trx", "round": 1})
    check("status: an untagged failing test is a regression → FAIL", d["result"] == "FAIL" and d["regression_count"] == 1)
    (Path(root) / "results/unit.xml").write_text(JUNIT.format(reg=">"))

    (Path(root) / "tests/OverdueTests.cs").write_text("// weakened\n")
    d = await call(s, "acceptance_status", {"feature": "f10", "results": "results/*.xml,results/int.trx", "round": 1})
    check("status: a frozen test changed → STOPPED", d["result"] == "STOPPED" and d["frozen_changed"] == ["tests/OverdueTests.cs"])
    d = await call(s, "lint_artifacts", {"feature": "f10"})
    check("lint: frozen test changed → error", any("frozen acceptance tests changed" in f["msg"] for f in d["findings"]))
    d = await call(s, "acceptance_freeze", {"feature": "f10"})
    check("freeze refuses a changed file without refreeze", "changed" in d.get("error", ""))
    d = await call(s, "acceptance_freeze", {"feature": "f10", "refreeze": True})
    check("  refreeze without a reason → error", "reason" in d.get("error", ""))
    d = await call(s, "acceptance_freeze", {"feature": "f10", "refreeze": True, "reason": "user: rename of the API, ruling 4"})
    check("  refreeze with the user's reason → ok", d.get("success") and d["refrozen"] == ["tests/OverdueTests.cs"])

    git(root, "add", "-A"); git(root, "commit", "-q", "-m", "impl")
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=root, capture_output=True, text=True).stdout.strip()
    write(root, "f10", "review-final.md", FINAL.format(n=1, v="READY", c=head))
    d = await call(s, "advance_phase", {"feature": "f10", "from_phase": 5})
    check("5→6 blocked without an acceptance round", "acceptance.md" in d.get("error", ""), json.dumps(d))
    d = await call(s, "get_next_actions", {"feature": "f10"})
    check("next actions offer 'accept'", any(a["action"] == "accept" for a in d["available_actions"]))
    check("phase card shows the AC count", "acceptance: 5 ACs · not run" in d["phase_card"])
    write(root, "f10", "acceptance.md", f"# Acceptance\n\n## Round 1 — x\n\n**Result**: FAIL\n**Commit**: {head}\n")
    d = await call(s, "advance_phase", {"feature": "f10", "from_phase": 5})
    check("5→6 blocked by a FAIL round", "every automated AC must pass" in d.get("error", ""))
    with open(Path(root) / "specs/f10/acceptance.md", "a") as fh:
        fh.write(f"\n## Round 2 — y\n\n**Result**: PASS\n**Commit**: {head}\n")
    d = await call(s, "advance_phase", {"feature": "f10", "from_phase": 5})
    check("5→6 ok with a fresh PASS round + READY review", d.get("success"), json.dumps(d))
    (Path(root) / "src").mkdir(); (Path(root) / "src/Rules.cs").write_text("// change\n")
    git(root, "add", "-A"); git(root, "commit", "-q", "-m", "code after acceptance")
    write(root, "f10", "close.md", "# Close\n\n## Architecture Decisions\n\nnone\n")
    d = await call(s, "close_feature", {"feature": "f10"})
    check("close refuses a stale acceptance round", "re-run 'accept" in d.get("error", ""), json.dumps(d))
    write(root, "f10", "acceptance.md", "# Acceptance\n\n## Round 1 — x\n\nnothing\n")
    d = await call(s, "lint_artifacts", {"feature": "f10"})
    msgs = " | ".join(f["msg"] for f in d["findings"])
    check("lint: acceptance round without Result / Commit → errors", "**Result**" in msgs and "**Commit**" in msgs)


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
              test_project_tools, test_next_id_and_lint, test_timestamp_and_history_guard,
              test_size_final_review_adr_and_diff_scan, test_epics_and_design, test_acceptance]:
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
