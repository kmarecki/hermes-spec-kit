     1|---
     2|name: spec-kit-plan
     3|description: Create technical implementation plan from feature specification. Phase 2 - defines HOW with constitutional gates.
     4|category: software-development
     5|---
     6|
     7|# spec-kit-plan
     8|
     9|**Phase**: 2
    10|
    11|**Purpose**: Create or update the implementation plan at `specs/[feature]/plan.md`. Defines technical architecture, resolves constitutional gates, generates design artifacts.
    12|
    13|**Prerequisites**: `spec-kit-constitution` + `spec-kit-specify` must be run first<br>
**Bugfix mode**: When run from the bugfix loop, `specs/[feature]/bugs.md` must also exist
    14|
    15|**Artifacts**:
    16|- `specs/[feature]/plan.md` (primary artifact)
    17|- `specs/[feature]/research.md` (technical research)
    18|- `specs/[feature]/data-model.md` (entity definitions)
    19|- `specs/[feature]/quickstart.md` (validation scenarios)
    20|- `specs/[feature]/contracts/` (API specifications)
    21|
    22|## Execution
    23|
    24|### Step 1: Validate prerequisites
    25|```
    26|IF specs/constitution.md NOT EXISTS:
    27|  ERROR: "Run spec-kit-constitution first"
    28|IF specs/[feature]/spec.md NOT EXISTS:
    29|  ERROR: "Run spec-kit-specify first"
    30|```
    31|
    ### Step 2: Load context
    - LOAD `specs/[feature]/spec.md`
    - LOAD `specs/constitution.md`
    - LOAD `templates/plan.md`
    - IF `specs/[feature]/bugs.md` EXISTS (bugfix mode): LOAD bugs.md for bug context
    36|
    37|### Step 3: Fill Technical Context
    38|Document:
    39|- Language/Version
    40|- Primary Dependencies
    41|- Storage (database, files)
    42|- Testing framework
    43|- Target Platform
    44|- Project Type (library/cli/web-service/mobile-app)
    45|- Performance Goals
    46|- Constraints (latency, memory, offline)
    47|- Scale/Scope
    48|
    49|Mark unknowns as "NEEDS CLARIFICATION"
    50|
    51|### Step 4: Constitutional Gates
    52|Evaluate gates BEFORE proceeding:
    53|- **Simplicity Gate** (Article VII): Using ≤3 projects? No future-proofing?
    54|- **Anti-Abstraction Gate** (Article VIII): Using framework directly? Single model representation?
    55|- **Integration-First Gate** (Article IX): Contracts defined? Contract tests written?
    56|
    57|```
    58|IF any gate FAILS without justification:
    59|  BLOCK: "Constitutional gate violation — document justification or adjust design"
    60|```
    61|
    62|### Step 5: Phase 0 - Research
    63|Generate `research.md`:
    64|- For each NEEDS CLARIFICATION: research task
    65|- For each technology choice: best practices
    66|- For each dependency: patterns
    67|- Format: Decision, Rationale, Alternatives Considered
    68|
    69|### Step 6: Phase 1 - Design & Contracts
    70|Generate `data-model.md`:
    71|- Entity name, fields, relationships
    72|- Validation rules
    73|- State transitions
    74|
    75|Generate `contracts/` directory:
    76|- API specifications
    77|- Command schemas
    78|- Test scenarios
    79|
    80|Generate `quickstart.md`:
    81|- Key validation scenarios
    82|
    83|### Step 7: Project structure
    84|Choose from template:
    85|- **Single project** (DEFAULT): `src/`, `tests/`
    86|- **Web app**: `backend/`, `frontend/`
    87|- **Mobile + API**: `api/`, `ios/` or `android/`
    88|
    89|Document structure decision in plan.
    90|
    ### Step 8: Complexity tracking
    If constitutional gates violated, document in plan:
    | Violation | Why Needed | Simpler Alternative Rejected Because |

    ### Step 9: Bugfix planning (bugfix mode only)
    IF `bugs.md` EXISTS:
      FOR EACH bug with Status: open or in-progress:
        - ANALYZE root cause in context of spec + plan
        - ADD bugfix section to plan.md: root cause, approach, files affected
        - SET Plan Ref in bugs.md to reference the plan section
      GENERATE bugfix plan content:
    ```markdown
    ## Bugfix: BUG-001 — [Title]
    - **Root Cause**: [analysis]
    - **Approach**: [fix strategy]
    - **Files Affected**: [list]
    - **Verification**: [how to verify the fix]
    ```
    94|
    95|## Completion
    96|
    97|Report:
    98|- Plan path
    99|- Generated artifacts (research.md, data-model.md, contracts/)
   100|- Gate status (pass/fail with justifications)
   101|- Suggest next command
   102|
   ## Next Skills

   - Run `spec-kit-tasks` to create task breakdown
   - Run `spec-kit-analyze` for optional quality gate before implementation
   - In bugfix mode: Run `spec-kit-tasks` for bugfix task breakdown

   **Re-running this skill**:
   1. LOAD existing plan, research, data-model
   2. COMPARE against current spec
   3. UPDATE only changed sections
   4. PRESERVE research findings unless spec changed

   ## Prerequisite Enforcement

   **BLOCKED** if:
   - `spec-kit-constitution` has not been run
   - `spec-kit-specify` has not been run
   119|
   120|## Re-run Enforcement
   121|
   122|After re-running `spec-kit-constitution`:
   123|1. Re-validate gates against updated principles
   124|2. Update plan if principles conflict
   125|
   126|After re-running `spec-kit-specify`:
   127|1. Re-validate architecture against updated requirements
   128|
   129|After re-running `spec-kit-clarify`:
   130|1. Re-evaluate technical decisions affected by clarifications
   131|
   132|## Completion
   133|
   134|Report:
   135|- Plan path
   136|- Generated artifacts (research.md, data-model.md, contracts/)
   137|- Gate status (pass/fail with justifications)
   138|- Suggest next command
   139|
   140|## Next Skills
   141|
   142|- Run `spec-kit-tasks` to create task breakdown
   143|- Run `spec-kit-analyze` for optional quality gate before implementation