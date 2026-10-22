---
name: spec-kit-review
description: Load when the user says 'spec-kit review [feature]', 'speckit review [feature]', "review [feature]", "quality check [feature]", or "analyze [feature]" — cross-artifact consistency check (pre-implement) and critical code quality review (post-implement).
version: 1.2.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, review, quality, consistency, code-review]
    related_skills: [spec-kit-tasks, spec-kit-implement, spec-kit-workflow, spec-kit-constitution]
---

# spec-kit-review

**Phase**: 3.5 (pre-implement) / 5.5 (post-implement) / closed-review · **Persona**: senior architect doing a critical design review — structural problems, security, design debt; not a style checker.
**Purpose**: pre-implement = spec/plan/tasks coherence + codebase fit + best-practice check (read-only report). Post-implement = does the code fulfil the spec and constitution, is the architecture sound, is the evidence real. Closed-review = same, without touching history.md.
**Full procedure**: `spec-kit/references/skills/spec-kit-review.md` (detection passes A–J, report formats, severity rules).

## Before reviewing
- Preflight checks 1 and 4 only (`spec-kit/references/preflight.md`); no writes except closed-review tasks with approval.
- Mode: close doc exists → closed-review; tasks.md and no code → pre-implement; code + tests → post-implement; unclear → **ASK**.
- **Author check** (`spec-kit/references/evidence.md`): read `Implemented-by` in history.md. Same agent as you → label the report *self-review* (not citable as verification) and recommend the other agent. Different → label `review:<you>`.
- Read `decisions.md` first if present: every assumption there is a review item.

## Pre-implement
1. Load spec (FR/SC/stories/edge cases), plan, tasks, constitution. Build requirement↔task coverage.
2. Passes: duplication, ambiguity, underspecification, constitution alignment (informational), naming, completeness, coverage gaps, inconsistency, bugfix coverage, **codebase fit** (patterns, reuse, integration points, paths), **best practice** (research the stack), design soundness.
3. Report: findings table, codebase assessment, best-practice table, coverage table, metrics. CRITICAL → resolve before implement.

## Post-implement / closed-review
1. Load spec, plan, tasks, constitution, git diff, `evidence/` and the `Evidence:` lines of bugs.md.
2. Checks: architecture conformance, spec fulfilment per FR, constitution, naming, docs, code quality (layers, error chains, security, data integrity, duplication, complexity, dependencies, API surface, concurrency), tests (behaviour, edge cases), **fixture reality** (every seam has a `probe:` matching its fixture — missing = HIGH), **evidence present** (phase commits and regression reference `output:`/`ci:`, else "unverified").
3. Deviations: per FR present spec vs code; **WAIT** for the user: update spec/plan, log a bug, or defer to close.
4. Closed-review with CRITICAL/HIGH: offer refactoring tasks in tasks.md (and reopen) — only with approval.

## Severity and nitpick filter
CRITICAL / HIGH / MEDIUM only. A finding must harm correctness, security, performance, maintainability or testability; style, formatting, naming taste, "I'd do it differently" → delete. "Top 5 things to change?" — if not, skip.

## Done when
- [ ] Report delivered with reviewer label, mode, counts, recommendation (proceed / fix critical first).
- [ ] Not closed-review → history.md entry + commit `spec(review): [feature] review findings` (Shared Commit Procedure).

## Next
Pre: `spec-kit-implement` once CRITICAL resolved. Post: `spec-kit-summarize`. Closed: `reopen [feature]` if needed.
