# Hermes Spec Kit

A spec-driven development workflow system for Hermes Agent, migrated from the Cline/OpenCode spec kit pattern.

## Overview

This system implements a structured, phase-based approach to software development using Hermes Agent's skills, delegation, and automation capabilities. It enforces a disciplined workflow:

**Constitution -> Specify -> Clarify -> Plan -> Tasks -> Implement**

Each phase produces documented artifacts before proceeding to the next, ensuring quality and traceability.

## Quick Start

1. Load the `spec-kit-workflow` skill in your Hermes Agent session
2. Say: "Create a spec for [feature description]"
3. Follow the guided phases through implementation

## File Structure

```
hermes-spec-kit/
  README.md              # This file
  design.md              # System architecture and design decisions
  workflow.md            # Workflow phases and execution flow
  skills.md              # Skill reference
  automation.md          # Cron jobs, delegation, and automation patterns
  src/skills/            # Skill files (installed to ~/.hermes/skills/)
  src/templates/         # Artifact templates
    AGENTS-template.md       # Starting AGENTS.md for spec-kit projects
    constitution-template.md
    spec-template.md
    plan-template.md
    tasks-template.md
    checklist-template.md
    research-template.md
    data-model-template.md
  scripts/
    install.sh           # Installs skills + templates to ~/.hermes/skills/
```

## Templates

Templates live in `src/templates/`. They are installed to `~/.hermes/skills/spec-kit/templates/` by `./scripts/install.sh`. Do not edit `templates/` directly.

- `AGENTS-template.md` — copy this to your project root as the starting `AGENTS.md` file. Spec-kit does NOT auto-update it; maintain the SPECKIT section manually as specs progress.
- `*template.md` — used by skills to generate spec artifacts. Do not edit these directly.

## Core Concepts

### Spec-Driven Development

Every feature starts with a specification, not code. The spec defines:
- What the feature does (user scenarios)
- How success is measured (acceptance criteria)
- What constraints exist (non-functional requirements)

### Phase Advancement

Each phase must produce documented artifacts before proceeding to the next. Phase transitions are manual — the user decides when to advance.

### Technology-Agnostic Specifications

Specs focus on user value and business needs, not implementation details. Technical decisions happen in the Plan phase.

### TDD Enforcement

Implementation tasks are organized to write tests before code, with explicit test tasks marked in the task breakdown.

## Hermes Agent Advantages Over OpenCode/Cline

| Feature | OpenCode/Cline | Hermes Agent |
|---------|----------------|--------------|
| Skill persistence | Session-only workflows | Persistent skills in ~/.hermes/skills/ |
| Multi-agent | Single agent | Parallel delegation for research/design |
| Automation | Manual phase progression | Cron jobs + automated validation |
| Memory | Context window only | Persistent cross-session memory |
| Portability | Agent-specific (.clinerules) | Universal skills |
| Project context | CLAUDE.md only | AGENTS.md + workdir + profile support |
| Slash commands | `/speckit.specify`, `/speckit.plan` — full commands with args | `/skill-name` loads skill text only, no arg parsing |

## Slash Command Limitation

Hermes Agent does **not** have a user-extensible slash command system like OpenCode. Skills installed in `~/.hermes/skills/` are automatically exposed as `/skill-name` commands, but they only **inject the skill's markdown text into context** — they do not execute the skill with parsed arguments.

| What you might expect | What actually happens |
|------------------------|------------------------|
| `/spec-kit-specify "user auth"` | Typing `/spec-kit-specify` loads the skill text. You then type "create a spec for user auth" as a normal message. |
| `/speckit plan 006` | No equivalent. Use "Plan 006-multi-layered-visualizer" as a normal message. |
| `/speckit.implement` | No dot-notation subcommands. Each skill is its own slash command. |

The Hermes `COMMAND_REGISTRY` is a hardcoded Python list in `hermes_cli/commands.py`. There is no config-driven or file-driven way for users to register new slash commands with argument parsing. The `quick_commands` field in `config.yaml` exists but is unimplemented.

**Workaround:** Use natural language. The `spec-kit-workflow` skill routes phrases like "Create a spec for ...", "Plan ...", "Implement ..." to the correct phase skill. See examples below.

## Usage

### Starting a New Feature

```
User: "Create a spec for user authentication with OAuth2"
Agent: Loads spec-kit-workflow skill, routes to spec-kit-specify, creates spec directory, generates spec.md
```

### Continuing an Existing Feature

```
User: "What phase is 006-multi-layered-visualizer in?"
Agent: Reads spec directory, reports current phase based on artifacts present

User: "Plan 006-multi-layered-visualizer"
Agent: Loads spec-kit-plan skill, generates plan.md, research.md, data-model.md

User: "Generate tasks for 006-multi-layered-visualizer"
Agent: Loads spec-kit-tasks skill, generates tasks.md

User: "Implement 006-multi-layered-visualizer"
Agent: Loads spec-kit-implement skill, executes tasks with TDD
```

### Using Slash Commands (Context Injection)

```
/spec-kit-workflow     — loads the orchestrator skill text
/spec-kit-specify      — loads the specify skill text
/spec-kit-plan         — loads the plan skill text
/spec-kit-tasks        — loads the tasks skill text
/spec-kit-implement    — loads the implement skill text
```

After typing a slash command, the skill instructions appear in context. You then type a normal message to execute the skill.

### Using Skill Bundles

Group all spec-kit skills under a single slash command:

```
hermes bundles create speckit \
  --skill spec-kit-workflow \
  --skill spec-kit-constitution \
  --skill spec-kit-specify \
  --skill spec-kit-clarify \
  --skill spec-kit-plan \
  --skill spec-kit-tasks \
  --skill spec-kit-analyze \
  --skill spec-kit-checklist \
  --skill spec-kit-implement
```

Then use `/speckit` to load all spec-kit skills at once. Same limitation applies — slash commands inject text, they don't execute with arguments.

### Reloading After Installation

After running `./scripts/install.sh`, reload skills in your Hermes session:

```
/reload-skills
```

## Related Projects

- [JRedeker/cline-spec-kit-workflows](https://github.com/JRedeker/cline-spec-kit-workflows) - Original Cline workflow files
- [juanklagos/spec-driven-development-template](https://github.com/juanklagos/spec-driven-development-template) - SDD framework with MCP support
- [Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs) - Hermes Agent documentation
