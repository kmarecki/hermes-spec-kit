# spec-kit MCP Server

Deterministic workflow orchestration for spec-kit. Replaces LLM-based state detection with a structured MCP server.

## Quick Start

```bash
# Install (copies server to ~/.hermes/skills/spec-kit/mcp-server/)
./scripts/install.sh

# Add to ~/.hermes/config.yaml:
mcp_servers:
  spec-kit:
    command: "python3"
    args: ["~/.hermes/skills/spec-kit/mcp-server/server.py"]

# Restart Hermes Agent — tools appear as mcp_spec_kit_*
```

## MCP Tools

| Tool | Purpose | Replaces |
|------|---------|----------|
| `spec_kit_get_feature_state` | Get current phase, artifacts, bugs | File-system phase detection |
| `spec_kit_get_next_actions` | Available actions from current state | Routing logic in skills |
| `spec_kit_advance_phase` | Validate and transition to next phase | Manual phase advancement |
| `spec_kit_log_bug` | Log bug, get auto-chain suggestion | Manual bug logging |
| `spec_kit_set_bug_status` | Update bug status | Manual status changes |
| `spec_kit_set_bug_plan_ref` | Link bug to plan section | Manual plan ref tracking |
| `spec_kit_init_feature` | Register new feature | Manual feature init |
| `spec_kit_list_features` | List all features | File-system directory scan |
| `spec_kit_reopen_feature` | Reopen closed feature | Manual reopen logic |
| `spec_kit_close_feature` | Close feature after Phase 6 | Manual close tracking |
| `spec_kit_update_artifact` | Update artifact status | Manual artifact tracking |
| `spec_kit_auto_detect_features` | Scan specs/ dir, reconcile state | Initial setup |

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
- **Zero deps**: Pure Python stdlib — no pip install needed

## Skill Integration

Skills reference MCP tools by their Hermes-registered name (`mcp_spec_kit_*`). When the MCP server is not configured, skills fall back to the existing filesystem-based behavior. This means:

- **With MCP**: Deterministic routing, enforced transitions, auto-chain
- **Without MCP**: Same workflow as before (LLM-based state detection)

No skill changes are required — the fallback is built in.
