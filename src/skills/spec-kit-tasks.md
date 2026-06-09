---
name: spec-kit-tasks
description: Use when the user says 'generate tasks for [feature]' or 'break down [feature]' — Phase 3 task breakdown.
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
LOAD spec-kit/templates/tasks-template.md
IF bugfix mode: LOAD bugs.md, plan.md bugfix sections
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

### Generate task breakdown
Organize by phase: Setup → Foundational → User Stories → Polish.
Format: `T### [P] [US#] Description — file/path.ext`

### Document dependencies
Phase dependencies, parallel execution opportunities.

### Note on commits
Design phase artifacts are NOT committed individually. See `spec-kit/references/auto-commit.md`.

## Completion
- Task count by phase, parallelizable count, coverage %
- Propose: `spec-kit-implement`

## Common Pitfalls
1. **Missing file paths**: Every task needs an exact file path — otherwise the implement skill can't execute it.
2. **Forcing 1:1 test-to-task**: Integration tests cover multiple tasks. Edge case tests cover one function. Let the test structure follow the behavior, not the task IDs.
3. **Not asking about TDD bypass**: Always ask the user at task generation time. Don't assume.

## Prerequisite Enforcement
**BLOCKED** if: plan.md or spec.md does not exist.
