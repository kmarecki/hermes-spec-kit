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

## Concrete Feature Walkthrough

Here's what a complete feature looks like on disk from start to finish:

```
specs/
  constitution.md                          # Project principles (Phase 0)
  001-user-auth/                           # Feature directory
    spec.md                                # Specification (Phase 1)
    clarify.md                             # Clarification log (Phase 1.5)
    plan.md                                # Implementation plan (Phase 2)
    research.md                            # Technical research (Phase 2)
    data-model.md                          # Entity definitions (Phase 2)
    contracts/                             # API contracts (Phase 2)
      auth-api.md
    quickstart.md                          # Integration guide (Phase 2)
    tasks.md                               # Task breakdown (Phase 3)
    checklists/                            # Quality checklists
      requirements.md
    bugs.md                                # Bug log (Phase 5)
    implementation-summary.md              # Close document (Phase 6)
    workflow.md                            # Transition log
  002-oauth-refresh/
    ...
```

### Example: tasks.md (TDD mode)

```markdown
# Tasks: 001-user-auth

## Phase 1: Setup
T001 [TEST] Write tests for auth middleware         — tests/auth/middleware_test.py
T002        Implement auth middleware                — src/auth/middleware.py

## Phase 2: Core
T003 [TEST] Write tests for login endpoint           — tests/auth/login_test.py
T004 [TEST] Write tests for token refresh            — tests/auth/refresh_test.py
T005 [TEST] Write tests for logout                   — tests/auth/logout_test.py
T006        Implement login endpoint                  — src/auth/login.py
T007        Implement token refresh                   — src/auth/refresh.py
T008        Implement logout                          — src/auth/logout.py

## Dependencies
- T002 depends on T001 (test first)
- T006-T008 depend on T003-T005 (all tests written before implementation)
- T006-T008 can run in parallel [P] (different files)
```

### Example: tasks.md (TDD bypassed)

```markdown
# Tasks: 001-user-auth

> **TDD**: Bypassed by user request — no test tasks generated.

## Phase 1: Setup
T001        Implement auth middleware                — src/auth/middleware.py

## Phase 2: Core
T002        Implement login endpoint                  — src/auth/login.py
T003        Implement token refresh                   — src/auth/refresh.py
T004        Implement logout                          — src/auth/logout.py
```

### Example: bugs.md entry

```markdown
### BUG-001: Token refresh returns 500 on expired refresh token

- **Severity**: critical
- **Area**: auth/token
- **Description**: When refresh token has been expired for >24h, the
  endpoint crashes with a KeyError instead of returning 401.
- **Steps to Reproduce**:
  1. Obtain a refresh token
  2. Wait 25 hours
  3. POST /auth/refresh with the expired token
- **Actual Result**: 500 Internal Server Error
- **Expected Result**: 401 Unauthorized with "token expired" message
- **Requires Clarification**: [ ] no / [x] yes
- **Plan Ref**: Bugfix: BUG-001 (in plan.md)
- **Status**: open
```

### Example: workflow.md (transition log)

```markdown
## 2026-06-08T10:00Z | Phase 1 → Specify → Complete
- **Skill**: spec-kit-specify
- **Artifacts**: specs/001-user-auth/spec.md
- **Notes**: OAuth2 with JWT tokens, 3 user stories

## 2026-06-08T11:30Z | Phase 3 → Tasks → Complete
- **Skill**: spec-kit-tasks
- **Artifacts**: specs/001-user-auth/tasks.md
- **Notes**: TDD active, 8 tasks generated

## 2026-06-08T12:00Z | Batch commit → Design frozen
- **Commit**: a1b2c3d4
- **Scope**: All spec artifacts for 001-user-auth

## 2026-06-08T14:00Z | Phase 4 → Implement → Phase 1
- **Commit**: e5f6g7h8
- **Notes**: Auth middleware + tests complete

## 2026-06-08T16:00Z | Phase 6 → Close → Complete
- **Commit**: i9j0k1l2
- **Spec Health**: 100%
```

## Three Development Modes

Spec-kit has three modes designed for different development situations. Each mode changes how phases relate to each other — whether they're manual, auto-chained, or parallel.

### 1. Specify Mode (Default)

Use this for normal forward feature development. The user decides when to advance between phases.

```
Constitution → Specify → Clarify (opt) → Plan → Tasks → Implement → Test → Close
```

**Phase advancement rules:**
- Each forward phase is **manual** — the user says "Plan [feature]", "Implement [feature]", etc.
- Clarify and Analyze are **optional** — skip when the feature is straightforward
- The agent proposes the next phase but never auto-advances without user consent
- The user can jump back to any earlier phase at any time (e.g., from Tasks back to Clarify)

**When to use:** Any well-understood feature where the requirements are clear enough to specify upfront.

### 2. Bugfix Mode

Use when bugs are discovered during testing. Once the user says "bugfix [feature]", the inner loop chains automatically:

```
Test → [Clarify if needed] → Plan → Tasks → Implement → Test → Close
```

**Auto-chain behavior:**
- After Plan completes → Tasks runs automatically (no prompt)
- After Tasks completes → Implement runs automatically (no prompt)
- The user committed to the fix path by invoking "bugfix" — no intermediate choices needed
- After all bugs verified → the workflow prompts for Close

**Plan Ref enforcement:**
Each bug must have a Plan Ref line in bugs.md that links to a plan section. If a bug lacks a Plan Ref, the workflow blocks and routes through Plan first. This prevents unplanned fixes from conflicting with the spec.

**When to use:** When automated tests or manual testing reveals regressions or incorrect behavior.

### 3. Explore Mode

Use for high-uncertainty features where the best approach isn't obvious. Spawns parallel subagents, each exploring a different approach:

```
User: "Explore 003-taskify with React, Vue, and Svelte frontends"
         ↓
   Spawn 3 subagents via delegate_task:
         ↓
  ┌── Variant A (React) ──┐
  │   branch: explore/003-taskify-react  │
  │   specs/003-taskify/variants/react/  │
  │   spec.md → plan.md → tasks.md       │
  └──────────────────────────────────────┘
  ┌── Variant B (Vue) ────┐
  │   branch: explore/003-taskify-vue   │
  │   specs/003-taskify/variants/vue/   │
  │   [independent cycle]               │
  └──────────────────────────────────────┘
  ┌── Variant C (Svelte) ─┐
  │   branch: explore/003-taskify-svelte │
  │   specs/003-taskify/variants/svelte/ │
  │   [independent cycle]               │
  └──────────────────────────────────────┘
         ↓
   Run spec-kit-compare:
   Compare matrix → Pick winner → Cherry-pick → Close
```

**Key details:**
- Each variant runs in its own `delegate_task` subagent with full tool access
- Each gets its own git branch (`explore/NNN-feature-<variant>`)
- All variants run in parallel (limited by `delegation.max_concurrent_children`)
- After completion, `spec-kit-compare` loads all variant artifacts and builds a comparison matrix
- The user can pick one winner or cherry-pick features from multiple variants
- Rejected variants remain in `variants/` for reference (can be deleted later)

**When to use:** Architectural decisions, technology choices, or when the user says "I'm not sure which approach is best."

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

Computed during Phase 6 (Close/Summarize). Measures how well spec/plan artifacts align with actual code.

### Formula

```
spec_health = (resolved + acknowledged) / total * 100
```

Where:
- **resolved** = requirements implemented as planned OR intentionally deviated with documented rationale (spec/plan auto-updated)
- **acknowledged** = requirements deferred with documented reason
- **not_done** = requirements missing without documented reason
- **total** = resolved + acknowledged + not_done

### Concrete Example

After implementing a login feature, the gap analysis finds:

| Requirement | Verdict | Reason |
|-------------|---------|--------|
| FR-001: User can log in with email/password | ✅ Resolved | Implemented as specified |
| FR-002: Rate limit to 5 attempts/min | ✅ Resolved | Implemented, but limit set to 10/min (intentional deviation, documented) |
| FR-003: Password reset email | ⚠️ Acknowledged | Deferred to phase 2 (scope cut) |
| FR-004: OAuth2 Google login | ❌ Not Done | Specified but not implemented (added to bugs.md) |

Calculation: `(2 resolved + 1 acknowledged) / 4 total * 100 = 75%`

### Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 100% | Artifacts fully aligned with code | No action needed |
| 80-99% | Minor gaps tracked — acceptable | Review at leisure |
| 50-79% | Significant drift | Run `refresh` before refactoring |
| <50% | Artifacts are misleading | Run `refresh` before proceeding |

### Usage

- **At feature close**: Written into `implementation-summary.md` or `close.md`
- **On future feature load**: Read from the last close/summary. If <80%, warns about drift
- **Drift detection**: Workflow reads the Artifact State table. If any artifact shows `⚠️ needs review` or `❌ outdated`, it suggests `refresh`

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

## Refresh Skill

When code has been changed outside the spec-kit workflow (manual edits, refactoring, or third-party changes), use `spec-kit-refresh` to reconcile spec/plan artifacts:

```
User:  "Refresh 001-user-auth"

Agent loads spec-kit-refresh and:
1. Compares spec.md and plan.md against actual code
2. Identifies discrepancies (spec says X, code does Y)
3. Presents each discrepancy with yes/no approval
4. Patches spec.md/plan.md per user's decisions
5. Commits: "spec(refresh): 001-user-auth reconcile artifacts"
```

**When to use refresh vs close:**

| Situation | Use |
|-----------|-----|
| Feature is complete, all bugs verified | `close` or `summarize` |
| Code changed outside workflow, mid-stream | `refresh` |
| Summary detected drift during close | `refresh` |
| Before starting a new feature on existing codebase | `refresh` |

## Troubleshooting

### "No specs/ directory found"

The project hasn't been initialized with spec-kit. Start with:
```
User: "Create a constitution for this project"
```
This creates `specs/constitution.md` and the `specs/` directory.

### "Feature [name] not found in specs/"

The feature directory doesn't exist. Check available features:
```
User: "What specs exist?"
```
Then create a new one or use the exact name from the listing.

### "This phase is BLOCKED — prerequisite missing"

Each phase skill checks for prerequisite artifacts. Common causes:
- Trying to Plan before Specifying: run `specify` first
- Trying to Implement without Tasks: run `tasks` first
- Workflow says "must close first": run `close [feature]` before starting a new feature

### "Commit says 'not a git repository'"

The auto-commit step runs `git rev-parse --git-dir` to detect git. If this fails:
```bash
git init
# Optionally: cp ~/.hermes/skills/spec-kit/templates/gitignore-template.md .gitignore
```
Then re-run the phase. Silently skipped commits don't lose data — artifacts are still written to disk.

### "Tests pass in Vitest but fail at runtime"

Vitest/Jest use esbuild to transpile TypeScript, which is more lenient than `tsc`. If tests pass but the production build fails, the issue is likely:
- Missing type annotation
- Invalid import path
- Incorrect generic constraint

Fix: Run `npm run build` or `tsc --noEmit` after GREEN. Build-after-GREEN is mandatory for TypeScript projects.

### "I accidentally skipped TDD during task generation"

If the user opted out of TDD but now wants tests:
1. Run `spec-kit-tasks` again
2. Say "yes" when asked about TDD
3. Regenerated tasks will have `[TEST]` markers
4. Run `spec-kit-implement` to execute the updated tasks

The old implementation tasks are preserved — new test tasks are added before them.

### "The agent is stuck in the bugfix loop"

The bugfix loop (Plan → Tasks → Implement) chains automatically. If you want to exit:
- Say "stop fixing" — this halts the loop
- Say "close [feature]" — this closes even with open bugs (marks them as acknowledged)
- Say "verify BUG-NNN" — if all bugs are verified, the loop naturally ends

### "Comparing files from explore mode variants"

Variant artifacts are in `specs/[feature]/variants/<variant>/`. To inspect manually:
```bash
ls specs/003-taskify/variants/
cat specs/003-taskify/variants/react/spec.md
```

### "Spec health score is low after close"

A low spec health score (below 80%) means spec artifacts have drifted from the actual code. This is normal for complex features where requirements changed during implementation. The score isn't a judgment — it's a signal:
- Use `refresh` before the next bugfix or feature that touches this area
- The close document documents every deviation with rationale
- ❌ Not Done items become bugs in bugs.md for future work

## Anti-Patterns
- Do NOT block on checklists — they are advisory
- Do NOT fix bugs before logging them in bugs.md
- Do NOT set bugs to verified preemptively — only the user
- Do NOT commit during RED sub-phase — write all tests first
- Do NOT run full suite per-task — only phase-relevant tests
- Do NOT skip TDD without asking the user first
- Do NOT allow features to complete without Phase 6 (Close)
- Do NOT pollute AGENTS.md with workflow mechanics — keep in skills
