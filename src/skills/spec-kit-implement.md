---
name: spec-kit-implement
description: Execute implementation following the task plan. Phase 4 - runs tasks in order with TDD approach.
category: software-development
---

# spec-kit-implement

**Phase**: 4

**Purpose**: Execute implementation following `specs/[feature]/tasks.md`. Runs tasks in order with TDD approach.

**Prerequisites**: `spec-kit-constitution` + `spec-kit-specify` + `spec-kit-plan` + `spec-kit-tasks` must be run first

**Artifacts**: Updated `specs/[feature]/tasks.md` (with completion markers)

## Execution

### Step 1: Validate prerequisites
```
IF specs/[feature]/tasks.md NOT EXISTS:
  ERROR: "Run spec-kit-tasks first to generate task breakdown"
IF specs/[feature]/plan.md NOT EXISTS:
  ERROR: "Run spec-kit-plan first"
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first"
```

### Step 2: Check checklists status
```
SCAN specs/[feature]/checklists/ for checklist files
FOR EACH checklist:
  COUNT total items: lines matching - [ ] or - [X]
  COUNT completed: lines matching - [X]
  COUNT incomplete: lines matching - [ ]
IF any checklist has incomplete items:
  DISPLAY status table
  ASK: "Some checklists are incomplete. Proceed with implementation? (yes/no)"
  WAIT for user response
  IF "no": HALT
  IF "yes": CONTINUE
```

### Step 3: Load implementation context
- LOAD `specs/[feature]/tasks.md` (REQUIRED)
- LOAD `specs/[feature]/plan.md` (REQUIRED)
- LOAD `specs/[feature]/data-model.md` (IF EXISTS)
- LOAD `specs/[feature]/contracts/` (IF EXISTS)
- LOAD `specs/[feature]/research.md` (IF EXISTS)
- LOAD `.specify/memory/constitution.md` (IF EXISTS)
- LOAD `specs/[feature]/quickstart.md` (IF EXISTS)

### Step 4: Parse tasks.md
Extract:
- Task phases: Setup, Foundational, Core, Integration, Polish
- Task dependencies: Sequential vs parallel execution rules
- Task details: ID, description, file paths, parallel markers [P]
- Execution flow: Order and dependency requirements

### Step 5: Execute implementation
Execute tasks following rules:
- **Phase-by-phase execution**: Complete each phase before moving to next
- **Respect dependencies**: Sequential tasks in order, parallel [P] can run together
- **TDD approach**: Execute test tasks before their corresponding implementation tasks
- **File-based coordination**: Tasks affecting same files must run sequentially
- **Validation checkpoints**: Verify each phase before proceeding

### Step 6: For each task:
a. READ task description and file path
b. IF test task: write failing test first
c. IF implementation task: implement to make test pass
d. VERIFY task completion
e. UPDATE tasks.md with [X] completion marker

### Step 7: Progress reporting
After each task:
- Report tasks completed: N/Total
- Report current phase
- Report next task
- Report tests passing: Yes/No

### Step 8: Handle errors
- HALT execution if non-parallel task fails
- FOR parallel tasks [P]: continue with successful, report failed
- PROVIDE clear error messages with context
- SUGGEST next steps if implementation cannot proceed

### Step 9: Write phase marker
```
WRITE specs/[feature]/.phase: "implement"
```

## Idempotency

**Re-running this skill**:
1. LOAD tasks.md and find next incomplete task
2. RESUME from where execution stopped
3. PRESERVE all [X] completion markers
4. Only execute remaining incomplete tasks

## Prerequisite Enforcement

**BLOCKED** if:
- `spec-kit-constitution` has not been run
- `spec-kit-specify` has not been run
- `spec-kit-plan` has not been run
- `spec-kit-tasks` has not been run

## Implementation Rules

- NEVER skip test tasks
- NEVER implement without understanding the requirement
- ALWAYS verify file paths exist or create them
- ALWAYS run tests after implementation
- STOP on test failures and report
- UPDATE tasks.md immediately after completion

## Completion

Report:
- Final status
- Tasks completed vs total
- Tests passing
- Summary of completed work

## Done When

- [ ] All tasks in tasks.md completed and marked [X]
- [ ] Implementation validated against spec and plan
- [ ] All tests passing
- [ ] Implementation complete