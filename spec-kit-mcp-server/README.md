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

## MCP Tools (12)

| Tool | Purpose | Replaces |
|------|---------|----------|
| `init_feature` | Register new feature | Manual feature init |
| `get_feature_state` | Get current phase, artifacts, bugs | File-system phase detection |
| `get_next_actions` | Available actions from current state | Routing logic in skills |
| `advance_phase` | Validate and transition to next phase | Manual phase advancement |
| `log_bug` | Log bug, get auto-chain suggestion | Manual bug logging |
| `set_bug_status` | Update bug status | Manual status changes |
| `set_bug_plan_ref` | Link bug to plan section | Manual plan ref tracking |
| `list_features` | List all features | File-system directory scan |
| `reopen_feature` | Reopen closed feature | Manual reopen logic |
| `close_feature` | Close feature after Phase 6 | Manual close tracking |
| `update_artifact` | Update artifact status | Manual artifact tracking |
| `auto_detect_features` | Scan specs/ dir, reconcile state | Initial setup |

> **Note**: In Hermes, tools appear with the `mcp_spec_kit_` prefix (e.g., `mcp_spec_kit_log_bug`).
> Call them using the full prefixed name.

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
  "features": {
    "003-user-auth": {
      "current_phase": 3,
      "mode": "bugfix",
      "status": "active",
      "artifacts": {
        "spec.md": "present",
        "plan.md": "present",
        "tasks.md": "present",
        "bugs.md": "present"
      },
      "bugs": [
        {"bug_id": "BUG-001", "severity": "critical", "status": "open"}
      ]
    }
  }
}
```

## Benefits

- **Deterministic**: State is stored in a file, not inferred by the LLM
- **Compaction-proof**: Survives context loss — MCP server always returns canonical state
- **Enforced transitions**: Server rejects `advance_phase` if prerequisites not met
- **Auto-chain**: `log_bug` returns `next_suggested: "bugfix_plan"` — the LLM doesn't guess what to do next
- **Uses MCP SDK**: Built on the official `mcp` Python SDK (FastMCP) — compatible with stdio transport

## Skill Integration

Skills reference MCP tools by their Hermes-registered name (`mcp_spec_kit_*`). When the MCP server is not configured, skills fall back to the existing filesystem-based behavior. This means:

- **With MCP**: Deterministic routing, enforced transitions, auto-chain
- **Without MCP**: Same workflow as before (LLM-based state detection)

No skill changes are required — the fallback is built in.
