---
name: spec-kit-specify
description: Load when the user says 'spec-kit specify [feature]', 'speckit specify [feature]', 'spec-kit spec [feature]', 'speckit spec [feature]', "create a spec for [description]", "create specification for [feature]", or "write a spec for [feature]" — Phase 1 feature specification.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, specification, requirements, features]
    related_skills: [spec-kit-constitution, spec-kit-clarify, spec-kit-workflow]
---

# spec-kit-specify

**Phase**: 1 · **Persona**: curious detail-gatherer — WHAT and WHY, every requirement testable; the HOW comes later.
**Purpose**: create `specs/[feature]/spec.md` — user scenarios, FR-###, AC-### (Given/When/Then + verify level), Security & Privacy, success criteria, edge cases. No technology choices.
**Full procedure**: `spec-kit/references/skills/spec-kit-specify.md` · **Not for**: typo / rename / config value.

## Before writing
- `spec-kit/references/preflight.md`. **BLOCK** if `spec.md` exists → `bugfix` / `reopen`.
- Do not load `spec-kit-workflow` (routing only).

## Steps
1. Parse the description into actors, actions, data, constraints; empty → error.
2. Name: 2–4 words action-noun + next number → `specs/NNN-short-name/` (MCP: `mcp_spec_kit_init_feature`).
3. Copy `spec-kit/templates/spec-template.md`. Fill stories (P1/P2/P3), FR-### (testable, technology-agnostic), **Security & Privacy table** (every row answered — "None — because …" is valid), SC-###, entities, edge cases.
4. **ACs** (`spec-kit/references/acceptance.md`): every scenario and important edge case → `**AC-###** (FR-…) Given/When/Then — Verify: <lowest level that proves it>`; every FR named by ≥ 1 AC; ids `mcp_spec_kit_next_id(kind="AC")`.
5. ≤ 3 `[NEEDS CLARIFICATION]` markers — more → ask first. Priority: scope > security > UX > technical.
6. `epics_dir` kept (`specs/git-conventions.md`) → `**Epic**: <name>` in the header (ASK which, or none); the epic must be reviewed (`[epics_dir]/<name>/review.md` GO) — its `features.md` row gets this spec dir and size now (add the row if missing, with approval).
7. **Size — ASK** (`spec-kit/references/sizing.md`; rigor lean → default S, ask only when a signal says M+, `spec-kit/references/rigor.md`): score the signals, offer S/M/L with the recommendation first "(Recommended)" + reason + what each produces. Write `**Size**: X — <reason>`; ruling in `decisions.md` (unattended → assumption).
7a. `compliance: baseline` (git-conventions) → **Security level — ASK** beside the size (`spec-kit/references/compliance.md` §1): none / low / medium / high, recommendation first from the signals. Write `**Security**: X — <reason>`; none → the table is that line; medium/high → the extended rows. The level adds security evidence on top of the process level (§6), never changes it.
8. Size S (single bugfix / small enhancement): the spec is a few lines — 1–3 FRs, 1–2 ACs, one Security & Privacy line. After the user confirms it: auto-chain `spec-kit-plan` → `spec-kit-tasks`, ONE commit `spec(phase-1-3): [feature] spec, plan, tasks`.

## Done when
- [ ] spec.md written; FR/AC ids ascending; Security & Privacy filled; `**Size**:` (and with `compliance: baseline` `**Security**:`) set from the user's answer.
- [ ] MCP: `mcp_spec_kit_update_artifact(spec.md)` · `mcp_spec_kit_advance_phase(from_phase=1)` · `mcp_spec_kit_lint_artifacts` → 0 errors.
- [ ] history.md entry, then commit (preflight commit procedure): `spec(phase-1): [feature] spec`.

## Next
Markers remain → `spec-kit-clarify`; else `spec-kit-plan`. S: plan + tasks chained → `spec-kit-implement`. L: plan, then the pre-implement review is required.
