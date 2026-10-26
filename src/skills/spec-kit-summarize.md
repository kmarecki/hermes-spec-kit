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

**Phase**: 6 (mandatory close) · **Persona**: thorough auditor and archivist — verify every claim against spec, plan and the git diff; leave the project's decision record and agent context true; detail proportional to the actual change.
**Purpose**: produce `implementation-summary.md` (full, "summarize") or `close.md` (lightweight, "close"); compute spec health; patch spec/plan for intentional deviations with approval; regenerate the plan's Current Design; **write or update ADRs** for decisions that pass the ADR bar; **keep AGENTS.md current**. A feature is not complete without this phase.
**Full procedure**: `spec-kit/references/skills/spec-kit-summarize.md` (gap analysis, health formula, ADR bar, AGENTS.md sync, reopen rules).
**Not for**: mid-stream alignment — `spec-kit-refresh`.

## Before writing
- Run `spec-kit/references/preflight.md`. Requires `tasks.md`. Load spec, plan, tasks, bugs, constitution, data-model, contracts, research, quickstart, clarify, history, `evidence/`, `decisions.md`, `review-final.md` (as present).
- **Gate**: `review-final.md` latest round must say READY or READY-WITH-FOLLOWUPS and its Reviewed-commit must cover the code (no code commit after it) — else **BLOCK** "run the final review" (`spec-kit-review`). Open/in-progress bug → **BLOCK** ("run bugfix").
- Mode: "close" → `spec-kit/templates/close-template.md`; "summarize" → `spec-kit/templates/implementation-summary-template.md`; neither said → S: close, L: summarize, M: **ASK**. Reopen (close doc exists) → APPEND a dated section, never overwrite.
- Output length follows the git diff (`git diff {branch_source} --name-status`), not the size of the spec.

## Steps
1. Tasks: count; mark completed ones `[X]` only. Bugs: count; **never change a status**. `claimed` without `Verified-by` → *Unverified claims*, bugs.md row ⚠️.
2. **Evidence table** (`spec-kit/references/evidence.md`): regression `output:`/`ci:`, a `probe:` per seam, the final review's verdict + reviewer label. No oracle → ❌ unverified.
3. Gap analysis (full mode; reuse review-final §1 rows): each FR / story / entity / contract → ✅ / ⚠️ / ❌. Health = (resolved + acknowledged) / total. READY-WITH-FOLLOWUPS items → *Open Questions / Future Work*.
4. Intentional deviations → propose each spec/plan patch; **WAIT**; rejected → ⚠️ needs review. Regenerate `plan.md` → `## Current Design` (≤ 1 page, what is BUILT).
5. **ADRs**: harvest decisions (decisions.md rulings, plan Rounds, research decisions, review findings that changed the design, deviations). Apply the ADR bar (full procedure). For each that passes, propose: new ADR (`mcp_spec_kit_next_id(kind="ADR")`, the project's ADR template, else `spec-kit/templates/adr-template.md`), supersede (new ADR + old one's status line → "Superseded by NNNN"), or append Evidence/Related to an existing ADR. **WAIT** per ADR; update the ADR index. Fill the close's *Architecture Decisions* table — "none met the ADR bar" is a valid row.
6. **AGENTS.md** (and CLAUDE.md / agent rule files that restate it): find statements the diff or the new ADRs make wrong or incomplete (commands, layout, boundaries, versions, conventions, known debt, ADR list). Propose targeted patches; **WAIT**; never rewrite the file. Record the result in the close.
7. ❌ Not Done gaps (full mode) → new `open` bugs (`mcp_spec_kit_next_id`). Write the document; fill Artifact/Spec State tables.

## Done when
- [ ] Document written with Evidence, *Architecture Decisions* and AGENTS.md lines; health computed; no bug status changed.
- [ ] MCP: `mcp_spec_kit_close_feature` (errors: open bugs, verified-without-oracle, final review missing/NOT READY/stale, no Architecture Decisions section) · `mcp_spec_kit_lint_artifacts`.
- [ ] history.md entry (phase 6, health %, ADRs), then ONE commit: close doc + patched spec/plan/data-model + ADR files + ADR index + AGENTS.md — `spec(phase-6): [feature] summary (health: N%)`.

## Next
Feature is **Complete**. Propose the PR (the final review drafted its description), `spec-kit-specify` for the next feature, `bugfix [feature]` if gaps became bugs.
