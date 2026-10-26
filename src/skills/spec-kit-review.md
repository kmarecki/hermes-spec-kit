---
name: spec-kit-review
description: >
  Load when the user says 'spec-kit review [feature]', 'speckit review [feature]', 'spec-kit final review [feature]', 'speckit final review [feature]', "review [feature]", "final review [feature]", "merge readiness [feature]", "is [feature] ready to merge", "quality check [feature]", or "analyze [feature]" — pre-implement cross-artifact check (3.5) and the mandatory final merge-readiness review (5.5): spec conformance, constitution rules, code quality, merge checklist.
version: 2.0.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, review, quality, consistency, code-review]
    related_skills: [spec-kit-tasks, spec-kit-implement, spec-kit-workflow, spec-kit-constitution]
---

# spec-kit-review

**Phase**: 3.5 (pre-implement) / 5.5 (final — **mandatory before close**) / closed-review · **Persona**: senior architect and the last reviewer before merge — structural problems, spec drift, broken project rules, security; not a style checker.
**Purpose**: pre-implement = spec/plan/tasks coherence + codebase fit + best practice (report). **Final** = does the code do what the spec says, does it obey the constitution and project rules, is it good code, is the branch mergeable → `review-final.md` with a verdict that gates close. Closed-review = final checks on a closed feature, history untouched.
**Full procedure**: `spec-kit/references/skills/spec-kit-review.md` (passes A–M, final-review steps, report formats, severity rules). Template: `spec-kit/templates/review-final-template.md`.

## Before reviewing
- Preflight checks 1 and 4 (`spec-kit/references/preflight.md`). Mode: close doc exists → closed-review; tasks.md and no code → pre-implement; all tasks `[X]` and no open/in-progress bug → **final**; open bugs → refuse ("run bugfix first"); unclear → **ASK**.
- **Author check** (`spec-kit/references/evidence.md`): `Implemented-by` in history.md = you → *self-review*. For the final review prefer the other agent; otherwise run it in a **fresh-context sub-agent** (no implementation transcript) and label `self-review by <agent> (fresh context)`.
- Read `decisions.md` first: every assumption is a review item. Size from spec.md (`spec-kit/references/sizing.md`): L requires a pre-implement review before implement.

## Pre-implement
1. Load spec, plan, tasks, constitution; build requirement↔task coverage.
2. Passes: duplication, ambiguity, underspecification, constitution alignment, naming, completeness, coverage gaps, inconsistency, bugfix coverage, **codebase fit**, **best practice** (research the stack), design soundness.
3. Report + history + commit `spec(review): [feature] review findings`. CRITICAL → resolve before implement.

## Final (5.5) — one `## Round N` appended to `specs/[feature]/review-final.md`
1. **Inputs**: spec, plan, tasks, data-model, contracts, constitution, `specs/merge-checklist.md` (missing → create from `spec-kit/templates/merge-checklist-template.md`, pre-fill commands from AGENTS.md / README, **ASK** the user to confirm), AGENTS.md / project rule files, `git diff <base>...HEAD`, `evidence/`, bugs.md.
2. **Mechanical**: MCP `mcp_spec_kit_diff_scan(feature)` → save `evidence/final-diff-scan.txt`. Run every checklist command (build, full test, lint, format, extra) → `evidence/final-<check>.txt`. Record `ci:<id>` for the reviewed commit when a pipeline exists.
3. **§1 Spec conformance**: every FR, SC, user-story scenario and edge case → the code that implements it (`path:line`) + the test that proves it. Contracts and data model vs code. Code no requirement asks for → unplanned. ❌ missing = CRITICAL; ↔ deviation → **WAIT**: patch spec/plan (intentional), log a bug, or defer to close.
4. **§2 Constitution & project rules**: list every constitution MUST/principle and checklist P-item that applies to the touched layers; verdict each with `path:line`. A violated MUST = HIGH (CRITICAL if security/data).
5. **§3 Code quality & best practice**: architecture conformance, layers/dependency direction, error chains, security, data integrity, concurrency, duplication, complexity, API surface; research current practice for the stack (skip research for size S). **§4 Tests**: behaviour not implementation, edge cases, fixtures match `probe:` files.
6. **§5 Checklist** table, every item with its evidence file. **Verdict**: any CRITICAL/HIGH or failing blocking item → `NOT READY`; only MEDIUM / non-blocking → `READY-WITH-FOLLOWUPS`; else `READY`. Write `**Verdict**:` and `**Reviewed-commit**: <git rev-parse --short HEAD>`.
7. NOT READY → log each CRITICAL/HIGH/blocking failure in bugs.md (bug format of `spec-kit-test`, ids via `mcp_spec_kit_next_id`), confirm with the user → `bugfix [feature]`, then a new round. Draft the PR description in §6.

## Severity and nitpick filter
CRITICAL / HIGH / MEDIUM only. A finding must harm correctness, security, performance, maintainability or testability; style, formatting, naming taste → delete. A broken explicit project rule is never a nitpick.

## Done when
- [ ] Pre: report + commit. Final: round appended with Verdict + Reviewed-commit, every FR/SC row filled, every applicable rule verdicted, every checklist item has evidence; `mcp_spec_kit_lint_artifacts` → 0 errors.
- [ ] Final: history.md entry (phase `Phase 5.5 — Final review`) + ONE commit `spec(review): [feature] final review (verdict: X)` — review-final.md, evidence, bugs.md. Closed-review: no history entry.

## Next
Pre: `spec-kit-implement`. Final READY / READY-WITH-FOLLOWUPS → `spec-kit-summarize` (close). NOT READY → `bugfix [feature]`, then final review again. Closed: `reopen [feature]` if needed.
