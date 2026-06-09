# Hermes Spec-Kit User Guide

Structured spec-driven development for Hermes Agent. Every feature starts with a specification and progresses through planning, task breakdown, TDD implementation, testing, and mandatory close.

## Installation

```bash
cd /path/to/hermes-spec-kit
./scripts/install.sh

# In a Hermes session:
/reload-skills
```

Installation is global — one install covers all projects and sessions.

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
Agent: Auto-chains Plan → Tasks → Implement → verify → mandatory close

User:  "Close 001-user-auth"
Agent: Routes to spec-kit-summarize, generates close.md or summary
```

---

## Workflow Phases

The workflow has 7 numbered phases plus 3 standalone skills. Each phase produces specific artifacts.

```
 Constitution (Phase 0 — one-time)
      ↓
   Specify (Phase 1) — what and why
      ↓
   Clarify (Phase 1.5 — optional) — resolve ambiguities
      ↓
   Plan (Phase 2) — architecture and design
      ↓
   Tasks (Phase 3) — breakdown into executable work
      ↓
   [Review — optional pre-implement gate] ← cross-artifact check
      ↓
   Implement (Phase 4) — TDD or bypass, phase-level commits
      ↓
   Test (Phase 5) — manual bug tracking in bugs.md
      ↓
   [Review — optional post-implement gate] ← code quality check
      ↓
   Close (Phase 6 — mandatory) — summary + health score
```

### Phase 0: Constitution
**Skill**: `spec-kit-constitution` · **Trigger**: "Create constitution" · **Artifact**: `specs/constitution.md`

Project-wide principles and MUST/SHOULD rules. Runs once per project. Always optional — all other phases warn but proceed without it.

### Phase 1: Specify
**Skill**: `spec-kit-specify` · **Trigger**: "Create a spec for [description]" · **Artifact**: `specs/NNN-name/spec.md`

Defines WHAT and WHY — no implementation details. The agent adopts a **curious detail-gatherer** persona, asking clarifying questions to extract requirements. Captures functional requirements (FR-###), success criteria, user scenarios, entities, and edge cases.

### Phase 1.5: Clarify
**Skill**: `spec-kit-clarify` · **Trigger**: "Clarify [feature]" · **Artifacts**: `clarify.md`, updated spec.md

Resolves ambiguities through structured Q&A. Same **curious detail-gatherer** persona as specify — probes edge cases, constraints, and unstated expectations. Max 5 questions per session. Can be run multiple times.

### Phase 2: Plan
**Skill**: `spec-kit-plan` · **Trigger**: "Plan [feature]" · **Artifacts**: `plan.md`, `research.md`, `data-model.md`, `contracts/*`, `quickstart.md`

Defines HOW: architecture, data model, API contracts, technology stack, constitutional gates. The agent adopts a **system architect + philosopher** persona — thinks deeply about tradeoffs, edge cases, failure modes, and scalability.

### Phase 3: Tasks
**Skill**: `spec-kit-tasks` · **Trigger**: "Generate tasks for [feature]" · **Artifact**: `tasks.md`

Breaks the design down into executable, ordered tasks. Same **system architect + philosopher** persona as planning — every requirement must become concrete work. The user is asked whether to use TDD (generate test tasks + implementation tasks) or bypass it. If TDD is active, `[TEST]` tasks come before implementation tasks within each phase.

### Phase 3.5: Review — Pre-Implement Gate (Optional)
**Skill**: `spec-kit-review` · **Trigger**: "Review [feature]" or "Quality check [feature]"

READ-ONLY cross-artifact consistency check. Verifies spec/plan/tasks are coherent before coding begins. The agent adopts a **thorough code auditor** persona and:

- Checks spec/plan/tasks coherence and coverage
- Detects duplication, ambiguity, underspecification
- Validates constitution alignment
- Checks naming conventions across artifacts
- Checks documentation completeness
- Scans user-defined checklists if they exist
- Can use web search to research best patterns

No files are modified — only a report is produced.

### Phase 4: Implement
**Skill**: `spec-kit-implement` · **Trigger**: "Implement [feature]" · **Artifact**: updated `tasks.md` with completion markers

The core of the workflow. The agent adopts a **disciplined engineer** persona — follows the plan exactly, no scope creep.

**Before any code is written**, all spec artifacts are committed as a single batch (spec.md, plan.md, tasks.md, etc.) — this freezes the design. Then execution proceeds **phase-level TDD**:

```
Phase N:
  ══ RED sub-phase ══
  For each [TEST] task: write test → run to verify RED (expected failure)
  
  ══ GREEN sub-phase ══
  For each implementation task: write code
  Run phase-relevant tests → confirm GREEN
  Run build (if applicable)
  Commit: "feat: [feature] Phase N - [Name]"
```

**Branch Guard**: Before any git operation, blocks if on `main`/`master` — you must be on a `feat/NNN-name` branch.

**After all phases — Regression Run**: Full test suite runs. Any regressions are captured in one umbrella fix task (BF-REGRESSION-001), fixed, and committed.

**TDD bypass**: If the user opted out during task generation, implementation runs directly without test tasks.

### Phase 5: Test
**Skill**: `spec-kit-test` · **Trigger**: "Test [feature]" · **Artifact**: `bugs.md`

Manual bug tracking. The agent adopts a **QA engineer** persona — primary deliverable is a detailed, structured bugs.md. Every bug must have: steps to reproduce, expected vs actual behavior, severity, and context. Vague bug reports are blocked.

**Safety lock**: Bugs are NEVER fixed before being logged. After logging, the user says "bugfix [feature]" to start the fix loop.

### Phase 5.5: Review — Post-Implement Gate (Optional)
**Skill**: `spec-kit-review` · **Trigger**: "Review [feature]" after code + tests

READ-ONLY code quality review. The same `spec-kit-review` skill auto-detects whether to run pre-implement or post-implement mode. Post-implement checks:

- Spec fulfillment (does code satisfy every FR-###?)
- Constitution alignment
- Architecture/design compliance with plan
- Naming conventions in code
- Documentation completeness (README, API docs, changelog)
- Code quality (error handling, duplication, complexity, security)
- Test quality
- User-defined custom gates from checklists/
- Can use web search to research best patterns and practices

### Phase 6: Close/Summarize — Mandatory
**Skill**: `spec-kit-summarize` · **Trigger**: "Close [feature]" or "Summarize [feature]" · **Artifact**: `close.md` or `implementation-summary.md`

**Mandatory** before a feature can be marked complete. The agent adopts a **thorough code auditor** persona — verifies every claim against real code, spec, plan, and git diff.

Two modes:
- **Full summary**: Deep gap analysis comparing code against spec/plan. Computes spec health score. Patches spec.md/plan.md for intentional deviations (with per-change user approval).
- **Lightweight close**: Quick health score, artifact state table, key decisions.

**Output rule**: Length and detail are proportional to actual git changes, not spec/task size. A one-line bugfix gets a one-line note; a multi-file feature gets thorough per-file coverage. Always precise, factual descriptions — no filler.

---

## Three Development Modes

### 1. Specify Mode (Default)

Forward feature development. User decides when to advance between phases.

```
Constitution → Specify → Clarify (opt) → Plan → Tasks → [Review] → Implement → Test → [Review] → Close
```

- Each forward phase is manual — the agent proposes but never auto-advances without consent
- Clarify and Review are optional
- User can jump back to any earlier phase at any time

### 2. Bugfix Mode

When bugs are discovered during testing. Once user says "bugfix [feature]", the inner loop chains automatically:

```
Test → [Clarify if needed] → Plan → Tasks → Implement → Test → [Review] → Close
```

- Plan → Tasks → Implement runs automatically (no intermediate prompts — the user committed to the fix path)
- Each bug must have a Plan Ref in bugs.md linking to a plan section. Missing Plan Refs block and route through Plan first.
- After all bugs verified → prompts for Close (does not auto-close)
- Close is mandatory before marking the feature complete

### 3. Explore Mode

For high-uncertainty features. Spawns parallel subagents, each on its own branch exploring a different approach:

```
User: "Explore 003-taskify with React, Vue, and Svelte"
  → 3 parallel subagents via delegate_task
  → Each on explore/003-taskify-<variant> branch
  → Each runs independent specify → plan → tasks → implement cycle
  → spec-kit-compare builds comparison matrix
  → User picks winner or cherry-picks from variants
```

---

## Spec Health Score

Computed during Phase 6 (Close). Measures how well spec/plan artifacts align with actual code.

```
spec_health = (resolved + acknowledged) / total * 100
```

| Score | Meaning | Action |
|-------|---------|--------|
| 100% | Fully aligned | No action needed |
| 80-99% | Minor gaps | Review at leisure |
| 50-79% | Significant drift | Run `refresh` before refactoring |
| <50% | Misleading artifacts | Run `refresh` before proceeding |

---

## Artifact Lifecycle

```
Design phases (no commits):
  Specify → Clarify → Plan → Tasks
  (User jumps freely. No git checkpoints.)

Phase transition (start of Implement):
  Batch commit: "spec: [feature] spec artifacts (...)"
       ↓
  Per-phase commits during implementation
       ↓
  Regression run + umbrella fix (if needed)
       ↓
  Manual testing → bugfix loop (per-bugfix commits)
       ↓
  Close/Summarize commit
```

---

## Branch Strategy

| Operation | Branch |
|-----------|--------|
| Feature work | `feat/NNN-feature-name` |
| Bugfix | `bug/NNN-bugfix-name` |
| Explore variants | `explore/NNN-feature-name-<variant>` |

The workflow blocks all git operations on `main`/`master`. Every skill that touches git has a branch guard check.

---

## Git Commit Messages

| Situation | Message |
|-----------|---------|
| Batch commit (start of Implement) | `spec: [feature] spec artifacts (spec, plan, tasks)` |
| Per-phase (Implement) | `feat: [feature] Phase N - [Name]` |
| Regression umbrella fix | `fix: [feature] BF-REGRESSION-001 - fix regressions` |
| Bugfix loop (per bug) | `fix: [feature] BF-### - description` |
| Close/Summary | `spec(phase-6): [feature] summary (health: N%)` |
| Refresh artifacts | `spec(refresh): [feature] reconcile artifacts` |

---

## TDD Integration

- **Default**: TDD is active. User is asked at task generation time.
- **Phase-level**: All tests for a phase written RED first, all code GREEN, one commit per phase.
- **RED is expected**: Test failures during RED prove the test is valid — NOT a bug.
- **Iron Law**: No production code without a failing test first. Exceptions require explicit user permission.
- **Bypass**: User can opt out entirely at task generation. Tracked in tasks.md header.

---

## Pre-Action Self-Check

Every skill includes a `## Pre-flight` section that references `spec-kit/references/preflight.md`. Before any action, the agent runs:

1. **Branch check** — not on `main`/`master`
2. **Mode detection** — if `bugs.md` has open entries, you're in bugfix mode
3. **Workflow load check** — must load `spec-kit-workflow` before writing code

---

## Standalone Skills

These don't belong to any numbered phase:

### refresh
**Trigger**: "Refresh [feature]" · **Skill**: `spec-kit-refresh`

Reconciles spec/plan artifacts with code that was changed outside the workflow (manual edits, refactoring, third-party changes). READ-ONLY on code — patches spec artifacts with per-change user approval.

### explore
**Trigger**: "Explore [feature] with [variants]" · **Skill**: `spec-kit-explore`

Spawns parallel subagents for creative exploration. Each variant runs its own independent specify→plan→tasks→implement cycle on a separate branch.

### compare
**Trigger**: "Compare [feature]" · **Skill**: `spec-kit-compare`

Loads all variant artifacts from `specs/[feature]/variants/` and builds a comparison matrix. The agent adopts a **thorough code auditor** persona, using web search to research best practices for each approach. User picks the winner or cherry-picks features.

---

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
| comparison-template.md | Compare | Variant comparison |
| AGENTS-template.md | Project setup | Starting AGENTS.md |
| workflow-template.md | Phase transition | Log entries |
| gitignore-template.md | Project setup | .gitignore starter |
| soul-template.md | Hermes setup | Neutral persona |

---

## References

Installed to `~/.hermes/skills/spec-kit/references/`:

| Reference | Content |
|-----------|---------|
| auto-commit.md | Standard commit pattern across all skills |
| preflight.md | Pre-action self-check rules (branch, mode, workflow) |

---

## Skill Reference

All 14 skills installed to `~/.hermes/skills/`:

| Skill | Phase | Purpose | Persona |
|-------|-------|---------|---------|
| spec-kit | — | Umbrella overview | — |
| spec-kit-workflow | — | Orchestrator — routes to correct phase | Workflow orchestrator |
| spec-kit-constitution | 0 | Project principles | Project founder |
| spec-kit-specify | 1 | Feature spec | Curious detail-gatherer |
| spec-kit-clarify | 1.5 | Resolve ambiguities | Curious detail-gatherer |
| spec-kit-plan | 2 | Technical plan | System architect + philosopher |
| spec-kit-tasks | 3 | Task breakdown | System architect + philosopher |
| spec-kit-review | 3.5 / 5.5 | Quality gate (pre- and post-implement) | Thorough code auditor |
| spec-kit-implement | 4 | TDD implementation | Disciplined engineer |
| spec-kit-test | 5 | Bug tracking | QA engineer |
| spec-kit-summarize | 6 | Close/summary | Thorough code auditor |
| spec-kit-refresh | — | Artifact reconciliation | Auditor |
| spec-kit-explore | — | Parallel variant exploration | Creative architect |
| spec-kit-compare | — | Variant comparison | Thorough code auditor |
