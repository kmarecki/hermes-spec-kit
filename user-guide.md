# Hermes Spec-Kit User Guide

Spec-driven development for Hermes Agent. Specifications drive code, not the other way around.

## Overview

Spec-kit is a structured, phase-based development workflow. Every feature starts with a specification, then progresses through planning, task breakdown, implementation (with TDD), testing, and close. The workflow has **three development modes**: forward specification, bugfix loop, and creative exploration.

## Installation

```bash
# From the hermes-spec-kit repository:
cd /path/to/hermes-spec-kit
./scripts/install.sh

# In a Hermes session, reload skills:
/reload-skills
```

This installs 14 skills and 14 templates to `~/.hermes/skills/`.

## Quick Start

```
User:  "Create a spec for user authentication with OAuth2"
Agent: Routes to spec-kit-specify, creates specs/001-user-auth/spec.md

User:  "Plan 001-user-auth"
Agent: Routes to spec-kit-plan, generates plan.md, research.md, data-model.md

User:  "Generate tasks for 001-user-auth"
Agent: Routes to spec-kit-tasks. Asks: "Generate test tasks (TDD) or skip tests?"

User:  "Implement 001-user-auth"
Agent: Commits all spec artifacts as a batch, then executes phase-level TDD

User:  "Test 001-user-auth"
Agent: Routes to spec-kit-test for manual bug tracking

User:  "bugfix 001-user-auth"
Agent: Routes through Plan → Tasks → Implement → verify → close

User:  "Close 001-user-auth"
Agent: Routes to spec-kit-summarize, generates close.md or summary
```

## Three Development Modes

### 1. Specify Mode (Default)

Forward phase progression. User decides when to advance between phases.

```
Constitution → Specify → Clarify (opt) → Plan → Tasks → Implement → Test → Close
```

All phases are manual except the bugfix inner loop and the mandatory close.

### 2. Bugfix Mode

When bugs are found during testing, the user says "bugfix [feature]" and the workflow routes through a fixed inner loop:

```
Test → [Clarify if needed] → Plan → Tasks → Implement → Test → Close
```

The inner loop (Plan → Tasks → Implement) chains automatically — no user prompts between steps. When all bugs are verified, the workflow prompts for Close.

### 3. Explore Mode

For high-uncertainty features, spawn N parallel subagents exploring different approaches:

```
Explore [feature] → Variant A, B, C → Compare → Pick winner → Close
```

Each variant runs on its own branch (`explore/NNN-feature-<variant>`) with its own spec/plan/tasks cycle. After completion, `spec-kit-compare` presents a comparison matrix and the user picks a winner.

## Phase Details

### Phase 0: Constitution (One-Time)

**Skill**: `spec-kit-constitution`
**Trigger**: "Create constitution"
**Artifact**: `specs/constitution.md`

Project-wide principles. Runs once per project. Constitution is always optional — all other phases warn but proceed without it.

### Phase 1: Specification

**Skill**: `spec-kit-specify`
**Trigger**: "Create a spec for [description]" or "Specify [feature]"
**Artifact**: `specs/NNN-name/spec.md`

Defines WHAT and WHY — no implementation details. Captures user scenarios, functional requirements (FR-###), success criteria, entities, and edge cases.

### Phase 1.5: Clarify (Optional)

**Skill**: `spec-kit-clarify`
**Trigger**: "Clarify [feature]"
**Artifacts**: `specs/NNN-name/clarify.md`, updated spec.md

Resolves ambiguities through structured Q&A (max 5 questions per session). Can be run multiple times.

### Phase 2: Plan

**Skill**: `spec-kit-plan`
**Trigger**: "Plan [feature]"
**Artifacts**: `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

Defines HOW: architecture, data model, API contracts, technology choices. Sub-phases (research, data-model, contracts) can be skipped for simple features.

### Phase 3: Tasks

**Skill**: `spec-kit-tasks`
**Trigger**: "Generate tasks for [feature]" or "Break down [feature]"
**Artifact**: `specs/NNN-name/tasks.md`

Generates an ordered task list. **The user is asked whether to use TDD** — if yes, test tasks are generated first (`[TEST]`), then implementation tasks. No mandatory 1:1 mapping between tests and tasks. If TDD is bypassed, the header `> **TDD**: Bypassed by user request` is added to tasks.md.

### Phase 3.5: Analyze (Optional)

**Skill**: Inline in workflow — no separate skill file
**Trigger**: "Analyze [feature]"

READ-ONLY consistency check across artifacts. Can run with just spec.md — more artifacts produce richer analysis. Checks: duplication, ambiguity, coverage gaps, constitution alignment, inconsistency.

### Phase 4: Implement

**Skill**: `spec-kit-implement`
**Trigger**: "Implement [feature]"
**Tasks**: Updated tasks.md with completion markers

The core of the workflow. Before any code is written, **all spec artifacts are committed as a single batch** (spec.md, plan.md, tasks.md, clarify.md, etc.) — this freezes the design. Then execution proceeds phase-by-phase:

```
Phase N:
  ══ RED sub-phase ══
  For each [TEST] task: write test → run to verify RED (expected failure)
  
  ══ GREEN sub-phase ══
  For each implementation task: write code
  Run phase-relevant tests → confirm GREEN
  Run build (if applicable)
  Commit: "feat: Phase N - [Name]"
```

**Key rules:**
- No commits during RED — write all tests first
- No per-task regression runs — only phase-relevant tests
- One commit per phase boundary

**After all phases — Regression Run:**
- Run FULL test suite (all existing tests)
- If any regressions: create ONE umbrella task `BF-REGRESSION-001`, fix all, commit once
- If all pass: ready for testing

**TDD bypass mode**: If the user opted out of TDD during task generation, the implement skill detects the header in tasks.md and runs implementation tasks directly without any test cycle.

### Phase 5: Test

**Skill**: `spec-kit-test`
**Trigger**: "Test [feature]"
**Artifact**: `specs/NNN-name/bugs.md`

Manual bug tracking. The user reports bugs in natural language; the agent formats them into structured entries (BUG-### with severity, description, reproduction steps). Bugs are NEVER fixed before being logged — the "bugfix [feature]" command starts the fix loop.

### Phase 6: Summarize / Close (Mandatory)

**Skill**: `spec-kit-summarize`
**Trigger**: "Summarize [feature]" or "Close [feature]"
**Artifacts**: `implementation-summary.md` or `close.md`

**Mandatory** before a feature can be marked complete. Two modes:
- **Full summary**: Deep gap analysis comparing code against spec/plan. Computes spec health score. Patches spec.md/plan.md for intentional deviations.
- **Lightweight close**: Quick health score, artifact state table, key decisions. For simple features.

The auto-trigger (after all bugs verified) asks the user which mode to use.

## Spec Health Score

Computed during Phase 6. Formula:

```
spec_health = (resolved + acknowledged) / total * 100
```

| Score | Meaning |
|-------|---------|
| 100% | Artifacts fully aligned with code |
| 80-99% | Minor gaps tracked — acceptable |
| 50-79% | Significant drift — run refresh before refactoring |
| <50% | Artifacts are misleading — refresh required |

## Artifact Lifecycle

```
Design Phase Iteration (no commits):
  Specify → Clarify → Plan → Tasks
  (User jumps freely between these. No git checkpoints.)

Phase Transition:
  Tasks → [user says "implement"]
         ↓
       Batch commit: "spec: [feature] spec artifacts (spec, plan, tasks)"
         ↓
       Implementation begins (Phase 4)
         ↓
       Per-phase commits during coding
         ↓
       Regression run + umbrella fix (if needed)
         ↓
       Manual testing → bugfix loop
         ↓
       Close/Summarize commit
```

## TDD Integration

- **Default**: TDD is active. The user is asked at task generation time.
- **Phase-level**: All tests for a phase are written and verified RED first, then all code is written GREEN. One commit per phase.
- **RED is expected**: Test failures during RED prove the test is valid. NOT a bug.
- **Iron Law**: NO production code without a failing test first. Exceptions require explicit user permission (prototypes, generated code, config).
- **Bypass**: User can opt out entirely. Tracked in tasks.md header, detected by implement and summarize.

## Templates

Installed to `~/.hermes/skills/spec-kit/templates/`:

| Template | Used By | Purpose |
|----------|---------|---------|
| constitution-template.md | Phase 0 | Project principles |
| spec-template.md | Phase 1 | Feature spec |
| plan-template.md | Phase 2 | Implementation plan |
| tasks-template.md | Phase 3 | Task breakdown |
| research-template.md | Phase 2 | Technical research |
| data-model-template.md | Phase 2 | Entity definitions |
| bugs-template.md | Phase 5 | Bug tracking |
| implementation-summary-template.md | Phase 6 | Full summary |
| close-template.md | Phase 6 | Lightweight close |
| checklist-template.md | Any | Quality checklists |
| comparison-template.md | Compare | Variant comparison |
| AGENTS-template.md | Project setup | Starting AGENTS.md |
| workflow-template.md | Phase transition | Log entries |
| gitignore-template.md | Project setup | .gitignore starter |

## References

Installed to `~/.hermes/skills/spec-kit/references/`:

| Reference | Content |
|-----------|---------|
| auto-commit.md | Standard commit pattern used across all skills |
| phase-guardrails.md | Permission matrix and phase detection |
| workflow-tracking.md | Transition log design |
| workflow-enforcement.md | Three-layer enforcement architecture |
| transition-design.md | Phase transition principles |
| skill-consistency.md | Cross-skill consistency checks |
| visual-bug-triage.md | Visual/layout bug diagnosis |
| bugfix-css-debugging.md | CSS debugging workflow |
| cluster-topology-validation.md | Cluster topology testing |

## Skill Reference

All 14 skills installed to `~/.hermes/skills/`:

| Skill | Phase | Purpose |
|-------|-------|---------|
| spec-kit-workflow | — | Orchestrator — routes requests |
| spec-kit-constitution | 0 | Project principles |
| spec-kit-specify | 1 | Feature spec |
| spec-kit-clarify | 1.5 | Resolve ambiguities |
| spec-kit-plan | 2 | Implementation plan |
| spec-kit-tasks | 3 | Task breakdown |
| spec-kit-analyze | 3.5 | Quality check (inline) |
| spec-kit-checklist | Any | Validation checklists |
| spec-kit-implement | 4 | Phase-level TDD execution |
| spec-kit-test | 5 | Bug tracking |
| spec-kit-summarize | 6 | Close/summary |
| spec-kit-refresh | — | Artifact alignment |
| spec-kit-explore | — | Parallel variants |
| spec-kit-compare | — | Variant comparison |

## Git Strategy

- **Design phases** (0-3): No individual commits. Iterate freely.
- **Batch commit** (start of Phase 4): `"spec: [feature] spec artifacts (spec, plan, tasks)"`
- **Implementation** (Phase 4): One commit per phase: `"feat: [feature] Phase N - [Name]"`
- **Regression fix**: `"fix: [feature] BF-REGRESSION-001 - fix regressions"`
- **Bugfix loop**: `"fix: [feature] BF-### - description"`
- **Close**: `"spec(phase-6): [feature] summary (health: N%)"`
- **Refresh**: `"spec(refresh): [feature] reconcile artifacts"`

## Anti-Patterns

- Do NOT block on checklists — they are advisory
- Do NOT fix bugs before logging them in bugs.md
- Do NOT set bugs to verified preemptively — only the user
- Do NOT commit during RED sub-phase — write all tests first
- Do NOT run full suite per-task — only phase-relevant tests
- Do NOT skip TDD without asking the user first
- Do NOT allow features to complete without Phase 6 (Close)
- Do NOT pollute AGENTS.md with workflow mechanics — keep in skills
