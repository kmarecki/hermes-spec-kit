# Tasks: [FEATURE NAME]

**Input**: plan.md, spec.md (+ data-model.md, contracts/ when present) · **TDD**: active
*(or `> **TDD**: test-after (Principle 1 C)` — from the constitution, `spec-kit/references/rigor.md` · or `> **TDD**: Bypassed by user request`)*

**Format**: `- [ ] T### [P] [US#] [TEST] [AC-###] [SEAM] Description — exact/file/path.ext`
- `[P]` parallel (different files, no dependency) · `[US#]` user story
- `[TEST]` written and run RED before the phase's code (RED and GREEN files saved under `evidence/`, every size — `spec-kit/references/evidence.md`)
- `[AC-###]` on a `[TEST]` task: the test proves that criterion; its NAME carries the id (`AC003_…` / `'AC-003 …'`); frozen after RED
- `[SEC]` implements or tests a Security & Privacy row / threat mitigation (`compliance: baseline`, `spec-kit/references/compliance.md`); tasks without it need no security assessment
- `[SEAM]` touches an external seam — starts with a read-only probe saved as `evidence/<ID>-probe-<seam>.txt`; the fixture matches its shape

> Size S: one flat list, tests first. M / L: phases below; every FR and AC maps to a task.

## Phase 1: Setup / Foundational

- [ ] T001 [SEAM] Probe + fixture for [seam] — tests/fixtures/[seam].json
- [ ] T002 [P] [TEST] [AC-001] [behaviour] — tests/[area]/[file].spec.ts

## Phase 2: User Story 1 — [Title] (P1)

**Goal**: [what this story delivers] · **Independent test**: [how]

- [ ] T003 [US1] [TEST] [AC-002] … — tests/…
- [ ] T004 [US1] Implement … — src/…

## Phase N: Polish

- [ ] T0XX Docs / AGENTS.md lines the change makes wrong — docs/…

## Dependencies & Execution Order

- Phase 1 blocks every story; stories run in parallel after it; Polish last.
- [other ordering constraints]
