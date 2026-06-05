# Hermes Spec Kit — Agent Instructions

This file provides project-level context for Hermes Agent when working on the spec-kit repository itself. Always read these guidelines before making changes.

## Project Overview

Hermes Spec Kit is a **spec-driven development (SDD) workflow system** for Hermes Agent. It implements a structured, phase-based approach to software development:

```
Constitution → Specify → Clarify (opt) → Plan → Tasks → Implement
```

Each phase produces documented markdown artifacts under `specs/NNN-feature-name/`. All phase transitions are manual.

## Key Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview, usage, quick start |
| `design.md` | System architecture and design decisions |
| `workflow.md` | Phase-by-phase workflow reference |
| `skills.md` | Skill file reference and routing |
| `automation.md` | Cron jobs, delegation, and automation patterns |
| `migration.md` | Migration from OpenCode/Cline spec kit |
| `AGENT.md` | This file — agent project context |
| `src/skills/*.md` | Source skill files (installed via install.sh) |
| `src/templates/` | Template files for spec artifacts |
| `scripts/install.sh` | Installs skills + templates to ~/.hermes/skills/ |
| `templates/` | Auto-generated copies (do NOT edit directly) |

## Skill Map

Skills live in `src/skills/` and are installed to `~/.hermes/skills/`:

- `spec-kit-workflow` — Master orchestrator, routes requests to phase skills
- `spec-kit-constitution` — Phase 0: Project principles and constraints
- `spec-kit-specify` — Phase 1: Feature specification creation
- `spec-kit-clarify` — Phase 1.5: Ambiguity resolution (optional)
- `spec-kit-plan` — Phase 2: Implementation planning
- `spec-kit-tasks` — Phase 3: Task breakdown generation
- `spec-kit-analyze` — Phase 3.5: Quality gate review (optional)
- `spec-kit-checklist` — N: Quality checklists (optional)
- `spec-kit-implement` — Phase 4: Task execution with TDD
- `spec-kit-test` — Phase 5: Testing & bug tracking

## Template Management

Templates live in `src/templates/`. They get installed to `~/.hermes/skills/spec-kit/templates/` by `./scripts/install.sh`.

- **Do NOT** edit files in `templates/` directly — that directory mirrors installed copies.
- Edit source files in `src/templates/` instead.
- After editing source templates, run `./scripts/install.sh` to update the installed copies.

The `AGENTS-template.md` is meant to be copied to a project root as a starting `AGENTS.md` for projects *using* spec-kit. It is **not** the AGENT.md for this repo.

## Phase State Detection

To determine a feature's current phase, check which artifacts exist:

| Artifacts Present | Interpretation |
|---|---|
| constitution.md only | Ready to Specify |
| spec.md exists | Specified |
| clarify.md exists | Clarifying/Clarified |
| plan.md exists | Planning/Planned |
| tasks.md exists | Tasking/Tasked |
| tasks.md with completions | Implementing |
| All tasks complete | Complete |
| bugs.md with open bugs | Testing (bugfix loop) |
| bugs.md all verified | Testing complete |
| All tasks complete + all bugs verified | Complete |

## Conventions

- Spec numbering: `NNN-feature-name` (sequential, 3 digits)
- Branch naming: `feature/NNN-feature-name` or `NNN-feature-name`
- Commit messages: `spec: [phase] - [feature name]`
- Tasks format: `[ID] [P?] [Story] Description`
  - `[P]` = can run in parallel
  - `[Story]` = user story tag like US1, US2
- Each skill is self-contained and idempotent — re-running updates its artifact without affecting downstream phases

## Installation

```bash
./scripts/install.sh
```

After installation, reload skills in Hermes:
```
/reload-skills
```

Or create a skill bundle:
```bash
hermes bundles create speckit \
  --skill spec-kit-workflow \
  --skill spec-kit-constitution \
  --skill spec-kit-specify \
  --skill spec-kit-clarify \
  --skill spec-kit-plan \
  --skill spec-kit-tasks \
  --skill spec-kit-analyze \
  --skill spec-kit-checklist \
  --skill spec-kit-implement \
  --skill spec-kit-test
```

## Hermes Slash Command Limitation

Hermes Agent does **not** support user-extensible slash commands with argument parsing. Skills are exposed as `/skill-name` but only inject markdown text into context. Natural language routing is the intended workflow.

## Related Projects

- [JRedeker/cline-spec-kit-workflows](https://github.com/JRedeker/cline-spec-kit-workflows) — Original Cline workflow files
- [juanklagos/spec-driven-development-template](https://github.com/juanklagos/spec-driven-development-template) — SDD framework with MCP support
- [Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs) — Hermes Agent documentation

## Communication Style

Concise. Show commands over explanations. Confirm before pushing or merging. Ask for clarification when blocked.
