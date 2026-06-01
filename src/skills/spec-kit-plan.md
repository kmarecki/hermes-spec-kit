---
name: spec-kit-plan
description: Create technical implementation plan from feature specification. Phase 2 - defines HOW with constitutional gates.
category: software-development
---

# spec-kit-plan

**Phase**: 2

**Purpose**: Create or update the implementation plan at `specs/[feature]/plan.md`. Defines technical architecture, resolves constitutional gates, generates design artifacts.

**Prerequisites**: `spec-kit-constitution` + `spec-kit-specify` must be run first

**Artifacts**:
- `specs/[feature]/plan.md` (primary artifact)
- `specs/[feature]/research.md` (technical research)
- `specs/[feature]/data-model.md` (entity definitions)
- `specs/[feature]/quickstart.md` (validation scenarios)
- `specs/[feature]/contracts/` (API specifications)

## Execution

### Step 1: Validate prerequisites
```
IF .specify/memory/constitution.md NOT EXISTS:
  ERROR: "Run spec-kit-constitution first"
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first"
```

### Step 2: Load context
- LOAD `specs/[feature]/spec.md`
- LOAD `.specify/memory/constitution.md`
- LOAD `templates/plan.md`

### Step 3: Fill Technical Context
Document:
- Language/Version
- Primary Dependencies
- Storage (database, files)
- Testing framework
- Target Platform
- Project Type (library/cli/web-service/mobile-app)
- Performance Goals
- Constraints (latency, memory, offline)
- Scale/Scope

Mark unknowns as "NEEDS CLARIFICATION"

### Step 4: Constitutional Gates
Evaluate gates BEFORE proceeding:
- **Simplicity Gate** (Article VII): Using ≤3 projects? No future-proofing?
- **Anti-Abstraction Gate** (Article VIII): Using framework directly? Single model representation?
- **Integration-First Gate** (Article IX): Contracts defined? Contract tests written?

```
IF any gate FAILS without justification:
  BLOCK: "Constitutional gate violation — document justification or adjust design"
```

### Step 5: Phase 0 - Research
Generate `research.md`:
- For each NEEDS CLARIFICATION: research task
- For each technology choice: best practices
- For each dependency: patterns
- Format: Decision, Rationale, Alternatives Considered

### Step 6: Phase 1 - Design & Contracts
Generate `data-model.md`:
- Entity name, fields, relationships
- Validation rules
- State transitions

Generate `contracts/` directory:
- API specifications
- Command schemas
- Test scenarios

Generate `quickstart.md`:
- Key validation scenarios

### Step 7: Project structure
Choose from template:
- **Single project** (DEFAULT): `src/`, `tests/`
- **Web app**: `backend/`, `frontend/`
- **Mobile + API**: `api/`, `ios/` or `android/`

Document structure decision in plan.

### Step 8: Complexity tracking
If constitutional gates violated, document in plan:
| Violation | Why Needed | Simpler Alternative Rejected Because |

## Completion

Report:
- Plan path
- Generated artifacts (research.md, data-model.md, contracts/)
- Gate status (pass/fail with justifications)
- Suggest next command

## Next Skills

- Run `spec-kit-tasks` to create task breakdown
- Run `spec-kit-analyze` for optional quality gate before implementation

**Re-running this skill**:
1. LOAD existing plan, research, data-model
2. COMPARE against current spec
3. UPDATE only changed sections
4. PRESERVE research findings unless spec changed

## Prerequisite Enforcement

**BLOCKED** if:
- `spec-kit-constitution` has not been run
- `spec-kit-specify` has not been run

## Re-run Enforcement

After re-running `spec-kit-constitution`:
1. Re-validate gates against updated principles
2. Update plan if principles conflict

After re-running `spec-kit-specify`:
1. Re-validate architecture against updated requirements

After re-running `spec-kit-clarify`:
1. Re-evaluate technical decisions affected by clarifications

## Completion

Report:
- Plan path
- Generated artifacts (research.md, data-model.md, contracts/)
- Gate status (pass/fail with justifications)
- Suggest next command

## Next Skills

- Run `spec-kit-tasks` to create task breakdown
- Run `spec-kit-analyze` for optional quality gate before implementation