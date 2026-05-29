---
name: spec-kit-tasks
description: Generate executable task breakdown from implementation plan. Phase 3 - decomposes plan into ordered, traceable tasks.
category: software-development
---

# spec-kit-tasks

**Phase**: 3

**Purpose**: Create or update `specs/[feature]/tasks.md` — an executable task list derived from the plan.

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
IF .specify/memory/constitution.md NOT EXISTS:
  ERROR: "Run spec-kit-constitution first"
```

### Step 2: Load context
- LOAD `specs/[feature]/plan.md` — for architecture and phases
- LOAD `specs/[feature]/spec.md` — for user stories and requirements
- LOAD `specs/[feature]/data-model.md` — for entities
- LOAD `specs/[feature]/contracts/` — for API specs
- LOAD `templates/tasks.md`

### Step 3: Map requirements to tasks
For each Functional Requirement (FR-###):
- IDENTIFY which tasks implement it
- RECORD requirement-task mapping

For each User Story:
- MAP acceptance scenarios to test tasks
- MAP entities to model tasks
- MAP services to implementation tasks

### Step 4: Generate task breakdown
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

### Step 5: Add task metadata
For each task:
- **ID**: T001, T002, etc.
- **[P]**: Mark as parallelizable (different files, no dependencies)
- **[US#]**: Which user story it belongs to
- **File paths**: Exact locations for implementation

### Step 6: Define checkpoints
After each phase, add checkpoint comment:
```
Checkpoint: Phase N complete — [description]
```

### Step 7: Document dependencies
At end of tasks.md:
- Phase dependencies
- User story dependencies
- Parallel execution opportunities

### Step 8: Write phase marker
```
WRITE specs/[feature]/.phase: "tasks"
```

## Idempotency

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

## Next Skills

- Run `spec-kit-analyze` for optional quality gate before implementation
- Run `spec-kit-implement` to execute tasks