     1|---
     2|name: spec-kit-clarify
     3|description: Iterative clarification dialog to resolve ambiguities. Phase 1.5 - between spec and plan.
     4|category: software-development
     5|---
     6|
     # spec-kit-clarify

     **Phase**: 1.5

     **Purpose**: Identify and resolve underspecified areas in the current feature spec through a structured Q&A dialog.
     **Bugfix mode**: When run from the bugfix loop, resolves ambiguities about specific bugs in bugs.md.
    12|
    13|**Prerequisites**: `spec-kit-constitution` + `spec-kit-specify` must be run first
    14|
    15|**Artifacts**:
    16|- `specs/[feature]/clarify.md` (clarification log)
    17|- Updated `specs/[feature]/spec.md` (with resolved ambiguities)
    18|
    19|## Execution
    20|
    21|### Step 1: Validate prerequisites
    22|```
    23|IF specs/constitution.md NOT EXISTS:
    24|  ERROR: "Run spec-kit-constitution first"
    25|IF specs/[feature]/spec.md NOT EXISTS:
    26|  ERROR: "Run spec-kit-specify first to create the feature specification"
    27|```
    28|
    ### Step 2: Load spec
    LOAD `specs/[feature]/spec.md`
    IF `specs/[feature]/bugs.md` EXISTS (bugfix mode):
      LOAD bugs.md
      FILTER bugs where Requires Clarification == yes
      USE bug descriptions as the basis for clarification questions
    31|
    32|### Step 3: Ambiguity scan
    33|Analyze these categories for gaps:
    34|- **Functional Scope**: Core user goals, out-of-scope declarations
    35|- **Domain & Data Model**: Entities, attributes, relationships, lifecycle
    36|- **Interaction & UX Flow**: Critical journeys, error/empty states
    37|- **Non-Functional Attributes**: Performance, scalability, security, observability
    38|- **Integration & Dependencies**: External APIs, data formats, failure modes
    39|- **Edge Cases**: Negative scenarios, rate limiting, conflict resolution
    40|- **Terminology**: Canonical glossary, avoided synonyms
    41|
    42|### Step 4: Generate questions (max 5)
    43|For each gap found, create candidate question:
    44|- **Maximum 5 questions** total per session
    45|- One question at a time
    46|- Each answerable with either:
    47|  - Multiple choice (2-5 options)
    48|  - Short answer (<=5 words)
    49|
    50|### Step 5: Sequential questioning loop
    51|For each question:
    52|1. Present question with recommended option + reasoning
    53|2. Include markdown table of all options
    54|3. Wait for user response
    55|4. Validate response (option letter, "yes", or short answer)
    56|5. Record answer
    57|
    ### Step 6: Integrate answers
    After each accepted answer:
    - UPDATE `specs/[feature]/spec.md` with the resolved value
    - REPLACE [NEEDS CLARIFICATION] marker with resolved answer
    - WRITE spec file after each integration
    - In bugfix mode: Also UPDATE the bug's Requires Clarification flag to "no" and add clarification notes
    63|
    ### Step 7: Generate clarify.md
    CREATE `specs/[feature]/clarify.md`:
    ```
    # Clarification Log: [Feature]

    **Feature**: specs/[feature]/spec.md
    **Created**: [DATE]
    **Questions Asked**: N
    **Questions Resolved**: N
    **Bugfix mode**: [yes/no — if yes, lists which BUG-IDs were clarified]

    ## Q1: [Question]
    **Context**: [Relevant spec section]
    **Options**:
    | Option | Answer | Implications |
    **Answer**: [Selected]
    **Resolution**: [How it was applied to spec]
    ```
    81|
    82|### Step 8: Update requirements checklist
    83|RE-EVALUATE `specs/[feature]/checklists/requirements.md`:
    84|- TOGGLE `[ ]` to `[x]` for newly satisfied criteria
    85|- TOGGLE `[x]` to `[ ]` for regressed criteria
    86|
    87|## Completion
    88|
    89|Report:
    90|- Number of questions asked and answered
    91|- Sections updated in spec
    92|- Checklist status (before → after)
    93|- Suggest next command
    94|
    95|## Next Skills
    96|
    97|- Run `spec-kit-specify` again to make additional changes
    98|- Run `spec-kit-plan` when all critical ambiguities are resolved
    99|
   100|**Re-running this skill**:
   101|1. LOAD current spec
   102|2. IDENTIFY which clarifications were previously resolved
   103|3. ASK only about remaining ambiguities
   104|4. DO NOT re-ask already-answered questions
   105|5. UPDATE clarify.md with new session
   106|
   107|## Prerequisite Enforcement
   108|
   109|**BLOCKED** if:
   110|- `spec-kit-constitution` has not been run
   111|- `spec-kit-specify` has not been run
   112|
   113|## Re-run Enforcement
   114|
   115|After re-running `spec-kit-specify`:
   116|1. RE-SCAN for new ambiguities introduced by spec changes
   117|2. FLAG any previously-clarified items that are now contradictory
   118|
   119|## Completion
   120|
   121|Report:
   122|- Number of questions asked and answered
   123|- Sections updated in spec
   124|- Checklist status (before → after)
   125|- Suggest next command
   126|
   127|## Next Skills
   128|
   129|- Run `spec-kit-specify` again to make additional changes
   130|- Run `spec-kit-plan` when all critical ambiguities are resolved