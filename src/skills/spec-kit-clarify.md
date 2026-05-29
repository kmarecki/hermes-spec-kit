---
name: spec-kit-clarify
description: Iterative clarification dialog to resolve ambiguities. Phase 1.5 - between spec and plan.
category: software-development
---

# spec-kit-clarify

**Phase**: 1.5

**Purpose**: Identify and resolve underspecified areas in the current feature spec through a structured Q&A dialog.

**Prerequisites**: `spec-kit-constitution` + `spec-kit-specify` must be run first

**Artifacts**:
- `specs/[feature]/clarify.md` (clarification log)
- Updated `specs/[feature]/spec.md` (with resolved ambiguities)

## Execution

### Step 1: Validate prerequisites
```
IF .specify/memory/constitution.md NOT EXISTS:
  ERROR: "Run spec-kit-constitution first"
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first to create the feature specification"
```

### Step 2: Load spec
LOAD `specs/[feature]/spec.md`

### Step 3: Ambiguity scan
Analyze these categories for gaps:
- **Functional Scope**: Core user goals, out-of-scope declarations
- **Domain & Data Model**: Entities, attributes, relationships, lifecycle
- **Interaction & UX Flow**: Critical journeys, error/empty states
- **Non-Functional Attributes**: Performance, scalability, security, observability
- **Integration & Dependencies**: External APIs, data formats, failure modes
- **Edge Cases**: Negative scenarios, rate limiting, conflict resolution
- **Terminology**: Canonical glossary, avoided synonyms

### Step 4: Generate questions (max 5)
For each gap found, create candidate question:
- **Maximum 5 questions** total per session
- One question at a time
- Each answerable with either:
  - Multiple choice (2-5 options)
  - Short answer (<=5 words)

### Step 5: Sequential questioning loop
For each question:
1. Present question with recommended option + reasoning
2. Include markdown table of all options
3. Wait for user response
4. Validate response (option letter, "yes", or short answer)
5. Record answer

### Step 6: Integrate answers
After each accepted answer:
- UPDATE `specs/[feature]/spec.md` with the resolved value
- REPLACE [NEEDS CLARIFICATION] marker with resolved answer
- WRITE spec file after each integration

### Step 7: Generate clarify.md
CREATE `specs/[feature]/clarify.md`:
```
# Clarification Log: [Feature]

**Feature**: specs/[feature]/spec.md
**Created**: [DATE]
**Questions Asked**: N
**Questions Resolved**: N

## Q1: [Question]
**Context**: [Relevant spec section]
**Options**:
| Option | Answer | Implications |
**Answer**: [Selected]
**Resolution**: [How it was applied to spec]
```

### Step 8: Update requirements checklist
RE-EVALUATE `specs/[feature]/checklists/requirements.md`:
- TOGGLE `[ ]` to `[x]` for newly satisfied criteria
- TOGGLE `[x]` to `[ ]` for regressed criteria

### Step 9: Write phase marker
```
WRITE specs/[feature]/.phase: "clarify"
```

## Idempotency

**Re-running this skill**:
1. LOAD current spec
2. IDENTIFY which clarifications were previously resolved
3. ASK only about remaining ambiguities
4. DO NOT re-ask already-answered questions
5. UPDATE clarify.md with new session

## Prerequisite Enforcement

**BLOCKED** if:
- `spec-kit-constitution` has not been run
- `spec-kit-specify` has not been run

## Re-run Enforcement

After re-running `spec-kit-specify`:
1. RE-SCAN for new ambiguities introduced by spec changes
2. FLAG any previously-clarified items that are now contradictory

## Completion

Report:
- Number of questions asked and answered
- Sections updated in spec
- Checklist status (before → after)
- Suggest next command

## Next Skills

- Run `spec-kit-specify` again to make additional changes
- Run `spec-kit-plan` when all critical ambiguities are resolved