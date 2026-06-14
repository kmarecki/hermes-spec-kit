---
name: spec-kit-workflow
description: Load when the user says 'spec-kit bugfix [feature]', 'speckit bugfix [feature]', 'spec-kit fix [feature]', 'speckit fix [feature]', 'spec-kit reopen [feature]', 'speckit reopen [feature]', 'spec-kit implement [feature]', 'speckit implement [feature]', 'spec-kit plan [feature]', 'speckit plan [feature]', 'spec-kit close [feature]', 'speckit close [feature]', 'spec-kit specify [feature]', 'speckit specify [feature]', 'spec-kit status [feature]', 'speckit status [feature]', or any 'spec-kit ...' or 'speckit ...' workflow routing command. Also triggers on natural phrases: "fix bugs in [feature]", "bugfix [feature]", "bugfixing [feature]", "continue bugfixing", "reopen [feature]", "implement [feature]", "plan [feature]", "close [feature]", "create a spec", "specify [feature]", "what phase is [feature] in". Routes to the correct phase skill.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec-kit, workflow, orchestrator, routing]
    related_skills: [spec-kit-constitution, spec-kit-specify, spec-kit-clarify, spec-kit-plan, spec-kit-tasks, spec-kit-review, spec-kit-implement, spec-kit-test, spec-kit-summarize, spec-kit-refresh]
---

# Spec Kit Workflow Orchestrator

**Load this skill when the user says: "bugfix [feature]", "reopen [feature]", "implement [feature]", "plan [feature]", "specify [feature]", "close [feature]", "create a spec", or any phase-routing command.**

**Task Persona**: Adopt the mindset of a workflow orchestrator. Your job is routing, not execution. Check prerequisites, validate state, and dispatch to the correct phase skill. Guardrails are your responsibility — enforce them before passing control.

This skill does NOT execute phases itself. It routes requests to the correct phase skill based on artifact state and trigger phrases. If you loaded this skill because the user said "bugfix", read the "Bugfix Routing" section below — do NOT start with spec-kit-specify.

## Pre-flight: Project Readiness

Load and follow `spec-kit/references/preflight.md` before any routing action. Preflight handles branch guardrails (checks #1, #4), mode detection (#2), unlogged bug check (#3), git conventions (#4 renamed), workflow load check (#5), and history.md readiness (#6).

> **Note**: If you already have preflight loaded from a prior skill call, you do not need to reload it. Re-run checks #1 and #4 as a quick sanity check, then proceed directly to routing.

Additionally, for any command that references a specific feature:

```text
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
|| 3.5 | `spec-kit-review` | Quality gate (optional) | Tasks |
|| 4 | `spec-kit-implement` | Execute tasks | Tasks |
|| 5 | `spec-kit-test` | Testing & bug tracking | Implement (or spec for bugfix loop) |
|| **6** | **`spec-kit-summarize`** | **Implementation summary / close** | **Implement + Test** |
|| — | **`spec-kit-refresh`** | **Lightweight artifact refresh** | **Any (standalone)** |
|| — | **Bugfix loop** | Test → [Clarify] → Plan → Tasks → [Review] → Implement → Test → **Close** (bugs.md with open bugs) |
|| — | **Quickfix** | Trivial bugfix: Plan section + tasks entry + fix in one batch commit (user opt-in, docs still exist) | bugfix sub-round with explicit "quickfix [feature]" |

> **Important**: Phase 6 (Close/Summarize) is **mandatory** before a feature can enter Complete state. After the bugfix loop finishes (all bugs verified), the user is prompted to run Phase 6.

## Routing Logic

Each skill BLOCKS if prerequisites are not met:
- `spec-kit-constitution`: No prerequisites (phase 0)
- `spec-kit-specify`: Requires `constitution.md`
- `spec-kit-clarify`: Requires `spec.md`
- `spec-kit-plan`: Requires `spec.md` + `constitution.md`
- `spec-kit-tasks`: Requires `plan.md` + `spec.md`
- `spec-kit-review`: Requires `spec.md` (at minimum — richer analysis if plan.md/tasks.md also exist)
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

### Review (Optional — Pre-implement or Post-implement)
- User says: "Analyze [feature]", "Review [feature]", or "Quality check [feature]"
- When: Before implementation (cross-artifact consistency) OR after code + tests (code quality review)
- Propose routing to: `spec-kit-review`
- NOTE: This skill auto-detects whether to run pre-implement or post-implement mode based on available artifacts

### Implement
- User says: "Implement [feature]"
- Propose routing to: `spec-kit-implement`

### Reopen (Closed Feature Bugfix)
- User says: "Reopen [feature]" or "reopen [feature]"
- **Purpose**: Fix bugs in a previously closed feature. Routes through bugfix flow, then updates close.md.
- **Prerequisites**: `close.md` or `implementation-summary.md` must exist
- **Full reopen flow**: See `spec-kit-summarize` — the reopen routing and branch creation logic is defined there. This skill only validates prerequisites and dispatches.
- **Conflict rule**: If the new close assessment contradicts the original close (same requirement went from ✅ to ❌), prompt the user to resolve before proceeding.

### Summarize / Close (Phase 6 — Mandatory)
- User says: "Summarize [feature]" or "Implementation summary for [feature]"
- Route to: `spec-kit-summarize` (full mode)
- User says: "Close [feature]" or "Complete [feature]"
- Route to: `spec-kit-summarize` (lightweight close mode)

### Block: Feature cannot be done without Phase 6
```text
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
|| `close.md` + `bugs.md` with open bugs | **Reopened (bugfix in progress)** |
|| All tasks complete + all bugs verified + (implementation-summary.md or close.md) | **Complete** |

> **Drift detection**: When entering any phase for an existing feature that has `implementation-summary.md` or `close.md`, read its Spec State / Artifact State table. If any artifact is `⚠️ needs review` or `❌ outdated`, emit a warning: "Artifact drift detected — spec/plan may not reflect current code. Run 'refresh [feature]' to reconcile."

## Bugfix Routing

### Start bugfix loop
- User says: "bugfix [feature]" or "fix bugs in [feature]"
- LOAD `specs/[feature]/bugs.md`
- IF `specs/[feature]/close.md` or `specs/[feature]/implementation-summary.md` EXISTS:
    NOTE: "Feature [feature] was previously closed. Use 'reopen [feature]' to explicitly reopen it."
    SUGGEST: "Reopen creates a bugfix branch and auto-creates bugs.md if needed."
    ROUTE to: reopen flow
- **Plan Ref enforcement** — for each bug with Status: open or in-progress:
  - CHECK for a **Plan Ref** entry
  - IF any open bug lacks a Plan Ref:
    - REPORT: "BUG-NNN lacks a Plan Ref. A plan section must address this bug before implementation."
    - SUGGEST: Route through `spec-kit-plan` first
    - REQUIRE: User confirms before proceeding without Plan Refs
- FOR each bug with Status: open or in-progress:
  - IF Requires Clarification checkbox "yes" is checked: ROUTE to `spec-kit-clarify` first, then auto-chain to plan → tasks → implement
  - ELSE: ROUTE to `spec-kit-plan` directly
- AFTER plan → AUTOMATICALLY route to `spec-kit-tasks`
- AFTER tasks → AUTOMATICALLY route to `spec-kit-implement`
- DEFAULT route: `spec-kit-plan` → `spec-kit-tasks` → `spec-kit-implement` (automatic chain, no user choice)
- NOTE: Review is optional — only run if user explicitly asks for it
- **TDD during bugfix**: `spec-kit-implement` enforces RED→GREEN per bugfix task.

### New bugs discovered during a fix round
See `spec-kit-implement` ("New bugs discovered during fix" section) for the full rules on logging mid-round bugs and the bugfix vs quickfix mode choice. Key routing summary:

```text
IF the current bugfix round is still in progress (BF-### tasks not all verified):
  New bugs are logged by spec-kit-test — do NOT start a new round yet.
  The current round completes normally.

AFTER the current round completes and all original BF-### tasks are verified:
  IF bugs.md has NEW open bugs:
    User chooses: "bugfix [feature]" (full sequence) or "quickfix [feature]" (batched).
```

### Bugfix loop completion — user decides when to close
After all bugs in bugs.md have Status: verified:
```text
  SUGGEST: "All N bugs verified. Ready to close? Say 'close [feature]' to
            generate a close document, or 'add bug' to log more bugs."
  DO NOT auto-trigger close. The user decides when to advance.
  The close is MANDATORY before the feature can be marked complete.
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
- "reopen 003-user-auth" (for closed features)
- "Verify BUG-001 in 003-user-auth"
- "Bug status 003-user-auth"
- "Summarize 003-user-auth" (full summary)
- "Close 003-user-auth" (lightweight close)
- "Refresh 003-user-auth" (artifact alignment only)

## Phase Guardrails — STRICT

You MUST determine the current phase before any tool call. Each phase has strict limits:

| Phase | Allowed to Write | Code-Editing Tools | Detect By |
|-------|-----------------|-------------------|-----------|
| **Constitution** | `constitution.md` only | BLOCKED | `specs/constitution.md` exists, no `spec.md` |
| **Specify** | `spec.md` only | BLOCKED | `specs/NNN-name/spec.md` exists, no `plan.md` |
| **Clarify** | `clarify.md`, `spec.md` (amend) | BLOCKED | `clarify.md` exists |
| **Plan** | `plan.md`, `research.md`, `data-model.md`, `contracts/*`, `quickstart.md` | BLOCKED | `plan.md` exists, no `tasks.md` |
| **Tasks** | `tasks.md` only | BLOCKED | `tasks.md` exists, no completions |
| **Review** | `tasks.md` only (closed-review mode, user approval) | BLOCKED | User says "review", "analyze", or "quality check" |
| **Implement** | source code, `tasks.md` (completions), `bugs.md` (mark resolved) | ALLOWED | `tasks.md` with pending tasks |
| **Test** | `bugs.md` only | BLOCKED | `bugs.md` with open bugs |
| **Reopen** | `bugs.md` (create if missing), source code (fix loop) | ALLOWED (same as bugfix) | `close.md` exists, user says "reopen" |
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

```text
Pre-Work Self-Check addition:
  5. Am I starting a NEW feature or marking an existing one complete?
     IF yes → Does specs/[feature]/contain either implementation-summary.md or close.md?
       IF no → Is bugs.md all verified?
         IF yes → BLOCK: Phase 6 required. Run 'close [feature]' first.
         IF no → OK, feature not ready for close yet.
```
