# Hermes Spec-Kit

Spec-driven development for Hermes Agent. 13 skills implementing a structured phase-based workflow with three development modes, a constitution 3-level decision tree (9 purposes × 25 architecture options), mandatory close with spec health scoring, and a reopen flow for fixing closed features.

## Quick Start

```bash
# 1. Clone (if you haven't already) and install
git clone https://github.com/kmarecki/hermes-spec-kit.git
cd hermes-spec-kit
./scripts/install.sh          # copies skills + templates to ~/.hermes/skills/

# 2. Reload skills in your Hermes session
/reload-skills                # or start a new session

# 3. Go to your project, create a spec
cd /path/to/your-project
```

Then in Hermes: `"Create a spec for [feature]"` or `"speckit specify [feature]"`.

**New project from scratch:**

```bash
git clone https://github.com/kmarecki/hermes-spec-kit.git ~/hermes-spec-kit
cd ~/hermes-spec-kit
./scripts/install.sh
cd /path/to/my-new-project
git init
mkdir specs
# In Hermes: "Create a constitution for my-project"
```

## Prerequisites

- **Hermes Agent** installed and configured (`hermes` command available)
- **Git** repository in your project directory (spec-kit creates branches, commits, and workflow logs)
- The project directory should have a `specs/` directory at the root (created automatically when you create the first spec)

Full workflow documentation: **[user-guide.md](user-guide.md)**

## Project Structure

```
src/
  skills/                # Skill source files (12 .md + 1 directory skill)
    spec-kit/SKILL.md    # Umbrella skill — overview and quick reference
  templates/             # Template source files (14 templates)
  references/            # Reference files (preflight.md, auto-commit.md, history-tracking.md)
scripts/
  install.sh             # Installs to ~/.hermes/skills/
```

## Three Development Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Specify** (default) | "Create a spec for [feature]" | Full forward phase sequence, manual transitions |
| **Bugfix** | "bugfix [feature]" | Auto-chain inner loop (Plan→Tasks→Implement), mandatory close |
| **Reopen** | "Reopen [feature]" | Reopens closed feature for bugfixing, additive-only edits, routes through bugfix loop |

## Skills

13 skills covering every phase + refresh and workflow routing.
See the [Phase Reference section](user-guide.md#phase-reference) in the user-guide for phases, purposes, and personas.

All skills respond to three trigger styles: `spec-kit` prefix, `speckit` prefix, and natural language
(e.g. `spec-kit plan 001-user-auth`, `speckit plan 001-user-auth`, or `"plan the implementation for 001-user-auth"`).

## Constitution Decision Tree

The constitution phase (Phase 0) guides users through a 3-level decision tree that
narrows from general purpose to specific technology choices, then pre-fills the 12
project principles with weighted defaults.

**Level 1 — Purpose** (9 options):

| Code | Purpose | Example use cases |
|------|---------|-------------------|
| **A** | User-Facing Application | SaaS, e-commerce, dashboard, CMS, API server |
| **B** | Content Site / Marketing | Portfolio, blog, docs site, landing page |
| **C** | Native / Desktop Client | iOS app, Android app, Electron, Tauri, Qt app |
| **D** | Library / SDK / Package | npm package, PyPI lib, Go module, Rust crate |
| **E** | Infrastructure / CLI / DevOps | CLI tool, Terraform module, CI pipeline, daemon, AI pipeline |
| **F** | Game | Unity/Unreal/Godot game, WebGL game, custom-engine game |
| **G** | Browser Extension | Chrome MV3, Firefox add-on, Safari extension, cross-browser |
| **H** | Research / Notebook | Jupyter, R Markdown, Quarto, MATLAB, experimental analysis |
| **I** | IoT / Embedded | Arduino, ESP32, STM32, Zephyr RTOS, Raspberry Pi Linux |

**Level 2 — Architecture** (25 options across all purposes): Each purpose has 2-4 architecture
variants — e.g., User-Facing App offers Monolith / Modular Monolith / Microservices / Serverless,
while Libraries offer Zero-Dependency / Curated / Umbrella.

**Level 3 — Technology choices**: Per-purpose language/framework bracketing — e.g., an Engine-Centric
Game (F1) gets C# (Unity), C++ (Unreal), or Rust (Bevy); a Browser Extension (G3) gets
TypeScript + webextension-polyfill or WXT framework.

**After Level 3**: The 12 principles (Testing, Linting, Architecture, Dependencies, Git Workflow,
Documentation, Error Handling, Performance, Code Review, Database, Config/Secrets, Dev Toolchain)
are pre-filled with purpose-weighted defaults. The user confirms or adjusts each one.

**Brownfield mode**: If the project already has code, the agent auto-detects language, framework,
test runner, CI, database, and linting — then pre-fills ⭐-marked defaults.

**Free-text mode** (new projects): User describes the project in natural language
(e.g. "React Native mobile app for fitness, small team, ship fast"). The agent
maps description → purpose → architecture → tech → principle defaults automatically.
User reviews the inference table and may accept or correct any item.

**Wizard mode** (guided, new projects): Interactive 3-level decision tree with
tradeoffs at each level.

**Monorepo support**: After choosing Level 1 purpose, the agent asks "Is this a multi-project
monorepo?" If yes, Levels 1-3 run independently per sub-project, and the constitution gets a
`Projects` table at the top.

Full walkthrough: see [Constitution Decision Tree](user-guide.md#constitution-decision-tree)
in the user-guide.

## Key Design Decisions

- Constitution is mandatory for all features — specify and plan block if missing
- Constitution uses a 3-level decision tree: Purpose → Architecture → Tech stack
- 9 purpose types (A-I) with 25 architecture variants across all purposes
- Purpose-to-principle default mappings for each of the 12 constitution principles
- Design phases (0-3) each commit immediately — no batch commit
- Bugfix sub-rounds: separate phase commits by default (`bugfix`), opt-in batch via `quickfix`
- Phase-level TDD: all tests RED first, all code GREEN, then commit
- TDD bypass at user request during task generation
- One umbrella regression fix task, not individual bugs
- Phase 6 (Close) is mandatory before feature completion
- Spec health score computed at close (0-100%)
- Branch guardrails block git operations on main/master
- Pre-action self-check in every skill (branch, mode, workflow)
