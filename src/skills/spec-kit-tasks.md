---
name: spec-kit-tasks
description: Load when the user says 'spec-kit tasks for [feature]', 'speckit tasks for [feature]', 'spec-kit break down [feature]', 'speckit break down [feature]', "generate tasks for [feature]", "break down [feature]", or "create tasks for [feature]" — Phase 3 task breakdown.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, tasks, breakdown, tdd]
    related_skills: [spec-kit-plan, spec-kit-implement, spec-kit-workflow]
---

# spec-kit-tasks

**Phase**: 3 · **Persona**: tech lead turning design into ordered, verifiable work — every task has a file path.
**Purpose**: `specs/[feature]/tasks.md` — tests first per phase, then code.
**Full procedure**: `spec-kit/references/skills/spec-kit-tasks.md` · **Not for**: one-step changes.

## Before writing
- `spec-kit/references/preflight.md`. **BLOCK** if `plan.md` or `spec.md` is missing. Load plan, spec, data-model, contracts. `tasks.md` exists and not bugfix mode → **BLOCK**; bugfix mode → append only.

## Steps
1. Copy `spec-kit/templates/tasks-template.md`. **ASK**: TDD or skip tests? Skip → header `> **TDD**: Bypassed by user request`. Never assume.
2. S → one flat list; M/L → phases Setup/Foundational → stories → Polish. `T### [P] [US#] [TEST] [AC-###] [SEAM] Description — path`.
3. Every FR and story → tasks. Every AC with level unit/integration/component/e2e → a `[TEST] [AC-###]` task at the plan's test file, test NAME carrying the id; command/probe ACs → a task writing the check. Every seam from the plan → `[SEAM]` on the task that touches it (`spec-kit/references/evidence.md`).
4. Bugfix mode: per open bug a `BF-###` task + its verifying test, inserted before `## Dependencies & Execution Order`; never delete tasks.
5. Ids: `mcp_spec_kit_next_id(kind="T"|"BF")` (no MCP: highest + 1). Dependencies and parallel opportunities in one short section.

## Done when
- [ ] Every task has a path; markers set; TDD answered. MCP: `mcp_spec_kit_update_artifact(tasks.md)` · `mcp_spec_kit_advance_phase(from_phase=3)` · `mcp_spec_kit_lint_artifacts` → 0 errors.
- [ ] Commit (`spec-kit/references/commits.md`): `spec(phase-3): [feature] tasks` (bugfix: `… bugfix tasks (BUG-NNN, …)`).

## Next
L → `spec-kit-review` (pre-implement, required). M → `spec-kit-review` lite, then `spec-kit-implement`. S → one commit `spec(phase-1-3)` then `spec-kit-implement`. Bugfix mode → `spec-kit-implement` automatically.
