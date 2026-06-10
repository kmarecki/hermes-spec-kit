---
name: spec-kit-workflow
description: Load when the user says 'spec-kit bugfix [feature]', 'speckit bugfix [feature]', 'spec-kit fix [feature]', 'speckit fix [feature]', 'spec-kit reopen [feature]', 'speckit reopen [feature]', 'spec-kit implement [feature]', 'speckit implement [feature]', 'spec-kit plan [feature]', 'speckit plan [feature]', 'spec-kit close [feature]', 'speckit close [feature]', 'spec-kit specify [feature]', 'speckit specify [feature]', 'spec-kit status [feature]', 'speckit status [feature]', or any 'spec-kit ...' or 'speckit ...' workflow routing command. Also triggers on natural phrases: "fix bugs in [feature]", "bugfix [feature]", "reopen [feature]", "implement [feature]", "plan [feature]", "close [feature]", "create a spec", "specify [feature]", "what phase is [feature] in". Routes to the correct phase skill.
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

Before routing any feature-level command, check that the project is initialized AND the branch is correct:

### Branch Guard — STRICT

Every feature, bugfix, or explore session MUST start on a branch named according to the project's git conventions. This prevents commits landing on blocked branches.

```
BEFORE any route action (specify, plan, tasks, implement, bugfix, explore, close):
  LOAD specs/git-conventions.md — read feature_prefix, bugfix_prefix, explore_prefix,
    reopen_suffix, branch_source, and blocked_branches. (Preflight step 3 already does this.)

  EXTRACT feature name from the user's command (e.g., "003-user-auth")

  IF feature has a spec number prefix (NNN-):
    DETECT current branch: $(git rev-parse --abbrev-ref HEAD)

    CLASSIFY the operation and construct expected branch from conventions:
      bugfix → expected branch: {bugfix_prefix}/NNN-{short-name}
      reopen → expected branch: {original_prefix}/NNN-{short-name}{reopen_suffix} (from closed feature)
      explore → expected branch: {explore_prefix}/NNN-feature-name-<variant>
      default (specify/plan/tasks/implement/close) → expected branch: {feature_prefix}/NNN-feature-name

    IF current branch is in blocked_branches (from conventions):
      IF operation == reopen:
        DETECT original prefix from close.md or git log
        SET reopen_branch = "${prefix}/${NNN}-${short_name}${reopen_suffix}"
        IF git branch --list "${reopen_branch}":
          PROMPT: "git checkout ${reopen_branch}  (reusing existing branch)"
        ELSE:
          PROMPT: "git checkout -b ${reopen_branch} ${branch_source} && git push -u origin ${reopen_branch}"
      ELSE:
        BLOCK: "Cannot work on feature [feature] while on [branch] branch."
        PROMPT: "Run these commands to create the feature branch:
          git checkout -b {feature_prefix}/NNN-feature-name
          git push -u origin {feature_prefix}/NNN-feature-name"

    IF current branch != expected branch AND current branch NOT in blocked_branches:
      WARN: "Currently on '[current]'. Expected branch is '[expected]'.
             Proceed anyway? If not, abort and switch branches."

  IF feature has NO spec number prefix:
    NOTE: "Feature name has no NNN- prefix — cannot enforce branch naming.
           Run spec-kit-specify first to create a numbered spec."
    SUGGEST: "Create spec first, then continue."

  IF NOT in a git repository:
    NOTE: "Not a git repository — branch guardrail skipped."
```

```
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
|| 3.5 | `spec-kit-review` | Quality gate (optional) | Tasks |
|| 4 | `spec-kit-implement` | Execute tasks | Tasks |
|| 5 | `spec-kit-test` | Testing & bug tracking | Implement (or spec for bugfix loop) |
| **6** | **`spec-kit-summarize`** | **Implementation summary / close** | **Implement + Test** |
| — | **`spec-kit-refresh`** | **Lightweight artifact refresh** | **Any (standalone)** |
| — | **Explore mode** | Parallel branches for N variants, each runs independent phase sequence | User provides variants |
| — | **Bugfix loop** | Test → [Clarify] → Plan → Tasks → [Review] → Implement → Test → **Close** | bugs.md with open bugs |

> **Important**: Phase 6 (Close/Summarize) is **mandatory** before a feature can enter Complete state. After the bugfix loop finishes (all bugs verified), the workflow auto-chains to Phase 6.

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
- **Purpose**: Fix bugs in a feature that was previously closed. Routes through bugfix flow, then regenerates close.md.
- **Prerequisites**: `close.md` or `implementation-summary.md` must exist

**Reopen flow:**
```
1. VALIDATE: close.md or implementation-summary.md EXISTS
   IF not: "Feature [feature] is not closed — nothing to reopen.
            Use 'bugfix [feature]' if bugs are already logged."

2. DETECT original branch prefix from close.md header or git log
   CONSTRUCT reopen_branch = {original_prefix}/NNN-{short-name}{reopen_suffix}
     (reopen_suffix from specs/git-conventions.md, default: -bugfixing)

3. BRANCH:
   IF on a blocked branch (from specs/git-conventions.md blocked_branches):
     CREATE reopen_branch from branch_source (from conventions, default: main)
   IF reopen_branch already exists:
     CHECKOUT and reuse

4. BUGS:
   IF bugs.md NOT FOUND:
     CREATE bugs.md from spec-kit/templates/bugs-template.md
     NOTE: "bugs.md created. Describe the bugs you're reopening for."
     ROUTE to: spec-kit-test (let user log bugs)
   IF bugs.md EXISTS (all verified):
     NOTE: "Existing bugs.md found with N verified bugs.
            Add new bugs, then the fix loop will start."
     ROUTE to: spec-kit-test (let user log new bugs)
   IF bugs.md EXISTS (open bugs):
     PROCEED to bugfix flow

5. ROUTE: spec-kit-plan → spec-kit-tasks → spec-kit-implement (auto-chain)

   **IMPORTANT — Additive-only rule for reopen:**
   - All edits to bugs.md, plan.md, and tasks.md during reopen must be **additive only**
   - Never remove or overwrite existing content — only append new sections, bugs, or tasks
   - If new content conflicts with existing content (same bug ID, same task ID, conflicting spec change):
     STOP and ask the user how to resolve before proceeding
   - Existing verified bugs, completed tasks, and original plan sections must be preserved exactly

6. WORKFLOW LOG:
   APPEND to specs/[feature]/history.md following spec-kit/references/history-tracking.md:
   - **Phase**: Reopen
   - **Notes**: "Feature reopened from closed state. Previous close.md will become stale — must close again after fixes."

7. AFTER fixes:
   User says "close [feature]" → updates close.md with new health score section
   (appends a new close entry with the updated health, preserving the original close data)
   NOTE: Previous health score loaded and compared.
   
   **Conflict rule for close update:**
   If the new close assessment contradicts the original close (e.g., same requirement
   went from ✅ Resolved to ❌ Not Done):
     PROMPT user: "Requirement FR-XXX was ✅ Resolved in the original close but
                   is now ❌ Not Done. How should I reflect this?
                   1. Mark as new ❌ Not Done (additive — original close preserved)
                   2. Override the status (update the entry)
                   3. Flag as ⚠️ Acknowledged instead"
```

> **Important**: Reopen is for bugfixes on already-closed features. If the feature never went through close, use "bugfix [feature]" instead. If no bugs are logged yet, reopen auto-creates bugs.md — unlike bugfix mode which expects bugs.md to already exist.

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
|| `close.md` + `bugs.md` with open bugs | **Reopened (bugfix in progress)** |
|| All tasks complete + all bugs verified + (implementation-summary.md or close.md) | **Complete** |
|| `variants/` directory exists with ≥2 entries | Exploring (creative mode) |
|| `comparison.md` exists | Compared — decision made |

> **Drift detection**: When entering any phase for an existing feature that has `implementation-summary.md` or `close.md`, read its Spec State / Artifact State table. If any artifact is `⚠️ needs review` or `❌ outdated`, emit a warning: "Artifact drift detected — spec/plan may not reflect current code. Run 'refresh [feature]' to reconcile."

## Bugfix Routing

### Start bugfix loop
- User says: "bugfix [feature]" or "fix bugs in [feature]"
- LOAD `specs/[feature]/bugs.md`
- IF `specs/[feature]/close.md` or `specs/[feature]/implementation-summary.md` EXISTS:
    NOTE: "Feature [feature] was previously closed. Use 'reopen [feature]' to explicitly reopen it."
    SUGGEST: "Reopen creates a bugfix branch from the project's branch_source (from conventions) and auto-creates bugs.md if needed."
    ROUTE to: reopen flow (user said 'reopen [feature]' to continue)
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
- NOTE: Review is optional — only run if user explicitly asks for it

### Bugfix loop completion — user decides when to close
```
AFTER all bugs in bugs.md have Status: verified:
  NOTE: Check for BF-REGRESSION tasks in tasks.md — these are auto-created
        regression fixes from Step 8 of implement. They are NOT user bugs
        and do NOT need manual verification.
  
  SUGGEST: "All N bugs verified. Ready to close? Say 'close [feature]' to
            generate a close document, or 'add bug' to log more bugs."
  
  DO NOT auto-trigger close. The user decides when to advance.
  
  The close is MANDATORY before the feature can be marked complete —
  enforced at the Block section below, not automatically here.
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
- "Explore 003-user-auth with React, Vue, and Svelte frontends"
- "Compare 003-user-auth"

## Phase Guardrails — STRICT

You MUST determine the current phase before any tool call. Each phase has strict limits:

| Phase | Allowed to Write | Code-Editing Tools | Detect By |
|-------|-----------------|-------------------|-----------|
| **Constitution** | `constitution.md` only | BLOCKED | `specs/constitution.md` exists, no `spec.md` |
| **Specify** | `spec.md` only | BLOCKED | `specs/NNN-name/spec.md` exists, no `plan.md` |
| **Clarify** | `clarify.md`, `spec.md` (amend) | BLOCKED | `clarify.md` exists |
| **Plan** | `plan.md`, `research.md`, `data-model.md`, `contracts/*`, `quickstart.md` | BLOCKED | `plan.md` exists, no `tasks.md` |
| **Tasks** | `tasks.md` only | BLOCKED | `tasks.md` exists, no completions |
| **Review** | None (read-only) | BLOCKED | User says "review", "analyze", or "quality check" |
| **Implement** | source code, `tasks.md` (completions), `bugs.md` (mark resolved) | ALLOWED | `tasks.md` with pending tasks |
| **Test** | `bugs.md` only | BLOCKED | `bugs.md` with open bugs |
| **Reopen** | `bugs.md` (create if missing), source code (fix loop) | ALLOWED (same as bugfix) | `close.md` exists, user says "reopen" |
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
