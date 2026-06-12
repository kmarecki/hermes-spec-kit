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

**Task Persona**: Adopt the mindset of a system architect and philosopher. Every requirement must become concrete, executable work. Break down the design into granular, ordered tasks — each one maps to a requirement and produces a verifiable deliverable. No gaps, no assumptions.

**Phase**: 3

**Purpose**: Create `specs/[feature]/tasks.md` — an executable task list. Tests generated first, then implementation tasks. No mandatory 1:1 mapping between tests and tasks. User may explicitly bypass TDD.

**When NOT to use**: For one-step changes (single file edit) — just implement directly.

**Routing**: Load this skill when the user says "generate tasks for [feature]" or "break down [feature]". If loaded directly, load spec-kit-workflow first to check prerequisites.


**Artifacts**: `specs/[feature]/tasks.md`

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Validate prerequisites
```
IF specs/[feature]/plan.md NOT EXISTS: ERROR "Run spec-kit-plan first"
IF specs/[feature]/spec.md NOT EXISTS: ERROR "Run spec-kit-specify first"
```

### Load context
```
LOAD specs/[feature]/plan.md, spec.md, data-model.md, contracts/

IF bugfix mode (reopened bugfix):
  NOTE: "Bugfix mode — tasks.md already exists with completed tasks. Will append new bugfix tasks only."
  LOAD existing specs/[feature]/tasks.md
  LOAD bugs.md, plan.md bugfix sections
ELSE:
  LOAD spec-kit/templates/tasks-template.md
  COPY spec-kit/templates/tasks-template.md → specs/[feature]/tasks.md
```

### Determine TDD mode
```
ASK user: "Generate test tasks (TDD) or skip tests?"
IF skip:
  SET tdd_bypassed = true
  ADD header to tasks.md: "> **TDD**: Bypassed by user request"
```

### Generate test tasks first (TDD mode)
For each phase, tests BEFORE implementation:
```
Phase N:
  T001 [TEST] Write tests for login          — tests/test_auth.py
  T002        Implement login                 — src/auth.py
```

Rules:
- All test tasks for a phase come first
- No mandatory 1:1: one test can cover multiple tasks, one task can have multiple tests
- Group tests by phase boundary, not implementation granularity
- Mark test tasks with `[TEST]`

### Map requirements to tasks
```
For each FR-###: IDENTIFY implementing tasks
For each User Story: MAP scenarios to test tasks, entities to model tasks
```

### Map bugfix tasks (bugfix mode)
```
For each open bug: CREATE BF-### task, include test task to verify fix
```

**Additive-safe**: Append new bugfix tasks at the end of tasks.md. Never delete existing tasks. You may update task status fields (e.g. mark tasks as completed). If a new bugfix task has the same ID as an existing one, ask the user how to resolve.

### Generate task breakdown
Organize by phase: Setup → Foundational → User Stories → Polish.
Format: `T### [P] [US#] Description — file/path.ext`

### Document dependencies
Phase dependencies, parallel execution opportunities.

### Note on commits
Report: task count, phases, TDD mode, parallel tasks, bugfix tasks

### Append to history.md and Commit

**Order is critical: history.md FIRST, then commit.**

1. **Append to history.md**:
   Append entry to `specs/[feature]/history.md` (create if missing):
   - Phase: Phase 3 — Complete
   - Artifact: `tasks.md`

2. **PRE-COMMIT GUARD**:
   READ `specs/[feature]/history.md` — confirm the tasks.md entry is recorded.
   If missing: BLOCK — must append before commit.

3. **Commit**:
   Follow `spec-kit/references/auto-commit.md`:
   - Scope: `specs/[feature]/tasks.md`
   - Message: `"spec(phase-3): [feature] tasks"`

## Completion

## Common Pitfalls
1. **Missing file paths**: Every task needs an exact file path — otherwise the implement skill can't execute it.
2. **Forcing 1:1 test-to-task**: Integration tests cover multiple tasks. Edge case tests cover one function. Let the test structure follow the behavior, not the task IDs.
3. **Not asking about TDD bypass**: Always ask the user at task generation time. Don't assume.

## Prerequisite Enforcement
**BLOCKED** if: plan.md or spec.md does not exist.
