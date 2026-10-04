# spec-kit MCP Server

Deterministic workflow orchestration for spec-kit. Replaces LLM-based state detection with a structured MCP server using the official `mcp` Python SDK.

## Quick Start

```bash
# Install (copies server to ~/.hermes/skills/spec-kit/mcp-server/)
./scripts/install.sh

# Activate in Hermes
/reload-mcp

# Verify tools
/toolsets    # should show mcp_spec_kit_*
```

## MCP Tools (11)

| Tool | Purpose | Replaces |
|------|---------|----------|
| `init_feature` | Register new feature | Manual feature init |
| `get_feature_state` | Get current phase, artifacts | File-system phase detection |
| `get_next_actions` | Available actions from current state | Routing logic in skills |
| `advance_phase` | Validate and transition to next phase | Manual phase advancement |
| `project_status` | Get project-level state (constitution) | Manual constitution checks |
| `project_set_constitution` | Mark constitution as present after creation | Manual constitution tracking |
| `list_features` | List all features | File-system directory scan |
| `reopen_feature` | Reopen closed feature | Manual reopen logic |
| `close_feature` | Close feature after Phase 6 | Manual close tracking |
| `update_artifact` | Update artifact status | Manual artifact tracking |
| `auto_detect_features` | Scan specs/ dir, reconcile state | Initial setup |

> **Note**: In Hermes, tools appear with the `mcp_spec_kit_` prefix (e.g., `mcp_spec_kit_advance_phase`).
> Call them using the full prefixed name.
>
> **No bug tools**: `bugs.md` is the single source of truth for bugs, written
> directly by `spec-kit-test`. Bug-sync tools (`log_bug`, `set_bug_status`,
> `set_bug_plan_ref`) were removed — see "Bug Tracking" below.

## Architecture

```
User → Hermes (LLM) → mcp_spec_kit_* tools → MCP Server (this)
                                                    ↓
                                              state.json
                                         (specs/.spec-kit/)
```

The MCP server is the **single source of truth** for workflow state. The LLM queries it instead of guessing from file presence. The server enforces transitions — it rejects invalid phase advances.

## State File

Stored at `specs/.spec-kit/state.json`:

```json
{
  "version": 2,
  "project": {
    "constitution": "present",
    "principles": {}
  },
  "features": {
    "003-user-auth": {
      "name": "003-user-auth",
      "current_phase": 3,
      "mode": "bugfix",
      "status": "active",
      "artifacts": {
        "spec.md": "present",
        "plan.md": "present",
        "tasks.md": "present",
        "bugs.md": "present"
      }
    }
  }
}
```

Note: bug state is NOT in state.json — it lives in the feature's `bugs.md`
file. The legacy `bugs` array in feature state is always empty and kept only
for backward compatibility with older state files.

## Bug Tracking

Bug tracking is deliberately **file-based**, not MCP-based:

- `specs/NNN-name/bugs.md` is the single source of truth for bug state.
- Only `spec-kit-test` writes bug entries (after user confirmation).
- Bugfix/verify routing parses `bugs.md` directly in the skills.

The server intentionally has no bug tools. Earlier versions exposed
`log_bug` / `set_bug_status` / `set_bug_plan_ref`, but they let the agent
bypass the bugs.md write and user-confirmation step (a filesystem guard only
caught the first call — once bugs.md existed, the bypass worked again). They
were removed; phase/artifact state — which has no markdown file — stays here.

## Benefits

- **Deterministic**: State is stored in a file, not inferred by the LLM
- **Compaction-proof**: Survives context loss — MCP server always returns canonical state
- **Enforced transitions**: Server rejects `advance_phase` if prerequisites not met
- **Uses MCP SDK**: Built on the official `mcp` Python SDK (FastMCP) — compatible with stdio transport

## Skill Integration

Skills reference MCP tools by their Hermes-registered name (`mcp_spec_kit_*`). When the MCP server is not configured, skills fall back to the existing filesystem-based behavior. This means:

- **With MCP**: Deterministic routing, enforced transitions
- **Without MCP**: Same workflow as before (LLM-based state detection)

No skill changes are required — the fallback is built in.
