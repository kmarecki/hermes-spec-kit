#!/usr/bin/env python3
"""spec-kit MCP server — deterministic workflow orchestration.

Provides structured state tools for the spec-kit workflow.
Hermes connects via stdio transport (built-in native MCP client).
State stored in specs/.spec-kit/state.json.

Protocol: JSON-RPC 2.0 over stdio with Content-Length framing.
Zero external dependencies — uses only Python stdlib.
"""

import json
import os
import sys
import datetime
import textwrap
from pathlib import Path

# ── State ──────────────────────────────────────────────────────────────────

STATE_DIR = Path("specs/.spec-kit")
STATE_FILE = STATE_DIR / "state.json"

# Phase definitions: phase_number -> (name, prerequisites, allowed_next)
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

# Prerequisites: target phase -> list of (required_phase, required_artifact)
PREREQUISITES = {
    1: [(0, "constitution.md")],                          # specify needs constitution
    2: [(1, "spec.md")],                                   # plan needs spec
    3: [(2, "plan.md"), (1, "spec.md")],                   # tasks needs plan+spec
    4: [(3, "tasks.md")],                                   # implement needs tasks
    5: [(4, None)],                                         # test needs implement done
    6: [(4, None), (5, None)],                              # close needs implement+test done
}


def _default_state():
    return {
        "features": {},
        "version": 1
    }


def _load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return _default_state()


def _save_state(state):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def _get_feature(state, feature):
    f = state["features"].get(feature)
    if f is None:
        return None
    # Ensure all artifact keys exist
    for p in PHASES.values():
        for art in p["artifacts"]:
            if art not in f.get("artifacts", {}):
                f.setdefault("artifacts", {})[art] = "absent"
    return f


# ── Phase validation ───────────────────────────────────────────────────────

def _validate_advance(feature, state, from_phase, to_phase):
    """Validate a phase transition. Returns (ok, reason)."""
    f = _get_feature(state, feature)
    if f is None:
        return False, f"Feature '{feature}' not initialized"
    if f["status"] == "closed":
        return False, f"Feature '{feature}' is closed — use reopen"
    if f["status"] == "reopened":
        return False, f"Feature '{feature}' is reopened — bugfix loop in progress"

    current = f["current_phase"]
    if current != from_phase:
        return False, f"Current phase is {current} ({PHASES[current]['name']}), not {from_phase}"

    # Check prerequisites
    prereqs = PREREQUISITES.get(to_phase, [])
    for req_phase, req_artifact in prereqs:
        if req_phase > current:
            phase_name = PHASES[req_phase]["name"]
            return False, f"Prerequisite not met: phase {req_phase} ({phase_name}) must be complete first"
        if req_artifact:
            if f["artifacts"].get(req_artifact) not in ("present", "verified"):
                return False, f"Prerequisite not met: {req_artifact} must exist"

    return True, None


# ── MCP Tool Handlers ──────────────────────────────────────────────────────

def _init_feature(args):
    """Initialize a new feature state."""
    feature = args.get("feature")
    name = args.get("name", feature)
    mode = args.get("mode", "specify")  # specify | bugfix | reopen
    if not feature:
        return {"error": "feature is required"}

    state = _load_state()
    if feature in state["features"]:
        return {"error": f"Feature '{feature}' already exists", "state": _get_feature(state, feature)}

    state["features"][feature] = {
        "name": name,
        "mode": mode,
        "current_phase": 0,
        "status": "active",
        "artifacts": {},
        "bugs": [],
        "last_transition": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "history_count": 0,
    }
    _save_state(state)
    return {"success": True, "state": _get_feature(state, feature)}


def _get_state(args):
    """Get current state for a feature."""
    feature = args.get("feature")
    if not feature:
        return {"error": "feature is required"}

    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return {"error": f"Feature '{feature}' not found", "available_features": list(state["features"].keys())}

    return {"state": f}


def _get_next_actions(args):
    """Get available actions from current phase."""
    feature = args.get("feature")
    if not feature:
        return {"error": "feature is required"}

    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return {"error": f"Feature '{feature}' not found"}

    phase = f["current_phase"]
    actions = []

    # Regular forward phases
    if phase < 6 and f["status"] in ("active",):
        next_phase = phase + 1
        name = PHASES[next_phase]["name"]
        ok, reason = _validate_advance(feature, state, phase, next_phase)
        if ok:
            actions.append({
                "action": f"advance_to_{name}",
                "phase": next_phase,
                "description": f"Advance to phase {next_phase} ({name})"
            })
        else:
            actions.append({
                "action": f"advance_to_{name}",
                "phase": next_phase,
                "blocked": True,
                "reason": reason
            })

    # Bugfix actions (if in test phase or has bugs)
    open_bugs = [b for b in f.get("bugs", []) if b.get("status") == "open"]
    if open_bugs:
        needs_plan = any(b.get("plan_ref") is None for b in open_bugs)
        if needs_plan:
            actions.append({
                "action": "bugfix_plan",
                "description": "Plan bugfix sections for unplanned bugs"
            })
        actions.append({
            "action": "bugfix_tasks",
            "description": "Generate bugfix tasks (BF-###)"
        })
        actions.append({
            "action": "bugfix_implement",
            "description": "Implement bugfix tasks"
        })

    # Verify actions
    resolved_bugs = [b for b in f.get("bugs", []) if b.get("status") == "resolved"]
    if resolved_bugs:
        actions.append({
            "action": "verify_bugs",
            "bug_ids": [b["bug_id"] for b in resolved_bugs],
            "description": "Mark resolved bugs as verified"
        })

    # Close action
    if phase == 5:
        all_verified = all(b.get("status") == "verified" for b in f.get("bugs", []))
        if not f.get("bugs") or all_verified:
            actions.append({
                "action": "close_feature",
                "description": "Generate close document (mandatory)"
            })

    return {
        "current_phase": phase,
        "phase_name": PHASES[phase]["name"],
        "status": f["status"],
        "available_actions": actions,
        "open_bugs": len(open_bugs),
    }


def _advance_phase(args):
    """Advance to the next phase after completing current work."""
    feature = args.get("feature")
    from_phase = args.get("from_phase")
    artifacts_created = args.get("artifacts_created", [])
    if not feature or from_phase is None:
        return {"error": "feature and from_phase are required"}

    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return {"error": f"Feature '{feature}' not found"}

    if f["current_phase"] != from_phase:
        return {"error": f"Phase mismatch: expected {from_phase}, current is {f['current_phase']}"}

    to_phase = from_phase + 1

    # Update artifacts FIRST so validation can check them
    for art in artifacts_created:
        f["artifacts"][art] = "present"

    # Mark required artifacts for the completed phase
    for art in PHASES[from_phase]["artifacts"]:
        if art not in f["artifacts"]:
            f["artifacts"][art] = "present"

    # Validate after artifacts are updated
    ok, reason = _validate_advance(feature, state, from_phase, to_phase)
    if not ok:
        return {"error": reason}

    # Advance
    f["current_phase"] = to_phase
    f["last_transition"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    f["history_count"] = f.get("history_count", 0) + 1

    _save_state(state)
    return {
        "success": True,
        "from_phase": from_phase,
        "to_phase": to_phase,
        "phase_name": PHASES[to_phase]["name"],
        "artifacts_updated": artifacts_created,
        "state": _get_feature(state, feature),
    }


def _log_bug(args):
    """Log a new bug for a feature. Auto-sets next action hint."""
    feature = args.get("feature")
    severity = args.get("severity", "minor")
    description = args.get("description", "")
    area = args.get("area", "")
    if not feature:
        return {"error": "feature is required"}

    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return {"error": f"Feature '{feature}' not found"}

    # Generate bug ID
    existing = f.get("bugs", [])
    bug_numbers = [int(b["bug_id"].replace("BUG-", "")) for b in existing if b["bug_id"].startswith("BUG-")]
    next_num = max(bug_numbers) + 1 if bug_numbers else 1
    bug_id = f"BUG-{next_num:03d}"

    new_bug = {
        "bug_id": bug_id,
        "severity": severity,
        "description": description,
        "area": area,
        "status": "open",
        "plan_ref": None,
        "created": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    f.setdefault("bugs", []).append(new_bug)

    # Ensure bugs.md artifact
    f["artifacts"]["bugs.md"] = "present"

    _save_state(state)
    return {
        "success": True,
        "bug_id": bug_id,
        "severity": severity,
        "next_suggested": "bugfix_plan",
        "reason": "Bug logged — plan a fix approach before implementing",
        "total_open": len([b for b in f["bugs"] if b["status"] == "open"]),
    }


def _set_bug_plan_ref(args):
    """Set the plan ref for a bug (called by spec-kit-plan)."""
    feature = args.get("feature")
    bug_id = args.get("bug_id")
    plan_ref = args.get("plan_ref")
    if not feature or not bug_id or not plan_ref:
        return {"error": "feature, bug_id, and plan_ref are required"}

    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return {"error": f"Feature '{feature}' not found"}

    for bug in f.get("bugs", []):
        if bug["bug_id"] == bug_id:
            bug["plan_ref"] = plan_ref
            _save_state(state)
            return {"success": True, "bug_id": bug_id, "status": bug["status"]}

    return {"error": f"Bug {bug_id} not found"}


def _set_bug_status(args):
    """Set bug status (resolved, verified, etc.)."""
    feature = args.get("feature")
    bug_id = args.get("bug_id")
    status = args.get("status")
    if not feature or not bug_id or not status:
        return {"error": "feature, bug_id, and status are required"}

    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return {"error": f"Feature '{feature}' not found"}

    for bug in f.get("bugs", []):
        if bug["bug_id"] == bug_id:
            bug["status"] = status
            _save_state(state)
            return {"success": True, "bug_id": bug_id, "new_status": status}

    return {"error": f"Bug {bug_id} not found"}


def _list_features(args):
    """List all registered features and their states."""
    state = _load_state()
    result = []
    for fid, f in state["features"].items():
        open_bugs = len([b for b in f.get("bugs", []) if b.get("status") == "open"])
        result.append({
            "feature": fid,
            "name": f.get("name", fid),
            "phase": f["current_phase"],
            "phase_name": PHASES[f["current_phase"]]["name"],
            "status": f["status"],
            "open_bugs": open_bugs,
        })
    return {"features": result}


def _reopen_feature(args):
    """Reopen a closed feature for bugfixing."""
    feature = args.get("feature")
    if not feature:
        return {"error": "feature is required"}

    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return {"error": f"Feature '{feature}' not found"}
    if f["status"] not in ("closed",):
        return {"error": f"Feature '{feature}' is not closed (status: {f['status']})"}

    f["status"] = "reopened"
    # Keep current phase at 5 (test) for bugfix loop
    f["last_transition"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    _save_state(state)
    return {
        "success": True,
        "feature": feature,
        "new_status": "reopened",
        "current_phase": f["current_phase"],
        "next": "log_bug or bugfix_plan",
    }


def _close_feature(args):
    """Mark a feature as closed (Phase 6 complete)."""
    feature = args.get("feature")
    if not feature:
        return {"error": "feature is required"}

    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return {"error": f"Feature '{feature}' not found"}
    if f["current_phase"] < 6:
        return {"error": f"Feature '{feature}' is at phase {f['current_phase']} — must complete phase 6 first"}

    f["status"] = "closed"
    f["last_transition"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    _save_state(state)
    return {
        "success": True,
        "feature": feature,
        "status": "closed",
    }


def _update_artifact(args):
    """Update artifact status for a feature."""
    feature = args.get("feature")
    artifact = args.get("artifact")
    status = args.get("status", "present")
    if not feature or not artifact:
        return {"error": "feature and artifact are required"}

    state = _load_state()
    f = _get_feature(state, feature)
    if f is None:
        return {"error": f"Feature '{feature}' not found"}

    f["artifacts"][artifact] = status
    _save_state(state)
    return {"success": True, "feature": feature, "artifact": artifact, "status": status}


def _auto_detect(args):
    """Scan specs/ directory and reconcile state with filesystem."""
    feature = args.get("feature")
    state = _load_state()

    specs_dir = Path("specs")
    if not specs_dir.exists():
        return {"error": "specs/ directory not found"}

    # List feature directories
    feature_dirs = [d for d in specs_dir.iterdir() if d.is_dir() and d.name != ".spec-kit"]
    found = []

    for fd in feature_dirs:
        fid = fd.name
        f = _get_feature(state, fid)
        if f is None:
            # Auto-detect phase from artifacts
            artifacts_present = set()
            for p in fd.iterdir():
                if p.suffix == ".md":
                    artifacts_present.add(p.name)

            # Determine highest phase with all artifacts present
            detected_phase = 0
            for phase_num, phase_info in sorted(PHASES.items()):
                all_present = all(
                    (art in artifacts_present)
                    for art in phase_info["artifacts"]
                )
                if all_present:
                    detected_phase = phase_num

            # Register detected feature
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
    return {
        "success": True,
        "features_detected": len(found),
        "features": list(state["features"].keys()),
    }


# ── MCP Server ─────────────────────────────────────────────────────────────

TOOL_REGISTRY = {
    "init_feature": {
        "handler": _init_feature,
        "description": "Initialize a new feature in the workflow state",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feature": {"type": "string", "description": "Feature ID (e.g., 003-user-auth)"},
                "name": {"type": "string", "description": "Human-readable name"},
                "mode": {"type": "string", "description": "specify, bugfix, or reopen", "enum": ["specify", "bugfix", "reopen"]},
            },
            "required": ["feature"],
        },
    },
    "get_feature_state": {
        "handler": _get_state,
        "description": "Get current workflow state for a feature — phase, artifacts, bugs, status",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feature": {"type": "string", "description": "Feature ID"},
            },
            "required": ["feature"],
        },
    },
    "get_next_actions": {
        "handler": _get_next_actions,
        "description": "Get available actions from current phase — includes advance, bugfix, verify, close",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feature": {"type": "string", "description": "Feature ID"},
            },
            "required": ["feature"],
        },
    },
    "advance_phase": {
        "handler": _advance_phase,
        "description": "Advance to the next phase. Validates prerequisites and artifact state. Rejects invalid transitions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feature": {"type": "string", "description": "Feature ID"},
                "from_phase": {"type": "integer", "description": "Current phase number (validated against stored state)"},
                "artifacts_created": {"type": "array", "items": {"type": "string"}, "description": "Artifact files created (e.g., spec.md, plan.md, tasks.md)"},
            },
            "required": ["feature", "from_phase"],
        },
    },
    "log_bug": {
        "handler": _log_bug,
        "description": "Log a bug. Auto-generates BUG-NNN ID. Suggests next action (bugfix_plan).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feature": {"type": "string", "description": "Feature ID"},
                "severity": {"type": "string", "enum": ["critical", "major", "minor", "trivial"]},
                "description": {"type": "string"},
                "area": {"type": "string"},
            },
            "required": ["feature"],
        },
    },
    "set_bug_status": {
        "handler": _set_bug_status,
        "description": "Update bug status (open, in-progress, resolved, verified)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feature": {"type": "string"},
                "bug_id": {"type": "string"},
                "status": {"type": "string", "enum": ["open", "in-progress", "resolved", "verified"]},
            },
            "required": ["feature", "bug_id", "status"],
        },
    },
    "set_bug_plan_ref": {
        "handler": _set_bug_plan_ref,
        "description": "Link a bug to its plan section (called by spec-kit-plan)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feature": {"type": "string"},
                "bug_id": {"type": "string"},
                "plan_ref": {"type": "string", "description": "Reference to plan section (e.g., plan.md#bugfix-BUG-001)"},
            },
            "required": ["feature", "bug_id", "plan_ref"],
        },
    },
    "list_features": {
        "handler": _list_features,
        "description": "List all registered features with phase, status, and bug counts",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    "reopen_feature": {
        "handler": _reopen_feature,
        "description": "Reopen a closed feature for bugfixing",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feature": {"type": "string"},
            },
            "required": ["feature"],
        },
    },
    "close_feature": {
        "handler": _close_feature,
        "description": "Mark feature as closed after Phase 6 completes",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feature": {"type": "string"},
            },
            "required": ["feature"],
        },
    },
    "update_artifact": {
        "handler": _update_artifact,
        "description": "Update artifact status (present, absent, verified)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feature": {"type": "string"},
                "artifact": {"type": "string"},
                "status": {"type": "string", "enum": ["present", "absent", "verified"]},
            },
            "required": ["feature", "artifact"],
        },
    },
    "auto_detect_features": {
        "handler": _auto_detect,
        "description": "Scan specs/ directory and reconcile state — auto-registers unknown features",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feature": {"type": "string"},
            },
        },
    },
}


# ── JSON-RPC over stdio ────────────────────────────────────────────────────

def _read_message():
    """Read a JSON-RPC message from stdin with Content-Length framing."""
    raw = b""
    content_length = None
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None  # EOF
        raw += line
        line = line.strip()
        if not line:
            # End of headers — read body based on Content-Length
            break
        if line.startswith(b"Content-Length:"):
            content_length = int(line.split(b":")[1].strip())

    if content_length is None:
        return None

    body = sys.stdin.buffer.read(content_length)
    if not body:
        return None

    return json.loads(body.decode("utf-8"))


def _send_message(msg):
    """Send a JSON-RPC message to stdout with Content-Length framing."""
    body = json.dumps(msg)
    data = f"Content-Length: {len(body)}\r\n\r\n{body}"
    sys.stdout.write(data)
    sys.stdout.flush()


# ── MCP lifecycle ──────────────────────────────────────────────────────────

def _handle_initialize(req):
    """Handle MCP initialize request."""
    return {
        "jsonrpc": "2.0",
        "id": req.get("id"),
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "sampling": {},
            },
            "serverInfo": {
                "name": "spec-kit-workflow",
                "version": "1.0.0",
            },
        },
    }


def _handle_list_tools(req):
    """Handle tools/list request."""
    tools = []
    for name, info in TOOL_REGISTRY.items():
        tools.append({
            "name": f"spec_kit_{name}",
            "description": info["description"],
            "inputSchema": info["inputSchema"],
        })
    return {
        "jsonrpc": "2.0",
        "id": req.get("id"),
        "result": {"tools": tools},
    }


def _handle_call_tool(req):
    """Handle tools/call request."""
    params = req.get("params", {})
    tool_name = params.get("name", "")
    args = params.get("arguments", {})

    # Strip spec_kit_ prefix for local dispatch
    local_name = tool_name.replace("spec_kit_", "", 1)
    tool_info = TOOL_REGISTRY.get(local_name)

    if not tool_info:
        return {
            "jsonrpc": "2.0",
            "id": req.get("id"),
            "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
        }

    try:
        result = tool_info["handler"](args)
        return {
            "jsonrpc": "2.0",
            "id": req.get("id"),
            "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]},
        }
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": req.get("id"),
            "error": {"code": -32603, "message": f"Internal error: {e}"},
        }


def _handle_notifications(req):
    """Handle notifications (discard)."""
    return None


def main():
    """Main MCP server loop."""
    while True:
        req = _read_message()
        if req is None:
            break

        method = req.get("method", "")

        if method == "initialize":
            response = _handle_initialize(req)
        elif method == "notifications/initialized":
            response = _handle_notifications(req)
        elif method == "tools/list":
            response = _handle_list_tools(req)
        elif method == "tools/call":
            response = _handle_call_tool(req)
        else:
            response = {
                "jsonrpc": "2.0",
                "id": req.get("id"),
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }

        if response is not None:
            _send_message(response)


if __name__ == "__main__":
    main()
