# Workflow Phases

The spec-kit workflow is a linear sequence of phases. Each phase produces documented artifacts. All phase transitions are manual — the user decides when to advance.

## Phase Sequence

```
Constitution → Specify → Clarify → Plan → Tasks → Implement
```

### Phase 0: Constitution
**Skill**: `spec-kit-constitution`

Establishes project-wide principles, constraints, and quality gates. One constitution per project.

**Artifacts**: `specs/constitution.md`

### Phase 1: Specify
**Skill**: `spec-kit-specify`

Creates a feature specification from a user description. User story format with acceptance scenarios.

**Artifacts**: `specs/NNN-feature-name/spec.md`

### Phase 2: Clarify (Optional)
**Skill**: `spec-kit-clarify`

Resolves ambiguities found in the spec. Run as many times as needed.

**Artifacts**: `specs/NNN-feature-name/clarify.md`

### Phase 3: Plan
**Skill**: `spec-kit-plan`

Technical design: research findings, data models, API contracts, and implementation approach.

**Artifacts**:
- `specs/NNN-feature-name/research.md`
- `specs/NNN-feature-name/data-model.md`
- `specs/NNN-feature-name/plan.md`
- `specs/NNN-feature-name/contracts/`

### Phase 4: Tasks
**Skill**: `spec-kit-tasks`

Breakdown of implementation tasks organized by user story. TDD format — test tasks precede implementation tasks.

**Artifacts**: `specs/NNN-feature-name/tasks.md`

### Phase 5: Implement
**Skill**: `spec-kit-implement`

Execute tasks from tasks.md. Tests first, then implementation. Update tasks as completed.

**Artifacts**: Updated `tasks.md`, code changes

## Phase Properties

| Property | Description |
|---------|-------------|
| **Manual advancement** | User decides when to move to the next phase |
| **Checklists optional** | Quality checklists guide but do not block |
| **Idempotent** | Each phase skill can be re-run to update its artifact |
| **Non-blocking** | User can skip phases or go back to revise |

## Resuming Work

To resume a stalled feature:
1. Identify the current phase by checking which artifacts exist
2. Load the appropriate skill
3. Continue from where work stopped

## Skipping Phases

Any phase can be skipped if not needed:
- Small features may skip Clarify entirely
- Simple features may skip Plan and go straight from Spec to Tasks
- User judgment determines when phases add value vs. overhead