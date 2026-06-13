# Hermes Spec-Kit: User Guide

Spec-driven development for Hermes Agent. Every feature starts with a
specification — not a line of code — and progresses through planning,
task breakdown, TDD implementation, testing, and a mandatory close phase.
Four development modes span the full feature lifecycle: forward development
(specify), bugfix loop, parallel exploration, and reopen for closed features.

Git conventions (branch naming, commit messages, merge behaviour) are
defined in `specs/git-conventions.md`. Copy the template from
`spec-kit/templates/git-conventions-template.md` and customise per
project.

This guide covers installation, the core workflow, the explore-and-compare
pattern for parallel variants, the reopen flow for closed features, and
day-to-day usage.

---

## Table of Contents

1.  [What is Spec-Kit?](#what-is-spec-kit)
2.  [Quick Start: Your First Feature](#quick-start-your-first-feature)
3.  [Four Development Modes](#four-development-modes)
4.  [Constitution Decision Tree](#constitution-decision-tree)
    - [Level 1: Purpose (9 options)](#level-1-purpose-9-options)
    - [Level 2: Architecture (25 options)](#level-2-architecture-25-options-across-9-purposes)
    - [Level 3: Technology Choices](#level-3-technology-choices)
    - [Purpose-to-Principle Defaults](#after-level-3-purpose-to-principle-defaults)
    - [Monorepo Mode](#monorepo-mode)
    - [Free-Text Mode](#free-text-mode-description--constitution)
    - [Brownfield Shortcut](#brownfield-shortcut)
5.  [Explore Mode: Parallel Variants (Deep Dive)](#explore-mode-parallel-variants-deep-dive)
    - [How Git Worktrees Keep Variants Apart](#how-git-worktrees-keep-variants-apart)
    - [Walkthrough: Explore → Compare → Promote](#walkthrough-explore--compare--promote)
6.  [Reopen Mode: Fixing Closed Features](#reopen-mode-fixing-closed-features)
7.  [Phase Reference](#phase-reference)
8.  [Branch Strategy](#branch-strategy)
9.  [Git Commit Conventions](#git-commit-conventions)
10. [Spec Health Score](#spec-health-score)
11. [Troubleshooting](#troubleshooting)
12. [Reference Tables](#reference-tables)

---

## What is Spec-Kit?

Spec-kit is a structured workflow for building features with an AI agent.
Instead of saying "build a login system" and hoping the agent gets it right,
you guide it through seven phases — from specification through close — with
checkpoints, guardrails, and review gates. Four modes cover the full feature
lifecycle: forward development (specify), bugfix loop, parallel exploration,
and reopen for closed features.

The constitution phase (Phase 0) adapts to how you work: describe your
project in a sentence (free-text mode), walk through an interactive wizard
(guided mode), or let the agent auto-detect from existing code (brownfield
mode).

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
- 15 spec-kit skills in `~/.hermes/skills/` — respond to `spec-kit` prefix, `speckit` prefix,
  and natural language phrases
  (e.g. `"speckit plan 001-user-auth"`, `"spec-kit plan 001-user-auth"`, or
  `"plan the implementation for 001-user-auth"` all trigger the same skill)
- Templates in `~/.hermes/skills/spec-kit/templates/`
- Reference files in `~/.hermes/skills/spec-kit/references/` (preflight checks, auto-commit patterns, history tracking)
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
  - Each design phase already committed individually (no batch)
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

```text
You: "bugfix 001-user-auth"

Agent: Auto-chains:
  Plan → Tasks → Implement → Test → prompts for Close
  Each fix gets a commit:
    fix: BF-001 - add state parameter to OAuth2 callback
    fix: BF-002 - extend password reset TTL to 1 hour

**If new bugs are discovered during a fix round**:
  They're logged in bugs.md separately, not fixed inline.
  After the current round completes, you have two choices:

  1. "bugfix 001-user-auth" — FULL phase sequence with separate
     commits at each phase:
       spec(phase-2): 001-user-auth bugfix plan (BUG-003)
       spec(phase-3): 001-user-auth bugfix tasks (BUG-003)
       fix: BF-003 - apply the fix

  2. "quickfix 001-user-auth" — BATCHED for trivial fixes
     (config typos, obvious one-liners). Plan section + tasks
     entry + fix in one commit:
       fix: BF-003 - description (plan+tasks+fix)
     Plan ref and task entry still exist — only commit
     granularity is reduced. User explicitly opts in.
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

## Four Development Modes

Spec-kit has four modes, each suited to a different level of uncertainty:

| Mode | When to use | How it runs | User involvement |
|------|-------------|-------------|-----------------|
| **Specify** (default) | You know what you want — low uncertainty | Starts with constitution decision tree (9 purposes × 25 architecture options). Then a linear forward phase sequence: Specify → Clarify (opt) → Plan → Tasks → [Review] → Implement → Test → [Review] → Close | Manual — you say "plan", "implement", etc. |
| **Bugfix** | You have a working feature with known bugs | Auto-chains Plan→Tasks→Implement→Test once you say "bugfix". If new bugs are discovered mid-round, they're logged separately and the next round runs the full plan→tasks→implement cycle (separate commits per phase). For trivial fixes, "quickfix [feature]" batches plan+tasks+fix in one commit (user explicitly opts in). | Minimal — inner loop is automatic |
| **Explore** | You're unsure about the approach — high uncertainty | Spawns parallel agents, each trying a different approach on an isolated branch | Hands-off after launch; you compare results later |
| **Reopen** | A closed feature needs more fixes | Creates bugfix branch from main, preserves original close data, routes through bugfix loop | Additive-only edits; must close again after fixes |

Phase sequence for each mode:

| Mode | Sequence |
|------|----------|
| **Specify** | `Constitution → Specify → Clarify (opt) → Plan → Tasks → [Review] → Implement → Test → [Review] → Close` |
| **Bugfix** | `Test → [Clarify if needed] → Plan → Tasks → Implement → Test → Close` |
| **Explore** | Deep dive below → |
| **Reopen** | Deep dive below → |

Explore and Reopen have full walkthroughs in dedicated sections below.

|---

## Constitution Decision Tree

Every spec-kit project starts with a **constitution** — a set of project-wide
principles that guide all future features. The constitution phase (Phase 0)
uses a 3-level decision tree to narrow from general purpose to specific
technology choices, then maps those choices to weighted defaults for each of
the 12 project principles.

The skill auto-detects whether the project already has code (**brownfield
mode**) or is starting fresh (**greenfield mode**). For greenfield projects,
two input methods are offered:

- **Free-text description**: User describes the project in a sentence
  (e.g. "React Native mobile app for fitness, small team, Firebase"). The
  agent maps the description to a purpose (A-I), architecture option (A1-I3),
  technology choices, and principle defaults automatically. The user reviews
  the inference table and may accept or correct any item. Total time: ~30 seconds.
- **Guided wizard**: Interactive 3-level decision tree with tradeoffs at
  each level. The agent walks through Purpose → Architecture → Tech → principles.
  Total time: ~5-10 minutes.

<!-- brownfield description stays the same -->

- **Brownfield**: Scans the project root for `package.json`, `pyproject.toml`,
  `go.mod`, `Cargo.toml`, `Gemfile`, `build.gradle`, `*.csproj`, `Dockerfile`,
  test configs, CI configs, database migrations, lint configs — 60+ detection
  patterns. Pre-fills ⭐-marked defaults for every principle based on what's
  detected.
- **Greenfield**: Guides the user through every choice, recommending purpose-
  specific defaults at each level.

### Level 1: Purpose (9 options)

The first question is always: *"What is this project's primary purpose?"*

| Code | Purpose | Examples | Testing impact | Architecture impact | Docs impact |
|------|---------|----------|---------------|-------------------|-------------|
| **A** | User-Facing Application | SaaS, e-commerce, dashboard, CMS, API server | Integration + E2E tests needed. TDD pays off. | Architecture matters — will need to scale. | API docs, setup guide critical. |
| **B** | Content Site / Marketing | Portfolio, blog, docs site, landing page | Minimal — visual checks + broken link checker. | Simple — SSG, template-driven, or plain HTML/CSS. | Content IS the documentation. |
| **C** | Native / Desktop Client | iOS app, Android app, Electron, Tauri, Qt desktop app | UI/snapshot + integration tests. Manual QA for visuals. | Platform SDK defines architecture (MVC, MVVM, Compose). | Store listing, user help. |
| **D** | Library / SDK / Package | npm package, PyPI lib, Go module, Rust crate | Exhaustive unit tests essential. API surface must be tested. | Clean public API, minimal coupling. | API docs, README, changelog mandatory. |
| **E** | Infra / CLI / DevOps | CLI tool, Terraform module, CI pipeline, daemon, AI pipeline | Integration-heavy. Manual testing common. | Simple and composable. No over-engineering. | README + --help. Code IS the documentation. |
| **F** | Game | Unity/Unreal/Godot game, WebGL game | Unit tests for game logic. Playtesting + visual QA critical. | ECS, scene graph, component-based. Engine-driven. | Design doc + mechanics + gameplay guide. |
| **G** | Browser Extension | Chrome MV3, Firefox add-on, Safari extension | Manual browser testing. Playwright for E2E. | Manifest-driven. Content scripts + service worker + popup. | Store listing + permissions + privacy policy. |
| **H** | Research / Notebook | Jupyter, R Markdown, Quarto, MATLAB | Minimal — visual inspection of outputs | Single notebook or notebook + scripts. No production infra. | README with reproduction steps. |
| **I** | IoT / Embedded | Arduino, ESP32, STM32, Zephyr RTOS, RPi Linux | Hardware-in-the-loop. Simulation for CI. | HAL, RTOS tasks, driver layer. Memory-constrained. | Pinout docs, protocol specs, register maps. |

Each option comes with pros/cons so the user understands tradeoffs before
committing.

**Monorepo check**: After picking a purpose, the agent asks whether this
is a multi-project monorepo (e.g., one repo containing a web app + mobile
app + shared library). If yes, Levels 1-3 run independently per sub-project,
and the constitution gets a `Projects` table at the top.

### Level 2: Architecture (25 options across 9 purposes)

Based on the chosen purpose, the agent presents architecture options.
Each option has a description, pros, cons, and best-use guidance.

**A — User-Facing App**: Monolith (A1), Modular Monolith (A2),
Microservices (A3), Serverless/FaaS (A4)

**B — Content Site**: Static Site Generator (B1), Headless CMS + SSG (B2),
Lightweight Backend (B3)

**C — Native / Desktop Client**: Native Platform (C1), Cross-Platform
Framework (C2), Web Wrapper (C3)

**D — Library / SDK**: Zero-Dependency (D1), Curated (D2),
Umbrella/Multi-Package (D3)

**E — Infra / CLI / DevOps**: Single Binary (E1), Multi-Binary (E2),
Plugin-Based (E3), Script/Pipeline/Declarative (E4)

**F — Game**: Engine-Centric (F1), Custom Engine (F2), Web/Retro (F3)

**G — Browser Extension**: Simple/Single-Browser (G1), Full MV3 (G2),
Cross-Browser (G3)

**H — Research / Notebook**: Single Notebook (H1), Notebook + Scripts (H2),
Package + Notebooks (H3)

**I — IoT / Embedded**: Bare-Metal / RTOS (I1), Linux-Based Embedded (I2),
MicroPython / Arduino (I3)

### Level 3: Technology Choices

With purpose + architecture settled, the agent brackets recommended
languages and frameworks. Examples:

- **A1 (Monolith web app)**: Django, Rails, Laravel, Next.js, ASP.NET
- **C1 (Native client)**: Swift (iOS/macOS), Kotlin (Android), C# (WinUI), C++ (Qt)
- **F1 (Engine-based game)**: C# + Unity, C++ + Unreal, GDScript + Godot, Rust + Bevy
- **I1 (Bare-metal IoT)**: C, C++ (constrained), Rust no-std, Zig

Each bracket presents 3-4 options with framework suggestions, pros, and
cons. The user picks one.

### After Level 3: Purpose-to-Principle Defaults

Once purpose, architecture, and tech are known, the agent maps them to
recommended defaults for all 12 constitution principles. Here are the
mappings for each purpose (architecture-independent):

| Principle | A (User-Facing) | B (Content) | C (Native) | D (Library) | E (Infra/CLI) | F (Game) | G (Browser Ext) | H (Research) | I (IoT/Embedded) |
|-----------|-----------------|-------------|------------|-------------|---------------|----------|-----------------|--------------|------------------|
| Testing | A or B | C | B | A | B | C | C | C | C |
| Linting | B | B | B | A | A | B | B | C | A |
| Dependencies | B | B | B | A or B | A | C | A | C | A |
| Git Workflow | B | A | B | B | A | B | B | A | A |
| Documentation | B | B | B | A | C | B | A | B | A |
| Error Handling | A | C | A | B | C | A | A | C | A |
| Performance | B | C | B | B | A | A | A | C | A |
| Code Review | A or B | C | A | A | B | B | A | C | A |
| Database | A | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP |
| Config/Secrets | B | C | B | A | A | C | A | C | B |
| Dev Toolchain | B | B | C | B | C | C | B | A | C |

Key: A = Strict, B = Pragmatic / Curated, C = Permissive / Minimal,
SKIP = principle not applicable

After showing these defaults, the agent walks through each of the 12
principles with 3 options (A/B/C) and their pros/cons. The user may
accept the recommended default or pick a different option.

### Monorepo Mode

When the user confirms a multi-project monorepo:

1. A `Projects` table is added to the constitution header
2. Each sub-project runs Levels 1-3 independently (different purposes
   and architectures are allowed)
3. Shared principles apply to the PRIMARY sub-project
4. The constitution notes: "Applies to all sub-projects" where broadly
   relevant

### Example Interaction

```
You: "Create a constitution for my-project"

Agent: "No existing project detected — greenfield mode."

Agent presents Level 1:
  "What is this project's primary purpose?"
  A — User-Facing Application
  B — Content Site / Marketing
  …
  I — IoT / Embedded

You: "A — User-Facing Application"

Agent: "Is this a multi-project monorepo?" → "No"

Agent presents Level 2:
  "Given User-Facing App, which architecture?"
  A1 — Monolith
  A2 — Modular Monolith
  A3 — Microservices
  A4 — Serverless

You: "A2 — Modular Monolith"

Agent presents Level 3 language/framework options and you pick one.
Then the agent shows recommended principle defaults and walks through
each principle for confirmation.

Result: specs/constitution.md with 12 principles and a full Tech Stack
section. Approx 5-10 minutes for a new project.
```

### Free-Text Mode: Description → Constitution

For users who know what they're building and want to skip the wizard, the
free-text mode maps a natural-language project description directly to
purpose, architecture, tech, and principle defaults.

```
You: "Create a constitution for my-project"

Agent: "No existing project detected. Which approach?
         1. Free-text — describe your project in a sentence
         2. Guided wizard — 3 levels of choices with tradeoffs"

You: "1 — Free-text"

Agent: "Describe your project in a few sentences — what are you building,
         what platform, team size, and any key constraints?"

You: "React Native mobile app for fitness tracking, small two-person team,
      want to ship quickly, no backend — Firebase for auth and data"

Agent infers:
  | Inference | Value | Correct? |
  |-----------|-------|----------|
  | Purpose | C — Native / Desktop Client | ✅ |
  | Architecture | C2 — Cross-Platform (React Native) | ✅ |
  | Language | TypeScript (React Native) | ✅ |
  | Testing | B — Pragmatic TDD | ✅ |

Agent: "Does this look right? Say 'all good' to proceed, or correct
         specific items. I'll then walk through the 12 principles."

You: "All good"

Agent: Walks through 12 principles (skipping Database, not applicable).
       Approx 30 seconds of interaction.
```

The key difference: instead of answering 3 levels of questions, the user
writes one sentence and reviews 4-5 inferred values. The 12 principles
still get confirmed/adjusted individually — only the purpose/architecture/
tech tree is shortcut.

### Brownfield Shortcut

For existing codebases, most of the decision tree is skipped. The agent
detects the stack from project files and pre-fills all defaults, only
asking the user to confirm or adjust principles that the detection was
uncertain about. This typically takes 1-2 minutes.

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
  - Appends to history.md: compare → promote record
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

## Reopen Mode: Fixing Closed Features

Reopen mode is for features that have already been closed (Phase 6 complete)
but need additional bugfixes or small changes. Instead of editing the closed
artifacts in place, reopen creates a fresh bugfix branch and preserves the
original close data, appending a new close entry when fixes are done.

**When to use reopening vs. a new feature:**
- **Reopen** — The change is a bugfix or small add-on to an existing closed feature
- **New feature** — The change is substantial enough to warrant its own spec number

### Walkthrough: Reopen → Fix → Close Again

#### Step 1: Reopen the feature

```text
You: "Reopen 001-user-auth"

Agent:
  - Detects close.md exists → confirms this is a reopen
  - Reads specs/git-conventions.md for reopen_suffix and branch_source
  - Creates branch from main: feat/001-user-auth-bugfixing
    (or reuses existing branch if already created)
  - Checks if bugs.md exists; if not, creates from template
  - Adds entry to history.md: "Feature reopened from closed state"
  - Routes to spec-kit-test so you can log bugs
```

#### Step 2: Log bugs

```text
You: "Add bugs to 001-user-auth — password reset token still expires too early"

Agent:
  - Opens bugs.md (additive only — preserves existing entries)
  - Appends BUG-NNN entries for the new issues
  - Reports: "Logged 2 bugs. Say 'bugfix 001-user-auth' to start the fix loop"
```

#### Step 3: Bugfix loop (same as normal bugfix mode)

```text
You: "bugfix 001-user-auth"

Agent:
  - Auto-chains Plan → Tasks → Implement
  - All edits to plan.md and tasks.md are additive — no existing content removed
  - If new content conflicts with existing content (same bug ID, conflicting spec change):
    STOPS and asks how to resolve
```

#### Step 4: Close again

```text
You: "Close 001-user-auth"

Agent:
  - Appends a new close entry to close.md (preserving original)
  - Compares new health score to original
  - Flags any requirements that changed status (e.g., FR-XXX went from
    ✅ Resolved to ❌ Not Done) and asks how to reflect the change
  - Commits: spec(phase-6): 001-user-auth close (reopen)
```

### Key Rules for Reopen

- **Additive-only**: Bugs, tasks, and plan sections are appended, never removed
- **Conflict resolution**: If new content would overwrite existing entries, the agent stops and asks
- **Original close preserved**: The prior close data remains intact — new entries are appended
- **Must close again**: After fixes are verified, the feature must go through Phase 6 again
- **Old branch rules**: Reopen branch uses `{feature_prefix}/NNN-{name}{reopen_suffix}` (default suffix: `-bugfixing`)

---

## Phase Reference
### Phase 0: Constitution
**Skill**: `spec-kit-constitution` · **Trigger**: "Create constitution"
· **Artifact**: `specs/constitution.md`

Project-wide principles and MUST/SHOULD rules. Runs once per project.
Required before specify or plan can proceed — both will block without it.

Uses a **3-level decision tree** to narrow from general purpose to specific
technology choices, then pre-fills the 12 project principles with
purpose-weighted defaults. Three input modes:

- **Brownfield** (existing codebase): Auto-detects language, framework,
  test runner, CI, database, and linting from 60+ detection patterns.
  Pre-fills ⭐-marked defaults — the user confirms or adjusts them.
- **Free-text** (new project): User describes the project in a sentence.
  Agent maps description to purpose, architecture, tech, and principle
  defaults. User reviews the inference table.
- **Wizard** (guided, new project): Walks the user through all 3 levels:
  Level 1 (9 purposes A–I), Level 2 (2–4 architecture options per purpose),
  Level 3 (language/framework bracketing).

Supports multi-project monorepos: after Level 1, asks whether the repo
contains multiple sub-projects. If yes, Levels 1-3 run independently per
sub-project, and the constitution gets a `Projects` table.

See the [Constitution Decision Tree](#constitution-decision-tree) section
for a full walkthrough with all 9 purposes, 25 architecture options, and
purpose-to-principle default mappings.

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
1. Each design phase already committed individually (no batch needed)
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

**Bug format**: Each bug gets an ID (BUG-NNN), severity
(critical/major/minor/trivial), area, steps to reproduce, expected vs actual
result, Requires Clarification flag, and status
(open/in-progress/resolved/verified).

**Plan Ref enforcement**: During bugfix, each open bug must have a Plan Ref
linking to the plan section that addresses it — no Plan Ref, no implementation.

**BF-### task tracing**: Bugfix tasks use `BF-###` prefix. When a bugfix task
supersedes specific original (buggy) tasks, append `[T###-fix]` to trace the
relationship (e.g., `BF-001 [BUGFIX] [T051-fix] Fix validate_cluster_shape`).

### Phase 5.5: Review — Post-Implement Gate (Optional)
**Skill**: `spec-kit-review` · **Trigger**: "Review [feature]" after
code + tests

Same skill as pre-implement, auto-detects mode. Three modes total:
- **Pre-implement** (Phase 3.5): Cross-artifact consistency check before coding
- **Post-implement** (Phase 5.5): Code quality, spec fulfillment, test quality
- **Closed-review**: Read-only audit of a closed feature — does not update history.md.
  If issues found, offers to add refactoring tasks and reopen the feature.

Post-implement checks:
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
- **Full summary** ("summarize [feature]"): Deep gap analysis comparing code
  against spec/plan. Computes spec health score. Patches spec.md/plan.md for
  intentional deviations (with per-change user approval).
- **Lightweight close** ("close [feature]"): Quick health score, artifact
  state table, key decisions.

**Output rule**: Length proportional to actual git changes, not spec size.
A one-line bugfix gets one line; a multi-file feature gets thorough
per-file coverage.

**Reopen compatibility**: If the feature was reopened, close appends a new
entry to close.md (preserving the original) and compares new vs. old health
scores, flagging any requirement status changes for user resolution.

---

## Branch Strategy

| Operation | Branch name | Created by |
|-----------|-------------|------------|
| Feature work | `feat/NNN-feature-name` | User (before first skill call) |
| Bugfix | `bug/NNN-bugfix-name` | User (before saying "bugfix") |
| Explore variant | `explore/NNN-feature-<variant>` | Explore skill (automatically) |
| Reopen | `feat/NNN-feature-name-bugfixing` | Reopen skill (automatically) |

Actual prefix values come from `specs/git-conventions.md` — the table above
shows defaults (`feat/`, `bug/`, `explore/`, suffix `-bugfixing`).

**Always on a feature branch.** The workflow blocks all git operations on
`main`/`master`. If you try to start work on main, the agent will refuse
and prompt you to create the correct branch.

**Bugfix branches**: Bugfix work happens on whatever branch the feature was
implemented on — you don't create a separate branch for individual bugfix
loop iterations.

**Explore branches**: Created automatically by the explore skill when it
creates worktrees. Branch naming convention follows the project's
`explore_prefix` from git conventions.

**Reopen branches**: Created automatically by the reopen flow from the
project's `branch_source` (typically `main`). Branch name follows the
pattern `{feature_prefix}/NNN-{name}{reopen_suffix}`. If the branch
already exists from a prior reopen, it's checked out and reused.

---

## Git Commit Conventions

| Situation | Commit message |
|-----------|---------------|
| Each design phase commits individually | See per-phase templates in auto-commit.md |
| Per phase (Implement) | `feat: [feature] Phase N - [Name]` |
| Regression umbrella fix | `fix: [feature] BF-REGRESSION-001 - fix regressions` |
| Bugfix loop (per bug) | `fix: [feature] BF-### - description` |
| Bugfix sub-round plan (new bugs, separate commit) | `spec(phase-2): [feature] bugfix plan (BUG-NNN, ...)` |
| Bugfix sub-round tasks (new bugs, separate commit) | `spec(phase-3): [feature] bugfix tasks (BUG-NNN, ...)` |
| Bugfix sub-round quickfix (batched) | `fix: [feature] BF-### - description (plan+tasks+fix)` |
| Explore variant promotion | `feat: [feature] merge winning variant [name]` |
| Explore cherry-pick | `feat: [feature] cherry-pick [features] from [variant]` |
| Close/Summary | `spec(phase-6): [feature] summary (health: N%)` |
| Refresh artifacts | `spec(refresh): [feature] reconcile artifacts` |
| Reopen begin | `spec(reopen): [feature] reopen from closed state` |
| Reopen close | `spec(phase-6): [feature] close (reopen, health: N%)` |
| History entry capture | Automated via `git rev-parse HEAD` |

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
spec_health = (resolved + acknowledged) / (resolved + acknowledged + not_done) * 100
```

- **resolved**: Requirements implemented as planned OR intentionally
  deviated with documented rationale (spec/plan auto-updated)
- **acknowledged**: Requirements deferred with documented reason
- **not_done**: Requirements missing without documented reason

| Score | Meaning | Action |
|-------|---------|--------|
| 100% | Artifacts fully aligned with code | No action needed |
| 80-99% | Minor gaps tracked but not blocking | Acceptable — review at leisure |
| 50-79% | Significant drift | Run `spec-kit-refresh` before refactoring |
| <50% | Artifacts are misleading | Run `spec-kit-refresh` before proceeding |

When you load an existing feature with a close document, the agent reads
the health score and checks the artifact state table in the close file.
If any artifact is flagged as `⚠️ needs review` or `❌ outdated`, a warning
is shown. If the score is below 80%, you'll be prompted to run refresh
before proceeding.

**Reopen comparison**: When a reopened feature is closed again, the new
health score is compared against the original. Any requirements that
changed status (e.g., from ✅ Resolved to ❌ Not Done) are flagged for
user resolution.

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

### "Feature [feature] is not closed"

You tried to reopen a feature that has no close.md or
implementation-summary.md. Only closed features can be reopened:

```text
If the feature has open bugs but was never closed:
  Say: "bugfix [feature]" to start the fix loop

If the feature is new or in progress:
  Continue working through the normal workflow phases
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
| history-template.md | Phase transitions | Append-only log entries |
| git-conventions-template.md | Project setup | Git branch/commit conventions |
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
| `close.md` exists | Closed — complete |
| `close.md` + `bugs.md` with open bugs | **Reopened (bugfix in progress)** |
| `implementation-summary.md` exists | Summarized — complete |
| `variants/` directory with ≥2 entries | Exploring |
| `comparison.md` exists | Compared — decision made |
| `history.md` last entry | Current phase (fastest lookup) |

### Quick CLI Reference

```bash
# Start a session with spec-kit preloaded
hermes -s spec-kit-workflow

# Both prefixes work: "spec-kit plan" and "speckit plan" trigger the same skill
# Natural language also works: "plan the implementation for 001-user-auth"

# Start in isolated git worktree (for manual parallel variants)
hermes -w -s spec-kit-workflow

# Reload skills after installation
/reload-skills

# Load a specific skill mid-session
/skill spec-kit-compare

# Check installed skills
hermes skills list | grep spec-kit
```

|### Workflow Diagram

```text
                                            ┌── Explore ───────────────┐
                                            │   git worktree add …     │
                                            │   delegate_task × N      │
                                            ▼                          │
Constitution (3-level tree) → Specify → Clarify (opt) → Plan → Tasks → Implement → Test
  │ Level 1: 9 purposes (A-I)                                                        │
  │ Level 2: 25 architecture options                                                 │
  │ Level 3: Tech bracketing                                              ┌──────────┘
  │ After: 12 principles with purpose-mapped defaults                     ▼
  └─────────────────────→                    ┌─→ [Clarify] → Plan → Tasks → Implement → Test → Close (mandatory)
                                             │
                                             └── Reopen ──→ bugfix loop → Close (append, preserve original)

                             Optional gates:
                               [Review] ← pre-implement (before code)
                               [Review] ← post-implement (after tests)
                               [Review] ← closed-review (read-only audit)
```
