---
name: spec-kit-implement
description: Execute implementation following the task plan. Phase 4 - runs tasks in order with TDD approach.
version: 1.0.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, implementation, tdd, coding]
    related_skills: [spec-kit-tasks, spec-kit-test, test-driven-development, writing-plans]
---

# spec-kit-implement

**Phase**: 4

**Purpose**: Execute implementation following `specs/[feature]/tasks.md`. Runs tasks in order with TDD approach.
**Bugfix mode**: When tasks.md contains bugfix tasks (prefixed with BF-###), executes them alongside regular tasks.

**Prerequisites**: `spec-kit-constitution` + `spec-kit-specify` + `spec-kit-plan` + `spec-kit-tasks` must be run first
**Bugfix mode**: When bugs.md exists, load it for bugfix task context. Plan Ref validation is handled by the workflow orchestrator before routing to this skill — if you reached Implement, all bugs have valid Plan Refs.

**Artifacts**: Updated `specs/[feature]/tasks.md` (with completion markers)

## Bugfix Mode

Bugfix tasks (prefixed with BF-###) are executed alongside regular tasks. Plan Ref validation and the bugfix routing decision (clarify vs direct plan) happen in the workflow orchestrator — this skill assumes all routing prerequisites are met.

## Execution

### Step 0: Load TDD skill
```
LOAD `test-driven-development` skill — RED-GREEN-REFACTOR cycle rules:
  - Iron Law: NO production code without a failing test first
  - RED: Write failing test, run to verify it fails for the right reason
  - GREEN: Write minimal code to pass, run to verify pass
  - REFACTOR: Clean up while keeping tests green
  - Full suite: Run all tests after each GREEN
  - Build: Run build (npm run build / tsc --noEmit / go build) after each GREEN for compiled projects
  (See the skill for full Iron Law enforcement and common rationalizations guide.)
```

### Step 1: Validate prerequisites
```
IF specs/[feature]/tasks.md NOT EXISTS:
  ERROR: "Run spec-kit-tasks first to generate task breakdown"
IF specs/[feature]/plan.md NOT EXISTS:
  ERROR: "Run spec-kit-plan first"
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first"
```

### Step 2: Check preconditions
```bash
# Checklist check — advisory only
SCAN specs/[feature]/checklists/ for checklist files
FOR EACH checklist:
  COUNT total items: lines matching - [ ] or - [X]
  COUNT completed: lines matching - [X]
  COUNT incomplete: lines matching - [ ]
IF any checklist has incomplete items:
  DISPLAY status table
  NOTE: "Checklists are advisory — they do not block implementation."
  (No confirmation needed; user may proceed directly)
```

### Step 3: Load implementation context
- LOAD `specs/[feature]/tasks.md` (REQUIRED)
- LOAD `specs/[feature]/plan.md` (REQUIRED)
- LOAD `specs/[feature]/data-model.md` (IF EXISTS)
- LOAD `specs/[feature]/contracts/` (IF EXISTS)
- LOAD `specs/[feature]/research.md` (IF EXISTS)
- LOAD `specs/constitution.md` (IF EXISTS)
- LOAD `specs/[feature]/quickstart.md` (IF EXISTS)
- IF `specs/[feature]/bugs.md` EXISTS: LOAD bugs.md for bugfix task context

### Step 4: Parse tasks.md
Extract:
- Task phases: Setup, Foundational, Core, Integration, Polish
- Task dependencies: Sequential vs parallel execution rules
- Task details: ID, description, file paths, parallel markers [P]
- Execution flow: Order and dependency requirements

### Step 5: Execute tasks via RED-GREEN-REFACTOR

For each task, follow the strict TDD cycle. Every result must be **verified by running tests**, not assumed.

#### Cycle: Test task → RED (verify failure — expected, NOT a bug)
For each task marked [TEST] (or any test-writing task):
```
a. WRITE one minimal test for the next behavior
   - One behavior per test
   - Clear descriptive name (if name has "and", split it)
   - Real code, not mocks (unless truly unavoidable)
   - Test behavior, not implementation

b. RUN the specific test to verify RED:
   terminal("pytest tests/test_file.py::test_name -v")
   
   CONFIRM:
   - Test fails (not errors from typos)
   - Failure message is expected and descriptive
   - Test fails because the feature is missing
   
   ⚠️ This RED failure is EXPECTED and PROVES the test is valid.
   It is NOT a bug — it's the first step of TDD.
   Do NOT log it in bugs.md.
   
   Test passes immediately? You tested existing behavior. Fix the test.
   Test errors? Fix the error, re-run until it fails correctly.
   
   ⚠️ SKIP THIS STEP? The test proves NOTHING. You never saw it catch a failure.
```

#### Cycle: Implementation task → GREEN (verify pass)
```
a. WRITE the simplest code to pass the test
   - Minimal — nothing more than needed
   - Cheating is OK in GREEN (hardcode, copy-paste, duplicate)
   - Don't add features, refactor, or "improve" beyond the test

b. RUN the specific test to verify GREEN:
   terminal("pytest tests/test_file.py::test_name -v")
   
   CONFIRM:
   - Test passes
   - Output pristine (no errors, warnings)

c. RUN the full test suite to check for regressions:
   terminal("pytest tests/ -q")
   
   CONFIRM:
   - All tests still pass
   - No regressions introduced
   
   Other tests fail? Fix regressions now.

d. RUN the project build (if applicable):
   terminal("npm run build") OR terminal("tsc --noEmit") OR terminal("go build")
   
   NOTE: Skip this if project has no build step. TypeScript projects MUST build —
   Vitest/Jest swallow type errors that crash at runtime.
   
   Build fails? Fix compilation errors, re-run tests, re-run build.

e. UPDATE tasks.md with [X] completion marker

f. COMMIT the task:
   git add -A
   git commit -m "feat: [feature] T### - description" --no-verify
   (Or "fix: [feature] BF-### - description" for bugfix tasks)
```

#### Cycle: REFACTOR (optional, after GREEN)
```
After GREEN is verified and committed:
  - Remove duplication
  - Improve names
  - Extract helpers
  - Simplify expressions
  
  Keep tests green throughout. Run full suite after each change.
  If tests fail during refactor → undo immediately. Take smaller steps.
```

#### Task execution order rules
- **Test tasks before implementation tasks** — always. Every T### has a T###-test predecessor.
- Phase-by-phase: Complete each phase before moving to next
- Sequential tasks in order; parallel [P] can run together if they affect different files
- File-based coordination: Tasks affecting same files must run sequentially

### Step 7: Progress reporting
After each task:
- Report tasks completed: N/Total
- Report current phase
- Report next task
- Report tests passing: Yes/No
- In bugfix mode: Also report bugfix task progress (BF-### completed/total)

### Step 8: Handle errors
- HALT execution if non-parallel task fails
- FOR parallel tasks [P]: continue with successful, report failed
- PROVIDE clear error messages with context
- SUGGEST next steps if implementation cannot proceed

### Step 9: Final verification — automated test run

After all tasks are complete, run the full automated test suite one final time. **Note**: RED test failures during the per-task TDD cycle (Step 5) are EXPECTED — they prove the test is valid. Only failures at this final stage indicate real problems.

```bash
DETECT test framework:
  IF pytest is available:        terminal("pytest tests/ -q --tb=short")
  ELSE IF go test is available:  terminal("go test ./...")
  ELSE IF npm test is available: terminal("npm test")
  ELSE:                          NOTE "No automated test framework detected — skipping."

IF tests run successfully:
  REPORT: "All N tests pass. Feature implementation verified."
  NOTE: "Ready for Phase 5 (manual testing) or Phase 6 (close/summarize)."

IF tests fail:
  REPORT failures:
    | Test | File | Failure |
    |------|------|---------|
  NOTE: "N test failures found after implementation. These must be resolved."
  REVIEW each failure:
    - IF the failure is from a test task written during this phase:
      The implementation is incomplete. RETURN to fix the failing code.
    - IF the failure is from a pre-existing test unrelated to this feature:
      The change introduced a regression. RETURN to fix.
    - IF the failure is from a test that the user will verify manually:
      LOG as bug in bugs.md (Status: open, Severity: determined by failure)
  
  REPEAT Step 9 after fixes until all tests pass.
```

Also run the project build if applicable:
```bash
IF npm run build / tsc --noEmit / go build / cargo build is available:
  terminal("[build command]")
  IF build fails: RETURN to fix compilation errors, re-run tests, re-run build
```

## Implementation Rules (TDD Enforcement)

- **Iron Law**: NO production code without a failing test first. If you wrote code before the test, delete it and start over.
- **RED verification is mandatory**: Every test must be run and confirmed failing before implementation begins. Without RED verification, the test proves nothing.
- **GREEN verification is mandatory**: After implementation, run the specific test AND the full suite.
- **Test before implement**: Test tasks always precede their corresponding implementation tasks.
- **One behavior per test**: If a test name has "and", split it into two tests.
- **Real code over mocks**: Use real implementations unless truly unavoidable (external APIs, hardware).
- **Build after GREEN**: TypeScript projects MUST build — Vitest/Jest swallow type errors.
- **Regressions block**: If the full suite fails after GREEN, fix regressions before moving to the next task.
- **Commit per task**: Each RED-GREEN cycle produces one commit.
- In bugfix mode: Update bugs.md Status after fixing a bug (set to "resolved")

## Phase Guardrail — STRICT

This is the **ONLY** phase where code-editing tools are permitted.

| Tool | Implement Phase | All Other Phases |
|------|----------------|-----------------|
| `write_file` (source code) | ALLOWED | **BLOCKED** |
| `patch` (source code) | ALLOWED | **BLOCKED** |
| `terminal` (build/compile/test) | ALLOWED | **BLOCKED** |
| `write_file` (spec artifacts) | ALLOWED (tasks.md, bugs.md status) | Allowed (phase-specific only) |
| `read_file`, `search_files`, `skill_view` | ALLOWED | ALLOWED |

If you are in ANY other phase (Constitution, Specify, Clarify, Plan, Tasks, Analyze, Test), you MUST NOT call `write_file`, `patch`, or `terminal` for compilation/builds on source code files.

### Bugfixing rule
- Bug reports always go to `bugs.md` first (via `spec-kit-test`)
- Bugfixes are NEVER implemented directly when a user mentions a bug
- Bugfixes must follow: "bugfix [feature]" → plan → tasks → implement

## Completion

Report:
- Final status
- Tasks completed vs total
- Tests passing
- Summary of completed work
- **Commit hash per task**: `git log --oneline --grep="T###"` for task-level commits

## Done When

- [ ] All tasks in tasks.md completed and marked [X]
- [ ] Every test was verified RED (watched it fail) before implementation
- [ ] Every implementation was verified GREEN (watched it pass)
- [ ] Full test suite passes after each task — no regressions
- [ ] Final automated test suite passes (Step 9) — all tests green
- [ ] Build passes (if applicable)
- [ ] Implementation validated against spec and plan
- [ ] Implementation complete
- [ ] In bugfix mode: All bugfix tasks completed and verified

**Re-running this skill**:
1. LOAD tasks.md and find next incomplete task
2. RESUME from where execution stopped
3. PRESERVE all [X] completion markers
4. Only execute remaining incomplete tasks

## Prerequisite Enforcement

**BLOCKED** if:
- `spec-kit-specify` has not been run
- `spec-kit-plan` has not been run
- `spec-kit-tasks` has not been run

**WARN** if:
- `spec-kit-constitution` has not been run — proceeding without constitutional gates
