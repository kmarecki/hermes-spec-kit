---
name: spec-kit-workflow
description: Master orchestrator for the spec-driven development workflow. Routes requests to appropriate phase skills and maintains workflow state.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, workflow, orchestrator, routing]
    related_skills: [spec-kit-constitution, spec-kit-specify, spec-kit-clarify, spec-kit-plan, spec-kit-tasks, spec-kit-analyze, spec-kit-checklist, spec-kit-implement, spec-kit-test, spec-kit-summarize, spec-kit-refresh]
---

# Spec Kit Workflow Orchestrator

This is the master orchestrator that routes user requests to the appropriate phase skill.

## Pre-flight: Project Readiness

Before routing any feature-level command, check that the project is initialized:

```
IF user command targets specs/[feature]/ (any feature-level operation):
  IF specs/ directory NOT EXISTS:
    IF user said "Create a spec for..." or "Create constitution":
      ALLOW — command creates the specs/ directory
      PROCEED with routing
    ELSE:
      BLOCK: "No specs/ directory found. This project hasn't been initialized.
              Start with: 'Create a constitution for [project]' or 'Create a spec for [description]'
              to create the first specification."
      PROMPT: "Run 'spec-kit-constitution' first."
```

Additionally, for any command that references a specific feature:

```
IF feature name is provided (e.g., "003-user-auth"):
  IF specs/[feature]/ directory NOT EXISTS:
    BLOCK: "Feature [feature] not found in specs/. Available specs: [list directories]"
    SUGGEST: "Create it with 'Create a spec for [description]'"
```

## Workflow Phases (in order)

|| Phase | Skill | Purpose | Prerequisite |
||:------|:------|:--------|:-------------|
|| 0 | `spec-kit-constitution` | Project principles | None |
|| 1 | `spec-kit-specify` | Feature spec | Constitution |
|| 1.5 | `spec-kit-clarify` | Iterative clarification | Spec |
|| 2 | `spec-kit-plan` | Technical plan | Spec + Constitution |
|| 3 | `spec-kit-tasks` | Task breakdown | Plan |
|| 3.5 | `spec-kit-analyze` | Quality gate (optional) | Tasks |
|| 4 | `spec-kit-implement` | Execute tasks | Tasks |
|| 5 | `spec-kit-test` | Testing & bug tracking | Implement (or spec for bugfix loop) |
| **6** | **`spec-kit-summarize`** | **Implementation summary / close** | **Implement + Test** |
| — | **`spec-kit-refresh`** | **Lightweight artifact refresh** | **Any (standalone)** |
| — | **Explore mode** | Parallel branches for N variants, each runs independent phase sequence | User provides variants |
| — | **Bugfix loop** | Test → [Clarify] → Plan → Tasks → [Analyze] → Implement → Test → **Close** | bugs.md with open bugs |

> **Important**: Phase 6 (Close/Summarize) is **mandatory** before a feature can enter Complete state. After the bugfix loop finishes (all bugs verified), the workflow auto-chains to Phase 6.

## Routing Logic

Each skill BLOCKS if prerequisites are not met:
- `spec-kit-constitution`: No prerequisites (phase 0)
- `spec-kit-specify`: Requires `constitution.md`
- `spec-kit-clarify`: Requires `spec.md`
- `spec-kit-plan`: Requires `spec.md` + `constitution.md`
- `spec-kit-tasks`: Requires `plan.md` + `spec.md`
- `spec-kit-analyze`: Requires `tasks.md` + `plan.md` + `spec.md`
- `spec-kit-implement`: Requires `tasks.md`
- `spec-kit-test`: Requires `spec.md` (or existing implementation)
  Bugfix prerequisite: `bugs.md` with at least one open bug
- `spec-kit-summarize`: Requires `tasks.md`
- `spec-kit-refresh`: No prerequisites (standalone)

### New Feature
- User says: "Create a spec for [description]"
- Propose routing to: `spec-kit-specify`

### Existing Feature
- User says: "What phase is [feature] in?"
- Check `specs/[feature]/` directory structure
- **Drift detection**: If `implementation-summary.md` or `close.md` exists, check its Spec State table. If any artifact shows ⚠️ or ❌ status, warn: "Artifact drift detected — run 'refresh [feature]' before proceeding."
- Report current phase and propose next available action

### Advance Phase
- User says: "Plan [feature]"
- Propose routing to: `spec-kit-plan`

### Clarify Ambiguities (Optional)
- User says: "Clarify [feature]"
- When: Only if spec has ambiguities or user explicitly asks
- Propose routing to: `spec-kit-clarify`

### Constitution
- User says: "Create constitution"
- Propose routing to: `spec-kit-constitution`

### Analyze (Optional)
- User says: "Analyze [feature]" or "Quality check [feature]"
- When: Only if user explicitly asks for quality review before implementing
- Propose routing to: `spec-kit-analyze`

### Implement
- User says: "Implement [feature]"
- Propose routing to: `spec-kit-implement`

### Summarize / Close (Phase 6 — Mandatory)
- User says: "Summarize [feature]" or "Implementation summary for [feature]"
- Route to: `spec-kit-summarize` (full mode)
- User says: "Close [feature]" or "Complete [feature]"
- Route to: `spec-kit-summarize` (lightweight close mode)
- **Auto-trigger**: After bugfix loop completes (all bugs verified), auto-route to `spec-kit-summarize`

### Block: Feature cannot be done without Phase 6
```
WHEN user says "[feature] is done" or tries to start a new feature for the same project:
  IF implementation-summary.md or close.md does NOT exist:
    BLOCK: "Cannot mark [feature] complete — Phase 6 (Close/Summarize) is mandatory."
    PROMPT: "Run 'close [feature]' or 'summarize [feature]' first."
  ELSE:
    ALLOW: Feature is Complete
```

### Refresh Artifacts
- User says: "Refresh [feature]" or "Sync spec for [feature]" or "Align artifacts for [feature]"
- Route to: `spec-kit-refresh`
- When: Manual code changes, mid-stream alignment, or artifacts flagged as outdated
- Standalone — no prerequisites

### Creative Exploration
- User says: "Explore [feature] with [variants]" or "Creative exploration for [feature]"
- Route to: `spec-kit-explore`
- When: User wants to compare N different approaches in parallel
- After explore: Propose running `spec-kit-compare`

### Compare Variants
- User says: "Compare [feature]" or "Compare variants for [feature]"
- Route to: `spec-kit-compare`
- Prerequisites: `specs/[feature]/variants/` must exist with at least 2 variants

## Phase Detection

Check for artifacts to determine current phase:

|| Artifacts Present | Current Phase |
||:-----------------|:-------------|
|| `constitution.md` only | Ready to Specify |
|| `spec.md` exists | Specified |
|| `clarify.md` exists | Clarifying/Clarified |
|| `plan.md` exists | Planning/Planned |
|| `tasks.md` exists | Tasking/Tasked |
|| `tasks.md` with completions | Implementing |
|| `bugs.md` with open bugs | Testing (bugfix loop) |
|| `bugs.md` all verified | Testing complete — **must close** |
|| `implementation-summary.md` exists | Summarized — complete |
|| `close.md` exists | Closed — complete |
|| All tasks complete + all bugs verified + (implementation-summary.md or close.md) | **Complete** |
|| `variants/` directory exists with ≥2 entries | Exploring (creative mode) |
|| `comparison.md` exists | Compared — decision made |

> **Drift detection**: When entering any phase for an existing feature that has `implementation-summary.md` or `close.md`, read its Spec State / Artifact State table. If any artifact is `⚠️ needs review` or `❌ outdated`, emit a warning: "Artifact drift detected — spec/plan may not reflect current code. Run 'refresh [feature]' to reconcile."

## Bugfix Routing

### Start bugfix loop
- User says: "bugfix [feature]" or "fix bugs in [feature]"
- LOAD `specs/[feature]/bugs.md`
- **Plan Ref enforcement** — for each bug with Status: open or in-progress:
  - CHECK for a **Plan Ref** entry
  - IF any open bug lacks a Plan Ref:
    - REPORT: "BUG-NNN lacks a Plan Ref. A plan section must address this bug before implementation."
    - SUGGEST: Route through `spec-kit-plan` first (the plan skill will create the Plan Ref)
    - REQUIRE: User confirms before proceeding without Plan Refs
- FOR each bug with Status: open or in-progress:
  - IF Requires Clarification checkbox "yes" is checked: ROUTE to `spec-kit-clarify` first, then automatically chain to plan → tasks → implement
  - ELSE: ROUTE to `spec-kit-plan` directly
- AFTER plan → AUTOMATICALLY route to `spec-kit-tasks`
- AFTER tasks → AUTOMATICALLY route to `spec-kit-implement`
- DEFAULT route: `spec-kit-plan` → `spec-kit-tasks` → `spec-kit-implement` (automatic chain, no user choice)
- NOTE: Analyze is optional — only run if user explicitly asks for it

### Bugfix loop completion → Mandatory Close
```
AFTER all bugs in bugs.md have Status: verified:
  AUTO-TRIGGER: spec-kit-summarize (Phase 6)
    - If feature is simple (≤5 tasks): lightweight close mode
    - If feature is complex (>5 tasks or elaborate plan.md): full summary mode
  This is MANDATORY — the feature cannot be marked done without Phase 6.
```

### Test phase
- User says: "Test [feature]"
- Propose routing to: `spec-kit-test`
- NOTE: `spec-kit-test` logs bugs to `bugs.md` then STOPS. It does NOT auto-chain to implement. User must say "bugfix [feature]" to start the fix loop.

### Verify bug
- User says: "Verify [BUG-ID] in [feature]"
- Propose routing to: `spec-kit-test` (to mark bug as verified)

## Usage Examples

- "Create a spec for user authentication"
- "What phase is 003-user-auth in?"
- "Plan the implementation for 003-user-auth"
- "Clarify ambiguities in 003-user-auth"
- "Generate tasks for 003-user-auth"
- "Analyze 003-user-auth for issues"
- "Implement 003-user-auth"
- "Test 003-user-auth"
- "bugfix 003-user-auth"
- "Verify BUG-001 in 003-user-auth"
- "Bug status 003-user-auth"
- "Summarize 003-user-auth" (full summary)
- "Close 003-user-auth" (lightweight close)
- "Refresh 003-user-auth" (artifact alignment only)
- "Explore 003-user-auth with React, Vue, and Svelte frontends"
- "Compare 003-user-auth"

## Phase Guardrails — STRICT

You MUST determine the current phase before any tool call. Each phase has strict limits:

| Phase | Allowed to Write | Code-Editing Tools | Detect By |
|-------|-----------------|-------------------|-----------|
| **Constitution** | `constitution.md` only | BLOCKED | `specs/constitution.md` exists, no `spec.md` |
| **Specify** | `spec.md`, `checklists/requirements.md` | BLOCKED | `specs/NNN-name/spec.md` exists, no `plan.md` |
| **Clarify** | `clarify.md`, `spec.md` (amend) | BLOCKED | `clarify.md` exists |
| **Plan** | `plan.md`, `research.md`, `data-model.md`, `contracts/*`, `quickstart.md` | BLOCKED | `plan.md` exists, no `tasks.md` |
| **Tasks** | `tasks.md` only | BLOCKED | `tasks.md` exists, no completions |
| **Analyze** | None (read-only) | BLOCKED | User says "analyze" |
| **Implement** | source code, `tasks.md` (completions), `bugs.md` (mark resolved) | ALLOWED | `tasks.md` with pending tasks |
| **Test** | `bugs.md` only | BLOCKED | `bugs.md` with open bugs |
| **Explore** | `specs/[feature]/variants/*/` | ALLOWED (delegate_task subagents) | User provides variants |
| **Compare** | `comparison.md` only | BLOCKED | `variants/` directory exists |
| **Summarize / Close** | `implementation-summary.md`, `close.md`, `spec.md` (patch deviations), `plan.md` (patch deviations), `tasks.md` (finalize), `bugs.md` (finalize) | BLOCKED | `implementation-summary.md` and `close.md` both missing |
| **Refresh** | `spec.md`, `plan.md`, `data-model.md`, `contracts/*` (per-item approval) | BLOCKED | User says "refresh" |

> **Bugfix loop**: reuses Plan, Tasks, and Implement — same permissions, just with `bugs.md` as additional input context.
> **Summarize/Close** gains `spec.md` and `plan.md` write access to patch intentional deviations.
> **Refresh** is read-only on code but can update spec artifacts with per-item user approval.

### Enforcement Rules
- `write_file`/`patch`/`terminal` for builds → **ONLY** during Implement (including bugfix loop implementations)
- Writing to spec artifacts (`spec.md`, `plan.md`, `tasks.md`, `bugs.md`) → only during their respective phase
- **Summarize/Close exception**: May patch `spec.md` and `plan.md` to reconcile intentional deviations (with user approval per change)
- **Refresh exception**: May patch `spec.md`, `plan.md`, `data-model.md`, `contracts/*` with per-item user approval
- Unknown phase → ASK the user
- User asks for code outside Implement → REFUSE, suggest correct phase

### Mandatory Close Enforcement

```
Pre-Work Self-Check addition:
  5. Am I starting a NEW feature or marking an existing one complete?
     IF yes → Does specs/[feature]/contain either implementation-summary.md or close.md?
       IF no → Is bugs.md all verified?
         IF yes → BLOCK: Phase 6 required. Run 'close [feature]' first.
         IF no → OK, feature not ready for close yet.
```
