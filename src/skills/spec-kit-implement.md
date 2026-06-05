     1|---
     2|name: spec-kit-implement
     3|description: Execute implementation following the task plan. Phase 4 - runs tasks in order with TDD approach.
     4|category: software-development
     5|---
     6|
     # spec-kit-implement

     **Phase**: 4

     **Purpose**: Execute implementation following `specs/[feature]/tasks.md`. Runs tasks in order with TDD approach.
     **Bugfix mode**: When tasks.md contains bugfix tasks (prefixed with BF-###), executes them alongside regular tasks.

     **Prerequisites**: `spec-kit-constitution` + `spec-kit-specify` + `spec-kit-plan` + `spec-kit-tasks` must be run first<br>
     **Bugfix mode**: When bugs.md exists, load it for bugfix task context
    14|
    15|**Artifacts**: Updated `specs/[feature]/tasks.md` (with completion markers)
    16|
    17|## Execution
    18|
    19|### Step 1: Validate prerequisites
    20|```
    21|IF specs/[feature]/tasks.md NOT EXISTS:
    22|  ERROR: "Run spec-kit-tasks first to generate task breakdown"
    23|IF specs/[feature]/plan.md NOT EXISTS:
    24|  ERROR: "Run spec-kit-plan first"
    25|IF specs/[feature]/spec.md NOT EXISTS:
    26|  ERROR: "Run spec-kit-specify first"
    27|```
    28|
    29|### Step 2: Check checklists status
    30|```
    31|SCAN specs/[feature]/checklists/ for checklist files
    32|FOR EACH checklist:
    33|  COUNT total items: lines matching - [ ] or - [X]
    34|  COUNT completed: lines matching - [X]
    35|  COUNT incomplete: lines matching - [ ]
    36|IF any checklist has incomplete items:
    37|  DISPLAY status table
    38|  ASK: "Some checklists are incomplete. Proceed with implementation? (yes/no)"
    39|  WAIT for user response
    40|  IF "no": HALT
    41|  IF "yes": CONTINUE
    42|```
    43|
    ### Step 3: Load implementation context
    - LOAD `specs/[feature]/tasks.md` (REQUIRED)
    - LOAD `specs/[feature]/plan.md` (REQUIRED)
    - LOAD `specs/[feature]/data-model.md` (IF EXISTS)
    - LOAD `specs/[feature]/contracts/` (IF EXISTS)
    - LOAD `specs/[feature]/research.md` (IF EXISTS)
    - LOAD `specs/constitution.md` (IF EXISTS)
    - LOAD `specs/[feature]/quickstart.md` (IF EXISTS)
    - IF `specs/[feature]/bugs.md` EXISTS: LOAD bugs.md for bugfix task context
    52|
    53|### Step 4: Parse tasks.md
    54|Extract:
    55|- Task phases: Setup, Foundational, Core, Integration, Polish
    56|- Task dependencies: Sequential vs parallel execution rules
    57|- Task details: ID, description, file paths, parallel markers [P]
    58|- Execution flow: Order and dependency requirements
    59|
    60|### Step 5: Execute implementation
    61|Execute tasks following rules:
    62|- **Phase-by-phase execution**: Complete each phase before moving to next
    63|- **Respect dependencies**: Sequential tasks in order, parallel [P] can run together
    64|- **TDD approach**: Execute test tasks before their corresponding implementation tasks
    65|- **File-based coordination**: Tasks affecting same files must run sequentially
    66|- **Validation checkpoints**: Verify each phase before proceeding
    67|
    68|### Step 6: For each task:
    69|a. READ task description and file path
    70|b. IF test task: write failing test first
    71|c. IF implementation task: implement to make test pass
    72|d. VERIFY task completion
    73|e. UPDATE tasks.md with [X] completion marker
    74|
    ### Step 7: Progress reporting
    After each task:
    - Report tasks completed: N/Total
    - Report current phase
    - Report next task
    - Report tests passing: Yes/No
    - In bugfix mode: Also report bugfix task progress (BF-### completed/total)

    ### Step 8: Handle errors
    83|- HALT execution if non-parallel task fails
    84|- FOR parallel tasks [P]: continue with successful, report failed
    85|- PROVIDE clear error messages with context
    86|- SUGGEST next steps if implementation cannot proceed
    87|
    88|## Completion
    89|
    90|Report:
    91|- Final status
    92|- Tasks completed vs total
    93|- Tests passing
    94|- Summary of completed work
    95|
    ## Done When

    - [ ] All tasks in tasks.md completed and marked [X]
    - [ ] Implementation validated against spec and plan
    - [ ] All tests passing
    - [ ] Implementation complete
    - [ ] In bugfix mode: All bugfix tasks completed and verified
   102|
   103|**Re-running this skill**:
   104|1. LOAD tasks.md and find next incomplete task
   105|2. RESUME from where execution stopped
   106|3. PRESERVE all [X] completion markers
   107|4. Only execute remaining incomplete tasks
   108|
   109|## Prerequisite Enforcement
   110|
   111|**BLOCKED** if:
   112|- `spec-kit-constitution` has not been run
   113|- `spec-kit-specify` has not been run
   114|- `spec-kit-plan` has not been run
   115|- `spec-kit-tasks` has not been run
   116|
   ## Implementation Rules

   - NEVER skip test tasks
   - NEVER implement without understanding the requirement
   - ALWAYS verify file paths exist or create them
   - ALWAYS run tests after implementation
   - STOP on test failures and report
   - UPDATE tasks.md immediately after completion
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
   125|
   126|## Completion
   127|
   128|Report:
   129|- Final status
   130|- Tasks completed vs total
   131|- Tests passing
   132|- Summary of completed work
   133|
   ## Done When

   - [ ] All tasks in tasks.md completed and marked [X]
   - [ ] Implementation validated against spec and plan
   - [ ] All tests passing
   - [ ] Implementation complete
   - [ ] In bugfix mode: All bugfix tasks completed and verified