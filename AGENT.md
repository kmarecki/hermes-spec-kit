# Hermes Spec Kit — Agent Instructions

Project-level context for Hermes Agent when working on the spec-kit repository. Read before making changes.

## Project Overview

A **spec-driven development (SDD) workflow system** for Hermes Agent. 13 skills implementing two development modes:

- **Specify** (default): Constitution → Specify → [Clarify] → Plan → Tasks → Implement → Test → Close
- **Bugfix**: Test → [Clarify] → Plan → Tasks → Implement → Test → Close (auto-chain inner loop)

## Key Files

| File | Purpose |
|------|---------|
| `user-guide.md` | Complete workflow documentation |
| `README.md` | Project overview and quick start |
| `AGENT.md` | This file — agent project context |
| `src/skills/*.md` | 12 source skill files (installed via install.sh) |
| `src/skills/spec-kit/SKILL.md` | Umbrella skill overview |
| `src/templates/` | 13 template files |
| `src/references/` | Reference files (auto-commit.md) |
| `scripts/install.sh` | Installs skills + templates + references |

## Skills (12)

| Skill | Phase | Purpose |
|-------|-------|---------|
| spec-kit-workflow | — | Orchestrator — routes requests to phases |
| spec-kit-constitution | 0 | Project principles (mandatory before specify/plan) |
| spec-kit-specify | 1 | Feature specification |
| spec-kit-clarify | 1.5 | Ambiguity resolution (optional) |
| spec-kit-plan | 2 | Implementation planning |
| spec-kit-tasks | 3 | Task breakdown (asks user about TDD) |
| spec-kit-implement | 4 | Phase-level TDD execution |
| spec-kit-test | 5 | Bug tracking (manual) |
| spec-kit-summarize | 6 | Close/summary (mandatory) |
| spec-kit-refresh | — | Artifact alignment |

## Key Behaviors

- **Constitution is mandatory** — specify and plan block without it
- **Design phases (0-3) do not auto-commit** — batch commit at start of Phase 4
- **Phase-level TDD** — all tests RED first, all code GREEN, one commit per phase
- **TDD bypass** — user asked at task generation, tracked in tasks.md header
- **Umbrella regression** — one BF-REGRESSION-001 task, not individual bugs
- **Phase 6 mandatory** — feature cannot complete without close or summary
- **Spec health score** — computed at close: (resolved + acknowledged) / total * 100
- **Analyze works from spec.md alone** — plan/tasks optional for richer analysis

## Template Management

Templates in `src/templates/` installed to `~/.hermes/skills/spec-kit/templates/`.
Edit source files in `src/templates/`, run `./scripts/install.sh` to deploy.

## Phase State Detection

| Artifacts Present | Phase |
|---|---|
| constitution.md only | Ready to Specify |
| spec.md exists | Specified |
| clarify.md exists | Clarified |
| plan.md exists | Planned |
| tasks.md exists | Tasked |
| tasks.md with completions | Implementing |
| bugs.md with open bugs | Testing |
| bugs.md all verified | Testing complete — must close |
| implementation-summary.md or close.md exists | Complete |

## Conventions

- Spec numbering: `NNN-feature-name` (sequential, 3 digits)
- Branch naming: `feature/NNN-feature-name`, `fix/NNN-name`
- Commit messages: see `src/references/auto-commit.md`
- Design phases: NO individual commits (batch at Phase 4)
- Implementation: one commit per phase

## Installation

```bash
./scripts/install.sh
```

Then `/reload-skills` in Hermes.

## Communication Style

Concise. Show commands over explanations. Confirm before destructive operations. Ask for clarification when blocked.

**Never restructure existing working skills without explicit user consent.** One new file = one new file.
