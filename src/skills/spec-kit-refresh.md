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
**Purpose**: bring `spec.md`, `plan.md`, `data-model.md`, `contracts/` back in line with the code after manual changes, without a close document or health score.
**Full procedure**: `spec-kit/references/skills/spec-kit-refresh.md`.
**Not for**: closing a feature — `spec-kit-summarize`.

## Before writing
- Run `spec-kit/references/preflight.md`. Requires `spec.md`.
- Load the artifacts and `git diff {branch_source} --name-status` (`branch_source` from `specs/git-conventions.md`, default main).

## Steps
1. Per FR-### and per plan/data-model/contract item: compare spec text with actual code → Match / Mismatch / Missing / Unplanned.
2. Present at most 5 discrepancies per session: "spec says … / code does … → update spec to match code?" **WAIT** for each yes/no; never bulk-apply.
3. Apply approved patches only; additive or targeted edits, nothing deleted. May regenerate the plan's `## Current Design` section.

## Done when
- [ ] Every patch approved before applying; history.md entry (pre-commit guard), then commit — Shared Commit Procedure in `spec-kit/references/preflight.md`: scope patched artifacts; message `spec(refresh): [feature] reconcile artifacts`.

| | summarize | refresh |
|---|---|---|
| Output | close / summary document | in-place patches |
| Health score | computed | not computed |
| When | end of feature | mid-stream |
