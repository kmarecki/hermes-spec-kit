# Hermes Spec-Kit

Spec-driven development for Hermes Agent. 14 skills implementing a structured phase-based workflow with three development modes, phase-level TDD, and mandatory close with spec health scoring.

## Quick Start

```bash
# 1. Clone the repository anywhere on your machine
git clone https://github.com/kmarecki/hermes-spec-kit.git
cd hermes-spec-kit

# 2. Install skills + templates to ~/.hermes/skills/
./scripts/install.sh

# 3. In your Hermes session, reload skills:
/reload-skills
# (or start a new Hermes session)

# 4. Navigate to your project and start working:
cd /path/to/your-project
# Then in Hermes: "Create a spec for [feature]"
```

## Installation From Scratch (New Project)

```
# 1. Clone the spec-kit repository (anywhere — it's not tied to your project)
git clone https://github.com/kmarecki/hermes-spec-kit.git ~/hermes-spec-kit

# 2. Install globally (one-time)
cd ~/hermes-spec-kit
./scripts/install.sh
# This copies all skills and templates to ~/.hermes/skills/
# Installation is global — one install covers all projects and sessions

# 3. Initialize your project directory
cd /path/to/my-new-project
git init                           # or clone an existing repo
mkdir specs/                       # spec-kit looks for specs/ at project root

# 4. In a Hermes session, reload skills
/reload-skills

# 5. Create your first feature spec
#    In Hermes, inside your project directory:
"Create a constitution for my-project"
"Create a spec for user authentication"
```

## Prerequisites

- **Hermes Agent** installed and configured (`hermes` command available)
- **Git** repository in your project directory (spec-kit creates branches, commits, and workflow logs)
- The project directory should have a `specs/` directory at the root (created automatically when you create the first spec)

## Documentation

- **[user-guide.md](user-guide.md)** — Complete workflow description, all phases, TDD integration, artifact lifecycle
- **src/skills/** — 13 skill files + 1 umbrella SKILL.md (installed to `~/.hermes/skills/`)
- **src/templates/** — 13 templates (installed to `~/.hermes/skills/spec-kit/templates/`)
- **src/references/** — Supporting reference files (installed to `~/.hermes/skills/spec-kit/references/`)

## Project Structure

```
src/
  skills/                # Skill source files (13 .md files)
    spec-kit/SKILL.md    # Umbrella skill — overview and quick reference
  templates/             # Template source files
  references/            # Reference files (auto-commit.md, preflight.md)
scripts/
  install.sh             # Installs to ~/.hermes/skills/
```

## Three Development Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Specify** (default) | "Create a spec for [feature]" | Full forward phase sequence, manual transitions |
| **Bugfix** | "bugfix [feature]" | Auto-chain inner loop (Plan→Tasks→Implement), mandatory close |
| **Explore** | "Explore [feature] with [variants]" | N parallel branches, compare, pick winner |

## Skills (14)

`workflow`, `constitution`, `specify`, `clarify`, `plan`, `tasks`, `review`, `implement`, `test`, `summarize`, `refresh`, `explore`, `compare`, `umbrella`

## Key Design Decisions

- Constitution is always optional (warn, don't block)
- Design phases (0-3) do not auto-commit — batch commit at start of implementation
- Phase-level TDD: all tests RED first, all code GREEN, then commit
- TDD bypass at user request during task generation
- One umbrella regression fix task, not individual bugs
- Phase 6 (Close) is mandatory before feature completion
- Spec health score computed at close (0-100%)
- Review works at two points: pre-implement (cross-artifact) and post-implement (code quality)
- Branch guardrails block git operations on main/master
- Pre-action self-check in every skill (branch, mode, workflow)
