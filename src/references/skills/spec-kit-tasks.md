# spec-kit-tasks — full procedure

> **Loaded on demand** — the one-screen SKILL.md is the entry point; this file holds only what it leaves out. Read the section you need. Hermes tools (`terminal`, `write_file`/`patch`, `read_file`, `search_files`, `skill_view`) map to Claude Code `Bash`, `Write`/`Edit`, `Read`, `Grep`/`Glob`, `Skill`; MCP `mcp_spec_kit_*` = `mcp__spec-kit__*`.

## Context
Load plan, spec, data-model, contracts. `tasks.md` present and not bugfix mode → BLOCK (No
Complete Overwrite). Bugfix mode → load tasks, bugs, the plan's rounds; append only.

## TDD question
ASK "Generate test tasks (TDD) or skip tests?" — every time. Skip → header
`> **TDD**: Bypassed by user request` (the final review notes the weaker guarantee).

## Layout
- S: one flat list, `[TEST]` tasks first, then code. M/L: Setup/Foundational → one phase per
  user story (its tests first) → Polish.
- `T### [P] [US#] [TEST] [AC-###] [SEAM] Description — exact/path.ext` — no task without a path.
- Tests are grouped by phase boundary, not 1:1 with code tasks: one test file may cover several
  tasks; one task may need several tests.

## Mapping
```
FOR each FR-### and user story: name the implementing task(s)
FOR each AC with level unit / integration / component / e2e:
  ≥ 1 "T### [TEST] [AC-###] … — <test file from the plan's Acceptance Test Strategy>"
  in the phase that delivers it; the test NAME carries the id (AC003_… / 'AC-003 …' / test_ac003_…)
FOR each command / probe AC: a task that writes the check, tagged [AC-###]
FOR each seam in the plan's External Seams: [SEAM] on the task that touches it
mcp_spec_kit_lint_artifacts → no "[AC-###] has no [TEST] task" error
```

## Bugfix mode
Per open bug: `BF-### [TEST]` reproducing test + `BF-###` fix task, inserted BEFORE
`## Dependencies & Execution Order`; never delete or renumber; duplicate id → ASK. Then route
`spec-kit-implement` automatically.

## Ids, MCP, commit
`mcp_spec_kit_next_id(kind="T"|"BF")` (no MCP: highest + 1) · `mcp_spec_kit_update_artifact(tasks.md)`
· `mcp_spec_kit_advance_phase(from_phase=3)` · `mcp_spec_kit_lint_artifacts` · commit per
`spec-kit/references/commits.md`. Report: task count, phases, TDD mode, parallel and bugfix tasks.
