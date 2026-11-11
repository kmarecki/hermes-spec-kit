---
name: spec-kit-review
description: >
  Load when the user says 'spec-kit review [feature]', 'speckit review [feature]', 'spec-kit final review [feature]', 'speckit final review [feature]', "review [feature]", "final review [feature]", "merge readiness [feature]", "is [feature] ready to merge", "quality check [feature]", or "analyze [feature]" — pre-implement cross-artifact check (3.5) and the mandatory final merge-readiness review (5.5): spec conformance, constitution rules, code quality, merge checklist.
version: 2.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, review, quality, consistency, code-review]
    related_skills: [spec-kit-tasks, spec-kit-implement, spec-kit-workflow, spec-kit-constitution]
---

# spec-kit-review

**Phase**: 3.5 (pre-implement) / 5.5 (final — **mandatory before close**) / closed-review · **Persona**: senior architect and last reviewer before merge — structural problems, spec drift, broken rules, security; not a style checker.
**Purpose**: pre-implement = does spec/plan/tasks hold together and fit the codebase (report). **Final** = does the code do what the spec says, obey the rules, is it good, is it mergeable → `review-final.md` round whose verdict gates the close. Both include a **devil's advocate** pass.
**Full procedure**: `spec-kit/references/skills/spec-kit-review.md` · template `spec-kit/templates/review-final-template.md`.

## Before reviewing
- Preflight checks 1 and 4 (`spec-kit/references/preflight.md`). Mode: close doc → closed-review; tasks.md and no code → pre-implement; all tasks `[X]`, no open bug → **final**; open bugs → refuse ("bugfix first"); unclear → **ASK**.
- PROCESS LEVEL from the phase card (`spec-kit/references/rigor.md`, size × rigor): **P1** → no pre-implement review; final = a **self-check round** ≤ 30 lines (checklist commands + diff scan, one line per section, the floor's oracle quoted, §4 inline by the same reviewer, Verdict + Reviewed-commit) · **P2** → lite pre-implement **with** devil's advocate; final exceptions-only ≤ 80 lines, §4 optional, round N+1 = the delta since round N · **P3** → full pre-implement; both devil's advocates by a **different agent**; final ≤ 150 lines by the other agent; strict L needs `**Approved-by**:` a named human. Objections are never capped. S skips the stack research; acceptance is checked the same way at every level.
- **Author check** (`spec-kit/references/evidence.md`): `Implemented-by` (history.md implement entries, or the tasks.md header when history is off; the phase card lists them) **includes** you → *self-review*, even if another agent did other phases; for the final review prefer the other agent, else a **fresh-context sub-agent** (procedure + feature path + base only; no transcript).
- Final review: read the code and the spec **before** `decisions.md` so the author's reasoning does not anchor you; then every assumption is a review item.

## Pre-implement (3.5)
1. Load spec, plan, tasks, constitution, the epic's cross-feature rules and the modules' design docs when the project keeps them; requirement ↔ task coverage; the Security & Privacy table answered in the plan.
2. M (lite): underspecification, coverage gaps, codebase fit, design soundness. L: + duplication, ambiguity, naming, completeness, inconsistency, best practice (research the stack).
3. **Devil's advocate**: the strongest case against the plan + a simpler alternative; a pre-mortem ("three months later it failed — why?"); abuse cases per new seam (authz, tenant crossover, input, data exposure, logging); the riskiest assumptions in decisions.md. ≤ 5 objections, each answered: accepted / rebutted with evidence / deferred. L: run it as a separate sub-agent (different model when available).
4. Report + commit `spec(review): [feature] review findings`. CRITICAL → resolve before implement.

## Final (5.5) — one `## Round N` appended, **exceptions only**
1. Inputs: spec, plan, tasks, data-model, contracts, constitution, `specs/merge-checklist.md` (missing → from `spec-kit/templates/merge-checklist-template.md`, **ASK** to confirm), AGENTS.md / rule files, `git diff <base>...HEAD`, `evidence/`, bugs.md, acceptance.md.
2. Mechanical: `mcp_spec_kit_diff_scan(feature)` → `evidence/final-diff-scan.txt`; every checklist command → `evidence/final-<check>.txt` (exit 126/127, missing tool or network → *could not run*: ASK, never a finding) — `review_run: ci | pr` → CI / the PR's checks are the evidence (full procedure), the rest locally; `ci:<id>` for the reviewed commit. Only specs/docs changed since a green `ci:<id>` → cite it, no re-run.
3. **§1** — one coverage line (FR n/N, SC, edge cases, acceptance round PASS @ sha, frozen unchanged) + rows ONLY for ⚠️ / ❌ / ↔ / 👤. Missing = CRITICAL; ↔ → **WAIT** (patch spec, log a bug, or defer). Manual / deferred ACs unconfirmed → 👤.
4. **§2** — every applicable constitution MUST, checklist P-item, AGENTS.md rule, epic cross-feature rule, design-doc invariant, **spec Security & Privacy row**, `[SEC]` task, threat-model row and S-item (`compliance: baseline`) verdicted with `path:line`; violated MUST = HIGH (CRITICAL if security / data / non-negotiable).
5. **§3** — findings on the changed code: architecture, error chains, security, data integrity, concurrency, duplication, complexity, API surface, tests (behaviour not implementation; fixtures match `probe:` files; RED/GREEN files per phase). Stack research: M/L.
6. **§4 Devil's advocate** — try to break it with concrete inputs (another tenant's id, empty/stale period, concurrent edit, failing dependency, unauthorized role); "would this test still pass if the code were wrong?"; argue the opposite of the verdict. P3: a different agent. `compliance: baseline`: Security medium+ → abuse cases per Security row; high → the security pass by a different agent at every level (`spec-kit/references/compliance.md` §6). Every objection answered; unanswered blocks READY at P3.
7. **§5** checklist table with evidence files. **Verdict**: CRITICAL/HIGH or blocking ❌ → `NOT READY`; no defect but owner confirmations pending, or Security high without a human `**Approved-by**:` → `AWAITING-OWNER`; MEDIUM / non-blocking only → `READY-WITH-FOLLOWUPS`; else `READY`. Write `**Verdict**:` and `**Reviewed-commit**:`.
8. NOT READY → bugs for each CRITICAL/HIGH (`mcp_spec_kit_next_id`), confirm with the user → `bugfix [feature]`, new round. AWAITING-OWNER → ask the owner; their quoted answer → specs-only Round N+1 (no code change ⇒ not stale). §6: PR description incl. "strongest objections and how they were answered".

## Severity
CRITICAL / HIGH / MEDIUM only; a finding must harm correctness, security, performance, maintainability or testability — style and taste → delete. A broken explicit project rule is never a nitpick.

## Done when
- [ ] Pre: report, history entry when on (`Phase 3.5`), commit. Final: round with Verdict + Reviewed-commit, §2 rules verdicted, §4 objections answered, §5 evidence; `mcp_spec_kit_lint_artifacts` → 0 errors; history entry when on (`Phase 5.5`), commit `spec(review): [feature] final review (verdict: X)`. Closed-review: report only, no history entry.

## Next
Pre → `spec-kit-implement`. Final READY / READY-WITH-FOLLOWUPS → `spec-kit-summarize`. AWAITING-OWNER → the owner, then Round N+1. NOT READY → `bugfix [feature]`.
