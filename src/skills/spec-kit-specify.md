---
name: spec-kit-specify
description: Use when the user says 'create a spec for [feature]' or 'specify [feature]' — Phase 1 feature specification.
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

**Phase**: 1

**Purpose**: Create or update a feature specification at `specs/[feature]/spec.md`. Defines WHAT users need and WHY, not HOW to implement.

**When NOT to use**: For tiny unambiguous changes (typo fix, rename), skip straight to implementation.

**Routing**: Load this skill when the user says "create a spec for [feature]" or "specify [feature]". If loaded directly, load spec-kit-workflow first to check prerequisites.


**Artifacts**:
- `specs/[feature]/spec.md`
- `specs/[feature]/checklists/requirements.md`

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Validate prerequisites
```
IF specs/constitution.md NOT EXISTS:
  WARN: "No constitution found — proceeding without constitutional gates."
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

### Generate checklist
Copy `spec-kit/templates/checklist-template.md` → `specs/[feature]/checklists/requirements.md`

Validate: no implementation leaks, all scenarios defined, criteria measurable.

### Note on commits
Design phase artifacts (spec.md, clarify.md, plan.md, tasks.md) are NOT committed individually. They are batch-committed when Phase 4 (Implement) begins. See `spec-kit/references/auto-commit.md`.

## Completion
- Feature directory path, spec file path
- Propose: `spec-kit-clarify` or `spec-kit-plan`

## Common Pitfalls
1. **Implementation details in spec**: Focus on user value. Move architecture decisions to the Plan phase.
2. **Too many `[NEEDS CLARIFICATION]` markers**: Keep to 3 max. If more, the feature scope is too vague — clarify with the user first.
3. **Over-specifying**: For simple features, a single paragraph + 2-3 FRs is enough. Don't force full template on trivial changes.

## Prerequisite Enforcement
**WARN** (not BLOCKED) if constitution missing — constitution is optional.
