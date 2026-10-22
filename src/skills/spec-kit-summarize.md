---
name: spec-kit-summarize
description: Load when the user says 'spec-kit summarize [feature]', 'speckit summarize [feature]', 'spec-kit close [feature]', 'speckit close [feature]', "summarize [feature]", "close [feature]", or "implementation summary for [feature]" — Phase 6 mandatory close with spec health score.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, summary, review, gap-analysis, close]
    related_skills: [spec-kit-test, spec-kit-workflow, spec-kit-refresh]
---

# spec-kit-summarize

**Phase**: 6 (mandatory close) · **Persona**: thorough auditor — verify every claim against spec, plan and the git diff; detail proportional to the actual change.
**Purpose**: produce `implementation-summary.md` (full, "summarize") or `close.md` (lightweight, "close"); compute spec health; patch spec/plan for intentional deviations with approval; regenerate the plan's Current Design. A feature is not complete without this phase.
**Full procedure**: `spec-kit/references/skills/spec-kit-summarize.md` (gap analysis, health formula, reopen conflict rules).
**Not for**: mid-stream alignment — `spec-kit-refresh`.

## Before writing
- Run `spec-kit/references/preflight.md`. Requires `tasks.md`. Load spec, plan, tasks, bugs, constitution, data-model, contracts, research, quickstart, clarify, history, `evidence/`, `decisions.md` (as present). TDD bypass noted from tasks.md.
- Mode: "close" → `spec-kit/templates/close-template.md`; "summarize" or default → `spec-kit/templates/implementation-summary-template.md`. Reopen (close doc exists) → APPEND a dated section, never overwrite; a requirement that got worse → **WAIT** for the user.
- Output length follows the git diff (`git diff {branch_source} --name-status`), not the size of the spec. The **narrative** of the feature (decisions, deviations, what went wrong) belongs here — history.md holds only the fixed-field record.

## Steps
1. Tasks: count done/remaining; mark completed ones `[X]` only. Bugs: count; **never change a status** here. Open/in-progress bug → **BLOCK** ("run bugfix"). `claimed` without `Verified-by` → list under *Unverified claims*, bugs.md row ⚠️.
2. **Evidence table** (`spec-kit/references/evidence.md`): regression `output:`/`ci:`, a `probe:` per external seam, review label (`review:<agent>` or self-review). No oracle → ❌ unverified, written, never omitted.
3. Gap analysis (full mode): each FR / story / entity / contract → ✅ Resolved (needs an evidence ref) / ⚠️ Acknowledged (reason) / ❌ Not Done. Health = (resolved + acknowledged) / total.
4. Intentional deviations → propose each spec/plan patch; **WAIT** for approval; rejected → ⚠️ needs review.
5. **Regenerate `plan.md` → `## Current Design`** (≤ 1 page, what is BUILT — the one section that is rewritten, not appended); rounds stay as dated records. Assumptions from `decisions.md` → list those still unconfirmed.
6. ❌ Not Done gaps (full mode) → new `open` bugs in bugs.md (`mcp_spec_kit_next_id`). Write the document; fill Artifact/Spec State tables.

## Done when
- [ ] Document written; health computed; Evidence table filled; unverified claims listed; no bug status changed.
- [ ] MCP (optional): `mcp_spec_kit_update_artifact(close.md)` · `mcp_spec_kit_close_feature` (errors on open bugs / verified-without-oracle) · `mcp_spec_kit_lint_artifacts`.
- [ ] history.md entry (phase 6, health %), then ONE commit: close doc + patched spec/plan/data-model — `spec(phase-6): [feature] summary (health: N%)`.

## Next
Feature is **Complete**. Propose `spec-kit-specify` for the next feature, `spec-kit-refresh` on drift, `bugfix [feature]` if gaps became bugs.
