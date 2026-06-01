---
name: spec-kit-workflow
description: Master orchestrator for the spec-driven development workflow. Routes requests to appropriate phase skills and maintains workflow state.
category: software-development
---

# Spec Kit Workflow Orchestrator

This is the master orchestrator that routes user requests to the appropriate phase skill.

## Workflow Phases (in order)

| Phase | Skill | Purpose | Prerequisite |
|:------|:------|:--------|:-------------|
| 0 | `spec-kit-constitution` | Project principles | None |
| 1 | `spec-kit-specify` | Feature spec | Constitution |
| 1.5 | `spec-kit-clarify` | Iterative clarification | Spec |
| 2 | `spec-kit-plan` | Technical plan | Spec + Constitution |
| 3 | `spec-kit-tasks` | Task breakdown | Plan |
| 3.5 | `spec-kit-analyze` | Quality gate (optional) | Tasks |
| 4 | `spec-kit-implement` | Execute tasks | Tasks |

## Routing Logic

### New Feature
- User says: "Create a spec for [description]"
- Route to: `spec-kit-specify`

### Existing Feature
- User says: "What phase is [feature] in?"
- Check `specs/[feature]/` directory structure
- Report current phase

### Advance Phase
- User says: "Plan [feature]"
- Route to: `spec-kit-plan`

### Clarify Ambiguities
- User says: "Clarify [feature]"
- Route to: `spec-kit-clarify`

### Constitution
- User says: "Create constitution"
- Route to: `spec-kit-constitution`

### Analyze
- User says: "Analyze [feature]"
- Route to: `spec-kit-analyze`

### Implement
- User says: "Implement [feature]"
- Route to: `spec-kit-implement`

## Phase Detection

Check for artifacts to determine current phase:

| Artifacts Present | Current Phase |
|:-----------------|:-------------|
| `constitution.md` only | Ready to Specify |
| `spec.md` exists | Specified |
| `clarify.md` exists | Clarifying/Clarified |
| `plan.md` exists | Planning/Planned |
| `tasks.md` exists | Tasking/Tasked |
| `tasks.md` with completions | Implementing |
| All tasks complete | Complete |

## Skill Routing

### New Feature
- User says: "Create a spec for [description]"
- Route to: `spec-kit-specify`

### Existing Feature
- User says: "What phase is [feature] in?"
- Check `specs/[feature]/` directory structure
- Report current phase

### Advance Phase
- User says: "Plan [feature]"
- Route to: `spec-kit-plan`

### Clarify Ambiguities
- User says: "Clarify [feature]"
- Route to: `spec-kit-clarify`

### Constitution
- User says: "Create constitution"
- Route to: `spec-kit-constitution`

### Analyze
- User says: "Analyze [feature]"
- Route to: `spec-kit-analyze`

### Implement
- User says: "Implement [feature]"
- Route to: `spec-kit-implement`

Each skill BLOCKS if prerequisites are not met:
- `spec-kit-constitution`: No prerequisites (phase 0)
- `spec-kit-specify`: Requires `constitution.md`
- `spec-kit-clarify`: Requires `spec.md`
- `spec-kit-plan`: Requires `spec.md` + `constitution.md`
- `spec-kit-tasks`: Requires `plan.md` + `spec.md`
- `spec-kit-analyze`: Requires `tasks.md` + `plan.md` + `spec.md`
- `spec-kit-implement`: Requires `tasks.md`

## Usage Examples

- "Create a spec for user authentication"
- "What phase is 003-user-auth in?"
- "Plan the implementation for 003-user-auth"
- "Clarify ambiguities in 003-user-auth"
- "Generate tasks for 003-user-auth"
- "Analyze 003-user-auth for issues"
- "Implement 003-user-auth"