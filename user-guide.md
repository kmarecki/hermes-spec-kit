# Hermes Spec-Kit: User Guide

Spec-driven development for Hermes Agent. Every feature starts with a
specification — not a line of code — and progresses through planning,
task breakdown, TDD implementation, testing, and a mandatory close phase.

Git conventions (branch naming, commit messages, merge behaviour) are
defined in `specs/git-conventions.md`. Copy the template from
`spec-kit/templates/git-conventions-template.md` and customise per
project.

This guide covers installation, the core workflow, the explore-and-compare
pattern for parallel variants, and day-to-day usage.

---

## Table of Contents

1.  [What is Spec-Kit?](#what-is-spec-kit)
2.  [Quick Start: Your First Feature](#quick-start-your-first-feature)
3.  [Three Development Modes](#three-development-modes)
4.  [Explore Mode: Parallel Variants (Deep Dive)](#explore-mode-parallel-variants-deep-dive)
    - [How Git Worktrees Keep Variants Apart](#how-git-worktrees-keep-variants-apart)
    - [Walkthrough: Explore → Compare → Promote](#walkthrough-explore--compare--promote)
5.  [Phase Reference](#phase-reference)
6.  [Branch Strategy](#branch-strategy)
7.  [Git Commit Conventions](#git-commit-conventions)
8.  [Spec Health Score](#spec-health-score)
9.  [Troubleshooting](#troubleshooting)
10. [Reference Tables](#reference-tables)

---

## What is Spec-Kit?

Spec-kit is a structured workflow for building features with an AI agent.
Instead of saying "build a login system" and hoping the agent gets it right,
you guide it through seven phases — from specification through close — with
checkpoints, guardrails, and review gates.

**Who is this for?**
- Developers who want AI-written code they can trust
- Anyone tired of agents that go off-track or leave incomplete features
- Teams that need audit trails and reproducible builds

**What problem does it solve?**
- Unconstrained agents produce wrong, incomplete, or hard-to-maintain code
- Without a spec, the agent doesn't know what "done" looks like
- Without phases, the agent skips planning and jumps straight to coding
- Without close, features accumulate half-finished

**What tools does it add?**
- 14 spec-kit skills in `~/.hermes/skills/`
- Templates in `~/.hermes/skills/spec-kit/templates/`
- A `specs/` directory in your project for feature artifacts

---

## Quick Start: Your First Feature

This walkthrough builds a simple user authentication feature from scratch.
Follow along in a real project to see how the workflow works.

### Before you begin

```bash
# Install spec-kit
cd /path/to/hermes-spec-kit
./scripts/install.sh

# In your project
mkdir specs/
git checkout -b feat/001-user-auth
```

### Step 1: Create the spec

```
hermes -s spec-kit-workflow

You: "Create a spec for user authentication with email and OAuth2"

Agent: Asks clarifying questions:
  - "What fields on the user model?"
  - "Password requirements?"
  - "OAuth2 providers?"
  - "Session expiry?"

You: Answer each one. The agent writes specs/001-user-auth/spec.md
```

The spec document captures functional requirements (`FR-001`), success
criteria, user scenarios, entities, and edge cases. No code yet.

### Step 2: Plan the architecture

```
You: "Plan 001-user-auth"

Agent: Generates plan.md, data-model.md, research.md
  - Database schema for users table
  - Auth flow (login, register, token refresh, logout)
  - API routes and contracts
  - Security considerations (password hashing, rate limiting)
```

### Step 3: Break down into tasks

```
You: "Generate tasks for 001-user-auth"

Agent: "Use TDD (write tests first)? [yes/no]"
You: "yes"

Agent: Generates tasks.md with phases:
  Phase 1: User model and database
  Phase 2: Registration and password hashing
  Phase 3: Login and JWT tokens
  Phase 4: OAuth2 integration
  Phase 5: Session management
  Each phase has [TEST] tasks before implementation tasks.
```

### Step 4: Implement phase by phase

```
You: "Implement 001-user-auth"

Agent:
  - Batch-commits spec/plan/tasks to freeze the design
  - Phase 1: Writes user model tests (RED) → implements (GREEN) → commits
  - Phase 2: Registration tests → code → commit
  - ... continues through all phases
  - Full regression run → fixes any breakage → umbrella commit
```

### Step 5: Test and log bugs

```
You: "Test 001-user-auth"

Agent: Runs tests, exercises the API, logs any bugs to bugs.md
  BUG-001: OAuth2 callback missing state parameter (severity: major)
  BUG-002: Password reset token expires too early (severity: minor)
```

### Step 6: Fix bugs

```
You: "bugfix 001-user-auth"

Agent: Auto-chains:
  Plan → Tasks → Implement → Test → prompts for Close
  Each fix gets a commit:
    fix: BF-001 - add state parameter to OAuth2 callback
    fix: BF-002 - extend password reset TTL to 1 hour
```

### Step 7: Close the feature

```
You: "Close 001-user-auth"

Agent: Generates close.md with spec health score
  Calculation: which FRs are fulfilled, which were deferred
  Health: 94% — minor gap (rate limiting deferred to separate feature)
  Patches spec.md to document the intentional deviation
  Commits: spec(phase-6): 001-user-auth summary (health: 94%)
```

Feature is complete. 30 minutes of interaction, fully traceable from spec
to closing commit.

---

## Three Development Modes

Spec-kit has three modes, each suited to a different level of uncertainty:

| Mode | When to use | How it runs | User involvement |
|------|-------------|-------------|-----------------|
| **Specify** (default) | You know what you want — low uncertainty | One linear path, user advances phase-by-phase | Manual — you say "plan", "implement", etc. |
| **Bugfix** | You have a working feature with known bugs | Auto-chains Plan→Tasks→Implement→Test once you say "bugfix" | Minimal — inner loop is automatic |
| **Explore** | You're unsure about the approach — high uncertainty | Spawns parallel agents, each trying a different approach on an isolated branch | Hands-off after launch; you compare results later |

### Specify Mode (Default)

```text
Constitution → Specify → Clarify (opt) → Plan → Tasks → [Review] → Implement → Test → [Review] → Close
```

- Each forward step is manual — the agent proposes but never advances without consent
- Clarify and Review are optional
- You can jump back to any earlier phase at any time
- Best for: features where the requirements are clear

### Bugfix Mode

```text
Test → [Clarify if needed] → Plan → Tasks → Implement → Test → Close
```

- Once you say "bugfix [feature]", the inner loop chains automatically
- No intermediate prompts — you committed to the fix path
- Each bug must have a plan section reference (Plan Ref)
- After all bugs verified → you're prompted for Close
- Close is mandatory before marking the feature complete
- Best for: fixing known issues in an existing implementation

### Explore Mode (Detailed Below)

```text
User says "explore [feature] with [variants]"
  → Parallel subagents, each in its own git worktree
  → Each runs independent specify → plan → tasks → implement
  → User says "compare [feature]" → comparison matrix
  → User picks winner → code promoted to main feature branch
```

- Best for: high-uncertainty features where you want to compare approaches

---

## Explore Mode: Parallel Variants (Deep Dive)

Explore mode is for features where you don't know the best approach upfront.
Instead of guessing, you try several approaches in parallel and compare the
results.

**Example scenario**: You're building a real-time collaborative editor.
Should it use Operational Transformation (OT), Conflict-Free Replicated
Data Types (CRDTs), or a simpler lock-based approach? You're not sure.
Explore mode tries all three.

### How Git Worktrees Keep Variants Apart

Each variant needs its own working directory so agents don't step on each
other's files. **Git worktrees** make this possible.

A git worktree is a separate directory that shares the same `.git` database
but has its own:
- Working tree (files on disk)
- Index (staging area)
- HEAD (checked-out branch)

```text
Your .git database (shared)
  │
  ├── ~/projects/editor/                   [feat/023-collab]
  │    (main worktree — normal hermes session)
  │
  ├── ~/projects/editor-worktrees/explore-ot/
  │    [explore/023-collab-ot]
  │    (worktree — Agent A works here)
  │
  ├── ~/projects/editor-worktrees/explore-crdt/
  │    [explore/023-collab-crdt]
  │    (worktree — Agent B works here)
  │
  └── ~/projects/editor-worktrees/explore-locks/
       [explore/023-collab-locks]
       (worktree — Agent C works here)
```

**Key properties:**
- Each worktree can have a **different branch checked out simultaneously**
- Files in one worktree are **invisible** to the others — no cross-contamination
- Commits are **shared** — a commit in worktree A is visible everywhere
- `git log` in any worktree sees all commits from all worktrees
- Worktrees live in `../<repo>-worktrees/` (sibling to your project root)
- Add `**/worktrees/` to `.gitignore` so they're never committed

**Compared to alternatives:**

| Approach | Contamination | Git history | Disk space | Setup |
|----------|---------------|-------------|------------|-------|
| Same folder, switch branches | ✗ Files change under agent's feet | Shared | Minimal | Manual |
| Separate clones | ✓ Fully isolated | N × full history | High | Manual |
| Git worktrees | ✓ Fully isolated | Shared (single .git) | Minimal (no history copy) | One command |
| Variant subdirectories in same branch | ✗ Agents modify same files | Shared branch | Minimal | Manual |

Git worktrees give you the isolation of separate clones with the storage
efficiency of shared history. This is the recommended approach.

### Walkthrough: Explore → Compare → Promote

Let's walk through a real explore session end-to-end.

#### Step 1: Launch explore

```
hermes -s spec-kit-workflow

You: "Explore 023-collab with OT, CRDT, and lock-based approaches"

Agent:
  - Creates specs/023-collab/variants/{ot,crdt,locks}/
  - Creates 3 git worktrees:
    git worktree add ../editor-worktrees/explore-ot     explore/023-collab-ot
    git worktree add ../editor-worktrees/explore-crdt   explore/023-collab-crdt
    git worktree add ../editor-worktrees/explore-locks  explore/023-collab-locks
  - Runs a quick smoke test in each worktree (npm install, etc.)
  - Spawns 3 delegate_task subagents
```

#### Step 2: Subagents work in parallel

Each subagent receives its own worktree path and branch, plus a copy of
the shared spec. They work simultaneously, completely independently.

```text
Subagent A (OT):
  cd ../editor-worktrees/explore-ot
  git checkout explore/023-collab-ot
  Creates specs/023-collab/variants/ot/spec.md
  Creates specs/023-collab/variants/ot/plan.md
  ... implements OT-based sync ...

Subagent B (CRDT):
  cd ../editor-worktrees/explore-crdt
  git checkout explore/023-collab-crdt
  Creates specs/023-collab/variants/crdt/spec.md
  Creates specs/023-collab/variants/crdt/plan.md
  ... implements CRDT-based sync ...

Subagent C (Locks):
  cd ../editor-worktrees/explore-locks
  git checkout explore/023-collab-locks
  Creates specs/023-collab/variants/locks/spec.md
  ... implements lock-based sync ...
```

**Spec artifacts** (spec.md, plan.md, tasks.md) for each variant are
written back to the main repo under `specs/023-collab/variants/<name>/`.
This keeps all compare-able documents in one place.

**Source code** stays in the worktree directory — separate from other
variants' code. When compare runs, it reads both the spec artifacts
and the source code from each worktree.

#### Step 3: Compare the results

After all three finish (typically 5-15 minutes):

```
You: "Compare 023-collab"

Agent:
  - Loads all 3 variant artifacts from specs/023-collab/variants/
  - Loads source code from each worktree
  - Builds comparison matrix:
```

| Dimension | OT | CRDT | Locks |
|-----------|----|------|-------|
| **Approach** | Operational transform | Conflict-free data types | Mutual exclusion |
| **Latency** | Low (server-mediated) | High (P2P consensus) | Very high (sequential) |
| **Conflict resolution** | Centralized server decides | Automatic via LWW registers | Blocking — no conflicts |
| **Offline support** | None — requires server | Full — local edits sync later | None |
| **Implementation effort** | ~800 lines | ~2,000 lines | ~400 lines |
| **Test coverage** | 12 tests | 28 tests | 6 tests |
| **Risk** | Ordering edge cases | Merge explosion under load | Deadlocks |

```
Recommendation: CRDT for offline-first use case, OT for real-time.
      (User priority is offline support → CRDT wins.)

You: "Pick CRDT"
```

#### Step 4: Promote the winning variant

After picking a winner, the agent merges the variant's code into the main
feature branch:

```
Agent: "Choose promotion method: full merge or selective cherry-pick?"

You: "Full merge"

Agent:
  git checkout feat/023-collab
  git merge explore/023-collab-crdt --no-ff
  → feat: 023-collab merge winning variant crdt

  - Copies specs/023-collab/variants/crdt/* → specs/023-collab/
  - Appends to workflow.md: compare → promote record
  - Cleans up worktrees:
    git worktree remove ../editor-worktrees/explore-ot
    git worktree remove ../editor-worktrees/explore-crdt
    git worktree remove ../editor-worktrees/explore-locks
    git worktree prune
```

The feature is now on `feat/023-collab` with the CRDT implementation.
Proceed normally with test → bugfix → close.

#### Cherry-picking (alternative)

If you want specific parts from multiple variants instead of one winner:

```
Agent: "Which features do you want from each variant?"
You:  "Take CRDT merge logic, but use OT's network layer"

Agent:
  - Finds commit range for CRDT merge on explore/023-collab-crdt
  - Finds commit range for OT network layer on explore/023-collab-ot
  - git cherry-pick <crdt-merge-commits>
  - git cherry-pick <ot-network-commits>
  - Resolves any conflicts
  - Updates spec/plan/tasks to reflect the combined approach
  - commit: feat: 023-collab cherry-pick CRDT merge + OT network
```

**Cherry-pick risk**: If the OT network layer depends on OT-specific data
structures, cherry-picking it onto CRDT code may break. Prefer full merge
from a single variant unless you're certain the cherry-picked commits are
self-contained.

#### Without code implementation (design-only explore)

Sometimes you only want to compare plans, not full implementations.
If variants are design-only (spec/plan/tasks, no code), worktrees aren't
needed — each variant lives in `specs/[feature]/variants/<name>/` only.
The agent skips the worktree creation when it detects no implementation
will be produced.

---

## Phase Reference

### Phase 0: Constitution
**Skill**: `spec-kit-constitution` · **Trigger**: "Create constitution"
· **Artifact**: `specs/constitution.md`

Project-wide principles and MUST/SHOULD rules. Runs once per project.
Always optional — all other phases warn but proceed without it.

### Phase 1: Specify
**Skill**: `spec-kit-specify` · **Trigger**: "Create a spec for [description]"
· **Artifact**: `specs/NNN-name/spec.md`

Defines WHAT and WHY — no implementation details. The agent adopts a
**curious detail-gatherer** persona, asking clarifying questions to
extract requirements. Captures functional requirements (FR-###), success
criteria, user scenarios, entities, and edge cases.

### Phase 1.5: Clarify (Optional)
**Skill**: `spec-kit-clarify` · **Trigger**: "Clarify [feature]"
· **Artifacts**: `clarify.md`, updated spec.md

Resolves ambiguities through structured Q&A. Max 5 questions per session.
Can run multiple times. Same **curious detail-gatherer** persona.

### Phase 2: Plan
**Skill**: `spec-kit-plan` · **Trigger**: "Plan [feature]"
· **Artifacts**: `plan.md`, `research.md`, `data-model.md`, `contracts/*`

Defines HOW: architecture, data model, API contracts, technology stack,
constitutional gates. The agent adopts a **system architect + philosopher**
persona — thinks about tradeoffs, edge cases, failure modes, and
scalability. May use web search to research libraries or patterns.

### Phase 3: Tasks
**Skill**: `spec-kit-tasks` · **Trigger**: "Generate tasks for [feature]"
· **Artifact**: `tasks.md`

Breaks the design into executable, ordered tasks. Same **system architect +
philosopher** persona. The user is asked whether to use TDD (generate test
tasks + implementation tasks) or bypass it. If TDD is active, `[TEST]`
tasks come before implementation tasks within each phase.

### Phase 3.5: Review — Pre-Implement Gate (Optional)
**Skill**: `spec-kit-review` · **Trigger**: "Review [feature]" or
"Quality check [feature]"

READ-ONLY cross-artifact consistency check. Verifies spec/plan/tasks are
coherent before coding begins. The **thorough code auditor** persona checks:

- Spec/plan/tasks coherence and requirement coverage
- Duplication, ambiguity, underspecification
- Constitution alignment
- Naming conventions and documentation completeness
- User-defined checklists

No files are modified — only a report is produced.

### Phase 4: Implement
**Skill**: `spec-kit-implement` · **Trigger**: "Implement [feature]"
· **Artifact**: updated `tasks.md` with completion markers

The core of the workflow. The agent adopts a **disciplined engineer**
persona — follows the plan exactly, no scope creep.

**Flow:**
1. Batch-commit all spec artifacts (freezes the design)
2. For each phase: write tests (RED) → write code (GREEN) → commit
3. Full regression suite at the end
4. Any regressions captured in BF-REGRESSION-001 umbrella task

**TDD bypass**: If you opted out during task generation, implementation
runs directly without test tasks.

### Phase 5: Test
**Skill**: `spec-kit-test` · **Trigger**: "Test [feature]"
· **Artifact**: `bugs.md`

Manual bug tracking. The **QA engineer** persona's primary deliverable is
a detailed, structured bugs.md. Every bug must have: steps to reproduce,
expected vs actual behavior, severity, and context. Vague bug reports are
blocked.

**Safety lock**: Bugs are NEVER fixed before being logged. After logging,
say "bugfix [feature]" to start the fix loop.

### Phase 5.5: Review — Post-Implement Gate (Optional)
**Skill**: `spec-kit-review` · **Trigger**: "Review [feature]" after
code + tests

Same skill as pre-implement, auto-detects mode. Post-implement checks:
- Spec fulfillment (does code satisfy every FR-###?)
- Constitution alignment
- Architecture compliance with plan
- Code quality (error handling, duplication, security)
- Test quality
- Documentation completeness

### Phase 6: Close/Summarize — Mandatory
**Skill**: `spec-kit-summarize` · **Trigger**: "Close [feature]" or
"Summarize [feature]" · **Artifact**: `close.md` or
`implementation-summary.md`

**Mandatory** before a feature can be marked complete. The **thorough code
auditor** persona verifies every claim against real code, spec, plan, and
git diff.

Two modes:
- **Full summary**: Deep gap analysis comparing code against spec/plan.
  Computes spec health score. Patches spec.md/plan.md for intentional
  deviations (with per-change user approval).
- **Lightweight close**: Quick health score, artifact state table, key
  decisions.

**Output rule**: Length proportional to actual git changes, not spec size.
A one-line bugfix gets one line; a multi-file feature gets thorough
per-file coverage.

---

## Branch Strategy

| Operation | Branch name | Created by |
|-----------|-------------|------------|
| Feature work | `feat/NNN-feature-name` | User (before first skill call) |
| Bugfix | `bug/NNN-bugfix-name` | User (before saying "bugfix") |
| Explore variant | `explore/NNN-feature-<variant>` | Explore skill (automatically) |

**Always on a feature branch.** The workflow blocks all git operations on
`main`/`master`. If you try to start work on main, the agent will refuse
and prompt you to create the correct branch.

**Bugfix branches**: Bugfix work happens on whatever branch the feature was
implemented on — you don't create a separate branch for individual bugfix
loop iterations.

**Explore branches**: Created automatically by the explore skill when it
creates worktrees. Branch naming convention: `explore/NNN-feature-<variant>`.

---

## Git Commit Conventions

| Situation | Commit message |
|-----------|---------------|
| Batch commit (start of Implement) | `spec: [feature] spec artifacts (spec, plan, tasks)` |
| Per phase (Implement) | `feat: [feature] Phase N - [Name]` |
| Regression umbrella fix | `fix: [feature] BF-REGRESSION-001 - fix regressions` |
| Bugfix loop (per bug) | `fix: [feature] BF-### - description` |
| Explore variant promotion | `feat: [feature] merge winning variant [name]` |
| Explore cherry-pick | `feat: [feature] cherry-pick [features] from [variant]` |
| Close/Summary | `spec(phase-6): [feature] summary (health: N%)` |
| Refresh artifacts | `spec(refresh): [feature] reconcile artifacts` |

Every commit message is traceable back to the spec number and feature name.
This lets you query git for the full lifecycle of any feature:

```bash
# All commits related to a feature
git log --oneline --grep="001-user-auth" --all

# All bugfixes for a feature
git log --oneline --grep="BF-" --all

# When the spec artifacts were frozen (just before implement started)
git log --oneline --grep="spec artifacts" --all
```

---

## Spec Health Score

Computed during Phase 6 (Close). Measures how well spec/plan artifacts
align with actual code.

```
spec_health = (resolved + acknowledged) / total * 100
```

- **resolved**: Requirements implemented as planned OR intentionally
  deviated with documented rationale
- **acknowledged**: Requirements deferred with documented reason
- **not_done**: Requirements missing without documented reason

| Score | Meaning | Action |
|-------|---------|--------|
| 100% | Fully aligned | No action needed |
| 80-99% | Minor gaps | Review at leisure |
| 50-79% | Significant drift | Run `refresh` before refactoring |
| <50% | Misleading artifacts | Run `refresh` before proceeding |

When you load an existing feature with a close document, the agent checks
the last recorded health score. If it's below 80%, you'll get a warning
about artifact drift.

---

## Troubleshooting

### "Skills not found" or "spec-kit-workflow not available"

```bash
# Verify installation
hermes skills list | grep spec-kit

# Reload skills in current session
/reload-skills

# Start a new session with explicit skill loading
hermes -s spec-kit-workflow
```

### "Cannot work on feature while on main branch"

You're on `main`/`master`. The workflow blocks git operations there.

```bash
git checkout -b feat/001-user-auth
git push -u origin feat/001-user-auth
```

Then retry your command.

### Git worktree conflicts during explore

```bash
# "fatal: 'explore/023-collab-ot' already exists"
git branch -D explore/023-collab-ot
git worktree prune
# Then re-run explore
```

### Merge conflicts during variant promotion

If both the main branch and the winning variant touched the same files,
`git merge` will produce conflicts. This is expected — step through each
conflict marker, resolve, then:

```bash
git add <resolved-files>
git merge --continue
```

### "No open bugs but no close document"

If all bugs are verified but the feature has no close.md or
implementation-summary.md, the feature is not complete:

```
Say: "close [feature]"
```

This generates a close document with health score and marks the feature
as done.

### Cherry-picked code doesn't compile

Cherry-picked commits may depend on intermediate commits you skipped.
Check for missing dependencies:

```bash
# See what the variant branch has that the main branch doesn't
git log feat/NNN-name..explore/NNN-feature-<variant> --oneline

# If the needed dependency is a single commit, cherry-pick it too
git cherry-pick <dependency-commit>
```

When in doubt, prefer full merge over cherry-pick.

### Worktrees left behind after explore

After promotion, clean up:

```bash
git worktree remove ../<repo>-worktrees/explore-<variant>
git worktree prune
```

Leftover worktrees don't break anything but cause warnings on git
operations and consume disk space.

### Subagent didn't produce any output

Subagents run asynchronously via `delegate_task`. If one fails silently:

```
Agent: "Variant B completed in 30s with 0 commits"
Cause: The subagent may have crashed or couldn't resolve dependencies
Fix:   Re-run explore for just that variant, or check the worktree directory
```

---

## Reference Tables

### All Skills

| Skill | Phase | Purpose | Persona |
|-------|-------|---------|---------|
| `spec-kit` | — | Umbrella overview | — |
| `spec-kit-workflow` | — | Routes requests to correct phase | Workflow orchestrator |
| `spec-kit-constitution` | 0 | Project principles | Project founder |
| `spec-kit-specify` | 1 | Feature specification | Curious detail-gatherer |
| `spec-kit-clarify` | 1.5 | Resolve ambiguities | Curious detail-gatherer |
| `spec-kit-plan` | 2 | Technical plan | System architect + philosopher |
| `spec-kit-tasks` | 3 | Task breakdown | System architect + philosopher |
| `spec-kit-review` | 3.5 / 5.5 | Quality gate (pre/post) | Thorough code auditor |
| `spec-kit-implement` | 4 | TDD implementation | Disciplined engineer |
| `spec-kit-test` | 5 | Bug tracking | QA engineer |
| `spec-kit-summarize` | 6 | Close/summary | Thorough code auditor |
| `spec-kit-refresh` | — | Artifact reconciliation | Auditor |
| `spec-kit-explore` | — | Parallel variant exploration | Creative architect |
| `spec-kit-compare` | — | Variant comparison | Thorough code auditor |

### Templates

Installed to `~/.hermes/skills/spec-kit/templates/`:

| Template | Used by | Purpose |
|----------|---------|---------|
| constitution-template.md | Phase 0 | Project principles |
| spec-template.md | Phase 1 | Feature specification |
| plan-template.md | Phase 2 | Implementation plan |
| tasks-template.md | Phase 3 | Task breakdown |
| research-template.md | Phase 2 | Technical research |
| data-model-template.md | Phase 2 | Entity definitions |
| bugs-template.md | Phase 5 | Bug tracking |
| implementation-summary-template.md | Phase 6 | Full summary |
| close-template.md | Phase 6 | Lightweight close |
| comparison-template.md | Compare | Variant comparison matrix |
| workflow-template.md | Phase transitions | Append-only log entries |
| gitignore-template.md | Project setup | .gitignore starter |
| AGENTS-template.md | Project setup | Starting AGENTS.md |
| soul-template.md | Hermes setup | Neutral persona |

### Artifact Detection (Phase Detection)

| Artifacts present | Current phase |
|-------------------|---------------|
| `specs/constitution.md` only | Ready to Specify |
| `specs/NNN-name/spec.md` | Specified |
| `clarify.md` exists | Clarifying/Clarified |
| `plan.md` exists | Planning/Planned |
| `tasks.md` exists | Tasking/Tasked |
| `tasks.md` with completion markers | Implementing |
| `bugs.md` with open bugs | Testing (bugfix loop) |
| `bugs.md` all verified | Ready to Close |
| `implementation-summary.md` or `close.md` exists | Complete |
| `variants/` directory with ≥2 entries | Exploring |
| `comparison.md` exists | Compared — decision made |
| `workflow.md` last entry | Current phase (fastest lookup) |

### Quick CLI Reference

```bash
# Start a session with spec-kit preloaded
hermes -s spec-kit-workflow

# Start in isolated git worktree (for manual parallel variants)
hermes -w -s spec-kit-workflow

# Reload skills after installation
/reload-skills

# Load a specific skill mid-session
/skill spec-kit-compare

# Check installed skills
hermes skills list | grep spec-kit
```

### Workflow Diagram

```text
                                            ┌── Explore ───────────────┐
                                            │   git worktree add …     │
                                            │   delegate_task × N      │
                                            ▼                          │
Constitution → Specify → Clarify (opt) → Plan → Tasks → Implement → Test
                                                                      │
                                    ┌─────────────────────────────────┘
                                    ▼
                              [Clarify] → Plan → Tasks → Implement → Test → Close (mandatory)
                                                                              
                              Optional gates:
                                [Review] ← pre-implement (before code)
                                [Review] ← post-implement (after tests)
```
