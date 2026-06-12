---
name: spec-kit-specify
description: Load when the user says 'spec-kit specify [feature]', 'speckit specify [feature]', 'spec-kit spec [feature]', 'speckit spec [feature]', "create a spec for [description]", "create specification for [feature]", or "write a spec for [feature]" — Phase 1 feature specification.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, specification, requirements, features]
    related_skills: [spec-kit-constitution, spec-kit-clarify, spec-kit-workflow]
---

# spec-kit-specify

**Task Persona**: Adopt the mindset of a curious detail-gatherer. Your job is to extract every relevant detail from the user before writing anything. Ask clarifying questions. Probe edge cases. Challenge vague statements. A complete spec answers WHAT and WHY — the HOW comes later. Every requirement must be testable.

**Phase**: 1

**Purpose**: Create or update a feature specification at `specs/[feature]/spec.md`. Defines **WHAT** users need and **WHY** — the feature, refactoring, or enhancement in full detail. Captures functional requirements (FR-###), user scenarios, success criteria, entities, and edge cases. 

**No implementation details, no code, no technology choices.** The spec describes what the system should do, not how to build it. Architecture decisions, data models, and technical approach belong in the Plan phase.

**When NOT to use**: For tiny unambiguous changes (typo fix, rename), skip straight to implementation.

**Routing**: Load this skill when the user says "create a spec for [feature]" or "specify [feature]". If loaded directly, load spec-kit-workflow first to check prerequisites.


**Artifacts**:
- `specs/[feature]/spec.md`

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Validate prerequisites
```
IF specs/constitution.md NOT EXISTS:
  BLOCK: "No constitution found. Project setup is mandatory — run spec-kit-constitution first."
  HALT
```

### Parse user description
- Extract: actors, actions, data, constraints
- If empty: ERROR "No feature description provided"

### Generate short name
2-4 word action-noun format: "user-auth", "oauth2-api-integration"

### Create feature directory
```
DETERMINE prefix (next sequential number: 001, 002...)
CREATE: specs/[###]-[short-name]/
```

### Generate spec.md
Copy `spec-kit/templates/spec-template.md` → `specs/[feature]/spec.md`

Populate with:
- **User Scenarios**: P1/P2/P3 with Given/When/Then
- **Functional Requirements**: FR-001, FR-002... — testable, technology-agnostic
- **Success Criteria**: Measurable outcomes
- **Key Entities**: Domain objects only (no implementation)
- **Edge Cases**: Error conditions, boundaries

### Apply constraints
- MAX 3 `[NEEDS CLARIFICATION]` markers
- NO implementation details (tech stack, frameworks, APIs)
- Prioritize: scope > security > UX > technical


### Note on commits
Each skill commits its own artifacts immediately. See `spec-kit/references/auto-commit.md`.

### Append to history.md and Commit

**Order is critical: history.md FIRST, then commit.**

1. **Append to history.md**:
   Append entry to `specs/[feature]/history.md` (create if missing):
   - Phase: Phase 1 — Complete
   - Artifact: `specs/[feature]/spec.md`

2. **PRE-COMMIT GUARD**:
   READ `specs/[feature]/history.md` — confirm the spec.md entry is recorded.
   If missing: BLOCK — must append before commit.

3. **Commit**:
   Follow `spec-kit/references/auto-commit.md`:
   - Scope: `specs/[feature]/spec.md`
   - Message: `"spec(phase-1): [feature] spec"`

### Done When
- [ ] spec.md created with FR-### requirements numbered sequentially
- [ ] No existing content deleted; modifications minimal (additive-safe)
- [ ] history.md entry appended
- [ ] Committed

## Completion
- Feature directory path, spec file path
- Propose: `spec-kit-clarify` or `spec-kit-plan`

## Common Pitfalls
1. **Implementation details in spec**: Focus on user value. Move architecture decisions to the Plan phase.
2. **Too many `[NEEDS CLARIFICATION]` markers**: Keep to 3 max. If more, the feature scope is too vague — clarify with the user first.
3. **Over-specifying**: For simple features, a single paragraph + 2-3 FRs is enough. Don't force full template on trivial changes.

## Prerequisite Enforcement
**BLOCKED** if: constitution.md does not exist.
