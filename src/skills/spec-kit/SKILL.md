---
name: spec-kit
description: Spec-Driven Development (SDD) workflow for Hermes Agent. Load via 'spec-kit' or 'speckit' prefix commands or natural language phrases (e.g. 'spec-kit bugfix [feature]', 'speckit bugfix [feature]', 'spec-kit implement [feature]', 'speckit implement [feature]', "bugfix [feature]", "implement [feature]", "plan [feature]").
category: software-development
---

# Spec-Driven Development (SDD)

Spec-driven development for Hermes Agent. Specifications drive code, not the other way around.

**For phase routing (bugfix, implement, plan, reopen, close), load `spec-kit-workflow` instead.** The workflow skill handles all routing decisions based on artifact state and trigger phrases. This skill only documents the overall workflow, conventions, and project structure.

## ⚠️ Critical Approach Rule: Read First, Build Second

**ALWAYS read the source repository design documents before implementing a skill or template that mirrors an existing system.** This prevents creating simplified approximations instead of faithful implementations.

When a user asks to implement parity with an existing system:
1. Read the actual source design docs, templates, and workflows FIRST
2. Analyze all commands, templates, and their exact structures
3. Only then build or update templates

## Core Workflow

```text
Constitution → Specify → Clarify (opt) → Plan → Tasks → Implement → Test
                                                                      │
                                                                      └── bugfix loop ──┐
                                                                ┌──────────────────────┘
                                                                ▼
                                                          [Clarify] → Plan → Tasks → [Review] → Implement → Test → Close (mandatory)
```

| Mode | Trigger | Behavior |
|------|---------|----------|
| **specify** (default) | "Create a spec for [feature]" | Full forward phase sequence, manual transitions |
| **bugfix** | "bugfix [feature]" | Auto-chains Plan→Tasks→Implement, prompts to close |
| **reopen** | "Reopen [feature]" | Creates bugfix branch from closed feature, preserves original close |

**Constitution is mandatory** in every mode. **Phase 6 (Close) is mandatory** to mark a feature complete.

## Phase Reference

Every phase skill is a **one-screen checklist**; its complete procedure lives in `spec-kit/references/skills/<skill>.md` and is loaded on demand. Phase skills carry their own guardrails through preflight — load `spec-kit-workflow` only for routing commands (bugfix, quickfix, reopen, close, status).

| Phase | Skill | Purpose |
|-------|-------|---------|
| 0 — Constitution | `spec-kit-constitution` | Project principles (brownfield/free-text/wizard) |
| 1 — Specify | `spec-kit-specify` | Functional requirements, user scenarios |
| 1.5 — Clarify | `spec-kit-clarify` | Resolve ambiguities in the spec |
| 2 — Plan | `spec-kit-plan` | Architecture, data flow, module boundaries |
| 3 — Tasks | `spec-kit-tasks` | Executable task breakdown with TDD flag |
| 3.5 — Review | `spec-kit-review` | Pre/post implement quality check (optional) |
| 4 — Implement | `spec-kit-implement` | Phase-level TDD execution |
| 5 — Test | `spec-kit-test` | Bug tracking and manual testing |
| 6 — Close | `spec-kit-summarize` | Spec health score, gap analysis, deviation patching |
| — Refresh | `spec-kit-refresh` | Standalone artifact reconciliation |

## AGENTS.md Conventions

**Put in AGENTS.md**: which skills are available, active spec directories, project-specific context (tech stack, build commands), project conventions.

**Keep out of AGENTS.md**: trigger phrase lists, routing tables, workflow mechanics, phase diagrams, bugfix loop details. Routing belongs in skill files.

## Workflow Tracking

Every spec directory maintains `specs/NNN-name/history.md` — an append-only **record** (not a story). Each phase skill appends one fixed-field entry via `mcp_spec_kit_append_history` or `spec-kit/scripts/spec-kit-log.sh`, which stamp the real time and cap the entry at 60 words:

```markdown
## <UTC timestamp> | Phase N — name | spec-kit-<skill> | <agent>
- Artifacts: … · - Tests: … · - Evidence: … · - Commit: … · - Note: ≤ 25 words
```

Narrative belongs in `implementation-summary.md`. Format and rules: `references/history-tracking.md`.

## Template Path Convention

All skills reference templates as `spec-kit/templates/<name>-template.md` — NOT bare paths like `templates/<name>.md`. This ensures correct resolution regardless of Hermes profile or working directory.

## Project Structure

```text
src/
  skills/                # One-screen skills (11 .md + umbrella directory)
    spec-kit/SKILL.md    # This file
  references/            # preflight, auto-commit, evidence, history-tracking, constitution-*
    skills/              # Full procedure per skill (loaded on demand)
  templates/             # 13 templates, all *-template.md
scripts/
  install.sh             # Hermes edition → ~/.hermes/skills/
  install-claude.sh      # Claude Code edition → ~/.claude/skills/
```

Skills and templates are maintained in the project directory and installed via `./scripts/install.sh`. Do not edit files in `~/.hermes/skills/` directly.

## Git Branch Naming

Default patterns (customise via `specs/git-conventions.md`):
- Forward development: `{feature_prefix}/NNN-short-name` (default: `feat/`)
- Bugfix: `{bugfix_prefix}/NNN-short-name` (default: `bug/`)
- Reopen: `{original_prefix}/NNN-short-name{reopen_suffix}` (default: `-bugfixing`)

During the bugfix loop, all work happens on the existing feature branch. Post-close branch management (squash/merge) follows the project's git workflow.

## Available Templates

Installed via `./scripts/install.sh` — see `src/templates/` for the full list: spec, plan, tasks, constitution, bugs, data-model, research, history, implementation-summary, close, AGENTS, git-conventions, gitignore (13 total).

## References

- `references/preflight.md` — Pre-action self-check (branch, mode, logged bug, conventions, phase card, history)
- `references/skills/<skill>.md` — the full procedure behind each one-screen skill
- `templates/decisions-template.md` — the assumptions log: every unanswered ASK is an assumption with the alternative not taken; rulings quote the user
- `references/evidence.md` — Evidence of Done: oracles (user / ci / other-agent review / probe / output), the claimed→verified status split, the author/reviewer split
- `references/auto-commit.md` — Standard commit patterns across all phases
- `references/history-tracking.md` — Process history design rationale
- `references/constitution-principles.md` — 12 principles × 3 options with pros/cons
- `references/constitution-tables.md` — Wizard tables and brownfield detection data

## MCP Server (optional)

Spec-kit includes a **derive-and-enforce MCP server**. It keeps no state: every call derives the feature's phase from the files under `specs/<feature>/` and validates. It is there for the things an agent does badly — id allocation (`next_id`), artifact lint (`lint_artifacts`), real timestamps (`timestamp`), the history-before-commit guard (`history_guard`) and a ten-line phase card to re-read after context compaction (`get_next_actions`). A legacy `specs/.spec-kit/state.json` is ignored — delete it and add `specs/.spec-kit/` to `.gitignore`.

See `spec-kit-mcp-server/README.md` for setup and usage. Enable by adding to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  spec-kit:
    command: "python3"
    args: ["~/.hermes/skills/spec-kit/mcp-server/server.py"]
```

16 MCP tools available: `mcp_spec_kit_get_feature_state`, `mcp_spec_kit_get_next_actions`, `mcp_spec_kit_advance_phase`, `mcp_spec_kit_next_id`, `mcp_spec_kit_lint_artifacts`, `mcp_spec_kit_timestamp`, `mcp_spec_kit_history_guard`, `mcp_spec_kit_project_status`, etc.
(In Hermes the tools appear with the `mcp_spec_kit_` prefix — call them by this full name.)

## ⚠️ MCP Tool Usage Rules — Critical

MCP tools are available globally, but they MUST only be called within their
designated skill context:

- `mcp_spec_kit_advance_phase` — ONLY call within the phase skill that owns the
  transition. It validates against the files and writes nothing; an error means
  an artifact is missing or you are not in the phase you think you are.
- `mcp_spec_kit_update_artifact` — ONLY call after writing the artifact file.
  The server checks the file exists.
- `mcp_spec_kit_next_id`, `lint_artifacts`, `timestamp`, `history_guard`,
  `get_next_actions` — read-only helpers; call them freely, and always before a commit.

Bug tracking (`bugs.md`) is purely file-based — no MCP tools for that. Write
bugs to `bugs.md` via `spec-kit-test`, which is the single source of truth.
