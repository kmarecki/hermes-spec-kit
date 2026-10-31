---
name: spec-kit-summarize
description: >
  Load when the user says 'spec-kit summarize [feature]', 'speckit summarize [feature]', 'spec-kit close [feature]', 'speckit close [feature]', "summarize [feature]", "close [feature]", or "implementation summary for [feature]" — Phase 6 mandatory close: spec health score, ADRs written/updated, AGENTS.md kept current.
version: 2.0.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, summary, review, gap-analysis, close]
    related_skills: [spec-kit-test, spec-kit-workflow, spec-kit-refresh]
---

# spec-kit-summarize

**Phase**: 6 (mandatory close) · **Persona**: auditor and archivist — verify every claim against spec, plan and the diff; leave the decision record and agent context true; detail proportional to the diff.
**Purpose**: `close.md` (S/M: "close"; L: "summarize" = full gap table) **+ `change-record.md`** (the auditor's page); spec health; approved deviation patches; regenerate the plan's Current Design; ADRs that pass the bar; AGENTS.md kept current. Not complete without this phase.
**Full procedure**: `spec-kit/references/skills/spec-kit-summarize.md` (gap analysis, health, ADR bar, AGENTS.md sync, reopen) · **Not for**: mid-stream alignment → `spec-kit-refresh`.

## Before writing
- `spec-kit/references/preflight.md`. Requires `tasks.md`. Load spec, plan, tasks, bugs, constitution, data-model, contracts, research, clarify, `history.md`, `evidence/`, `decisions.md`, `acceptance.md`, `review-final.md`.
- **Gate**: latest `review-final.md` round READY / READY-WITH-FOLLOWUPS and not stale — else **BLOCK** ("run the final review"; AWAITING-OWNER → get the owner's answer, Round N+1). Open bug → **BLOCK**.
- Mode: "close" / "summarize" as said; else S/M → close, L → summarize. Reopen (close doc exists) → APPEND a dated section.

## Steps
1. Tasks: count, mark done ones `[X]` only. Bugs: count; **never change a status**; `claimed` without `Verified-by` → *Unverified claims*.
2. **Evidence table** (`spec-kit/references/evidence.md`): acceptance/regression `output:`/`ci:`, a `probe:` per seam, the final review's verdict + reviewer label. No oracle → ❌ unverified.
3. Gaps: M → exceptions only; L → every FR / story / entity / contract. Health = (resolved + acknowledged) / total. Follow-ups from the review → *Open questions*.
4. Deviations → propose each spec/plan patch; **WAIT**; rejected → ⚠️ needs review. Regenerate `plan.md` → `## Current Design` (≤ 1 page, what is BUILT).
5. **ADRs**: harvest (decisions.md rulings, plan Rounds, research, review findings, deviations); apply the ADR bar; per candidate propose new / supersede / append-evidence (`mcp_spec_kit_next_id(kind="ADR")`, project template else `spec-kit/templates/adr-template.md`); **WAIT** per ADR; update the index. Fill *Architecture Decisions* — "none met the bar" is a valid row.
6. **AGENTS.md** (+ CLAUDE.md / rule files): statements the diff or new ADRs make wrong (commands, layout, boundaries, versions, conventions, debt, ADR list) → targeted patches; **WAIT**; never rewrite.
6a. **Runbooks + changelog** (only what git-conventions keeps: `runbooks_dir`, `changelog`): runbook statements the diff makes wrong (commands, settings, endpoints, procedures) → targeted patches, **WAIT**; one *Unreleased* line in the changelog (Keep a Changelog: Added / Changed / Fixed, one sentence, the ticket) — no narrative.
6b. **Design doc + epic row** (only when `specs/git-conventions.md` sets `design_dir` / `epics_dir`; else skip in one line): for each module in plan.md `**Modules**:` → the `[design_dir]/[module].md` sections the diff makes wrong (components, flow, seams, invariants, debt) → targeted patches + a change-log line; **WAIT** per patch; a module without a doc → say so, never create one here (`spec-kit-design`). `**Epic**:` in spec.md → set this feature's row in `[epics_dir]/[epic]/features.md` (status closed, PR, health, ADRs) and the epic's row in `[epics_dir]/README.md` when `epics_index: on`; last row → suggest `close epic`.
7. **`change-record.md`** from `spec-kit/templates/change-record-template.md`: ticket, branch/PR, size, what/why, Security & Privacy impact (from spec), data/config changes, implemented-by, reviewed-by (agent + human PR reviewer or `pending`), verification, decisions, deployment approval (or `pending`), rollback, follow-ups; **Timeline** = one row per `history.md` entry (history on) or `spec-kit/scripts/spec-kit-history.sh [feature]` run now on the branch (history off — before the squash).
8. ❌ Not Done gaps → new `open` bugs. Write `close.md` from `spec-kit/templates/close-template.md`.

## Done when
- [ ] close.md + change-record.md written (no `pending` field left blank); health computed; no bug status changed; design doc / epic row patched or "none kept" recorded.
- [ ] MCP: `mcp_spec_kit_close_feature` · `mcp_spec_kit_lint_artifacts` → 0 errors.
- [ ] history.md entry when on (`Phase 6`, health %, ADRs), then ONE commit: close doc, change record, patched spec/plan/data-model, ADRs + index, AGENTS.md, runbooks, changelog line, design doc, epic + index rows — `spec(phase-6): [feature] close (health: N%)`.

## Next
Feature **Complete**. Propose the PR (description drafted by the final review; the human reviewer's name goes into the change record when known), `spec-kit-specify` for the next feature, `bugfix [feature]` if gaps became bugs.
