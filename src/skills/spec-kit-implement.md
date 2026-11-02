---
name: spec-kit-implement
description: Load when the user says 'spec-kit implement [feature]', 'speckit implement [feature]', 'spec-kit start [feature]', 'speckit start [feature]', "implement [feature]", or "start implementing [feature]" — Phase 4 phase-level TDD execution.
version: 1.3.0
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
**Purpose**: execute `tasks.md` phase by phase — the phase's tests RED, then code GREEN, then one commit. `BF-###` tasks run the same cycle.
**Full procedure**: `spec-kit/references/skills/spec-kit-implement.md` (bugfix / quickfix, regression umbrella, re-run). **Rules that bind**: `spec-kit/references/evidence.md` (your word is not evidence; RED/GREEN/probe files every tier) · `spec-kit/references/commits.md`.

## Before writing
- `spec-kit/references/preflight.md`. **BLOCK** if `tasks.md`, `plan.md` or `spec.md` is missing. The only phase that edits source code.
- Load tasks, plan, data-model, contracts, research, quickstart, constitution, bugs (as present). `> **TDD**: Bypassed` → no test cycle. Evidence rules are the same for every size.
- MCP: `mcp_spec_kit_get_next_actions` — read the phase card now and after every compaction.

## Per phase
1. **RED** — `> **TDD**: test-after` → skip RED: write the code, then the phase's tests, freeze after GREEN (`spec-kit/references/rigor.md`). Else write every `[TEST]` task of the phase; run them; each fails for the right reason. Save `evidence/<phase>-red.txt` (phase card `process:` — P3 every phase; P2 only a phase with an `[AC-###]` test or a `[SEAM]`; P1 none). Then `mcp_spec_kit_acceptance_freeze(feature)` — a frozen `[AC-###]` test changes only with the user's approval (`spec-kit/references/acceptance.md`).
2. **`[SEAM]`** — before the fixture: read-only probe of the real system → `evidence/<TASK>-probe-<seam>.txt`; the fixture matches its shape. All sizes; rigor lean: recommended, not required.
3. **GREEN** — simplest code; run this phase's tests; save `evidence/<phase>-green.txt`; run the build (TypeScript must compile).
4. Mark the phase's tasks `[X]`; fixed bugs → `claimed` + `Evidence:` (never `verified`).
5. History on (phase card) → entry (`mcp_spec_kit_append_history`: phase, skill, **agent = Implemented-by**, artifacts, tests, evidence = the RED/GREEN/probe files, commit, note ≤ 25 words); history off → every phase makes sure its agent is on the tasks.md header line `**Implemented-by**: <agent>[, <agent>]` (add yourself when another agent started the feature — `claude, hermes`) and the commit body names the evidence files. Then `mcp_spec_kit_history_guard` + `mcp_spec_kit_lint_artifacts` (P1: once, before the single commit; P2: at phase end) → commit `feat: [feature] Phase N - [name]` with the agent trailer (commits.md) (P1: one commit for the whole implementation; bugfix: `fix: [feature] BF-### - description`).
- Legacy code without tests → characterisation test first. Untestable item → note beside the task; the close flags it.
- No commits during RED; no per-task regression runs; a non-parallel task that cannot complete → HALT and report.
- New bug mid-fix → log it (`mcp_spec_kit_next_id(kind="BUG")`), do not fix inline (trivial test-only fixes excepted).
- A question the user would want to decide → `decisions.md` assumption (preflight 6).

## After all phases
6. Spec has ACs → route `accept [feature]` (P1: ONE recorded run, no loop — failures → bugs, the user decides; else `spec-kit-test` accept mode — full fast suites + this feature's e2e, failures → bugs → bugfix chain). No ACs → full regression `evidence/regression-<date>.txt` + `ci:<id>`; failures → `BF-REGRESSION-001`.
7. Build verification. MCP: `mcp_spec_kit_advance_phase(from_phase=4)`.

## Done when
- [ ] Every phase committed with its evidence files (process level) and its history entry (or tasks.md `Implemented-by` when history is off); AC tests frozen after RED; every `[SEAM]` has a matching `probe:`; fixed bugs `claimed`, none `verified` here; all tasks `[X]`.

## Next
`accept [feature]` (automatic with ACs) → `spec-kit-test` for user-found bugs → **final review** (`spec-kit-review`) by the other agent or a fresh-context sub-agent. **No PR yet** — one PR, after the close.
