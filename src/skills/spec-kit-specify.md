     1|---
     2|name: spec-kit-specify
     3|description: Create or update a feature specification. Phase 1 - defines WHAT users need and WHY, without implementation details.
     4|category: software-development
     5|---
     6|
     7|# spec-kit-specify
     8|
     9|**Phase**: 1
    10|
    11|**Purpose**: Create or update a feature specification at `specs/[feature]/spec.md`. Defines WHAT users need and WHY, not HOW to implement.
    12|
    13|**Prerequisites**: `spec-kit-constitution` must be run first
    14|
    15|**Artifacts**:
    16|- `specs/[feature]/spec.md` (primary artifact)
    17|- `specs/[feature]/checklists/requirements.md` (quality checklist)
    18|
    19|## Execution
    20|
    21|### Step 1: Validate prerequisites
    22|```
    23|IF specs/constitution.md NOT EXISTS:
    24|  ERROR: "Run spec-kit-constitution first to establish project principles"
    25|```
    26|
    27|### Step 2: Parse user description
    28|- Parse the feature description from user input
    29|- If empty: ERROR "No feature description provided"
    30|- Extract: actors, actions, data, constraints
    31|
    32|### Step 3: Generate short name
    33|Create 2-4 word short name:
    34|- Use action-noun format: "user-auth", "oauth2-api-integration"
    35|- Preserve technical terms: OAuth2, API, JWT
    36|- Examples:
    37|  - "I want to add user authentication" → "user-auth"
    38|  - "Implement OAuth2 integration for the API" → "oauth2-api-integration"
    39|
    40|### Step 4: Create feature directory
    41|```
    42|DETERMINE prefix:
    43|  - Scan existing specs/ directories
    44|  - Find next sequential number (001, 002, ...)
    45|DIRECTORY: specs/[###]-[short-name]/
    46|CREATE: mkdir -p specs/[feature]/checklists
    47|```
    48|
    49|### Step 5: Generate spec.md
    50|COPY `templates/spec.md` → `specs/[feature]/spec.md`
    51|
    52|Populate with:
    53|- **User Scenarios**: P1/P2/P3 priority with Given/When/Then acceptance scenarios
    54|- **Functional Requirements**: FR-001, FR-002, etc. — testable, technology-agnostic
    55|- **Success Criteria**: Measurable outcomes (time, performance, volume)
    56|- **Key Entities**: Domain objects without implementation details
    57|- **Edge Cases**: Error conditions, boundary handling
    58|
    59|### Step 6: Apply constraints
    60|- Focus on WHAT users need and WHY
    61|- **NO implementation details**: no tech stack, frameworks, APIs
    62|- **MAX 3 [NEEDS CLARIFICATION] markers** — use only for critical decisions
    63|- Prioritize: scope > security/privacy > user experience > technical details
    64|
    65|### Step 7: Generate requirements checklist
    66|COPY `templates/checklist.md` → `specs/[feature]/checklists/requirements.md`
    67|
    68|Validate:
    69|- No implementation details leaked
    70|- All acceptance scenarios defined
    71|- Success criteria measurable
    72|- Max 3 [NEEDS CLARIFICATION] markers
    73|
    74|## Completion
    75|
    76|Report:
    77|- Feature directory path
    78|- Spec file path
    79|- Checklist status
    80|- List readiness for next phase
    81|
    82|## Next Skills
    83|
    84|- Run `spec-kit-clarify` for iterative clarification (optional but recommended)
    85|- Run `spec-kit-plan` when ready for technical planning
    86|
    87|**Re-running this skill**:
    88|1. LOAD existing `specs/[feature]/spec.md`
    89|2. Compare user input against current spec
    90|3. UPDATE only changed sections
    91|4. PRESERVE unchanged content
    92|5. PRESERVE branch name and feature number
    93|6. PRESERVE completed checklist status
    94|
    95|## Prerequisite Enforcement
    96|
    97|**BLOCKED** if `spec-kit-constitution` has not been run:
    98|```
    99|CHECK: specs/constitution.md EXISTS
   100|IF NOT:
   101|  ERROR: "Run spec-kit-constitution first to establish project principles"
   102|```
   103|
   104|## Re-run Enforcement
   105|
   106|After re-running `spec-kit-constitution`:
   107|1. Re-validate spec against updated principles
   108|2. UPDATE any sections that conflict with new principles
   109|3. FLAG constitution violations as CRITICAL
   110|
   111|## Completion
   112|
   113|Report:
   114|- Feature directory path
   115|- Spec file path
   116|- Checklist status
   117|- List readiness for next phase
   118|
   119|## Next Skills
   120|
   121|- Run `spec-kit-clarify` for iterative clarification (optional but recommended)
   122|- Run `spec-kit-plan` when ready for technical planning