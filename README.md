# Hermes Spec-Kit

Spec-driven development for Hermes Agent. 14 skills implementing a structured phase-based workflow with three development modes, phase-level TDD, and mandatory close with spec health scoring.

## Quick Start

```bash
./scripts/install.sh                    # Install skills + templates
# In Hermes: /reload-skills
# Then: "Create a spec for [feature]"
```

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
