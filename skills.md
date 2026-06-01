# Skill Reference

Each workflow phase is implemented as a standalone skill file. Skills are installed from `src/skills/` into `~/.hermes/skills/` via `./scripts/install.sh`.

## Skill Map

| Skill | Phase | Purpose |
|-------|-------|---------|
| `spec-kit-workflow` | — | Master orchestrator — routes requests to phase skills |
| `spec-kit-constitution` | 0 | Project principles and constraints |
| `spec-kit-specify` | 1 | Feature specification creation |
| `spec-kit-clarify` | 1.5 | Ambiguity resolution (optional) |
| `spec-kit-plan` | 2 | Implementation planning |
| `spec-kit-tasks` | 3 | Task breakdown generation |
| `spec-kit-analyze` | 3.5 | Quality gate review (optional) |
| `spec-kit-checklist` | N | Checklists (optional, not a gate) |
| `spec-kit-implement` | 4 | Task execution |

## Workflow Phases

```
Constitution → Specify → Clarify (opt) → Plan → Tasks → Implement
```

All phase transitions are manual. Checklists are optional — they guide quality but do not block progression.

## Phase Routing

When the user requests spec kit operations, the agent:

1. **New Feature**: "Create a spec for [description]" → loads `spec-kit-specify`
2. **Existing Feature Status**: "What phase is [feature] in?" → analyzes spec directory
3. **Advance Phase**: "Plan [feature]" / "Generate tasks for [feature]" / "Implement [feature]" → loads appropriate phase skill
4. **Clarify**: "Clarify [feature]" → loads `spec-kit-clarify`
5. **Project Constitution**: "Create constitution" → loads `spec-kit-constitution`

## Skill Files

All skill files live in `src/skills/` and are installed to `~/.hermes/skills/`:

```
src/skills/
  spec-kit-workflow.md
  spec-kit-constitution.md
  spec-kit-specify.md
  spec-kit-clarify.md
  spec-kit-plan.md
  spec-kit-tasks.md
  spec-kit-analyze.md
  spec-kit-checklist.md
  spec-kit-implement.md
```

Each skill is self-contained, idempotent, and can be re-run to update its output without affecting downstream phases.

## Idempotency

Each skill can be re-run safely. Re-running a skill updates its own artifact; downstream artifacts remain valid. This allows the user to go back and revise any phase without invalidating later phases.

## Phase State Detection

To determine the current phase of a feature, check which artifacts exist:

| Artifacts Present | Interpretation |
|----------------|---------------|
| constitution.md only | Ready to Specify |
| spec.md exists | Specified |
| clarify.md exists | Clarifying/Clarified |
| plan.md exists | Planning/Planned |
| tasks.md exists | Tasking/Tasked |
| tasks.md with completions | Implementing |
| All tasks complete | Complete |

## Project Setup

### AGENTS.md

Use `src/templates/AGENTS-template.md` as the starting `AGENTS.md` for projects using spec-kit. Copy it to the project root at the beginning. Spec-kit does NOT auto-update AGENTS.md — maintain the SPECKIT section manually as specs progress.

### Constitution

Run `spec-kit-constitution` first for a new project. This creates `specs/constitution.md` (or `.specify/memory/constitution.md` per official spec-kit convention) with project principles. All plans must address these principles.

## Templates

Templates are in `src/templates/`. Each template is a standalone markdown file:

```
src/templates/
  AGENTS-template.md       # Starting AGENTS.md for new projects
  constitution-template.md
  spec-template.md
  plan-template.md
  tasks-template.md
  checklist-template.md   # Both spec quality + implementation checklists
  research-template.md
  data-model-template.md
```

Templates are installed alongside skills via `./scripts/install.sh`.