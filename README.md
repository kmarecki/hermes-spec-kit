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

## Usage

### Starting a New Feature

```
User: "Create a spec for user authentication with OAuth2"
Agent: Loads spec-kit-workflow skill, creates spec directory, generates spec.md
```

### Continuing an Existing Feature

```
User: "What phase is 006-multi-layered-visualizer in?"
Agent: Reads spec directory, checks task completion, reports status
```

### Implementing Tasks

```
User: "Implement the next tasks for 006-multi-layered-visualizer"
Agent: Loads tasks.md, finds next incomplete task, executes with TDD
```

## Related Projects

- [JRedeker/cline-spec-kit-workflows](https://github.com/JRedeker/cline-spec-kit-workflows) - Original Cline workflow files
- [juanklagos/spec-driven-development-template](https://github.com/juanklagos/spec-driven-development-template) - SDD framework with MCP support
- [Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs) - Hermes Agent documentation
