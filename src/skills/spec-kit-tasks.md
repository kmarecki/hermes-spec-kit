---
name: spec-kit-tasks
description: Generate executable task breakdown from implementation plan. Phase 3 - decomposes plan into ordered, traceable tasks.
version: 1.0.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, tasks, breakdown, tdd]
    related_skills: [spec-kit-plan, spec-kit-implement, test-driven-development]
---

# spec-kit-tasks

**Phase**: 3

**Purpose**: Create or update `specs/[feature]/tasks.md` — an executable task list derived from the plan. Tests are generated first, then implementation tasks. No mandatory 1:1 mapping between tests and tasks (a test can cover multiple tasks, a task can have multiple tests). User may explicitly bypass TDD.
**Bugfix mode**: When run from the bugfix loop, generates bugfix tasks from bugs.md + plan.md.

**Prerequisites**: `spec-kit-constitution` + `spec-kit-specify` + `spec-kit-plan` must be run first

**Artifacts**:
- `specs/[feature]/tasks.md` (primary artifact)

## Execution

### Step 1: Validate prerequisites
```
IF specs/[feature]/plan.md NOT EXISTS:
  ERROR: "Run spec-kit-plan first to generate the implementation plan"
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first"
IF specs/constitution.md NOT EXISTS:
  WARN: "No constitution found — proceeding without constitutional gates. Constitution is optional."
```

### Step 2: Load context
- LOAD `specs/[feature]/plan.md` — for architecture and phases
- LOAD `specs/[feature]/spec.md` — for user stories and requirements
- LOAD `specs/[feature]/data-model.md` — for entities
- LOAD `specs/[feature]/contracts/` — for API specs
- LOAD `spec-kit/templates/tasks-template.md`
- LOAD `test-driven-development` skill — for RED-GREEN-REFACTOR cycle rules and Iron Law enforcement
- IF `specs/[feature]/bugs.md` EXISTS (bugfix mode):
  - LOAD bugs.md for bug context
  - LOAD plan.md bugfix sections for fix approaches

### Step 2.5: Determine TDD mode — ask user first
```
ASK user: "Generate test tasks for this feature? (TDD) Or skip tests and go straight to implementation?"
  IF user says skip/no tests:
    SET tdd_bypassed = true
    NOTE: "TDD bypassed by user request — no test tasks will be generated."
    PROCEED to Step 3 (implementation tasks only)
  IF user says yes/TDD:
    SET tdd_bypassed = false
    PROCEED to generate test tasks
```

### Step 2.6: Generate test tasks first (TDD mode)

For each phase, generate test tasks BEFORE implementation tasks. Tests are grouped by phase:

```
Phase N: [Phase Name]
  T001 [TEST] Write tests for user login           — tests/test_auth.py
  T002 [TEST] Write tests for token refresh         — tests/test_auth.py
  T003        Implement user login                   — src/auth.py
  T004        Implement token refresh                — src/auth.py
```

Rules:
- ALL test tasks for a phase come first, before any implementation tasks in that phase
- Test IDs come before implementation IDs (T001-T00N = tests, T00N+1+ = implementation)
- No mandatory 1:1 mapping:
  - One test can cover multiple implementation tasks (e.g., an integration test)
  - One task can have multiple tests (e.g., edge cases in separate test functions)
  - Group tests by phase boundary, not by implementation granularity
- Mark test tasks with tag `[TEST]` for easy identification
- The implement skill runs ALL tests for a phase RED first, then ALL implementations GREEN, then commits the phase

### Step 3: Map requirements to tasks
For each Functional Requirement (FR-###):
- IDENTIFY which tasks implement it
- RECORD requirement-task mapping

For each User Story:
- MAP acceptance scenarios to test tasks
- MAP entities to model tasks
- MAP services to implementation tasks

### Step 4: Map bugfix tasks (bugfix mode only)
IF bugs.md EXISTS:
  FOR EACH bug with Status: open or in-progress:
    - CREATE bugfix task matching the plan's bugfix section
    - TASKS use prefix: BF-### (e.g., BF-001, BF-002)
    - MARK with tag [BUGFIX]
    - INCLUDE test task to verify the fix
    - INCLUDE regression test task if needed

### Step 5: Generate task breakdown

IF tdd_bypassed:
  ADD header to tasks.md: `> **TDD**: Bypassed by user request — no test tasks generated.`

Organize tasks by phase:

**Phase 1: Setup (Shared Infrastructure)**
- Project initialization
- Dependency configuration
- Linting/formatting setup

**Phase 2: Foundational (Blocking Prerequisites)**
- Database schema and migrations
- Authentication/authorization framework
- API routing structure
- Base models
- Error handling infrastructure

**Phase 3+: User Story Implementation**
- Tasks for each user story (US1, US2, US3...)
- Contract tests first (if tests requested)
- Integration tests
- Unit tests
- Implementation tasks

**Phase N: Polish & Cross-Cutting**
- Documentation
- Code cleanup
- Performance optimization
- Security hardening

### Step 6: Add task metadata
For each task:
- **ID**: T001, T002, etc.
- **[P]**: Mark as parallelizable (different files, no dependencies)
- **[US#]**: Which user story it belongs to
- **File paths**: Exact locations for implementation

### Step 7: Define checkpoints
After each phase, add checkpoint comment:
```
Checkpoint: Phase N complete — [description]
```

### Step 8: Document dependencies
At end of tasks.md:
- Phase dependencies
- User story dependencies
- Parallel execution opportunities

### Step 9: Commit spec artifacts (auto)
```bash
IF `git rev-parse --git-dir > /dev/null 2>&1`; THEN
  COMMIT_MSG="spec(phase-3): [feature] task breakdown"
  git add specs/[feature]/tasks.md
  git commit -m "$COMMIT_MSG" --no-verify
  COMMIT_HASH=$(git rev-parse HEAD)
  NOTE: "Committed as $COMMIT_HASH"
ELSE
  NOTE: "Not a git repository — skipping automatic commit"
```

## Task Format
```
T001 [P] [US1] Description — src/path/file.ext
T002 [US1] Description — src/path/file.ext (depends on T001)
```

## Completion

Report:
- Task count by phase
- Parallelizable task count
- Requirement coverage percentage
- Suggest next command
- **Commit**: `$COMMIT_HASH` (auto — `git log` for details)

### Auto-Chaining (Bugfix Mode)

When running in bugfix mode (bugs.md exists):
- After tasks completes, **automatically route** to `spec-kit-implement` without waiting for user input
- Do NOT ask the user "run spec-kit-implement now?" — the bugfix loop chains automatically
- The user invoked bugfix mode, so the path is deterministic: plan → tasks → implement

## Next Skills

- Propose to the user: Run `spec-kit-analyze` for optional quality gate before implementation
- Propose to the user: Run `spec-kit-implement` to execute tasks
- In bugfix mode: **automatically route** to `spec-kit-implement` — no user choice needed

**Re-running this skill**:
1. LOAD existing tasks.md
2. COMPARE against current plan and spec
3. ADD new tasks for changed requirements
4. REMOVE tasks for deleted requirements
5. PRESERVE completed task status ([X] markers)

## Prerequisite Enforcement

**BLOCKED** if:
- `spec-kit-constitution` has not been run
- `spec-kit-specify` has not been run
- `spec-kit-plan` has not been run

## Re-run Enforcement

After re-running `spec-kit-plan`:
1. Re-derive tasks from updated architecture
2. Mark changed tasks as incomplete

After re-running `spec-kit-specify`:
1. Re-map tasks to updated requirements
2. ADD/REMOVE tasks as needed

After re-running `spec-kit-clarify`:
1. Re-evaluate tasks affected by clarifications
