# Hermes Spec-Kit: User Guide

Spec-driven development for Hermes Agent. Every feature starts with a
specification — not a line of code — and progresses through planning,
task breakdown, TDD implementation, testing, and a mandatory close phase.
Three development modes span the full feature lifecycle: forward development
(specify), bugfix loop, and reopen for closed features.

This guide covers installation, the core workflow, the reopen flow for closed features, and
day-to-day usage.

---

## Table of Contents

1.  [What is Spec-Kit?](#what-is-spec-kit)
2.  [Quick Start: Your First Feature](#quick-start-your-first-feature)
3.  [Three Development Modes](#three-development-modes)
4.  [Constitution Decision Tree](#constitution-decision-tree)
    - [Level 1: Purpose (9 options)](#level-1-purpose-9-options)
    - [Level 2: Architecture (44 options)](#level-2-architecture-44-options-across-11-purposes)
    - [Level 3: Technology Choices](#level-3-technology-choices)
    - [Purpose-to-Principle Defaults](#after-level-3-purpose-to-principle-defaults)
    - [Monorepo Mode](#monorepo-mode)
    - [Free-Text Mode](#free-text-mode-description--constitution)
    - [Brownfield Shortcut](#brownfield-shortcut)
5.  [Reopen Mode: Fixing Closed Features](#reopen-mode-fixing-closed-features)
6.  [Phase Reference](#phase-reference)
7.  [Branch Strategy](#branch-strategy)
8.  [Git Commit Conventions](#git-commit-conventions)
9.  [Spec Health Score](#spec-health-score)
10. [MCP Server](#mcp-server)
11. [Troubleshooting](#troubleshooting)
12. [Reference Tables](#reference-tables)

---

## What is Spec-Kit?

Spec-kit is a structured workflow for building features with an AI agent.
Instead of saying "build a login system" and hoping the agent gets it right,
you guide it through seven phases — from specification through close — with
checkpoints, guardrails, and review gates. Three modes cover the full feature
lifecycle: forward development (specify), bugfix loop, and reopen for closed features.

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
- 11 spec-kit skills in `~/.hermes/skills/` — respond to `spec-kit` prefix, `speckit` prefix,
  and natural language phrases
  (e.g. `"speckit plan 001-user-auth"`, `"spec-kit plan 001-user-auth"`, or
  `"plan the implementation for 001-user-auth"` all trigger the same skill)
- Templates in `~/.hermes/skills/spec-kit/templates/`
- Reference files in `~/.hermes/skills/spec-kit/references/` (preflight, commits, history tracking, sizing, evidence, acceptance)
- A `specs/` directory in your project for feature artifacts
- An optional MCP server (`mcp_spec_kit_*` tools) for deterministic state management
  — auto-configured by install.sh, activates with `/reload-mcp`

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

## Three Development Modes

Spec-kit has three modes, each suited to a different level of uncertainty:

| Mode | When to use | How it runs | User involvement |
|------|-------------|-------------|-----------------|
| **Specify** (default) | You know what you want — low uncertainty | Starts with constitution decision tree (11 purposes × 44 architecture options). Then a linear forward phase sequence: Specify → Clarify (opt) → Plan → Tasks → [Review] → Implement → Test → [Review] → Close | Manual — you say "plan", "implement", etc. |
| **Bugfix** | You have a working feature with known bugs | Auto-chains Plan→Tasks→Implement→Test once you say "bugfix". If new bugs are discovered mid-round, they're logged separately and the next round runs the full plan→tasks→implement cycle (separate commits per phase). For trivial fixes, "quickfix [feature]" batches plan+tasks+fix in one commit (user explicitly opts in). | Minimal — inner loop is automatic |
| **Reopen** | A closed feature needs more fixes | Creates bugfix branch from main, preserves original close data, routes through bugfix loop | Additive-only edits; must close again after fixes |

Phase sequence for each mode:

| Mode | Sequence |
|------|----------|
| **Specify** | `Constitution → Specify → Clarify (opt) → Plan → Tasks → [Review] → Implement → Test → [Review] → Close` |
| **Bugfix** | `Test → [Clarify if needed] → Plan → Tasks → Implement → Test → Close` |
| **Reopen** | Deep dive below → |

Reopen has a full walkthrough in the dedicated section below.

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
  agent maps the description to a purpose (A-K), architecture option (A1-K3), traits,
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

### Level 1: Purpose (11 options)

The first question is always: *"What is this project's primary purpose?"*

| Code | Purpose | Examples | Weighs most |
|------|---------|----------|-------------|
| **A** | Applications & Services | SaaS, web / mobile backend, APIs, workers, AI apps | Integration tests, architecture, defensive errors |
| **B** | Content Site | Marketing site, blog, docs | Publishing speed, Core Web Vitals |
| **C** | Native / Desktop Client | iOS, Android, desktop (Flutter, Tauri, Qt) | UI tests, crash-free, store review |
| **D** | Library / SDK | npm / PyPI / NuGet package, Rust crate, smart contract | Public API, exhaustive tests, docs |
| **E** | Infrastructure / CLI / DevOps | CLI, IaC, CI pipeline, MCP server | Composability, static binaries |
| **F** | Game / XR | Unity / Unreal / Godot game, WebGL, VR / AR | Frame budget, playtesting |
| **G** | Extensions & Integrations | Browser extension, VS Code / JetBrains plugin, Office add-in, Slack / Teams bot | Host APIs, permissions, store review |
| **H** | Research, Data & ML | Notebooks, data warehouse / dbt, model training and serving | Reproducibility, data quality, evals |
| **I** | IoT / Embedded | Firmware, embedded Linux, connected device fleets | No hotfix once flashed, hard limits |
| **J** | Systems Software | Kernel, driver, database engine, compiler, HPC | Memory safety, fuzzing, performance gates |
| **K** | Business Platform | Salesforce, Dynamics / Power Platform, SAP, ServiceNow | Vendor limits, release cadence, metadata deploys |

Nothing fits → **Other**: the agent takes the closest purpose, writes three options of its own
and marks them *(not from the reference tables)* in the constitution.

### Level 1.5: Project traits

One multi-select question that adjusts the defaults (the stricter option wins):

- **Runs where** — multi-tenant SaaS, single-tenant, on-prem, local-first / offline, edge
- **Regulated domain** — none, personal data, finance, health, safety-critical, EU AI Act high-risk
  (safety-critical → Testing, Review, Docs and Error handling A; regulated or personal data →
  suggests `compliance: baseline`)
- **Lifecycle** — prototype, product, modernization (characterisation tests first, strangler-fig
  target, an ADR for the cut-over)

Each option comes with pros/cons so the user understands tradeoffs before
committing.

**Monorepo check**: After picking a purpose, the agent asks whether this
is a multi-project monorepo (e.g., one repo containing a web app + mobile
app + shared library). If yes, Levels 1-3 run independently per sub-project,
and the constitution gets a `Projects` table at the top.

### Level 2: Architecture (44 options across 11 purposes)

Based on the chosen purpose, the agent presents architecture options.
Each option has a description, pros, cons, and best-use guidance; ⭐ marks the 2026 default
for the purpose (refreshed 2026-11).

**A — User-Facing App**: Monolith (A1), Modular Monolith ⭐ (A2),
Microservices (A3), Serverless — functions or scale-to-zero containers (A4),
AI-native / Agentic — model gateway, retrieval, tools, evals (A5),
Event-driven / Workers / Streams (A6)

**B — Content Site**: Static / Islands ⭐ (B1), Headless CMS + SSG (B2),
Lightweight Backend (B3)

**C — Native / Desktop Client**: Native Platform (C1), Cross-Platform ⭐
(C2), Web Wrapper (C3)

**D — Library / SDK**: Zero-Dependency (D1), Curated ⭐ (D2),
Umbrella/Multi-Package (D3), Smart Contracts (D4)

**E — Infra / CLI / DevOps**: Single Binary ⭐ (E1), Multi-Binary (E2),
Plugin-Based (E3), Declarative / Pipeline (E4), MCP Server / Agent Tool (E5)

**F — Game / XR**: Engine-Centric ⭐ (F1), Custom Engine (F2), Web (F3), XR / Spatial (F4)

**G — Extensions & Integrations**: Simple browser (G1), Full MV3 (G2),
Cross-Browser ⭐ (G3), Host Plugin / Bot — IDE, Office, Figma, Slack / Teams, SaaS marketplace (G4)

**H — Research, Data & ML**: Single Notebook (H1), Notebook + Modules ⭐ (H2),
Package + Notebooks (H3), Data Platform (H4), ML Training & Serving (H5)

**I — IoT / Embedded**: Bare-Metal / RTOS (I1), Linux-Based Embedded (I2),
High-Level Firmware — Arduino / MicroPython (I3), Connected Fleet — devices + cloud + OTA (I4)

**J — Systems Software**: Kernel / Driver (J1), Engine / Runtime / Compiler ⭐ (J2),
Scientific / HPC (J3)

**K — Business Platform**: Configuration / Low-code ⭐ (K1), Platform Code (K2),
Marketplace App (K3)

### Level 3: Technology Choices

With purpose + architecture settled, the agent brackets recommended
languages and frameworks. Examples:

- **A1 (Monolith web app)**: Rails 8, Laravel, Django, ASP.NET Core, Next.js / SvelteKit
- **A5 (AI-native app)**: Python (FastAPI + LangGraph / Pydantic AI), TypeScript (Vercel AI SDK), C# (Microsoft.Extensions.AI) + an eval harness
- **C1 (Native client)**: Swift (SwiftUI), Kotlin (Compose), C# (WinUI 3), C++ (Qt 6)
- **F1 (Engine-based game)**: C# + Unity, C++ + Unreal, GDScript + Godot, Rust + Bevy
- **I1 (Bare-metal IoT)**: C (Zephyr, FreeRTOS, ESP-IDF), Rust (Embassy), C++ (constrained)

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
  Level 1 (11 purposes A–K), Level 1.5 (project traits), Level 2 (3–6 architecture options per purpose),
  Level 3 (language/framework bracketing).

Supports multi-project monorepos: after Level 1, asks whether the repo
contains multiple sub-projects. If yes, Levels 1-3 run independently per
sub-project, and the constitution gets a `Projects` table.

**Project documents**: the last step asks the project's **scale** — *small* (no ADR / design /
epic directories) or *platform* (`adr_dir`, `design_dir`, `epics_dir` written to
`specs/git-conventions.md`) — and creates or patches `AGENTS.md`. Platform then runs
**`spec-kit design map`**: brownfield recovers `system.md`, proposes the module split, writes
a design doc per approved module, indexes existing ADRs and proposes `Accepted (retroactive)`
ADRs for decisions the code already embodies; greenfield writes the target `system.md`, the
planned module map and ADRs 0001–0003 from the decision tree. Every step waits for approval.

See the [Constitution Decision Tree](#constitution-decision-tree) section
for a full walkthrough with all 11 purposes, 44 architecture options, and
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
(open/in-progress/claimed/verified/superseded — `claimed` is the agent's word, `verified` needs a user, CI or other-agent oracle; see Evidence of Done).

**Plan Ref enforcement**: During bugfix, each open bug must have a Plan Ref
linking to the plan section that addresses it — no Plan Ref, no implementation.

**BF-### task tracing**: Bugfix tasks use `BF-###` prefix. When a bugfix task
supersedes specific original (buggy) tasks, append `[T###-fix]` to trace the
relationship (e.g., `BF-001 [BUGFIX] [T051-fix] Fix validate_cluster_shape`).

### Phase 5.5: Final Review — Merge Gate (Mandatory)
**Skill**: `spec-kit-review` · **Trigger**: "Final review [feature]", "Is [feature] ready
to merge", or "Review [feature]" once every task is done and no bug is open ·
**Artifact**: `review-final.md` (one round per run)

Same skill as pre-implement, auto-detects mode (pre-implement / final / closed-review).
The final review answers four questions and ends with a verdict:

1. **Does the code do what the spec says?** Every FR, success criterion, acceptance
   scenario and edge case → the code (`path:line`) and the test that proves it; contracts
   and data model vs code; unplanned changes.
2. **Does it obey the constitution and project rules?** Every applicable MUST in
   `specs/constitution.md`, every rule in `specs/merge-checklist.md` and AGENTS.md — each
   verdicted with evidence. This is where the constitution is enforced.
3. **Is it good code?** Architecture, error handling, security, data integrity,
   concurrency, duplication, complexity, API surface, current best practice; test quality.
4. **Can it merge?** `diff_scan` (conflicts, secrets, forbidden files, focused tests,
   TODOs) and the checklist commands (build, full tests, lint, format), outputs saved under
   `evidence/final-*`.

**Verdict**: `READY`, `READY-WITH-FOLLOWUPS` (only MEDIUM findings) or `NOT READY` (any
CRITICAL/HIGH or failing blocking check → logged as bugs → bugfix loop → new round). The
round records the reviewed commit; a later code commit makes it stale. The close refuses
without a fresh READY round. Run it by the other agent, or a fresh-context sub-agent.

### Acceptance criteria and the acceptance loop
Every scenario in spec.md is an acceptance criterion with an id and a verify level:
`**AC-003** (FR-002) Given … When … Then … — Verify: unit`. The level is the lowest that can
prove it — unit, integration, component, e2e (with a reason), command, probe, manual (with a
reason). The plan maps each AC to a harness and test file; its tests are ordinary `[TEST]`
tasks tagged `[AC-003]`, written RED in the implement phase that delivers the behaviour and
then **frozen** (checksummed) so the loop cannot pass by weakening them.

After the last implement phase, `accept [feature]` runs automatically: the full unit,
integration and component suites (this is also the regression run), this feature's own e2e
specs only if the stack is up (otherwise deferred to the final review — the full e2e suite
never runs in the loop), and any command/probe checks. Results (JUnit XML / TRX) map back to
the ACs by the id in the test name. Failures become bugs, the bugfix chain runs, and the
acceptance round repeats — until every automated AC passes, or it stops and asks after 5
rounds, no progress, a needed spec or frozen-test change, or a run that cannot execute.

### Size tiers (S / M / L)
Specify always asks for the tier, with its recommendation first. S trims the templates and
chains specify → plan → tasks into one commit; M is the default; L adds the full artifact
set and a required pre-implement review. See `references/sizing.md`.

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

Both modes, after the final-review gate:
- **ADRs**: decisions harvested from decisions.md, plan rounds, research and reviews are
  tested against the ADR bar (cross-feature, hard to reverse, real alternatives, changes an
  existing ADR); passing ones become new / superseding / amending project ADRs (approved one
  by one) and the ADR index is updated. The close's *Architecture Decisions* table lists
  every candidate.
- **AGENTS.md**: statements the change made wrong (commands, layout, boundaries, versions,
  conventions, debt, ADR list) get targeted patches, approved one by one.

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

## MCP Server (Optional)

An MCP server acts as a **derive-and-enforce** service. It keeps no state: on every call it
derives the current phase from the files under `specs/<feature>/` and validates against them.
It exists for the things an agent does badly — allocating the next id, linting `bugs.md` and
`tasks.md`, stamping real times, guarding that `history.md` was written before the commit, freezing acceptance tests — and
to hand back a ten-line **phase card** that survives context compaction.

### How it works

```
Hermes / Claude Code ─→ mcp_spec_kit_* tools ─→ MCP Server (server.py)
                                                        ↓ reads only
                                              specs/<feature>/*.md
```

The server uses the official [mcp Python SDK](https://pypi.org/project/mcp/) (`FastMCP`) for stdio transport. Nothing is persisted; a legacy `specs/.spec-kit/state.json` is ignored and should be deleted and gitignored.

### Tools provided

| Tool | Purpose |
|------|---------|
| `mcp_spec_kit_init_feature` | Create `specs/<feature>/` with a history.md header |
| `mcp_spec_kit_get_feature_state` | Derived phase, artifacts, task/bug counts, phase card |
| `mcp_spec_kit_get_next_actions` | Available actions + the phase card |
| `mcp_spec_kit_advance_phase` | Validate a transition against the files (writes nothing) |
| `mcp_spec_kit_project_status` | Constitution present?, feature count, legacy state file? |
| `mcp_spec_kit_project_set_constitution` | Confirm `specs/constitution.md` exists |
| `mcp_spec_kit_list_features` | Every feature's derived state |
| `mcp_spec_kit_reopen_feature` | Check the feature is closed; return the branch hint |
| `mcp_spec_kit_close_feature` | Validate the close (no open bugs, verified bugs have Verified-by) |
| `mcp_spec_kit_update_artifact` | Confirm an artifact is on disk |
| `mcp_spec_kit_auto_detect_features` | Derived state of all features |
| `mcp_spec_kit_next_id` | Next BUG / T / BF id |
| `mcp_spec_kit_lint_artifacts` | Schema lint of bugs.md, tasks.md, history.md, ACs, rounds |
| `mcp_spec_kit_history_guard` | Fresh history entry since the last commit? |
| `mcp_spec_kit_append_history` | Append a fixed-field, time-stamped, word-capped history entry |
| `mcp_spec_kit_timestamp` | Real UTC time |

### Benefits

- **No drift**: nothing to keep in sync — the files are the state
- **Enforced transitions**: `advance_phase` and `close_feature` reject moves the files do not support
- **Mechanical hygiene**: ids, statuses, timestamps, probes, RED files and the history guard are checked by code, not by prose
- **Backward compatible**: without the server every skill falls back to filesystem detection, `date -u` and manual id counting

Bug tracking is deliberately NOT in the MCP server: `bugs.md` is the single
source of truth and is written directly by `spec-kit-test`. The server only reads it.

### Installation

The install script (`./scripts/install.sh`) automatically:

1. Copies `server.py` to `~/.hermes/skills/spec-kit/mcp-server/`
2. Creates a Python venv at `~/.hermes-venv` if the `mcp` SDK is not found
3. Runs `hermes mcp add spec-kit` to register the server in `config.yaml`
4. Prints instructions to activate with `/reload-mcp`

If `hermes mcp add` times out during connection verification, add the config
manually to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  spec-kit:
    command: "/home/krzys/.hermes-venv/bin/python3"
    args: ["/home/krzys/.hermes/skills/spec-kit/mcp-server/server.py"]
```

Then run `/reload-mcp` in Hermes and verify with `/toolsets` — the
`mcp_spec_kit_*` tools should appear.

### Skill integration

When the MCP server is available (its tools exist in the Hermes toolset), skills
defer to it for state queries and transitions. When unavailable, the same skills
use the filesystem-based detection and routing from the table above.

`spec-kit-test` logs bugs and stops in both modes; with MCP it allocates the
BUG id with `mcp_spec_kit_next_id` and lints before committing. The user
starts the fix loop with "bugfix [feature]".

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
| history-template.md | Phase transitions (size L by default — `history: large`) | Append-only log entries |
| epic-template.md · epic-plan-template.md · epic-features-template.md · epic-review-template.md · epics-index-template.md | `spec-kit epic` (opt-in `epics_dir`) | E1 specify (goal, EACs, rules) · E2 plan (target architecture, ED decisions, sequencing) · E3 breakdown (ordered features) · E3.5 / E6 reviews with devil's advocate |
| design-doc-template.md | `spec-kit design` (opt-in `design_dir`) | Living module design: components, flow, seams, invariants, security, debt |
| change-record-template.md | Close | The auditor's one page: ticket, risk tier, security impact, approvals, verification, rollback, timeline |
| git-conventions-template.md | Project setup | Git branch/commit conventions |
| gitignore-template.md | Project setup | .gitignore starter |
| AGENTS-template.md | Project setup | Starting AGENTS.md |

### Artifact Detection (Phase Detection)

When the MCP server is configured, `mcp_spec_kit_get_feature_state` derives the
current phase, artifact status and bug counts from the files below — the same
table, applied by code. Use it (or the table) before any write.

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
| `history.md` last entry | Current phase (fastest lookup) — or the MCP phase card |

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
/skill spec-kit-summarize

# Check installed skills
hermes skills list | grep spec-kit

# MCP server commands (if installed)
/reload-mcp                    # Activate MCP server after install/config change
hermes mcp status              # Check MCP server status
mcp_spec_kit_list_features     # List all registered features via MCP
```

### Workflow Diagram

```text
                                            ┌── Explore ───────────────┐
                                            │   git worktree add …     │
                                            │   delegate_task × N      │
                                            ▼                          │
Constitution (3-level tree) → Specify → Clarify (opt) → Plan → Tasks → Implement → Test
  │ Level 1: 11 purposes (A-K) + traits                                              │
  │ Level 2: 44 architecture options                                                 │
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
