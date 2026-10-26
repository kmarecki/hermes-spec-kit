# spec-kit-plan — full procedure

> **Loaded on demand.** The one-screen `spec-kit-plan` SKILL.md is the entry point; this file holds the complete
> procedure (every branch, template field and pitfall). Read the section you need, not the whole file.
> Tool names: Hermes (`terminal`, `write_file`, `patch`, `read_file`, `skill_view`) — Claude Code maps them to
> `Bash`, `Write`/`Edit`, `Read`, `Skill`; MCP tools are `mcp_spec_kit_*` / `mcp__spec-kit__*`.

**Task Persona**: Adopt the mindset of a system architect and philosopher. Think deeply about tradeoffs, edge cases, failure modes, and scalability. Challenge assumptions. Every requirement must be accounted for — missing details now cause rework later. A thorough plan saves tenfold time in implementation.

**Phase**: 2

**Purpose**: Create or update the implementation plan at `specs/[feature]/plan.md`. Defines **HOW** to implement the spec: architecture, data flow, module boundaries, API contracts.

The plan must:
- **Study existing specs and codebase** to understand current architecture, patterns, and conventions
- **Minimize impact on existing code** — design the implementation with the smallest possible footprint while respecting constitution rules and architecture principles
- **Avoid code-level implementation details** — the plan describes approach and structure, not line-level implementation. Concrete coding belongs in the Implement phase.
- **Resolve constitutional gates** — verify the approach aligns with project principles
- **Generate design artifacts**: `research.md`, `data-model.md`, `contracts/*`, `quickstart.md`

**When NOT to use**: For trivial changes (typo fix, config change) — skip planning and go directly to implementation.

**Routing**: Load this skill when the user says "plan [feature]" or "create plan for [feature]".


**Artifacts**:
- `specs/[feature]/plan.md`
- `specs/[feature]/research.md`
- `specs/[feature]/data-model.md`
- `specs/[feature]/quickstart.md`
- `specs/[feature]/contracts/`

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Validate prerequisites
```
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first"
```

### Load context
```
LOAD specs/[feature]/spec.md
LOAD specs/constitution.md (project-level — provides guidance principles)

IF bugfix mode (reopened bugfix):
  NOTE: "Bugfix mode — plan.md already exists. Will append bugfix sections only."
  LOAD existing specs/[feature]/plan.md
  LOAD bugs.md for bug context
ELIF specs/[feature]/plan.md EXISTS:
  BLOCK: "plan.md already exists for [feature]. The No Complete Overwrite rule
          forbids overwriting it. If you need to add new architecture sections
          (e.g. for a bugfix round), run the relevant workflow instead.
          Route: 'bugfix [feature]' for bugfix additions,
                 'reopen [feature]' for reopening a closed feature."
  HALT
ELSE:
  LOAD spec-kit/templates/plan-template.md
  COPY spec-kit/templates/plan-template.md → specs/[feature]/plan.md
```

### Size tier
Read `**Size**` from spec.md (absent → M; `spec-kit/references/sizing.md`). S → short plan
(Summary, Current Design placeholder, the Technical Context lines that matter, external
seams, Rounds), no research.md / data-model.md / contracts/ / quickstart.md unless the plan
cannot be understood without one. M → only the artifacts the feature needs. L → all that
apply. If the design turns out bigger than the tier (a new seam, another layer), STOP and
ASK to raise the tier; on approval edit the Size line and record the ruling.

### Fill Technical Context
Document: language/version, dependencies, storage, test framework, platform, project type, performance goals, constraints.

### Constitutional Gates (advisory)
Evaluate: simplicity (≤3 projects), anti-abstraction (use framework directly), integration-first (contracts defined).
If gate fails without justification → document as violation in plan.

### Research
Generate `research.md`: decision → rationale → alternatives considered for each technology choice.

### Design & Contracts
Generate `data-model.md`: entities, fields, relationships, validation, state transitions.
Generate `contracts/`: API specs, command schemas.
Generate `quickstart.md`: key validation scenarios.

### Project structure
Choose template: Single project (`src/`, `tests/`) / Web app / Mobile + API.

### Bugfix planning (bugfix mode)
For each open bug: analyze root cause, append ONE dated round under `## Rounds (ADR log)` at the end of plan.md (`### Round N — <date> — <BUG ids> — supersedes: <§ or nothing>` with Context / Decision / Consequences / Plan Ref), set Plan Ref in bugs.md. Do NOT touch `## Current Design` — the close regenerates it from what was built.

**Additive-safe**: Append new bugfix sections at the end of plan.md. Never delete existing plan sections. You may modify existing sections minimally (e.g. mark a section as superseded by a bugfix). If a new fix contradicts an existing plan section, ask the user for guidance.

### MCP checks (optional, when MCP server is configured)

The server keeps no state — it derives the phase from the files and validates.
After writing the artifact(s) and before committing:

```text
CALL mcp_spec_kit_update_artifact(feature="[feature]", artifact="plan.md", status="present")
CALL mcp_spec_kit_advance_phase(feature="[feature]", from_phase=2, artifacts_created=["plan.md"])   # validates; returns the phase card
CALL mcp_spec_kit_lint_artifacts(feature="[feature]")
```

### Append to history.md and Commit

Follow the **Shared Commit Procedure** in `spec-kit/references/preflight.md`:
- Phase: Phase 2 — Plan
- Artifact: `plan.md`, `research.md`, `data-model.md`, `contracts/*`, `quickstart.md`
- Scope: all plan artifacts for this feature
- Message: `"spec(phase-2): [feature] plan"`

### Done When
- [ ] All plan artifacts created (plan.md, research.md, data-model.md, contracts/*, quickstart.md)
- [ ] Bugfix mode: plan sections appended only (additive-only) — existing content preserved
- [ ] history.md entry appended
- [ ] Committed

## Completion
- Generated artifacts list
- Gate status (pass/fail with justifications)
- Propose: `spec-kit-tasks`

### Auto-Chaining (Bugfix Mode)
After plan → automatically route to `spec-kit-tasks` (no user choice).

## Common Pitfalls
1. **Over-engineering simple features**: Not every feature needs research, data-model, and contracts. Generate only what's needed for clarity.
2. **Ignoring constitution gates**: Gates are advisory but flagging violations helps the user understand trade-offs.
3. **Skipping bugfix Plan Ref**: In bugfix mode, always add a Plan Ref to bugs.md — it provides traceability.

## Prerequisite Enforcement
**BLOCKED** if: spec.md does not exist.
