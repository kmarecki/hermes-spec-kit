# spec-kit-specify — full procedure

> **Loaded on demand.** The one-screen `spec-kit-specify` SKILL.md is the entry point; this file holds the complete
> procedure (every branch, template field and pitfall). Read the section you need, not the whole file.
> Tool names: Hermes (`terminal`, `write_file`, `patch`, `read_file`, `skill_view`) — Claude Code maps them to
> `Bash`, `Write`/`Edit`, `Read`, `Skill`; MCP tools are `mcp_spec_kit_*` / `mcp__spec-kit__*`.

**Task Persona**: Adopt the mindset of a curious detail-gatherer. Your job is to extract every relevant detail from the user before writing anything. Ask clarifying questions. Probe edge cases. Challenge vague statements. A complete spec answers WHAT and WHY — the HOW comes later. Every requirement must be testable.

**Phase**: 1

**Purpose**: Create or update a feature specification at `specs/[feature]/spec.md`. Defines **WHAT** users need and **WHY** — the feature, refactoring, or enhancement in full detail. Captures functional requirements (FR-###), user scenarios, success criteria, entities, and edge cases. 

**No implementation details, no code, no technology choices.** The spec describes what the system should do, not how to build it. Architecture decisions, data models, and technical approach belong in the Plan phase.

**When NOT to use**: For tiny unambiguous changes (typo fix, rename), skip straight to implementation.

**Routing**: Load this skill when the user says "create a spec for [feature]" or "specify [feature]".


**Artifacts**:
- `specs/[feature]/spec.md`

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Validate prerequisites
```
IF specs/[feature]/spec.md EXISTS:
  BLOCK: "spec.md for [feature] already exists. The No Complete Overwrite rule
          forbids overwriting it. If you need to modify the spec for bugfix,
          run: 'bugfix [feature]' or 'reopen [feature]'."
  HALT
```

### Parse user description
- Extract: actors, actions, data, constraints
- If empty: ERROR "No feature description provided"

### Generate short name
2-4 word action-noun format: "user-auth", "oauth2-api-integration"

### Create feature directory
```
DETERMINE prefix (next sequential number: 001, 002...)
CREATE: specs/[###]-[short-name]/
```

### Generate spec.md
Copy `spec-kit/templates/spec-template.md` → `specs/[feature]/spec.md`

Populate with:
- **User Scenarios**: P1/P2/P3 with Given/When/Then
- **Functional Requirements**: FR-001, FR-002... — testable, technology-agnostic
- **Success Criteria**: Measurable outcomes
- **Key Entities**: Domain objects only (no implementation)
- **Edge Cases**: Error conditions, boundaries

### Ask for the size tier (ALWAYS)
```
SCORE the signals in spec-kit/references/sizing.md (layers, files, seams, dependencies,
  security/money/tenancy, expected tasks, unknowns) → RECOMMENDED = the highest tier any
  signal triggers
ASK the user — every time, even when the answer looks obvious:
  "Size for [feature]?"
    1. <RECOMMENDED> (Recommended) — <the signals that triggered it>
    2./3. the other two tiers, each with one line on what it produces
       (S: short spec/plan/tasks auto-chained, no pre-review; M: default artifacts;
        L: full artifacts + required pre-implement review)
  (Claude Code: AskUserQuestion with the recommended option first, labelled "(Recommended)")
WRITE "**Size**: <answer> — <reason>" in the spec.md header
RECORD a ruling in decisions.md quoting the answer; the user picked a tier other than the
  recommendation → note the recommendation too. No human to ask → record RECOMMENDED as an
  assumption (preflight check 7) and continue.
```

### Size S: auto-chain
```
IF Size == S AND the user has confirmed the spec:
  RUN spec-kit-plan (short plan, no research/data-model/contracts/quickstart unless
    indispensable) and spec-kit-tasks (flat list; the TDD question is still asked)
  ONE history entry per phase, ONE commit for the three: "spec(phase-1-3): [feature] spec, plan, tasks"
```

### Apply constraints
- MAX 3 `[NEEDS CLARIFICATION]` markers
- NO implementation details (tech stack, frameworks, APIs)
- Prioritize: scope > security > UX > technical


### MCP checks (optional, when MCP server is configured)

The server keeps no state — it derives the phase from the files and validates.
After writing the artifact(s) and before committing:

```text
CALL mcp_spec_kit_init_feature(feature="[feature]", name="[name]")   # creates the dir + history.md header (skip if it exists)
CALL mcp_spec_kit_update_artifact(feature="[feature]", artifact="spec.md", status="present")   # confirms the file is on disk
CALL mcp_spec_kit_advance_phase(feature="[feature]", from_phase=1, artifacts_created=["spec.md"])   # validates; returns the phase card
CALL mcp_spec_kit_lint_artifacts(feature="[feature]")   # must report 0 errors before the commit
```

### Append to history.md and Commit

Follow the **Shared Commit Procedure** in `spec-kit/references/preflight.md`:
- Phase: Phase 1 — Specify
- Artifact: `specs/[feature]/spec.md`
- Scope: `specs/[feature]/spec.md`
- Message: `"spec(phase-1): [feature] spec"`

### Done When
- [ ] spec.md created with FR-### requirements numbered sequentially
- [ ] The user was asked for the size (recommendation first); `**Size**:` line written; ruling in decisions.md
- [ ] No existing content deleted; modifications minimal (additive-safe)
- [ ] history.md entry appended
- [ ] Committed

## Completion
- Feature directory path, spec file path
- Propose: `spec-kit-clarify` or `spec-kit-plan`

## Common Pitfalls
1. **Implementation details in spec**: Focus on user value. Move architecture decisions to the Plan phase.
2. **Too many `[NEEDS CLARIFICATION]` markers**: Keep to 3 max. If more, the feature scope is too vague — clarify with the user first.
3. **Over-specifying**: For simple features, a single paragraph + 2-3 FRs is enough. Don't force full template on trivial changes.

## Prerequisite Enforcement
**BLOCKED** if: spec.md for this feature already exists (No Complete Overwrite rule).
