---
name: spec-kit-implement
description: Load when the user says 'spec-kit implement [feature]', 'speckit implement [feature]', 'spec-kit start [feature]', 'speckit start [feature]', "implement [feature]", or "start implementing [feature]" — Phase 4 phase-level TDD execution.
version: 1.2.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, implementation, tdd, coding]
    related_skills: [spec-kit-tasks, spec-kit-test, spec-kit-workflow, writing-plans]
---

# spec-kit-implement

**Task Persona**: Adopt the mindset of a disciplined engineer building to spec. Follow the plan exactly. No scope creep, no unrequested refactoring, no added features. Write correct code and verify it with tests. Think like a builder, not a designer.

**Phase**: 4

**Purpose**: Execute implementation following `specs/[feature]/tasks.md`. Phase-level TDD: all tests for a phase written RED first, then all code written GREEN, then phase committed.

**When NOT to use**: For spec-only changes (design iteration) — use `spec-kit-specify` or `spec-kit-plan`.

**Routing**: Load this skill when the user says "implement [feature]" or "start implementation". If loaded directly, load spec-kit-workflow first to check prerequisites.

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Git Commit Guidelines

> **Branch Guard**:

| Situation | Use commit template from specs/git-conventions.md |
|-----------|--------------------------------------------------|
| Phase boundary (TDD or bypass) | Implement template (default: `feat: [feature] Phase N - [Phase Name]`) |
| Regression umbrella fix | Regression template (default: `fix: [feature] BF-REGRESSION-001 - fix regressions`) |
| Bugfix loop (per BF-### task) | Bugfix template (default: `fix: [feature] BF-### - description`) |

See `spec-kit/references/auto-commit.md` for the standard pattern. Commits use `--no-verify` to bypass pre-commit hooks.

Note: design artifacts (spec.md, plan.md, tasks.md) were already batch-committed at implementation start. Do NOT re-commit them.


**Bugfix mode**: When tasks.md contains bugfix tasks (prefixed with BF-###), executes them alongside regular tasks.

**Prerequisites**: `spec-kit-constitution` + `spec-kit-specify` + `spec-kit-plan` + `spec-kit-tasks` must be run first
**Bugfix mode**: When bugs.md exists, load it for bugfix task context. Plan Ref validation is handled by the workflow orchestrator before routing to this skill — if you reached Implement, all bugs have valid Plan Refs.

**Artifacts**: Updated `specs/[feature]/tasks.md` (with completion markers)

## Bugfix Mode

Bugfix tasks (prefixed with BF-###) follow the same RED→GREEN TDD cycle as regular feature phases:

```text
For each BF-### task:
  0. READ — Confirm root cause understanding
     - Read the relevant source code for the bug area
     - Cross-check against the Plan Ref in bugs.md (created by spec-kit-plan)
     - Verify the bug report description matches what the code actually does
     - If the code contradicts the bug report or Plan Ref: STOP, flag the
       discrepancy to the user before proceeding
  1. RED — Write a test that reproduces the bug
     - Focused test that demonstrates the faulty behaviour
     - Run it → confirm it fails (proves the bug exists)
  2. GREEN — Apply the minimal fix
     - Run the test → confirm it passes
  3. COMMIT with the bugfix template from specs/git-conventions.md
     (default: "fix: [feature] BF-### - description")
```

This "read first" step prevents the common AI-agent trap where code is changed based on a bug report alone without verifying root cause against the actual code. The Plan Ref (from spec-kit-plan) gives the analysis; this step validates it against live code.

Plan Ref validation and the bugfix routing decision (clarify vs direct plan) happen in the workflow orchestrator — this skill assumes all routing prerequisites are met.

**New bugs discovered during fix**: If while fixing BF-### you discover new failures or edge cases not covered by the original bug report (reported by the user or found during code reading):
- Log them as new entries in `bugs.md` (do NOT merge into the current BF-### task)
- Each new bug must follow its own RED→GREEN cycle — do not fix it inline with the current task
- Report to the user: "Found additional issue BUG-NNN — logged separately. Address it via 'bugfix [feature]' after this round completes."
- Exception: trivial test-only fixes (missing assertion, wrong test fixture) can be fixed inline

**What if a test cannot be written for a bug?** (e.g. visual layout issue, race condition, external dependency)
- Note the reason in tasks.md next to the BF-### task
- Apply the fix, then verify manually
- The summary/close will flag the untested fix as a risk

## Execution

### TDD Mode Detection
```
SCAN tasks.md for `> **TDD**: Bypassed by user request`
  IF found:
    SET tdd_bypassed = true
    NOTE: "TDD bypassed by user — implementation-only tasks, no test cycle."
  IF not found:
    SET tdd_bypassed = false
    NOTE: "TDD active — phase-level RED-GREEN cycle enforced."
```

### Step 1: Branch guard — prevent blocked branch commits

Before any file operation, verify you are not on a blocked branch (from specs/git-conventions.md blocked_branches):

```bash
IF `git rev-parse --git-dir > /dev/null 2>&1`; THEN
  LOAD specs/git-conventions.md — read blocked_branches, feature_prefix
  CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
  IF current branch is in blocked_branches; THEN
    BLOCK: "On a blocked branch — implementation must happen on a feature branch."
    PROMPT: "Switch to a feature branch first:
      git checkout -b {feature_prefix}/NNN-feature-name
      git push -u origin {feature_prefix}/NNN-feature-name"
    HALT
  FI
ELSE
  NOTE: "Not a git repository — branch guardrail skipped."
FI
```

### Step 2: Commit spec artifacts (batch — all design phases)

Before starting implementation, commit all spec artifacts created during design phases as a single batch.
Use the batch commit template from specs/git-conventions.md (default: "spec: [feature] spec artifacts (spec, plan, tasks)"):

```bash
IF `git rev-parse --git-dir > /dev/null 2>&1`; THEN
  # Use the batch commit template from specs/git-conventions.md
  # Default: "spec: [feature] spec artifacts (spec, plan, tasks)"
  COMMIT_MSG="[batch commit message from conventions]"
  git add specs/[feature]/spec.md       \
         specs/[feature]/clarify.md      \
         specs/[feature]/plan.md         \
         specs/[feature]/research.md     \
         specs/[feature]/data-model.md   \
         specs/[feature]/contracts/      \
         specs/[feature]/quickstart.md   \
         specs/[feature]/tasks.md
  git commit -m "$COMMIT_MSG" --no-verify
  COMMIT_HASH=$(git rev-parse HEAD)
  NOTE: "Spec artifacts committed as $COMMIT_HASH — design phase is frozen."
  NOTE: "Implementation begins from this checkpoint. If you need to change the spec,"
        "commit a spec amendment separately or start a new feature branch."
ELSE
  NOTE: "Not a git repository — skipping batch commit. No design checkpoint created."
```

### Step 3: Validate prerequisites
```
IF specs/[feature]/tasks.md NOT EXISTS:
  ERROR: "Run spec-kit-tasks first to generate task breakdown"
IF specs/[feature]/plan.md NOT EXISTS:
  ERROR: "Run spec-kit-plan first"
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first"
```

### Step 5: Load implementation context
- LOAD `specs/[feature]/tasks.md` (REQUIRED)
- LOAD `specs/[feature]/plan.md` (REQUIRED)
- LOAD `specs/[feature]/data-model.md` (IF EXISTS)
- LOAD `specs/[feature]/contracts/` (IF EXISTS)
- LOAD `specs/[feature]/research.md` (IF EXISTS)
- LOAD `specs/constitution.md` (IF EXISTS)
- LOAD `specs/[feature]/quickstart.md` (IF EXISTS)
- IF `specs/[feature]/bugs.md` EXISTS: LOAD bugs.md for bugfix task context

### Step 6: Parse tasks.md
Extract:
- Task phases: Setup, Foundational, Core, Integration, Polish
- Task dependencies: Sequential vs parallel execution rules
- Task details: ID, description, file paths, parallel markers [P], [TEST] tags
- Execution flow: Phase order and dependency requirements
- TDD bypass header (if present)

### Step 7: Phase-level TDD execution

For each phase (Setup → Foundational → Core → Integration → Polish):
Execute the entire phase as a batch, not task-by-task:

```
  Phase N: [Phase Name]
  
  ═══ RED SUB-PHASE ═══
  For EACH [TEST] task in this phase (in order):
    a. WRITE the test(s)
       - One behavior per test function
       - Group related tests in the same file
       - No mandatory 1:1 with implementation tasks:
         * One test file can cover multiple implementation tasks
         * One implementation task can have multiple test functions
       - Real code, not mocks (unless truly unavoidable)
       - Test behavior, not implementation
    
    b. RUN the specific test to verify RED:
       terminal("pytest tests/test_file.py::test_name -v")
       CONFIRM:
         - Test fails (not errors from typos)
         - Fails because the feature is missing
         - ⚠️ This is EXPECTED — proves the test is valid. NOT a bug.
         
  ═══ GREEN SUB-PHASE ═══
  For EACH implementation task in this phase (in order):
    a. WRITE the simplest code to pass the test(s)
       - Minimal — nothing more than needed
       - Cheating is OK (hardcode, copy-paste — fix in refactor)
    
  After ALL implementation tasks in this phase are written:
    b. RUN ONLY the tests relevant to this phase (NOT full suite):
       terminal("pytest tests/test_auth.py -v")   # phase-specific test file(s)
       CONFIRM:
         - All tests for this phase pass ✓
         - Do NOT run full test suite yet
    
    c. RUN the project build (if applicable):
       terminal("npm run build") OR terminal("tsc --noEmit") OR terminal("go build")
       NOTE: TypeScript projects MUST build — Vitest/Jest swallow type errors.
    
    d. UPDATE tasks.md — mark all tasks in this phase [X]
    
    e. COMMIT the full phase using the implement commit template from specs/git-conventions.md:
       (default: "feat: [feature] Phase N - [Phase Name]")
       git add -A
       git commit -m "[commit message from conventions]" --no-verify
       COMMIT_HASH=$(git rev-parse HEAD)
       NOTE: "Phase N committed as $COMMIT_HASH"

  ═══ Done with this phase ═══
```

**Execution rules:**
- Test tasks always come before implementation tasks within a phase
- All tests in a phase are written first (RED sub-phase), then all code (GREEN sub-phase)
- No commits during RED sub-phase — commit happens once per phase at GREEN
- No per-task regression runs — only run relevant tests for this phase
- Parallel [P] tasks can be written in any order but still within RED/GREEN sub-phase boundaries

#### TDD bypass mode (no test tasks)
```
IF tdd_bypassed:
  For each phase:
    For EACH task in the phase:
      a. IMPLEMENT directly
      b. VERIFY manually (no automated tests to run)
    UPDATE tasks.md — mark all tasks in phase [X]
    COMMIT the phase using the implement template from specs/git-conventions.md:
      (default: "feat: [feature] Phase N - [Phase Name]")
      git add -A
      git commit -m "[commit message from conventions]" --no-verify
```

### Step 8: Progress reporting
After each phase:
- Report phase completed: N/Total phases
- Report tasks completed: N/Total
- Report tests passing: Yes/No
- In bugfix mode: Also report bugfix task progress (BF-### completed/total)

### Step 9: Handle errors
- HALT execution if a non-parallel task cannot be completed
- FOR parallel tasks [P]: continue with working tasks, report failed
- PROVIDE clear error messages with context
- SUGGEST next steps if implementation cannot proceed

### Step 10: Full regression run — all existing tests

After ALL phases are complete and committed, run the ENTIRE test suite:

```bash
IF tdd_bypassed:
  NOTE: "TDD was bypassed — skipping automated test verification."
  PROCEED to Step 11 (build verification)
  STOP

DETECT test framework:
  IF pytest is available:        terminal("pytest tests/ -q --tb=short")
  ELSE IF go test is available:  terminal("go test ./...")
  ELSE IF npm test is available: terminal("npm test")
  ELSE:                          NOTE "No automated test framework detected — skipping."

IF all tests pass:
  REPORT: "All N tests pass. Feature implementation verified."
  PROCEED to Step 11 (build verification)

IF any tests fail:
  REPORT failing tests:
    | Test | File | Failure Type |
    |------|------|-------------|
  
  CLASSIFY each failure:
    - NEW failures (tests written during this implementation) → implementation is incomplete
    - PRE-EXISTING failures (tests that existed before, now broken) → regression
  
  IF any failures:
    CREATE one umbrella bugfix task appended to tasks.md:
    ```
    BF-REGRESSION-001 [BUGFIX] Fix regressions from [feature] implementation
      — Fix all failing tests introduced by this implementation
      — All N failures must be resolved
    ```
    NOTE: "Umbrella bugfix task BF-REGRESSION-001 created — fixing N regressions."
    
    For each regression:
      a. DEBUG the root cause
      b. FIX the code
      c. RUN the specific failing test to verify GREEN
      d. DO NOT run full suite again yet
    
    After all regressions fixed:
      RUN full suite again
      IF all pass:
        Follow `spec-kit/references/auto-commit.md`:
        - Scope: source code changes
        - Message: Use the regression commit template from specs/git-conventions.md
          (default: `"fix: [feature] BF-REGRESSION-001 - fix regressions"`)
        MARK BF-REGRESSION-001 as [X] in tasks.md
        REPORT: "All regressions fixed. All N tests pass."
      IF any still fail:
        RETURN to fix remaining failures
```

### Step 11: Build verification (if applicable)
```bash
IF npm run build / tsc --noEmit / go build / cargo build is available:
  terminal("[build command]")
  IF build fails: RETURN to fix compilation errors, then repeat Step 9 (full suite) then Step 10
```

## Implementation Rules (TDD Enforcement)

- **Phase-level TDD**: All tests for a phase are written and verified RED first, then all code is written and verified GREEN. One commit per phase.
- **RED verification is mandatory**: Every test must run and fail before implementation code is written. Without RED, the test proves nothing.
- **GREEN verification at phase level**: After all implementation code, run the phase's tests to confirm green.
- **No per-task commits**: Commit once per phase boundary, not after each individual test or task.
- **No per-task regression runs**: Only run relevant tests for the current phase. Full suite runs once after all phases.
- **Regression umbrella**: All post-implementation regressions are captured in one umbrella bugfix task (BF-REGRESSION-001), not individual bugs.
- **TDD bypass**: If the user explicitly bypassed TDD, skip all automated test steps. The summary will note the bypass.
- **Build after GREEN**: TypeScript projects MUST build — Vitest/Jest swallow type errors.

### Iron Law: Why Tests Must Come First

**If you wrote code before the test → delete it. Start over.** No exceptions without user permission.

```
Excuse                      | Reality
----------------------------|-------------------------------------------
"Too simple to test"        | Simple code breaks. Test takes 30s.
"I'll test after"           | Tests-after pass immediately → prove nothing.
"Already manually tested"   | Ad-hoc ≠ systematic. No record, can't re-run.
"Deleting X hours wasteful" | Sunk cost. Keep unverified code = tech debt.
"TDD is dogmatic"           | TDD finds bugs pre-commit, prevents regressions.
"Tests after same goal"     | Tests-after = "what does it do?" Tests-first = "what should it do?"
```

In bugfix mode: Update bugs.md Status after fixing a bug (set to "resolved")

## Phase Guardrail — STRICT

This is the **ONLY** phase where code-editing tools are permitted.

| Tool | Implement Phase | All Other Phases |
|------|----------------|-----------------|
| `write_file` (source code) | ALLOWED | **BLOCKED** |
| `patch` (source code) | ALLOWED | **BLOCKED** |
| `terminal` (build/compile/test) | ALLOWED | **BLOCKED** |
| `write_file` (spec artifacts) | ALLOWED (tasks.md, bugs.md status) | Allowed (phase-specific only) |
| `read_file`, `search_files`, `skill_view` | ALLOWED | ALLOWED |

If you are in ANY other phase (Constitution, Specify, Clarify, Plan, Tasks, Review, Test), you MUST NOT call `write_file`, `patch`, or `terminal` for compilation/builds on source code files.

### Bugfixing rule
- Bug reports always go to `bugs.md` first (via `spec-kit-test`)
- Bugfixes are NEVER implemented directly when a user mentions a bug
- Bugfixes must follow: "bugfix [feature]" → plan → tasks → implement

## Transition Log
Append to `specs/[feature]/history.md` following `spec-kit/references/history-tracking.md`:
- Phase: Phase 4 (per-phase entries for each completed phase)
- Artifacts: source code changes per phase

## Completion

Report:
- Final status
- TDD mode: Active / Bypassed by user
- Phases completed: N/Total
- Tests passing (TDD mode)
- Regressions found and fixed (if any)
- Build status (if applicable)
- Summary of completed work
- **Commit hash per phase**: `git log --oneline --grep="Phase [0-9]"`

## Done When

- [ ] All phases completed and committed
- [ ] TDD mode (if active): Every test was verified RED before implementation
- [ ] TDD mode (if active): Every phase's tests verified GREEN before commit
- [ ] TDD mode (if active): Full regression suite passes — all tests green
- [ ] TDD mode (if active): Regressions (if any) fixed via umbrella task
- [ ] Build passes (if applicable)
- [ ] All tasks in tasks.md marked [X]
- [ ] In bugfix mode: All bugfix tasks completed and verified

**Re-running this skill**:
1. LOAD tasks.md and find the first incomplete phase
2. RESUME from that phase's RED sub-phase
3. PRESERVE all [X] completion markers from completed phases
4. Only execute remaining incomplete phases

## Prerequisite Enforcement

**BLOCKED** if:
- `spec-kit-specify` has not been run
- `spec-kit-plan` has not been run
- `spec-kit-tasks` has not been run

**WARN** if:
- `spec-kit-constitution` has not been run — proceeding without constitutional gates
