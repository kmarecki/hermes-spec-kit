# Workflow Phases

The spec-kit workflow is a linear sequence of phases. Each phase produces documented artifacts. All phase transitions are manual — the user decides when to advance.

### Phase 5: Implement
**Skill**: `spec-kit-implement`

Execute tasks from tasks.md. Tests first, then implementation. Update tasks as completed.

**Artifacts**: Updated `tasks.md`, code changes

### Phase 6: Test
**Skill**: `spec-kit-test`

Manual testing phase. User discovers bugs and logs them in `bugs.md`. Routes back through the bugfix loop.

**Artifacts**: `specs/NNN-feature-name/bugs.md`

#### Bugfix Loop

The Testing phase is iterative — it can run multiple times until the user is satisfied:

```
[Test] ──► [Clarify if needed] ──► [Plan] ──► [Tasks] ──► [Implement] ──► [Test again]
                                                      │
                                                      └── all automatic, no user choice
```

1. **Log bugs**: User adds bugs to `bugs.md` with severity, description, and clarification flag
2. **Route to Plan** (default): `spec-kit-plan` generates bugfix approach
3. **Route to Clarify** (per bug): If a bug needs clarification, `spec-kit-clarify` runs first, then automatically proceeds to plan
4. **Automatic chain**: After plan completes, bugfix tasks are generated automatically (no user prompt), then implementation runs automatically
5. **Optionally analyze**: User can request `spec-kit-analyze` explicitly, but it is NOT part of the automatic chain
6. **Implement**: `spec-kit-implement` executes bugfix tasks with TDD
7. **Re-test**: User tests again, marks bugs as verified, or discovers new bugs
8. **Repeat**: Loop continues until all bugs are verified and user is satisfied

> **Key rule**: Bugfix loop never stops to ask "tasks or implement" — plan → tasks → implement runs automatically.

## Phase Sequence

```
Constitution → Specify → Clarify → Plan → Tasks → Implement → Test → Summarize
                                                              │
                                                              └── bugfix loop ──┐
                                                        ┌──────────────────────┘
                                                        ▼
                                                  Clarify → Plan → Tasks → [Analyze] → Implement → Test
```

The workflow has two distinct paths:
- **Initial path** (forward): Constitution → Specify → Clarify → Plan → Tasks → Implement → Test → Summarize
- **Bugfix loop** (iterative): Test → [Clarify] → Plan → Tasks → [Analyze] → Implement → Test (repeat)

### Phase 7: Summarize
**Skill**: `spec-kit-summarize`

Reads all artifacts and generates `implementation-summary.md`. Updates tasks.md (marks all complete) and bugs.md (marks all verified). Provides a final snapshot of what was implemented, what changed, test results, and remaining open items.

**Artifacts**: `specs/NNN-feature-name/implementation-summary.md`

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
| **Bugfix loop** | Testing phase routes back to Plan (or Clarify) for iterative bugfix cycles |
| **Code-freeze guardrail** | Source code changes are only permitted during Implement and bugfix-implementation phases. All other phases are read-only for code. See Permission Matrix below. |

## Permission Matrix (Phase Guardrails)

You MUST determine the current phase before any tool call. Each phase has strict limits on what files and tools are allowed:

| Phase | Allowed to Write | Code-Editing Tools | Required Prerequisite Artifact |
|-------|-----------------|-------------------|-------------------------------|
| **Constitution** (0) | `constitution.md` only | **BLOCKED** | None |
| **Specify** (1) | `spec.md`, `checklists/requirements.md` | **BLOCKED** | `constitution.md` |
| **Clarify** (1.5) | `clarify.md`, `spec.md` (ammend) | **BLOCKED** | `spec.md` |
| **Plan** (2) | `plan.md`, `research.md`, `data-model.md`, `contracts/*` | **BLOCKED** | `spec.md` + `constitution.md` |
| **Tasks** (3) | `tasks.md` only | **BLOCKED** | `plan.md` |
| **Analyze** (3.5) | None (read-only report) | **BLOCKED** | `tasks.md` |
| **Implement** (4) | source code, `tasks.md` (completions) | **ALLOWED** | `tasks.md` |
| **Test** (5) | `bugs.md` only | **BLOCKED** | `spec.md` (or implementation) |
| **Summarize** (6) | `implementation-summary.md`, `tasks.md` (finalize), `bugs.md` (finalize) | **BLOCKED** | `tasks.md` |

> **Bugfix loop**: reuses Plan, Tasks, and Implement — same permissions, just with `bugs.md` as additional input context. No separate bugfix phases.

### Enforcement Rules
- `write_file`, `patch`, `terminal` (for compilation/builds) → **ONLY** during Implement (including bugfix loop implementations)
- Writing to spec artifacts (`spec.md`, `plan.md`, `tasks.md`, `bugs.md`) → only during their respective phase
- Reading files, searching, loading skills → allowed in all phases
- If you cannot determine the phase → ASK the user
- If the user asks for code changes outside Implement → politely refuse and suggest running the correct phase first

## Resuming Work

To resume a stalled feature:
1. Identify the current phase by checking which artifacts exist
2. If `bugs.md` exists with open bugs, you're in the Testing phase — run "bugfix [feature]" to continue
3. Load the appropriate skill
4. Continue from where work stopped

## Skipping Phases

Any phase can be skipped if not needed:
- Small features may skip Clarify entirely
- Simple features may skip Plan and go straight from Spec to Tasks
- User judgment determines when phases add value vs. overhead