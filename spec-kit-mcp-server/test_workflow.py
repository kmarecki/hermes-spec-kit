#!/usr/bin/env python3
"""Workflow integration tests for the MCP server.

Tests phase transitions, prerequisite enforcement, bug lifecycle,
reopen flow, and error cases — all via the mcp SDK client.

Run:  python3 spec-kit-mcp-server/test_workflow.py
"""

import anyio, json, os, sys, tempfile, shutil
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession

SERVER_DIR = Path(__file__).resolve().parent
SERVER_SCRIPT = SERVER_DIR / "server.py"

failures = 0


def check(label, ok, detail=""):
    global failures
    if ok:
        print(f"  ✓ {label}")
    else:
        print(f"  ✗ {label}  {detail}")
        failures += 1


async def session():
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_SCRIPT)],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as s:
            await s.initialize()
            yield s


def call(session, tool, args):
    """Call a tool and return parsed result."""
    import anyio
    result = anyio.run(session.call_tool, tool, args)
    return json.loads(result.content[0].text)


# ── Helpers ────────────────────────────────────────────────────────────────

STATE_PATH = Path("specs/.spec-kit/state.json")


def cleanup():
    if STATE_PATH.exists():
        STATE_PATH.unlink()
        parent = STATE_PATH.parent
        if parent.exists() and not any(parent.iterdir()):
            parent.rmdir()


def with_session(fn):
    """Decorator: run test inside a fresh MCP session."""
    async def wrapper():
        params = StdioServerParameters(
            command=sys.executable,
            args=[str(SERVER_SCRIPT)],
        )
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as s:
                await s.initialize()
                await fn(s)
    return wrapper


# ── Tests ──────────────────────────────────────────────────────────────────


async def test_happy_path_forward(session):
    """Full forward cycle: init → phase 0 → 1 → 2 → 3 → 4 → 5 → 6 → close."""
    print("\n═══ Happy path: full forward cycle ═══")

    # Init
    r = await session.call_tool("init_feature", {"feature": "test-feat"})
    d = json.loads(r.content[0].text)
    check("init_feature succeeds", d["success"])
    check("  starts at phase 0", d["state"]["current_phase"] == 0)
    check("  status is active", d["state"]["status"] == "active")

    phases = [
        (0, ["constitution.md"], 1),
        (1, ["spec.md"], 2),
        (2, ["plan.md"], 3),
        (3, ["tasks.md"], 4),
        (4, [], 5),
        (5, ["bugs.md"], 6),
    ]
    for from_phase, artifacts, expected in phases:
        r = await session.call_tool("advance_phase", {
            "feature": "test-feat", "from_phase": from_phase, "artifacts_created": artifacts
        })
        d = json.loads(r.content[0].text)
        name = d.get("phase_name", "?")
        check(f"advance {from_phase} -> {expected} ({name})", d["success"])

    # Close
    r = await session.call_tool("close_feature", {"feature": "test-feat"})
    d = json.loads(r.content[0].text)
    check("close_feature succeeds", d["success"])
    check("  status becomes closed", d["status"] == "closed")

    # List features
    r = await session.call_tool("list_features", {})
    d = json.loads(r.content[0].text)
    feats = [f["feature"] for f in d["features"]]
    check("list_features shows test-feat", "test-feat" in feats)
    closed = [f for f in d["features"] if f["feature"] == "test-feat"][0]
    check("  status is closed", closed["status"] == "closed")
    check("  phase is 6", closed["phase"] == 6)


async def test_prerequisite_enforcement(session):
    """Cannot advance without meeting prerequisites."""
    print("\n═══ Prerequisite enforcement ═══")
    r = await session.call_tool("init_feature", {"feature": "prereq-test"})
    assert json.loads(r.content[0].text)["success"]

    # Try to advance from phase 0 to 2 (skip phase 1 — needs spec.md)
    r = await session.call_tool("advance_phase", {
        "feature": "prereq-test", "from_phase": 0, "artifacts_created": []
    })
    d = json.loads(r.content[0].text)
    check("advance 0->1 succeeds (only needs constitution)", d["success"])

    # Now try to advance from 1 to 3 (skip phase 2 — needs plan.md)
    r = await session.call_tool("advance_phase", {
        "feature": "prereq-test", "from_phase": 1, "artifacts_created": ["spec.md"]
    })
    d = json.loads(r.content[0].text)
    check("advance 1->2 succeeds (spec.md provided)", d["success"])

    # Try to advance from 2 to 4 (skip phase 3 — needs tasks.md)
    r = await session.call_tool("advance_phase", {
        "feature": "prereq-test", "from_phase": 2, "artifacts_created": ["plan.md"]
    })
    d = json.loads(r.content[0].text)
    check("advance 2->3 succeeds (plan.md provided)", d["success"])


async def test_wrong_phase_rejected(session):
    """Advancing from wrong phase should fail."""
    print("\n═══ Wrong phase rejection ═══")
    r = await session.call_tool("init_feature", {"feature": "wrong-phase"})
    assert json.loads(r.content[0].text)["success"]

    r = await session.call_tool("advance_phase", {
        "feature": "wrong-phase", "from_phase": 5, "artifacts_created": []
    })
    d = json.loads(r.content[0].text)
    check("advance from wrong phase rejected", "error" in d and "Phase mismatch" in d["error"])


async def test_duplicate_feature_rejected(session):
    """Cannot init a feature that already exists."""
    print("\n═══ Duplicate feature rejection ═══")
    r = await session.call_tool("init_feature", {"feature": "dup-test"})
    assert json.loads(r.content[0].text)["success"]

    r = await session.call_tool("init_feature", {"feature": "dup-test"})
    d = json.loads(r.content[0].text)
    check("duplicate init returns error", "error" in d and "already exists" in d["error"])


async def test_missing_feature(session):
    """Operations on non-existent features return error."""
    print("\n═══ Missing feature handling ═══")
    r = await session.call_tool("get_feature_state", {"feature": "nope"})
    d = json.loads(r.content[0].text)
    check("get_feature_state on missing returns error", "error" in d)

    r = await session.call_tool("advance_phase", {"feature": "nope", "from_phase": 0})
    d = json.loads(r.content[0].text)
    check("advance_phase on missing returns error", "error" in d)


async def test_reopen_flow(session):
    """Close → reopen → log bug → close again."""
    print("\n═══ Reopen flow ═══")
    r = await session.call_tool("init_feature", {"feature": "reopen-test"})
    assert json.loads(r.content[0].text)["success"]

    # Fast-forward to close
    for f, arts in [(0, ["constitution.md"]), (1, ["spec.md"]), (2, ["plan.md"]),
                     (3, ["tasks.md"]), (4, []), (5, ["bugs.md"])]:
        r = await session.call_tool("advance_phase", {
            "feature": "reopen-test", "from_phase": f, "artifacts_created": arts
        })
        assert json.loads(r.content[0].text)["success"]

    r = await session.call_tool("close_feature", {"feature": "reopen-test"})
    assert json.loads(r.content[0].text)["success"]

    # Reopen
    r = await session.call_tool("reopen_feature", {"feature": "reopen-test"})
    d = json.loads(r.content[0].text)
    check("reopen_feature succeeds", d["success"])
    check("  new_status is reopened", d["new_status"] == "reopened")

    # Close again
    # reopened feature advances 5->6 then closes
    r = await session.call_tool("advance_phase", {
        "feature": "reopen-test", "from_phase": 5, "artifacts_created": []
    })
    d3 = json.loads(r.content[0].text)
    check("advance reopened 5->6 succeeds", d3["success"])

    r = await session.call_tool("close_feature", {"feature": "reopen-test"})
    d4 = json.loads(r.content[0].text)
    check("close reopened feature succeeds", d4["success"])

    # Cannot reopen twice
    r = await session.call_tool("reopen_feature", {"feature": "reopen-test"})
    d5 = json.loads(r.content[0].text)
    check("reopen already-closed feature works again", d5["success"])


async def test_reopen_non_closed_rejected(session):
    """Cannot reopen a feature that isn't closed."""
    print("\n═══ Reopen guard ═══")
    r = await session.call_tool("init_feature", {"feature": "no-reopen"})
    assert json.loads(r.content[0].text)["success"]

    r = await session.call_tool("reopen_feature", {"feature": "no-reopen"})
    d = json.loads(r.content[0].text)
    check("reopen non-closed feature rejected", "error" in d and "not closed" in d["error"])


async def test_update_artifact(session):
    """Update artifact status independently."""
    print("\n═══ Update artifact ═══")
    r = await session.call_tool("init_feature", {"feature": "art-test"})
    assert json.loads(r.content[0].text)["success"]

    r = await session.call_tool("update_artifact", {
        "feature": "art-test", "artifact": "custom.md", "status": "verified"
    })
    d = json.loads(r.content[0].text)
    check("update_artifact succeeds", d["success"])
    check("  status is verified", d["status"] == "verified")

    # Verify via get_feature_state
    r = await session.call_tool("get_feature_state", {"feature": "art-test"})
    d2 = json.loads(r.content[0].text)
    art_status = d2["state"]["artifacts"].get("custom.md")
    check("  artifact visible in state", art_status == "verified")


async def test_get_next_actions_progression(session):
    """get_next_actions shows correct actions at each phase."""
    print("\n═══ Next actions progression ═══")
    r = await session.call_tool("init_feature", {"feature": "actions-test"})
    assert json.loads(r.content[0].text)["success"]

    # Phase 0 — should show advance_to_specify
    r = await session.call_tool("get_next_actions", {"feature": "actions-test"})
    d = json.loads(r.content[0].text)
    actions = [a["action"] for a in d.get("available_actions", [])]
    check("phase 0: advance_to_specify available", "advance_to_specify" in actions)
    check("phase 0: no close yet", "close_feature" not in actions)

    # Advance through phases
    for f, arts in [(0, ["constitution.md"]), (1, ["spec.md"]), (2, ["plan.md"]),
                     (3, ["tasks.md"]), (4, [])]:
        await session.call_tool("advance_phase", {
            "feature": "actions-test", "from_phase": f, "artifacts_created": arts
        })

    # Phase 5 — should show close_feature (no bugs, so close available)
    r = await session.call_tool("get_next_actions", {"feature": "actions-test"})
    d = json.loads(r.content[0].text)
    actions = [a["action"] for a in d.get("available_actions", [])]
    check("phase 5: close_feature available (no bugs)", "close_feature" in actions)


async def test_auto_detect_features(session):
    """Auto-detect registers features from specs/ directory."""
    print("\n═══ Auto-detect ═══")
    # Create a temporary specs dir with some artifacts
    orig_cwd = os.getcwd()
    tmpdir = tempfile.mkdtemp(prefix="spec-kit-test-")
    try:
        os.chdir(tmpdir)
        specs_dir = Path(tmpdir) / "specs" / "auto-feat"
        specs_dir.mkdir(parents=True)
        (specs_dir / "spec.md").write_text("# spec")
        (specs_dir / "plan.md").write_text("# plan")
        (specs_dir / "tasks.md").write_text("# tasks")

        # Re-init session in new cwd
        params = StdioServerParameters(
            command=sys.executable,
            args=[str(SERVER_SCRIPT)],
            cwd=tmpdir,
        )
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as s2:
                await s2.initialize()

                r = await s2.call_tool("auto_detect_features", {})
                d = json.loads(r.content[0].text)
                check("auto_detect found features", d["features_detected"] >= 1)
                check("  auto-feat registered", "auto-feat" in d["features"])

                # Check detected phase — spec+plan+tasks = phase 4 (implement ready)
                r2 = await s2.call_tool("get_feature_state", {"feature": "auto-feat"})
                d2 = json.loads(r2.content[0].text)
                check(f"  detected phase is 4 (has spec+plan+tasks)", d2["state"]["current_phase"] == 4)

        # Cleanup temp state
        os.chdir(orig_cwd)
        tmp_state = Path(tmpdir) / "specs" / ".spec-kit"
        if tmp_state.exists():
            shutil.rmtree(str(tmp_state))
        shutil.rmtree(str(tmpdir))
    except Exception:
        os.chdir(orig_cwd)
        raise


# ── Main ───────────────────────────────────────────────────────────────────


async def main():
    print("═" * 55)
    print("  spec-kit MCP Server — Workflow Integration Tests")
    print("═" * 55)

    cleanup()

    # Run each test in its own session
    tests = [
        test_missing_feature,
        test_duplicate_feature_rejected,
        test_wrong_phase_rejected,
        test_update_artifact,
        test_reopen_non_closed_rejected,
        test_get_next_actions_progression,
        test_happy_path_forward,
        test_prerequisite_enforcement,
        test_reopen_flow,
        test_auto_detect_features,
    ]

    for t in tests:
        # Each test gets its own session (spawns fresh server process)
        async def run_test(test_fn):
            params = StdioServerParameters(
                command=sys.executable,
                args=[str(SERVER_SCRIPT)],
            )
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as s:
                    await s.initialize()
                    await test_fn(s)

        try:
            await run_test(t)
        except Exception as e:
            print(f"  ✗ {t.__name__} crashed: {e}")
            import traceback
            traceback.print_exc()
            global failures
            failures += 1
        finally:
            cleanup()

    print(f"\n{'═' * 55}")
    if failures:
        print(f"  FAILURES: {failures} test(s) failed")
    else:
        print(f"  All tests passed!")
    print(f"{'═' * 55}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(anyio.run(main))
