---
name: spec-kit-workflow
description: Master orchestrator for the spec-driven development workflow. Routes requests to appropriate phase skills and maintains workflow state.
category: software-development
---

# Spec Kit Workflow Orchestrator

This is the master orchestrator that routes user requests to the appropriate phase skill.

## Workflow Phases (in order)

|| Phase | Skill | Purpose | Prerequisite |
||:------|:------|:--------|:-------------|
|| 0 | `spec-kit-constitution` | Project principles | None |
|| 1 | `spec-kit-specify` | Feature spec | Constitution |
|| 1.5 | `spec-kit-clarify` | Iterative clarification | Spec |
|| 2 | `spec-kit-plan` | Technical plan | Spec + Constitution |
|| 3 | `spec-kit-tasks` | Task breakdown | Plan |
|| 3.5 | `spec-kit-analyze` | Quality gate (optional) | Tasks |
|| 4 | `spec-kit-implement` | Execute tasks | Tasks |
|| 5 | `spec-kit-test` | Testing & bug tracking | Implement (or spec for bugfix loop) |
|| 6 | `spec-kit-summarize` | Implementation summary | Implement + Test |
|| — | **Bugfix loop** | Test → [Clarify] → Plan → Tasks → [Analyze] → Implement → Test | bugs.md with open bugs |

## Routing Logic

Each skill BLOCKS if prerequisites are not met:
- `spec-kit-constitution`: No prerequisites (phase 0)
- `spec-kit-specify`: Requires `constitution.md`
- `spec-kit-clarify`: Requires `spec.md`
- `spec-kit-plan`: Requires `spec.md` + `constitution.md`
- `spec-kit-tasks`: Requires `plan.md` + `spec.md`
- `spec-kit-analyze`: Requires `tasks.md` + `plan.md` + `spec.md`
- `spec-kit-implement`: Requires `tasks.md`
- `spec-kit-test`: Requires `spec.md` (or existing implementation)
  Bugfix prerequisite: `bugs.md` with at least one open bug
- `spec-kit-summarize`: Requires `tasks.md`

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

### Summarize
- User says: "Summarize [feature]" or "Implementation summary for [feature]"
- Route to: `spec-kit-summarize`

## Phase Detection

Check for artifacts to determine current phase:

|| Artifacts Present | Current Phase |
||:-----------------|:-------------|
|| `constitution.md` only | Ready to Specify |
|| `spec.md` exists | Specified |
|| `clarify.md` exists | Clarifying/Clarified |
|| `plan.md` exists | Planning/Planned |
|| `tasks.md` exists | Tasking/Tasked |
|| `tasks.md` with completions | Implementing |
|| `bugs.md` with open bugs | Testing (bugfix loop) |
|| `bugs.md` all verified | Testing complete |
|| `implementation-summary.md` exists | Summarized — complete |
|| All tasks complete + all bugs verified | Complete |

## Bugfix Routing

### Start bugfix loop
- User says: "bugfix [feature]" or "fix bugs in [feature]"
- LOAD `specs/[feature]/bugs.md`
- FOR each bug with Status: open or in-progress:
  - IF Requires Clarification checkbox "yes" is checked: ROUTE to `spec-kit-clarify` first, then automatically chain to plan → tasks → implement
  - ELSE: ROUTE to `spec-kit-plan` directly
- AFTER plan → AUTOMATICALLY route to `spec-kit-tasks`
- AFTER tasks → AUTOMATICALLY route to `spec-kit-implement`
- DEFAULT route: `spec-kit-plan` → `spec-kit-tasks` → `spec-kit-implement` (automatic chain, no user choice)
- NOTE: Analyze is optional — only run if user explicitly asks for it

### Test phase
- User says: "Test [feature]"
- Route to: `spec-kit-test`
- NOTE: When user reports a bug during testing, `spec-kit-test` always logs it to `bugs.md` — never implement directly

### Verify bug
- User says: "Verify [BUG-ID] in [feature]"
- Route to: `spec-kit-test` (mark bug as verified)

## Usage Examples

- "Create a spec for user authentication"
- "What phase is 003-user-auth in?"
- "Plan the implementation for 003-user-auth"
- "Clarify ambiguities in 003-user-auth"
- "Generate tasks for 003-user-auth"
- "Analyze 003-user-auth for issues"
- "Implement 003-user-auth"
- "Test 003-user-auth"
- "bugfix 003-user-auth"
- "Verify BUG-001 in 003-user-auth"
- "Bug status 003-user-auth"
- "Summarize 003-user-auth"

## Phase Guardrails — STRICT

You MUST determine the current phase before any tool call. Each phase has strict limits:

| Phase | Allowed to Write | Code-Editing Tools | Detect By |
|-------|-----------------|-------------------|-----------|
| **Constitution** | `constitution.md` only | BLOCKED | `specs/constitution.md` exists, no `spec.md` |
| **Specify** | `spec.md`, `checklists/requirements.md` | BLOCKED | `specs/NNN-name/spec.md` exists, no `plan.md` |
| **Clarify** | `clarify.md`, `spec.md` (amend) | BLOCKED | `clarify.md` exists |
| **Plan** | `plan.md`, `research.md`, `data-model.md`, `contracts/*`, `quickstart.md` | BLOCKED | `plan.md` exists, no `tasks.md` |
| **Tasks** | `tasks.md` only | BLOCKED | `tasks.md` exists, no completions |
| **Analyze** | None (read-only) | BLOCKED | User says "analyze" |
| **Implement** | source code, `tasks.md` (completions), `bugs.md` (mark resolved) | ALLOWED | `tasks.md` with pending tasks |
| **Test** | `bugs.md` only | BLOCKED | `bugs.md` with open bugs |
| **Summarize** | `implementation-summary.md`, `tasks.md` (finalize), `bugs.md` (finalize) | BLOCKED | `implementation-summary.md` missing |

> **Bugfix loop**: reuses Plan, Tasks, and Implement — same permissions, just with `bugs.md` as additional input context.

### Enforcement Rules
- `write_file`/`patch`/`terminal` for builds → **ONLY** during Implement (including bugfix loop implementations)
- Writing to spec artifacts (`spec.md`, `plan.md`, `tasks.md`, `bugs.md`) → only during their respective phase
- Unknown phase → ASK the user
- User asks for code outside Implement → REFUSE, suggest correct phase
