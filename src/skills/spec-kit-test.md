---
name: spec-kit-test
description: Load when the user says 'spec-kit accept [feature]', 'speckit accept [feature]', "accept [feature]", "run acceptance for [feature]", 'spec-kit test [feature]', 'speckit test [feature]', 'spec-kit bug [feature]', 'speckit bug [feature]', 'spec-kit log [feature]', 'speckit log [feature]', "test [feature]", "run tests for [feature]", "log bugs for [feature]", or "bug [feature]" — Phase 5 bug tracking and manual testing.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, testing, bugs, qa, bug, error, failure, issue, problem]
    related_skills: [spec-kit-implement, spec-kit-workflow]
---

# spec-kit-test

**Phase**: 5 · **Persona**: QA engineer — steps, observed vs expected, severity; a vague bug report is worse than none.
**Purpose**: log user-reported bugs in `bugs.md`; mark bugs verified **only with an oracle**; **accept mode** runs the acceptance criteria and logs every failure for the loop. Log, then STOP — never fix here.
**Full procedure**: `spec-kit/references/skills/spec-kit-test.md` · status rules `spec-kit/references/evidence.md`.

## Before writing
- `spec-kit/references/preflight.md`. **ERROR** if `spec.md` is missing. `bugs.md` missing → `spec-kit/templates/bugs-template.md`; exists → summary, **ASK**: add, bugfix, or verify?

## Log a bug
1. Id `mcp_spec_kit_next_id(kind="BUG")`. Entry `### BUG-NNN: summary` — Severity, Area, Description (observed vs expected), Steps, Actual, Expected, Requires Clarification, Plan Ref (empty), **Status: open**.
2. Insert before the `---` preceding `## Summary`; add the Summary row; fix counts. Confirm each: "Logged BUG-NNN — correct?"
3. 0 open → suggest `final review [feature]`; > 0 → `bugfix [feature]`. **Never fix directly.**

## Accept mode — one round (`spec-kit/references/acceptance.md` §5–6)
Rigor lean: one recorded run (or the user's quoted "works", kept for the final self-check) — no loop, no round limit.
1. Commands = `specs/merge-checklist.md` `acceptance_*` (missing → add from `spec-kit/templates/merge-checklist-template.md`, **ASK** once). COMMIT = HEAD.
2. Run `acceptance_fast` (full unit + integration + component = the regression); `acceptance_e2e` with this feature's e2e specs only if `acceptance_e2e_ready` exits 0 (else deferred); command/probe ACs → `evidence/acceptance-r<N>-AC-###.txt` (`RESULT: PASS|FAIL`). Console → `evidence/acceptance-r<N>.txt`.
3. `mcp_spec_kit_acceptance_status(feature, results, round=N)` → append `## Round N` to `acceptance.md` (`spec-kit/templates/acceptance-template.md`): Result, Commit, counts, matrix.
4. FAIL → per failing/missing AC and regression: existing bug → back to `open` ("failed again in round N"); else new bug (Area `AC-###`, Steps = Given/When, Actual = first failing assertion, Source: round N) — no per-bug confirmation in the loop.
5. **Stop and ASK** when: round = `acceptance_max_rounds` (5); same ACs + same assertion two rounds running; the fix needs a spec or frozen-test change; STOPPED; the run cannot execute twice. Else hand to `bugfix [feature]` (then `accept` again). PASS → final review.
6. Commit `spec(phase-5): [feature] acceptance round N (RESULT a/b)` — acceptance.md, evidence, bugs.md.

## Verify a bug
Only with an oracle: the user's quoted words, a green `ci:<id>` on that commit, or `review:<other-agent>`. Else refuse: "claimed, not verified." Set `Status: verified` + `Verified-by:`.

## Done when
- [ ] Bugs confirmed with the user (loop-logged bugs carry their round); ids ascending; Summary counts match (`mcp_spec_kit_lint_artifacts` → 0 errors). history.md entry, then commit (`spec-kit/references/preflight.md` procedure): `spec(phase-5): [feature] bug log`.
