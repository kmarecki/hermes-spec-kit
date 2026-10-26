---
name: spec-kit-plan
description: Load when the user says 'spec-kit plan [feature]', 'speckit plan [feature]', "plan [feature]", "plan the implementation for [feature]", or "design the architecture for [feature]" — Phase 2 technical planning for the feature.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, planning, architecture, design]
    related_skills: [spec-kit-specify, spec-kit-tasks, spec-kit-workflow]
---

# spec-kit-plan

**Phase**: 2 · **Persona**: system architect — trade-offs, failure modes, smallest footprint on existing code; a thorough plan saves tenfold in implementation.
**Purpose**: create `specs/[feature]/plan.md` (+ `research.md`, `data-model.md`, `contracts/`, `quickstart.md`) — HOW: architecture, data flow, module boundaries, API contracts. Approach and structure, not line-level code.
**Full procedure**: `spec-kit/references/skills/spec-kit-plan.md`.
**Not for**: trivial changes — implement directly.

## Before writing
- Run `spec-kit/references/preflight.md`. **BLOCK** if `spec.md` is missing.
- Load `spec.md`, `specs/constitution.md` (guidance, not a gate); study the existing codebase for patterns and conventions.
- `plan.md` exists and not bugfix mode → **BLOCK** (No Complete Overwrite; route `bugfix`/`reopen`). Bugfix mode → load `plan.md` + `bugs.md`, append only.

## Steps
1. New plan: copy `spec-kit/templates/plan-template.md`. Fill Technical Context (language, deps, storage, tests, platform, project type, performance, constraints, scale).
2. Constitution gates (advisory): simplicity, anti-abstraction, integration-first — document violations with justification.
3. Read `**Size**` from spec.md (`spec-kit/references/sizing.md`). S → short plan, no research/data-model/contracts/quickstart unless indispensable. M → only the artifacts the feature needs. L → all that apply. Scope bigger than the tier → stop and **ASK** to raise it. `research.md`: decision → rationale → alternatives, per technology choice.
4. `## Acceptance Test Strategy` in plan.md: per AC the level, harness, test file, environment it needs and where its result (JUnit/TRX) lands (`spec-kit/references/acceptance.md`). `data-model.md` (entities, fields, relations, validation, state transitions); `contracts/` (API/command schemas); `quickstart.md` (key validation scenarios). Name every **external seam** (database function, HTTP contract, file format) the feature touches — implement will probe each one.
5. Project structure: single / web / mobile+API.
6. Every design question you cannot put to the user → `decisions.md` assumption (`spec-kit/templates/decisions-template.md`); a real ruling quotes the user.
7. Bugfix mode: per open bug, root cause → append ONE dated round under `## Rounds (ADR log)` at the END of `plan.md`: `### Round N — <date> — <BUG ids> — supersedes: <§ or nothing>` with Context / Decision / Consequences / Plan Ref → set `Plan Ref` in `bugs.md`. Never edit earlier rounds or `## Current Design` (the close regenerates it); a contradiction with the current design → say so in *supersedes* and ask the user.

## Done when
- [ ] All needed plan artifacts written; bugfix mode: appended only.
- [ ] MCP (optional): `mcp_spec_kit_update_artifact(plan.md)` · `mcp_spec_kit_advance_phase(from_phase=2)` · `mcp_spec_kit_lint_artifacts` → 0 errors.
- [ ] history.md entry, then commit — Shared Commit Procedure in `spec-kit/references/preflight.md`: scope all plan artifacts; message `spec(phase-2): [feature] plan` (bugfix: `spec(phase-2): [feature] bugfix plan (BUG-NNN, …)`).

## Next
Report artifacts + gate status; propose `spec-kit-tasks`. Bugfix mode and size S: route to `spec-kit-tasks` automatically.
