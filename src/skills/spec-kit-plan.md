---
name: spec-kit-plan
description: Load when the user says 'spec-kit plan [feature]', 'speckit plan [feature]', "plan [feature]", "plan the implementation for [feature]", or "design the architecture for [feature]" — Phase 2 technical planning for the feature.
version: 1.2.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, planning, architecture, design]
    related_skills: [spec-kit-specify, spec-kit-tasks, spec-kit-workflow]
---

# spec-kit-plan

**Phase**: 2 · **Persona**: system architect — trade-offs, failure modes, smallest footprint on existing code.
**Purpose**: `specs/[feature]/plan.md` (+ `research.md`, `data-model.md`, `contracts/`, `quickstart.md` when the tier needs them) — HOW: architecture, data flow, boundaries, seams, acceptance test strategy. Approach, not line-level code.
**Full procedure**: `spec-kit/references/skills/spec-kit-plan.md` · **Not for**: trivial changes.

## Before writing
- `spec-kit/references/preflight.md`. **BLOCK** if `spec.md` is missing. Load `spec.md`, `specs/constitution.md` (guidance), the codebase's patterns.
- `plan.md` exists and not bugfix mode → **BLOCK** (`bugfix` / `reopen`). Bugfix mode → append only.

## Steps
1. Copy `spec-kit/templates/plan-template.md`; Technical Context — only the lines that matter. `design_dir` kept → `**Modules**:` names the design docs the close will patch — take them from the module map `[design_dir]/README.md` by the paths the feature touches (read them first — they describe what is built).
2. Tier from spec.md (`spec-kit/references/sizing.md`): S → Summary, Current Design, Seams, Acceptance strategy, Rounds; M → + Design, and research / data-model / contracts / quickstart only when needed; L → all that apply. Bigger than the tier → stop, **ASK** to raise it.
3. Constitution gates (advisory) — violations justified in Complexity Tracking.
4. **External Seams** table — every DB function, HTTP contract, message, file format the feature touches (implement probes each). **Acceptance Test Strategy** — per AC: level, harness, test file, needs, result source (`spec-kit/references/acceptance.md`). The Security & Privacy rows of the spec get a design answer here (where the check lives). Deployed-env ACs → settled here, ONE PR (`acceptance.md` §2).
5. `research.md`: decision → rationale → alternatives, per real technology choice only.
6. Questions the user would want to decide → ASK; no human → `decisions.md` assumption. Design choices within the plan's remit stay in plan.md.
7. Bugfix mode: per open bug, root cause → ONE dated round under `## Rounds (ADR log)` (Context / Decision / Consequences / Plan Ref) → set `Plan Ref` in `bugs.md`. Never edit earlier rounds or `## Current Design`.

## Done when
- [ ] Plan artifacts for the tier written; bugfix: appended only.
- [ ] MCP: `mcp_spec_kit_update_artifact(plan.md)` · `mcp_spec_kit_advance_phase(from_phase=2)` · `mcp_spec_kit_lint_artifacts` → 0 errors.
- [ ] history.md entry, then commit (`spec-kit/references/preflight.md` procedure): `spec(phase-2): [feature] plan` (bugfix: `… bugfix plan (BUG-NNN, …)`).

## Next
`spec-kit-tasks` (bugfix mode and size S: automatically).
