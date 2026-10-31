---
name: spec-kit-refresh
description: Load when the user says 'spec-kit refresh [feature]', 'speckit refresh [feature]', "refresh [feature]", "sync spec for [feature]", or "align artifacts for [feature]" — standalone artifact reconciliation for outdated specs.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, refresh, alignment, reconciliation]
    related_skills: [spec-kit-summarize, spec-kit-workflow]
---

# spec-kit-refresh

**Phase**: standalone · **Persona**: auditor reconciling intent with reality — flag, propose, get approval; never over-correct.
**Purpose**: bring `spec.md`, `plan.md`, `data-model.md`, `contracts/` back in line with the code after manual changes — no close document, no health score (that is `spec-kit-summarize`).

## Steps
1. Preflight (`spec-kit/references/preflight.md`); requires `spec.md`. Load the artifacts and `git diff {branch_source} --name-status` (`specs/git-conventions.md`, default main).
2. Per FR-### and per plan / data-model / contract item: Match / Mismatch / Missing / Unplanned.
3. ≤ 5 discrepancies per session: "spec says … / code does … → update spec to match code?" **WAIT** for each; never bulk-apply.
4. Apply approved patches only — additive or targeted, nothing deleted. May regenerate `plan.md` → `## Current Design`.

## Done when
- [ ] Every patch approved before applying. Commit (`spec-kit/references/commits.md`): `spec(refresh): [feature] reconcile artifacts`.
