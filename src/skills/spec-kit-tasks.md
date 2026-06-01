     1|---
     2|name: spec-kit-tasks
     3|description: Generate executable task breakdown from implementation plan. Phase 3 - decomposes plan into ordered, traceable tasks.
     4|category: software-development
     5|---
     6|
     7|# spec-kit-tasks
     8|
     9|**Phase**: 3
    10|
    11|**Purpose**: Create or update `specs/[feature]/tasks.md` — an executable task list derived from the plan.
    12|
    13|**Prerequisites**: `spec-kit-constitution` + `spec-kit-specify` + `spec-kit-plan` must be run first
    14|
    15|**Artifacts**:
    16|- `specs/[feature]/tasks.md` (primary artifact)
    17|
    18|## Execution
    19|
    20|### Step 1: Validate prerequisites
    21|```
    22|IF specs/[feature]/plan.md NOT EXISTS:
    23|  ERROR: "Run spec-kit-plan first to generate the implementation plan"
    24|IF specs/[feature]/spec.md NOT EXISTS:
    25|  ERROR: "Run spec-kit-specify first"
    26|IF specs/constitution.md NOT EXISTS:
    27|  ERROR: "Run spec-kit-constitution first"
    28|```
    29|
    30|### Step 2: Load context
    31|- LOAD `specs/[feature]/plan.md` — for architecture and phases
    32|- LOAD `specs/[feature]/spec.md` — for user stories and requirements
    33|- LOAD `specs/[feature]/data-model.md` — for entities
    34|- LOAD `specs/[feature]/contracts/` — for API specs
    35|- LOAD `templates/tasks.md`
    36|
    37|### Step 3: Map requirements to tasks
    38|For each Functional Requirement (FR-###):
    39|- IDENTIFY which tasks implement it
    40|- RECORD requirement-task mapping
    41|
    42|For each User Story:
    43|- MAP acceptance scenarios to test tasks
    44|- MAP entities to model tasks
    45|- MAP services to implementation tasks
    46|
    47|### Step 4: Generate task breakdown
    48|Organize tasks by phase:
    49|
    50|**Phase 1: Setup (Shared Infrastructure)**
    51|- Project initialization
    52|- Dependency configuration
    53|- Linting/formatting setup
    54|
    55|**Phase 2: Foundational (Blocking Prerequisites)**
    56|- Database schema and migrations
    57|- Authentication/authorization framework
    58|- API routing structure
    59|- Base models
    60|- Error handling infrastructure
    61|
    62|**Phase 3+: User Story Implementation**
    63|- Tasks for each user story (US1, US2, US3...)
    64|- Contract tests first (if tests requested)
    65|- Integration tests
    66|- Unit tests
    67|- Implementation tasks
    68|
    69|**Phase N: Polish & Cross-Cutting**
    70|- Documentation
    71|- Code cleanup
    72|- Performance optimization
    73|- Security hardening
    74|
    75|### Step 5: Add task metadata
    76|For each task:
    77|- **ID**: T001, T002, etc.
    78|- **[P]**: Mark as parallelizable (different files, no dependencies)
    79|- **[US#]**: Which user story it belongs to
    80|- **File paths**: Exact locations for implementation
    81|
    82|### Step 6: Define checkpoints
    83|After each phase, add checkpoint comment:
    84|```
    85|Checkpoint: Phase N complete — [description]
    86|```
    87|
    88|### Step 7: Document dependencies
    89|At end of tasks.md:
    90|- Phase dependencies
    91|- User story dependencies
    92|- Parallel execution opportunities
    93|
    94|## Completion
    95|
    96|Report:
    97|- Task count by phase
    98|- Parallelizable task count
    99|- Requirement coverage percentage
   100|- Suggest next command
   101|
   102|## Next Skills
   103|
   104|- Run `spec-kit-analyze` for optional quality gate before implementation
   105|- Run `spec-kit-implement` to execute tasks
   106|
   107|**Re-running this skill**:
   108|1. LOAD existing tasks.md
   109|2. COMPARE against current plan and spec
   110|3. ADD new tasks for changed requirements
   111|4. REMOVE tasks for deleted requirements
   112|5. PRESERVE completed task status ([X] markers)
   113|
   114|## Prerequisite Enforcement
   115|
   116|**BLOCKED** if:
   117|- `spec-kit-constitution` has not been run
   118|- `spec-kit-specify` has not been run
   119|- `spec-kit-plan` has not been run
   120|
   121|## Re-run Enforcement
   122|
   123|After re-running `spec-kit-plan`:
   124|1. Re-derive tasks from updated architecture
   125|2. Mark changed tasks as incomplete
   126|
   127|After re-running `spec-kit-specify`:
   128|1. Re-map tasks to updated requirements
   129|2. ADD/REMOVE tasks as needed
   130|
   131|After re-running `spec-kit-clarify`:
   132|1. Re-evaluate tasks affected by clarifications
   133|
   134|## Task Format
   135|```
   136|T001 [P] [US1] Description — src/path/file.ext
   137|T002 [US1] Description — src/path/file.ext (depends on T001)
   138|```
   139|
   140|## Completion
   141|
   142|Report:
   143|- Task count by phase
   144|- Parallelizable task count
   145|- Requirement coverage percentage
   146|- Suggest next command
   147|
   148|## Next Skills
   149|
   150|- Run `spec-kit-analyze` for optional quality gate before implementation
   151|- Run `spec-kit-implement` to execute tasks