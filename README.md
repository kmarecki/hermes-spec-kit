# Hermes Spec-Kit

Spec-driven development for Hermes Agent. 14 skills implementing a structured phase-based workflow with four development modes, phase-level TDD, mandatory close with spec health scoring, and a reopen flow for fixing closed features.

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
- **src/templates/** — 15 templates (installed to `~/.hermes/skills/spec-kit/templates/`)
- **src/references/** — Supporting reference files (preflight.md, auto-commit.md, history-tracking.md — installed to `~/.hermes/skills/spec-kit/references/`)

## Project Structure

```
src/
  skills/                # Skill source files (13 .md files)
    spec-kit/SKILL.md    # Umbrella skill — overview and quick reference
  templates/             # Template source files (15 templates)
  references/            # Reference files (preflight.md, auto-commit.md, history-tracking.md)
scripts/
  install.sh             # Installs to ~/.hermes/skills/
```

## Four Development Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Specify** (default) | "Create a spec for [feature]" | Full forward phase sequence, manual transitions |
| **Bugfix** | "bugfix [feature]" | Auto-chain inner loop (Plan→Tasks→Implement), mandatory close |
| **Explore** | "Explore [feature] with [variants]" | N parallel branches, compare, pick winner |
| **Reopen** | "Reopen [feature]" | Reopens closed feature for bugfixing, additive-only edits, routes through bugfix loop |

## Skills (14)

`workflow`, `constitution`, `specify`, `clarify`, `plan`, `tasks`, `review`, `implement`, `test`, `summarize`, `refresh`, `explore`, `compare`, `umbrella`

Each skill responds to three trigger styles: `spec-kit` prefix, `speckit` prefix, and natural language
(e.g. `spec-kit plan 001-user-auth`, `speckit plan 001-user-auth`, or `"plan the implementation for 001-user-auth"`).

## Key Design Decisions

- Constitution is always optional (warn, don't block)
- Design phases (0-3) do not auto-commit — batch commit at start of implementation
- Phase-level TDD: all tests RED first, all code GREEN, then commit
- TDD bypass at user request during task generation
- One umbrella regression fix task, not individual bugs
- Phase 6 (Close) is mandatory before feature completion
- Spec health score computed at close (0-100%)
- Review works at three points: pre-implement (cross-artifact), post-implement (code quality), and closed-review (read-only audit)
- Branch guardrails block git operations on main/master
- Pre-action self-check in every skill (branch, mode, workflow)
- Git conventions are externalized to `specs/git-conventions.md` (copy template per project)
- Reopen mode creates bugfix branch, additive-only edits, preserves original close data
- `history.md` append-only transition log for phase detection and audit trail
