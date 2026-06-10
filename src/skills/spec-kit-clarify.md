---
name: spec-kit-clarify
description: Load when the user says 'spec-kit clarify [feature]', 'speckit clarify [feature]', "clarify [feature]", or "resolve ambiguities in [feature]" — Phase 1.5 optional clarification of ambiguities in the spec.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, clarification, ambiguity, qa]
    related_skills: [spec-kit-specify, spec-kit-plan, spec-kit-workflow]
---

# spec-kit-clarify

**Task Persona**: Adopt the mindset of a curious detail-gatherer. Ambiguities hide assumptions that cause rework. Ask precise, targeted questions. Probe edge cases, constraints, and unstated expectations. Do not proceed until the ambiguity is resolved — uncertain specs produce broken code.

**Phase**: 1.5

**Purpose**: Identify and resolve underspecified areas in the current feature spec through a structured Q&A dialog.

**When NOT to use**: For straightforward specs with no ambiguities — proceed to Plan directly.

**Routing**: Load this skill when the user says "clarify [feature]" or "resolve ambiguities". If loaded directly, load spec-kit-workflow first to check prerequisites.
 Do NOT ask questions for the sake of process.

**Artifacts**:
- `specs/[feature]/clarify.md`
- Updated `specs/[feature]/spec.md` (with resolved ambiguities)

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Validate prerequisites
```
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first"
```

### Load spec
```
LOAD specs/[feature]/spec.md
IF bugfix mode: LOAD bugs.md, filter for bugs needing clarification
```

### Ambiguity scan
Check: Functional scope, domain model, UX flow, non-functional attributes, integrations, edge cases, terminology.

### Generate questions (max 5 per session)
One question at a time. Each answerable via multiple choice (2-5 options) or short answer.

### Sequential questioning loop
For each question: present → wait → validate → record.
After each answer: UPDATE spec.md, replace `[NEEDS CLARIFICATION]` markers.

### Generate clarify.md
```markdown
# Clarification Log: [Feature]
## Q1: [Question]
**Answer**: [Selected]
**Resolution**: [How applied to spec]
```

### Note on commits
Design phase artifacts are NOT committed individually. See `spec-kit/references/auto-commit.md`.

## Transition Log
Append to `specs/[feature]/history.md` following `spec-kit/references/history-tracking.md`:
- Phase: Phase 1.5
- Artifacts: `clarify.md`, `spec.md` (amended)

## Completion
- Questions asked/answered
- Sections updated in spec
- Propose: `spec-kit-plan`

## Common Pitfalls
1. **Asking unnecessary questions**: If the answer is obvious from context, don't ask. The user's time is valuable.
2. **More than 5 questions**: Keep sessions focused. Unanswered questions can be addressed in a second session.
3. **Not updating the spec**: After each answer, immediately update spec.md. The clarify.md is a log; spec.md is the source of truth.

## Prerequisite Enforcement
**BLOCKED** if: spec.md does not exist (run `spec-kit-specify` first).
