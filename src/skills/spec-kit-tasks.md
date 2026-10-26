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

**Phase**: 3 · **Persona**: architect turning design into concrete, ordered, verifiable work — no gaps, no assumptions.
**Purpose**: create `specs/[feature]/tasks.md` — tests first per phase, then implementation; every task has an exact file path.
**Full procedure**: `spec-kit/references/skills/spec-kit-tasks.md`.
**Not for**: one-step changes — implement directly.

## Before writing
- Run `spec-kit/references/preflight.md`. **BLOCK** if `plan.md` or `spec.md` is missing.
- Load `plan.md`, `spec.md`, `data-model.md`, `contracts/`. `tasks.md` exists and not bugfix mode → **BLOCK** (route `bugfix`/`reopen`). Bugfix mode → load `tasks.md`, `bugs.md`, plan bugfix sections; append only.

## Steps
1. New file: copy `spec-kit/templates/tasks-template.md`.
2. **ASK** the user: TDD or skip tests? Skip → header `> **TDD**: Bypassed by user request`. Never assume.
3. Size S → one flat phase (tests first, then code); M/L → phases Setup → Foundational → User Stories → Polish. Format `T### [P] [US#] Description — file/path.ext`. Test tasks `[TEST]` first in each phase; no forced 1:1 test↔task.
4. Map every FR-### and user story to tasks. Every AC with level unit/integration/component/e2e gets a `[TEST] [AC-###]` task at the plan's test file, its test NAME carrying the id (`AC003_…` / `'AC-003 …'`); command/probe ACs get a task writing the check. Mark tasks touching an external seam `[SEAM]` (they need a real-data probe fixture — see `spec-kit/references/evidence.md`).
5. Bugfix mode: per open bug a `BF-###` task + its verifying test; insert BEFORE `## Dependencies & Execution Order`; never delete tasks; duplicate id → ask.
6. Ids: MCP `mcp_spec_kit_next_id(kind="T"|"BF")`; without MCP, highest existing + 1. Document phase dependencies and parallel opportunities.

## Done when
- [ ] Every task has a file path; `[TEST]`/`[SEAM]`/`[P]` markers set; TDD question answered.
- [ ] MCP (optional): `mcp_spec_kit_update_artifact(tasks.md)` · `mcp_spec_kit_advance_phase(from_phase=3)` · `mcp_spec_kit_lint_artifacts` → 0 errors (ascending ids).
- [ ] history.md entry, then commit — Shared Commit Procedure in `spec-kit/references/preflight.md`: scope `specs/[feature]/tasks.md`; message `spec(phase-3): [feature] tasks` (bugfix: `spec(phase-3): [feature] bugfix tasks (BUG-NNN, …)`).

## Next
Report task count, phases, TDD mode, parallel and bugfix tasks. L → `spec-kit-review` (pre-implement, required); M → review optional, then `spec-kit-implement`; S → commit spec+plan+tasks together (`spec(phase-1-3)`) and propose `spec-kit-implement`; bugfix mode routes to `spec-kit-implement` automatically.
