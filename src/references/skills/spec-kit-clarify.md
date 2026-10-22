# spec-kit-clarify — full procedure

> **Loaded on demand.** The one-screen `spec-kit-clarify` SKILL.md is the entry point; this file holds the complete
> procedure (every branch, template field and pitfall). Read the section you need, not the whole file.
> Tool names: Hermes (`terminal`, `write_file`, `patch`, `read_file`, `skill_view`) — Claude Code maps them to
> `Bash`, `Write`/`Edit`, `Read`, `Skill`; MCP tools are `mcp_spec_kit_*` / `mcp__spec-kit__*`.

**Task Persona**: Adopt the mindset of a curious detail-gatherer. Ambiguities hide assumptions that cause rework. Ask precise, targeted questions. Probe edge cases, constraints, and unstated expectations. Do not proceed until the ambiguity is resolved — uncertain specs produce broken code.

**Phase**: 1.5

**Purpose**: Identify and resolve underspecified areas in the current feature spec through a structured Q&A dialog.

**When NOT to use**: For straightforward specs with no ambiguities — proceed to Plan directly.

**Routing**: Load this skill when the user says "clarify [feature]" or "resolve ambiguities". If loaded directly, load spec-kit-workflow first to check prerequisites.
 Do NOT ask questions for the sake of process.

**Artifacts**:
- `specs/[feature]/clarify.md`
- Updated `specs/[feature]/spec.md` (with resolved ambiguities)

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Validate prerequisites
```
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first"
```

### Load spec
```
LOAD specs/[feature]/spec.md
IF bugfix mode: LOAD bugs.md, filter for bugs needing clarification
```

### Ambiguity scan
Check: Functional scope, domain model, UX flow, non-functional attributes, integrations, edge cases, terminology.

### Generate questions (max 5 per session)
One question at a time. Each answerable via multiple choice (2-5 options) or short answer.

### Sequential questioning loop
For each question: present → wait → validate → record.
After each answer: UPDATE spec.md, replace `[NEEDS CLARIFICATION]` markers.

### Generate clarify.md
```markdown
# Clarification Log: [Feature]
## Q1: [Question]
**Answer**: [Selected]
**Resolution**: [How applied to spec]
```

### Repeat
After answer, loop: next question → answer → update spec.md.

### Append to history.md and Commit

Follow the **Shared Commit Procedure** in `spec-kit/references/preflight.md`:
- Phase: Phase 1.5 — Clarify
- Artifact: `clarify.md`, `spec.md` (amended)
- Scope: `specs/[feature]/clarify.md`, `spec.md`
- Message: `"spec(phase-1.5): [feature] clarifications"`

## Completion
- Propose: `spec-kit-plan`

## Common Pitfalls
1. **Asking unnecessary questions**: If the answer is obvious from context, don't ask. The user's time is valuable.
2. **More than 5 questions**: Keep sessions focused. Unanswered questions can be addressed in a second session.
3. **Not updating the spec**: After each answer, immediately update spec.md. The clarify.md is a log; spec.md is the source of truth.

## Prerequisite Enforcement
**BLOCKED** if: spec.md does not exist (run `spec-kit-specify` first).
