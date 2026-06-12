---
name: spec-kit-plan
description: Load when the user says 'spec-kit plan [feature]', 'speckit plan [feature]', "plan [feature]", "plan the implementation for [feature]", or "design the architecture for [feature]" — Phase 2 technical planning for the feature.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, planning, architecture, design]
    related_skills: [spec-kit-specify, spec-kit-tasks, spec-kit-workflow]
---

# spec-kit-plan

**Task Persona**: Adopt the mindset of a system architect and philosopher. Think deeply about tradeoffs, edge cases, failure modes, and scalability. Challenge assumptions. Every requirement must be accounted for — missing details now cause rework later. A thorough plan saves tenfold time in implementation.

**Phase**: 2

**Purpose**: Create or update the implementation plan at `specs/[feature]/plan.md`. Defines **HOW** to implement the spec: architecture, data flow, module boundaries, API contracts.

The plan must:
- **Study existing specs and codebase** to understand current architecture, patterns, and conventions
- **Minimize impact on existing code** — design the implementation with the smallest possible footprint while respecting constitution rules and architecture principles
- **Avoid code-level implementation details** — the plan describes approach and structure, not line-level implementation. Concrete coding belongs in the Implement phase.
- **Resolve constitutional gates** — verify the approach aligns with project principles
- **Generate design artifacts**: `research.md`, `data-model.md`, `contracts/*`, `quickstart.md`

**When NOT to use**: For trivial changes (typo fix, config change) — skip planning and go directly to implementation.

**Routing**: Load this skill when the user says "plan [feature]" or "create plan for [feature]". If loaded directly, load spec-kit-workflow first to check prerequisites.


**Artifacts**:
- `specs/[feature]/plan.md`
- `specs/[feature]/research.md`
- `specs/[feature]/data-model.md`
- `specs/[feature]/quickstart.md`
- `specs/[feature]/contracts/`

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Validate prerequisites
```
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first"
IF specs/constitution.md NOT EXISTS:
  BLOCK: "No constitution found. Run spec-kit-constitution first."
  HALT
```

### Load context
```
LOAD specs/[feature]/spec.md, specs/constitution.md (IF EXISTS)

IF bugfix mode (reopened bugfix):
  NOTE: "Bugfix mode — plan.md already exists. Will append bugfix sections only."
  LOAD existing specs/[feature]/plan.md
  LOAD bugs.md for bug context
ELSE:
  LOAD spec-kit/templates/plan-template.md
  COPY spec-kit/templates/plan-template.md → specs/[feature]/plan.md
```

### Fill Technical Context
Document: language/version, dependencies, storage, test framework, platform, project type, performance goals, constraints.

### Constitutional Gates (advisory)
Evaluate: simplicity (≤3 projects), anti-abstraction (use framework directly), integration-first (contracts defined).
If gate fails without justification → document as violation in plan.

### Research
Generate `research.md`: decision → rationale → alternatives considered for each technology choice.

### Design & Contracts
Generate `data-model.md`: entities, fields, relationships, validation, state transitions.
Generate `contracts/`: API specs, command schemas.
Generate `quickstart.md`: key validation scenarios.

### Project structure
Choose template: Single project (`src/`, `tests/`) / Web app / Mobile + API.

### Bugfix planning (bugfix mode)
For each open bug: analyze root cause, append bugfix section to plan.md (do NOT remove existing plan content), set Plan Ref in bugs.md.

**Additive-safe**: Append new bugfix sections at the end of plan.md. Never delete existing plan sections. You may modify existing sections minimally (e.g. mark a section as superseded by a bugfix). If a new fix contradicts an existing plan section, ask the user for guidance.

### Note on commits
Each skill commits its own artifacts immediately. See `spec-kit/references/auto-commit.md`.

### Append to history.md
Append entry to `specs/[feature]/history.md` (create if missing):
- Phase: Phase 2 — Complete
- Artifact: `plan.md`, `research.md`, `data-model.md`, `contracts/*`, `quickstart.md`

### Commit
Follow `spec-kit/references/auto-commit.md`:
- Scope: all plan artifacts for this feature
- Message: `"spec(phase-2): [feature] plan"`

### Done When
- [ ] All plan artifacts created (plan.md, research.md, data-model.md, contracts/*, quickstart.md)
- [ ] Bugfix mode: plan sections appended only (additive-only) — existing content preserved
- [ ] history.md entry appended
- [ ] Committed

## Completion
- Generated artifacts list
- Gate status (pass/fail with justifications)
- Propose: `spec-kit-tasks`

### Auto-Chaining (Bugfix Mode)
After plan → automatically route to `spec-kit-tasks` (no user choice).

## Common Pitfalls
1. **Over-engineering simple features**: Not every feature needs research, data-model, and contracts. Generate only what's needed for clarity.
2. **Ignoring constitution gates**: Gates are advisory but flagging violations helps the user understand trade-offs.
3. **Skipping bugfix Plan Ref**: In bugfix mode, always add a Plan Ref to bugs.md — it provides traceability.

## Prerequisite Enforcement
**BLOCKED** if: spec.md does not exist, or constitution.md does not exist.
