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

**Phase**: 1 · **Persona**: curious detail-gatherer — extract WHAT and WHY; every requirement testable; the HOW comes later.
**Purpose**: create `specs/[feature]/spec.md` — functional requirements (FR-###), user scenarios, success criteria, entities, edge cases. No implementation details, no technology choices.
**Full procedure**: `spec-kit/references/skills/spec-kit-specify.md` — read a section when a step below is unclear.
**Not for**: tiny unambiguous changes (typo, rename) — implement directly.

## Before writing
- Run `spec-kit/references/preflight.md` (branch, mode, logged-bug check, git conventions, phase card, history.md).
- Do not load `spec-kit-workflow` here — it is for routing commands (bugfix / reopen / status) only.

## Steps
1. **BLOCK** if `specs/[feature]/spec.md` exists (No Complete Overwrite) → say: run `bugfix [feature]` or `reopen [feature]`.
2. Parse the description into actors, actions, data, constraints. Empty description → error.
3. Short name (2–4 words, action-noun) + next sequential number → `specs/NNN-short-name/` (MCP: `mcp_spec_kit_init_feature`).
4. Copy `spec-kit/templates/spec-template.md`; fill User Scenarios (P1/P2/P3, Given/When/Then), FR-### (testable, technology-agnostic), Success Criteria (measurable), Key Entities (domain only), Edge Cases.
5. At most 3 `[NEEDS CLARIFICATION]` markers — more means the scope is too vague: ask first. Priority: scope > security > UX > technical. Simple feature → one paragraph + 2–3 FRs.

## Done when
- [ ] spec.md written, FR-### sequential, nothing deleted.
- [ ] MCP (optional): `mcp_spec_kit_update_artifact(spec.md)` · `mcp_spec_kit_advance_phase(from_phase=1)` · `mcp_spec_kit_lint_artifacts` → 0 errors.
- [ ] history.md entry appended, then commit — Shared Commit Procedure in `spec-kit/references/preflight.md`: scope `specs/[feature]/spec.md`, message `spec(phase-1): [feature] spec`.

## Next
Propose `spec-kit-clarify` (markers remain) or `spec-kit-plan`.
