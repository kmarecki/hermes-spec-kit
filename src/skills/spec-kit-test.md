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

**Phase**: 5 · **Persona**: QA engineer — a vague bug report is worse than none: steps, observed vs expected, severity.
**Purpose**: log user-reported bugs in `specs/[feature]/bugs.md` and mark bugs verified **only with an oracle**. Log, then STOP — never fix here. **Accept mode** runs the feature's acceptance criteria automatically and logs every failure as a bug for the loop.
**Full procedure**: `spec-kit/references/skills/spec-kit-test.md`. Status rules: `spec-kit/references/evidence.md`.
**Not for**: logging bugs during implementation (accept mode is the exception: it runs after the last implement phase).

## Before writing
- Run `spec-kit/references/preflight.md`. **ERROR** if `spec.md` is missing.
- `bugs.md` missing → copy `spec-kit/templates/bugs-template.md`. Exists → report the summary; **ASK**: add bugs, continue bugfixing, or verify?

## Log a bug
1. Id: MCP `mcp_spec_kit_next_id(kind="BUG")` or highest existing + 1.
2. Entry: `### BUG-NNN: summary` with Severity (critical/major/minor/trivial), Area, Description (observed vs expected), Steps, Actual, Expected, Requires Clarification, Plan Ref (empty), **Status: open**.
3. Insert BEFORE the `---` that precedes `## Summary`; add the Summary row; fix the counts.
4. Confirm each entry with the user: "Logged BUG-NNN: … — correct?"
5. When done: 0 open bugs → suggest the final review (`final review [feature]`, mandatory before close); >0 → say `bugfix [feature]`. **Never fix directly.**

## Accept mode — one acceptance round (`spec-kit/references/acceptance.md` §5–6)
1. Commands from `specs/merge-checklist.md` (`acceptance_*`; missing → add them from `spec-kit/templates/merge-checklist-template.md`, **ASK** to confirm once). Note HEAD = the round's commit.
2. Run `acceptance_fast` (full unit + integration + component — also the regression); `acceptance_e2e` with only this feature's e2e spec files, only if `acceptance_e2e_ready` exits 0 (else those ACs are deferred); each command/probe AC → `evidence/acceptance-r<N>-AC-###.txt` (`RESULT: PASS|FAIL` first line). Console → `evidence/acceptance-r<N>.txt`.
3. `mcp_spec_kit_acceptance_status(feature, results=<the *_results globs>, round=N)` → append `## Round N` to `acceptance.md` (`spec-kit/templates/acceptance-template.md`): **Result**, **Commit**, counts, matrix.
4. FAIL → per failing/missing AC and regression: an open/claimed bug already names it → back to `open` ("failed again in round N"); else a new bug (Area `AC-###`, Steps = its Given/When/Then, Actual = the failing assertion, Source: acceptance round N) — **no per-bug confirmation in the loop**; the failing test is the evidence.
5. **Stop and ASK** (no fix) when: round = `acceptance_max_rounds` (5); same ACs failing with the same first assertion two rounds running; the fix needs a spec or frozen-test change; STOPPED (frozen test changed); the run cannot execute twice. Else hand to the bugfix chain (`spec-kit-workflow` routes `bugfix [feature]`, then `accept` again). PASS → route the final review.
6. History (phase `Acceptance R<N>`) + commit `spec(phase-5): [feature] acceptance round N (RESULT a/b)` — acceptance.md, evidence, bugs.md.

## Verify a bug
- Allowed only with an oracle: the user said so (quote), a green `ci:<run-id>` on that commit, or `review:<other-agent>`. The implementing agent's claim is not enough → refuse: "BUG-NNN is claimed, not verified."
- Set `Status: verified` + `Verified-by: user | ci:<id> | review:<agent>`. All verified → "run `final review [feature]`, then `close [feature]`".

## Done when
- [ ] Every user-reported bug confirmed with the user (acceptance-logged bugs carry their round instead); ids ascending; Summary table and counts match (MCP `mcp_spec_kit_lint_artifacts` → 0 errors).
- [ ] history.md entry, then commit — Shared Commit Procedure in `spec-kit/references/preflight.md`: scope `specs/[feature]/bugs.md`; message `spec(phase-5): [feature] bug log`.
