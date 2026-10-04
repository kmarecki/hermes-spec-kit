#!/usr/bin/env python3
"""spec-kit MCP server — deterministic workflow orchestration.

Provides structured state tools for the spec-kit workflow.
Uses the mcp Python SDK (FastMCP) for proper stdio transport.
State stored in specs/.spec-kit/state.json.

KEY DESIGN: Project-level state (constitution) is separate from
feature-level state. Features start at phase 1 (specify) — the
constitution is a one-time project bootstrap, not a per-feature phase.

Dependency: pip install mcp  (auto-installed by install.sh venv)
"""

import json
import datetime
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# ── State ──────────────────────────────────────────────────────────────────

STATE_DIR = Path("specs/.spec-kit")
STATE_FILE = STATE_DIR / "state.json"

PHASES = {
    0: {"name": "constitution", "artifacts": ["constitution.md"]},
    1: {"name": "specify",       "artifacts": ["spec.md"]},
    2: {"name": "plan",          "artifacts": ["plan.md"]},
    3: {"name": "tasks",         "artifacts": ["tasks.md"]},
    4: {"name": "implement",     "artifacts": []},
    5: {"name": "test",          "artifacts": ["bugs.md"]},
    6: {"name": "close",         "artifacts": ["close.md"]},
}

PHASE_NAMES = {v["name"]: k for k, v in PHASES.items()}

# Feature-level prerequisites only. Constitution is NOT a feature prerequisite
# — it is project-level state checked by the workflow orchestrator.
PREREQUISITES = {
    2: [(1, "spec.md")],
    3: [(2, "plan.md"), (1, "spec.md")],
    4: [(3, "tasks.md")],
    5: [(4, None)],
    6: [(4, None), (5, None)],
}


def _default_state():
    return {
        "version": 2,
        "project": {
            "constitution": "absent",
            "principles": {},
        },
        "features": {},
    }


def _load_state():
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            # Migrate legacy v1 state (features-only) to v2 (project + features)
            if data.get("version", 1) < 2:
                data["version"] = 2
                if "project" not in data:
                    data["project"] = {"constitution": "absent", "principles": {}}
                if "features" not in data:
                    data["features"] = data.get("features", {})
            return data
        except (json.JSONDecodeError, OSError):
            pass
    return _default_state()


def _save_state(state):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    # Atomic write: a crash mid-write must not corrupt state.json (a torn file
    # would make _load_state silently return a fresh default state, losing all
    # feature tracking). Write to a temp file, then atomically replace.
    tmp = STATE_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2))
    tmp.replace(STATE_FILE)


def _get_feature(state, feature):
    f = state["features"].get(feature)
    if f is None:
        return None
    for p in PHASES.values():
        for art in p["artifacts"]:
            if art not in f.get("artifacts", {}):
                f.setdefault("artifacts", {})[art] = "absent"
    return f


def _validate_advance(feature, state, from_phase, to_phase):
    """Validate a phase transition. Returns (ok, reason)."""
    f = _get_feature(state, feature)
    if f is None:
        return False, f"Feature '{feature}' not initialized"
    if f["status"] == "closed":
        return False, f"Feature '{feature}' is closed — use reopen"

    current = f["current_phase"]
    if current != from_phase:
        return False, f"Current phase is {current} ({PHASES[current]['name']}), not {from_phase}"

    # Constitution phase (0) is project-level — features should never advance from it
    if from_phase == 0:
        return False, "Phase 0 (constitution) is project-level — use project_set_constitution, not feature advance_phase"

    prereqs = PREREQUISITES.get(to_phase, [])
    for req_phase, req_artifact in prereqs:
        if req_phase > current:
            phase_name = PHASES[req_phase]["name"]
            return False, f"Prerequisite not met: phase {req_phase} ({phase_name}) must be complete first"
        if req_artifact:
            if f["artifacts"].get(req_artifact) not in ("present", "verified"):
                return False, f"Prerequisite not met: {req_artifact} must exist"

    return True, None


mcp = FastMCP("spec-kit-workflow")


# ── Tools ──────────────────────────────────────────────────────────────────


@mcp.tool(name="project_status")
def project_status() -> str:
    """Get project-level workflow state — constitution status, principles.

    Use this to check whether the project has been bootstrapped before
    routing to feature skills.
    """
    state = _load_state()
    proj = state["project"]
    return json.dumps({
        "version": state["version"],
        "constitution": proj["constitution"],
        "principles": proj.get("principles", {}),
    })


@mcp.tool(name="project_set_constitution")
def project_set_constitution(status: str = "present", principles: str = "") -> str:
    """Set project constitution status after creation/review.

    Args:
        status: 'present' or 'absent'
        principles: Optional JSON string of parsed principle key-value pairs
    """
    state = _load_state()
    state["project"]["constitution"] = status
    if principles:
        try:
            state["project"]["principles"] = json.loads(principles)
        except json.JSONDecodeError:
            return json.dumps({"error": "principles must be valid JSON object", "status": status})
    _save_state(state)
    return json.dumps({"success": True, "constitution": status, "principles": state["project"].get("principles", {})})


@mcp.tool(name="init_feature")
def init_feature(feature: str, name: str = None, mode: str = "specify") -> str:
    """Initialize a new feature in the workflow state.

    Features start at phase 1 (specify). The constitution is project-level
    state tracked separately — see project_status tool.

    Args:
        feature: Feature ID (e.g., 003-user-auth)
        name: Human-readable name (defaults to feature ID)
        mode: specify, bugfix, or reopen
    """
    name = name or feature
    state = _load_state()
    if feature in state["features"]:
        return json.dumps({"error": f"Feature '{feature}' already exists", "state": _get_feature(state, feature)})

    # Features start at phase 1 (specify) — constitution is project-level
    state["features"][feature] = {
        "name": name,
        "mode": mode,
        "current_phase": 1,
        "status": "active",
        "artifacts": {},
        "bugs": [],
        "last_transition": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "history_count": 0,
    }
    _save_state(state)
    return json.dumps({"success": True, "state": _get_feature(state, feature)})


@mcp.tool(name="get_feature_state")
def get_feature_state(feature: str) -> str:
    """Get current workflow state for a feature — phase, artifacts, bugs, status.

    Args:
        feature: Feature ID
    """
    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return json.dumps({"error": f"Feature '{feature}' not found", "available_features": list(state["features"].keys())})
    return json.dumps({"state": f})


@mcp.tool(name="get_next_actions")
def get_next_actions(feature: str) -> str:
    """Get available actions from current phase — includes advance, bugfix, verify, close.

    Args:
        feature: Feature ID
    """
    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return json.dumps({"error": f"Feature '{feature}' not found"})

    phase = f["current_phase"]
    actions = []

    if phase < 6 and f["status"] in ("active",):
        next_phase = phase + 1
        name = PHASES[next_phase]["name"]
        ok, reason = _validate_advance(feature, state, phase, next_phase)
        if ok:
            actions.append({"action": f"advance_to_{name}", "phase": next_phase, "description": f"Advance to phase {next_phase} ({name})"})
        else:
            actions.append({"action": f"advance_to_{name}", "phase": next_phase, "blocked": True, "reason": reason})

    # Bug state lives in bugs.md (file-based, single source of truth).
    # The MCP server cannot see bug status — bugfix/verify routing is done
    # by parsing bugs.md in the skills, not here.

    return json.dumps({"current_phase": phase, "phase_name": PHASES[phase]["name"], "status": f["status"], "available_actions": actions})


@mcp.tool(name="advance_phase")
def advance_phase(feature: str, from_phase: int, artifacts_created: list[str] = None) -> str:
    """Advance to the next phase. Validates prerequisites and artifact state.

    Args:
        feature: Feature ID
        from_phase: Current phase number (validated against stored state)
        artifacts_created: Artifact files created (e.g., spec.md, plan.md)
    """
    artifacts_created = artifacts_created or []
    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return json.dumps({"error": f"Feature '{feature}' not found"})
    if f["current_phase"] != from_phase:
        return json.dumps({"error": f"Phase mismatch: expected {from_phase}, current is {f['current_phase']}"})

    # Phase 0 is project-level — features use project_set_constitution instead
    if from_phase == 0:
        return json.dumps({"error": "Phase 0 (constitution) is project-level — use project_set_constitution tool instead"})

    to_phase = from_phase + 1

    # Mark explicitly provided artifacts
    for art in artifacts_created:
        f["artifacts"][art] = "present"

    # Auto-mark required artifacts for the completed phase (if still absent)
    for art in PHASES[from_phase]["artifacts"]:
        if f["artifacts"].get(art) == "absent":
            f["artifacts"][art] = "present"

    # Validate after artifacts are updated
    ok, reason = _validate_advance(feature, state, from_phase, to_phase)
    if not ok:
        return json.dumps({"error": reason})

    f["current_phase"] = to_phase
    f["last_transition"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    f["history_count"] = f.get("history_count", 0) + 1
    _save_state(state)

    return json.dumps({"success": True, "from_phase": from_phase, "to_phase": to_phase, "phase_name": PHASES[to_phase]["name"], "artifacts_updated": artifacts_created, "state": _get_feature(state, feature)})


@mcp.tool(name="list_features")
def list_features() -> str:
    """List all registered features with phase, status, and bug counts."""
    state = _load_state()
    result = []
    for fid, f in state["features"].items():
        open_bugs = len([b for b in f.get("bugs", []) if b.get("status") == "open"])
        result.append({"feature": fid, "name": f.get("name", fid), "phase": f["current_phase"], "phase_name": PHASES[f["current_phase"]]["name"], "status": f["status"], "open_bugs": open_bugs})
    return json.dumps({"features": result})


@mcp.tool(name="reopen_feature")
def reopen_feature(feature: str) -> str:
    """Reopen a closed feature for bugfixing.

    Args:
        feature: Feature ID
    """
    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return json.dumps({"error": f"Feature '{feature}' not found"})
    if f["status"] not in ("closed",):
        return json.dumps({"error": f"Feature '{feature}' is not closed (status: {f['status']})"})

    f["status"] = "reopened"
    f["current_phase"] = 5
    f["last_transition"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    _save_state(state)

    return json.dumps({"success": True, "feature": feature, "new_status": "reopened", "current_phase": f["current_phase"], "next": "Write bugs to bugs.md via spec-kit-test, or run 'bugfix [feature]'"})


@mcp.tool(name="close_feature")
def close_feature(feature: str) -> str:
    """Mark feature as closed after Phase 6 completes.

    Args:
        feature: Feature ID
    """
    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return json.dumps({"error": f"Feature '{feature}' not found"})
    if f["current_phase"] < 6:
        return json.dumps({"error": f"Feature '{feature}' is at phase {f['current_phase']} — must complete phase 6 first"})

    f["status"] = "closed"
    f["last_transition"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    _save_state(state)
    return json.dumps({"success": True, "feature": feature, "status": "closed"})


@mcp.tool(name="update_artifact")
def update_artifact(feature: str, artifact: str, status: str = "present") -> str:
    """Update artifact status (present, absent, verified).

    Args:
        feature: Feature ID
        artifact: Artifact filename (e.g., spec.md, plan.md)
        status: present, absent, or verified
    """
    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return json.dumps({"error": f"Feature '{feature}' not found"})

    f["artifacts"][artifact] = status
    _save_state(state)
    return json.dumps({"success": True, "feature": feature, "artifact": artifact, "status": status})


@mcp.tool(name="auto_detect_features")
def auto_detect_features(feature: str = None) -> str:
    """Scan specs/ directory and reconcile state — auto-registers unknown features.

    Detects project-level constitution from specs/constitution.md (not per-feature).
    Detects feature phase from per-feature artifact files.

    Args:
        feature: Optional feature ID to scan (scans all if omitted)
    """
    state = _load_state()
    specs_dir = Path("specs")
    if not specs_dir.exists():
        return json.dumps({"error": "specs/ directory not found"})

    # Detect project-level constitution
    proj_constitution = specs_dir / "constitution.md"
    if proj_constitution.exists():
        state["project"]["constitution"] = "present"
    else:
        state["project"]["constitution"] = "absent"

    # Detect features
    feature_dirs = [d for d in specs_dir.iterdir() if d.is_dir() and d.name != ".spec-kit"]
    found = []

    for fd in feature_dirs:
        fid = fd.name
        if feature and fid != feature:
            continue
        f = _get_feature(state, fid)
        if f is None:
            artifacts_present = set()
            for p in fd.iterdir():
                if p.suffix == ".md":
                    artifacts_present.add(p.name)

            # Phase 0 (constitution) is project-level — features start at phase 1
            detected_phase = 1
            for phase_num, phase_info in sorted(PHASES.items()):
                if phase_num == 0:
                    continue  # skip project-level phase for feature detection
                all_present = all((art in artifacts_present) for art in phase_info["artifacts"])
                if all_present:
                    detected_phase = phase_num

            state["features"][fid] = {
                "name": fid,
                "mode": "specify",
                "current_phase": detected_phase,
                "status": "active",
                "artifacts": {a: "present" if a in artifacts_present else "absent" for p in PHASES.values() for a in p["artifacts"]},
                "bugs": [],
                "last_transition": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "history_count": 0,
            }
            found.append(fid)

    _save_state(state)
    return json.dumps({
        "success": True,
        "features_detected": len(found),
        "features": list(state["features"].keys()),
        "project": {"constitution": state["project"]["constitution"]},
    })


# ── Entry point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")
