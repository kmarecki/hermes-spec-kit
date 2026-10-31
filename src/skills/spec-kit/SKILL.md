---
name: spec-kit
description: Spec-Driven Development (SDD) for Hermes Agent — the overview, conventions and project layout. Load for "how does spec-kit work", "spec-kit conventions", "spec-kit help". Phase commands ('spec-kit specify|plan|tasks|implement|test|review|close [feature]', 'speckit …', "implement [feature]", "plan [feature]") load their own phase skill; routing commands (bugfix, quickfix, reopen, accept, status) load spec-kit-workflow.
version: 2.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec-kit, sdd, overview]
    related_skills: [spec-kit-workflow, spec-kit-constitution, spec-kit-specify, spec-kit-clarify, spec-kit-plan, spec-kit-tasks, spec-kit-review, spec-kit-implement, spec-kit-test, spec-kit-summarize, spec-kit-refresh]
---

# Spec-Driven Development (SDD)

Specifications drive code. Every phase is a one-screen skill with a full procedure under
`spec-kit/references/skills/<skill>.md`, loaded on demand. Routing (bugfix, quickfix, reopen,
accept, status) is `spec-kit-workflow`; phase skills trigger themselves.

```text
Constitution → Specify (size S/M/L, ACs, Security & Privacy) → [Clarify] → Plan → Tasks → [Review 3.5]
  → Implement (RED/GREEN + probes, every tier) → Accept loop → Test → Final review 5.5 (+ devil's advocate)
  → Close (close.md + change-record.md, ADRs, AGENTS.md)            bugfix loop: Plan → Tasks → Implement → Accept
```

| Phase | Skill | Produces |
|-------|-------|----------|
| 0 | `spec-kit-constitution` | `specs/constitution.md` (brownfield / free-text / wizard) |
| 1 · 1.5 | `spec-kit-specify` · `spec-kit-clarify` | `spec.md` (FR, AC, Security & Privacy, size), `clarify.md`, `decisions.md` |
| 2 · 3 | `spec-kit-plan` · `spec-kit-tasks` | `plan.md` (+ research / data-model / contracts / quickstart by tier), `tasks.md` |
| 3.5 · 5.5 | `spec-kit-review` | pre-implement report (M lite, L full) · `review-final.md` — the merge gate |
| 4 | `spec-kit-implement` | code, `evidence/` (RED/GREEN/probes), one commit per phase |
| 5 | `spec-kit-test` | `bugs.md`; accept mode → `acceptance.md` rounds |
| 6 | `spec-kit-summarize` | `close.md`, **`change-record.md`**, ADRs, AGENTS.md patches |
| — | `spec-kit-refresh` | spec/plan reconciled with the code mid-stream |
| — | `spec-kit-epic` · `spec-kit-design` | optional, only when `epics_dir` / `design_dir` are set: an epic plan (many features, one goal — **time**) · a living module design doc (how a part works now — **space**); feature closes patch both |

**Mandatory**: constitution once per project; size asked at specify; the final review; the close.

## Conventions
- **Record = `history.md`** (`spec-kit/references/history-tracking.md`): one fixed-field entry per phase (time, phase, skill, agent = Implemented-by, artifacts, tests, evidence, commit, note ≤ 25 words), appended before every commit (`mcp_spec_kit_append_history` / `spec-kit/scripts/spec-kit-log.sh`, guarded by `mcp_spec_kit_history_guard`). It survives the squash-merge; the close copies it into `change-record.md`. Messages: `spec-kit/references/commits.md`.
- **Evidence** (`spec-kit/references/evidence.md`): the agent's word is never evidence; probes per seam, RED/GREEN files every tier, `ci:`/`user`/`review:<other-agent>` verify.
- **Size** (`spec-kit/references/sizing.md`): S / M / L — leaner workflow and shorter artifacts (S = a bugfix or small enhancement: a few-line spec, 1–2 ACs, one commit for spec+plan+tasks); evidence and the acceptance round never shrink.
- **Additive only**: no spec artifact is ever rewritten (`spec-kit/references/preflight.md`).
- **Decisions**: questions the user would want to decide → `decisions.md` (ruling quotes them; assumption otherwise); design choices stay in plan.md.
- Templates: `spec-kit/templates/<name>-template.md`. Git: `specs/git-conventions.md` (`feat/NNN-name`, `bug/NNN-name`, reopen suffix `-bugfixing`).
- AGENTS.md carries: available skills, active spec dirs, build commands, project conventions — not routing tables or phase mechanics.
- **Scale**: a small project keeps no `design_dir` / `epics_dir` / `adr_dir` and the close has nothing to patch; a platform sets all three. Document roles: spec = one feature · epic = what and in what order · design doc = how it works now · ADR = why · AGENTS.md = where things are and what never to do.

## MCP server (optional, stateless)
`spec-kit-mcp-server/server.py` derives the phase from `specs/<feature>/` on every call and validates: `mcp_spec_kit_get_next_actions` (phase card — re-read after compaction), `mcp_spec_kit_advance_phase` (only from the owning phase skill), `mcp_spec_kit_next_id`, `mcp_spec_kit_lint_artifacts` (before every commit), `mcp_spec_kit_acceptance_freeze` / `mcp_spec_kit_acceptance_status`, `mcp_spec_kit_diff_scan`, `mcp_spec_kit_close_feature`, `mcp_spec_kit_timestamp`, `mcp_spec_kit_append_history`, `mcp_spec_kit_history_guard`, `mcp_spec_kit_init_feature`, `mcp_spec_kit_get_feature_state`, `mcp_spec_kit_list_features`, `mcp_spec_kit_project_status`, `mcp_spec_kit_project_set_constitution`, `mcp_spec_kit_reopen_feature`, `mcp_spec_kit_update_artifact`, `mcp_spec_kit_auto_detect_features`. Bugs are file-based (`bugs.md`) — no bug tools. Setup: `spec-kit-mcp-server/README.md`; enable by adding to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  spec-kit:
    command: <python-with-mcp-sdk>
    args: ["~/.hermes/skills/spec-kit/mcp-server/server.py"]
```
