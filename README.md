# Hermes Spec-Kit

Spec-driven development for Hermes Agent. 14 skills implementing a structured phase-based workflow with four development modes, phase-level TDD, mandatory close with spec health scoring, and a reopen flow for fixing closed features.

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

## Skills

14 skills covering every phase + explore, compare, refresh, and workflow routing.
See the [Phase Reference section](user-guide.md#phase-reference) in the user-guide for phases, purposes, and personas.

All skills respond to three trigger styles: `spec-kit` prefix, `speckit` prefix, and natural language
(e.g. `spec-kit plan 001-user-auth`, `speckit plan 001-user-auth`, or `"plan the implementation for 001-user-auth"`).

## Key Design Decisions

- Constitution is mandatory for all features — specify and plan block if missing
- Design phases (0-3) do not auto-commit — batch commit at start of implementation
- Phase-level TDD: all tests RED first, all code GREEN, then commit
- TDD bypass at user request during task generation
- One umbrella regression fix task, not individual bugs
- Phase 6 (Close) is mandatory before feature completion
- Spec health score computed at close (0-100%)
- Branch guardrails block git operations on main/master
- Pre-action self-check in every skill (branch, mode, workflow)
