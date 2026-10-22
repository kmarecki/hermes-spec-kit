---
name: spec-kit-implement
description: Load when the user says 'spec-kit implement [feature]', 'speckit implement [feature]', 'spec-kit start [feature]', 'speckit start [feature]', "implement [feature]", or "start implementing [feature]" — Phase 4 phase-level TDD execution.
version: 1.2.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, implementation, tdd, coding]
    related_skills: [spec-kit-tasks, spec-kit-test, spec-kit-workflow, writing-plans]
---

# spec-kit-implement

**Phase**: 4 · **Persona**: disciplined engineer building to spec — no scope creep, no unrequested refactoring; builder, not designer.
**Purpose**: execute `specs/[feature]/tasks.md` phase by phase: all tests of a phase RED, then all code GREEN, then one commit per phase. Bugfix tasks (`BF-###`) run the same cycle.
**Full procedure**: `spec-kit/references/skills/spec-kit-implement.md` (bugfix mode, quickfix, regression umbrella, re-run rules).
**Rules that bind**: `spec-kit/references/evidence.md` (your word is not evidence) · `spec-kit/references/auto-commit.md`.

## Before writing
- Run `spec-kit/references/preflight.md`. **BLOCK** if `tasks.md`, `plan.md` or `spec.md` is missing. This is the only phase that may edit source code.
- Load `tasks.md`, `plan.md`, `data-model.md`, `contracts/`, `research.md`, `quickstart.md`, `constitution.md`, `bugs.md` (as present). TDD bypassed if `tasks.md` carries `> **TDD**: Bypassed by user request`.
- MCP (optional): `mcp_spec_kit_get_next_actions` → read the phase card now and after every context compaction.

## Per phase (Setup → Foundational → Core → Integration → Polish)
1. **RED** — write every `[TEST]` task of the phase; run each; it must fail for the right reason. Save the run: `specs/[feature]/evidence/<phase>-red.txt`.
2. `[SEAM]` tasks — before writing the fixture, run a read-only **probe** against the real system/data; save command + result as `evidence/<TASK>-probe-<seam>.txt`; the fixture must match that shape.
3. **GREEN** — write the simplest code; run only this phase's tests; save `evidence/<phase>-green.txt`; run the build (TypeScript must compile).
4. Mark the phase's tasks `[X]`; bug fixes → `bugs.md` Status `claimed` + `Evidence:` (never `verified`).
5. History record (`mcp_spec_kit_append_history` or `spec-kit/scripts/spec-kit-log.sh`: phase, skill, agent, artifacts, tests, evidence, commit, note ≤ 25 words) → MCP `mcp_spec_kit_history_guard` + `mcp_spec_kit_lint_artifacts` → commit `feat: [feature] Phase N - [name]` (bugfix: `fix: [feature] BF-### - description`).
- Pure logic: test first. Legacy code without tests: characterisation test first (`evidence/<TASK>-characterisation.txt`), then change. Untestable item → note it beside the task; the close flags it unverified.
- No commits during RED; no per-task regression runs; a non-parallel task that cannot complete → HALT and report.
- New bug found mid-fix → log it in `bugs.md` (`mcp_spec_kit_next_id(kind="BUG")`), do not fix inline (trivial test-only fixes excepted).

## After all phases
6. Full regression: save `evidence/regression-<date>.txt`; queue CI when a pipeline exists and record `ci:<run-id>`; failures → one umbrella task `BF-REGRESSION-001`, fix, re-run, commit `fix: [feature] BF-REGRESSION-001 - fix regressions`.
7. Build verification. MCP: `mcp_spec_kit_advance_phase(from_phase=4)`.

## Done when
- [ ] Every phase committed with its `output:` evidence; regression has `output:` + `ci:` (or states "no pipeline — unverified claim").
- [ ] Every `[SEAM]` task has a `probe:` file matching its fixture. Every fixed bug is `claimed`, none `verified` by this skill.
- [ ] All tasks `[X]` (status-only edits); history entries carry `Implemented-by`.

## Next
Report phases, tests, regressions, build, evidence. Propose `spec-kit-test` (log bugs) or `spec-kit-review` by the **other** agent.
