---
name: spec-kit-test
description: Load when the user says 'spec-kit test [feature]', 'speckit test [feature]', 'spec-kit bug [feature]', 'speckit bug [feature]', 'spec-kit log [feature]', 'speckit log [feature]', "test [feature]", "run tests for [feature]", "log bugs for [feature]", or "bug [feature]" — Phase 5 bug tracking and manual testing.
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
**Purpose**: log user-reported bugs in `specs/[feature]/bugs.md` and mark bugs verified **only with an oracle**. Log, then STOP — never fix here.
**Full procedure**: `spec-kit/references/skills/spec-kit-test.md`. Status rules: `spec-kit/references/evidence.md`.
**Not for**: during implementation or before the full regression run.

## Before writing
- Run `spec-kit/references/preflight.md`. **ERROR** if `spec.md` is missing.
- `bugs.md` missing → copy `spec-kit/templates/bugs-template.md`. Exists → report the summary; **ASK**: add bugs, continue bugfixing, or verify?

## Log a bug
1. Id: MCP `mcp_spec_kit_next_id(kind="BUG")` or highest existing + 1.
2. Entry: `### BUG-NNN: summary` with Severity (critical/major/minor/trivial), Area, Description (observed vs expected), Steps, Actual, Expected, Requires Clarification, Plan Ref (empty), **Status: open**.
3. Insert BEFORE the `---` that precedes `## Summary`; add the Summary row; fix the counts.
4. Confirm each entry with the user: "Logged BUG-NNN: … — correct?"
5. When done: 0 open bugs → suggest the final review (`final review [feature]`, mandatory before close); >0 → say `bugfix [feature]`. **Never fix directly.**

## Verify a bug
- Allowed only with an oracle: the user said so (quote), a green `ci:<run-id>` on that commit, or `review:<other-agent>`. The implementing agent's claim is not enough → refuse: "BUG-NNN is claimed, not verified."
- Set `Status: verified` + `Verified-by: user | ci:<id> | review:<agent>`. All verified → "run `final review [feature]`, then `close [feature]`".

## Done when
- [ ] Every bug confirmed with the user; ids ascending; Summary table and counts match (MCP `mcp_spec_kit_lint_artifacts` → 0 errors).
- [ ] history.md entry, then commit — Shared Commit Procedure in `spec-kit/references/preflight.md`: scope `specs/[feature]/bugs.md`; message `spec(phase-5): [feature] bug log`.
