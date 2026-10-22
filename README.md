# Hermes Spec-Kit

Spec-driven development for Hermes Agent. 11 skills implementing a structured phase-based workflow with three development modes, a constitution 3-level decision tree (9 purposes × 25 architecture options), mandatory close with spec health scoring, and a reopen flow for fixing closed features. Includes an optional MCP server for deterministic state management.

## Quick Start

```bash
# 1. Clone (if you haven't already) and install
git clone https://github.com/kmarecki/hermes-spec-kit.git
cd hermes-spec-kit
./scripts/install.sh          # copies skills + templates + MCP server to ~/.hermes/skills/
./scripts/install-claude.sh   # (optional) the same skills for Claude Code → ~/.claude/skills/

# 2. Reload skills and MCP in your Hermes session
/reload-skills                # or start a new session
/reload-mcp                   # if MCP server was auto-configured

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

```text
src/
  skills/                # Skill source files (11 .md + 1 umbrella directory)
    spec-kit/SKILL.md    # Umbrella skill — overview and quick reference
  templates/             # Template source files (13 templates, all *-template.md)
  references/            # preflight, auto-commit, evidence, history-tracking, constitution-*
    skills/              # Full procedure per skill — loaded on demand by the one-screen SKILL.md
  skills/
    spec-kit-bugfix/      [removed] — function absorbed into spec-kit-workflow
scripts/
  install.sh             # Installs to ~/.hermes/skills/ + MCP config
  uninstall.sh           # Full clean uninstall (skills, MCP, config)
spec-kit-mcp-server/
  server.py              # MCP server — 11 tools, Python + mcp SDK (<2)
  README.md              # MCP server docs
  test_server.py         # Smoke test
```

## Three Development Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Specify** (default) | "Create a spec for [feature]" | Full forward phase sequence, manual transitions |
| **Bugfix** | "bugfix [feature]" | Auto-chain inner loop (Plan→Tasks→Implement), mandatory close |
| **Reopen** | "Reopen [feature]" | Reopens closed feature for bugfixing, additive-only edits, routes through bugfix loop |

## Skills

11 skills covering every phase + refresh and workflow routing.
(The former `spec-kit-bugfix` alias skill was removed — its function is absorbed into the
workflow skill's bugfix routing.)

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

## MCP Server (Optional)

An MCP server (`spec-kit-mcp-server/server.py`) is a **derive-and-enforce** service: it
keeps no state, derives every feature's phase from the files under `specs/<feature>/` on
each call, and does the things an agent does badly — id allocation, artifact lint, real
timestamps, the history-before-commit guard, and a ten-line phase card to re-read after
context compaction. 16 tools exposed as `mcp_spec_kit_*` in Hermes (`mcp__spec-kit__*` in
Claude Code).

**Tools:**

| Tool | Purpose |
|------|---------|
| `init_feature` | Create `specs/<feature>/` with a history.md header |
| `get_feature_state` | Derived phase, artifacts, task/bug counts, phase card |
| `get_next_actions` | Available actions + the phase card |
| `advance_phase` | Validate a transition against the files (writes nothing) |
| `project_status` | Constitution present?, feature count, legacy state file? |
| `project_set_constitution` | Confirm `specs/constitution.md` exists |
| `list_features` | Every feature's derived state |
| `reopen_feature` | Check closed, return branch hint |
| `close_feature` | Validate the close (bugs verified with Verified-by; lists claimed-unverified) |
| `update_artifact` | Confirm an artifact is on disk |
| `auto_detect_features` | Derived state of all features |
| `next_id` | Next BUG / T / BF id by scanning the files |
| `lint_artifacts` | Schema lint of bugs.md, tasks.md, history.md |
| `timestamp` | Real UTC time |
| `history_guard` | Fresh history entry since the last commit? |
| `append_history` | Append a fixed-field, time-stamped, word-capped history entry |

**State file**: none. The files are the state. A legacy `specs/.spec-kit/state.json` is
ignored — delete it and add `specs/.spec-kit/` to `.gitignore` (the gitignore template does).

**Bug tracking is file-based**: bugs live in `specs/NNN-name/bugs.md` — the single
source of truth. The MCP server intentionally has no bug tools; bugfix routing
parses bugs.md directly.

**Dependency**: Requires the [mcp Python SDK](https://pypi.org/project/mcp/) pinned
to `<2` (`mcp 2.x` renamed FastMCP → MCPServer and breaks this server). Install
from `spec-kit-mcp-server/requirements.txt`; the install script auto-installs it
in a venv at `~/.hermes-venv/`.

**Fallback**: When the MCP server is not configured, all skills fall back to
filesystem-based artifact detection — backward compatible, no skill changes needed.

**Installation**: `install.sh` copies the server and auto-configures via `hermes mcp add`.
Activate in Hermes with `/reload-mcp`.

**Claude Code**: `install-claude.sh` registers the same server at user scope
(`claude mcp add -s user spec-kit …`); the tools appear as `mcp__spec-kit__<tool>`.
Both agents derive the same state from the same files; nothing is persisted.

Full docs: [spec-kit-mcp-server/README.md](spec-kit-mcp-server/README.md)

## Claude Code (dual-agent use)

The same skills install for **Claude Code** from the same sources, so Hermes and
Claude Code can hand phases to each other on one `specs/` tree — e.g. Claude Code
runs `/spec-kit-specify`, `/spec-kit-plan`, `/spec-kit-tasks`, Hermes runs
`spec-kit implement`, Claude Code runs `/spec-kit-summarize`.

```bash
./scripts/install-claude.sh            # → ~/.claude/skills/spec-kit*/SKILL.md + MCP registration
./scripts/install-claude.sh --no-mcp   # skills only
./scripts/install-claude.sh --uninstall
```

What the installer does:

1. Transforms each `src/skills/*.md` into a Claude Code `SKILL.md` — frontmatter
   reduced to `name` / `description` / `argument-hint`, Hermes tool names translated
   (`terminal` → `Bash`, `write_file`/`patch` → `Write`/`Edit`, `read_file` → `Read`,
   `search_files` → `Grep`/`Glob`, `skill_view` → `Skill`, `mcp_spec_kit_*` →
   `mcp__spec-kit__*`), shared-file paths resolved, and a "Claude Code edition" note
   added under the title (arguments, how to load another skill, tool mapping).
2. **Symlinks** `references/`, `templates/` and `mcp-server/` to the installed Hermes
   tree (`~/.hermes/skills/spec-kit/…`), including per-skill `references/` folders —
   one source of truth, so what Hermes reads is what Claude Code reads. Falls back to
   copying from `src/` when Hermes is not installed.
3. Registers the MCP state server for Claude Code at user scope (skipped with `--no-mcp`
   or when already registered).

Invoke in Claude Code as `/spec-kit-specify <feature>`, `/spec-kit-plan <feature>`, …
(`$ARGUMENTS` carries the feature) or by the same natural phrases as in Hermes.
Restart Claude Code after installing. Re-run the installer after editing any
`src/skills/*.md` — the generated files say so in their header and must not be
edited by hand.

## Running Tests

Two test suites validate the project:

**MCP server workflow tests** (11 tests) — exercises the server state machine
via the `mcp` Python SDK client. No Hermes session needed.

```bash
cd spec-kit-mcp-server
pip install mcp
python3 test_workflow.py
```

**Skill validation tests** (12 checks) — validates all skill markdown files:
frontmatter YAML, reference/template file existence, cross-skill links,
phase coverage, pre-flight compliance, and workflow diagram completeness.

```bash
pip install pyyaml
python3 test_skills.py
```

Run both together:

```bash
pip install -r spec-kit-mcp-server/requirements.txt
python3 spec-kit-mcp-server/test_workflow.py && python3 spec-kit-mcp-server/test_skills.py
```

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
- MCP server (optional): deterministic state, compaction-proof, uses `mcp` Python SDK
- Skills fall back to filesystem detection when MCP server is not configured (backward compatible)
