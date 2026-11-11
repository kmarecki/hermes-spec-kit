# spec-kit-plan — full procedure

> **Loaded on demand** — the one-screen SKILL.md is the entry point; this file holds only what it leaves out. Read the section you need.

## Context
Load `spec.md`, `specs/constitution.md` (guidance, not a gate), and the codebase: existing
layers, DI style, test harnesses, naming. The plan reuses what exists before inventing.
`plan.md` present and not bugfix mode → BLOCK (No Complete Overwrite → `bugfix` / `reopen`).

## By tier (`spec-kit/references/sizing.md`)
- **S**: Summary · Current Design placeholder · the Technical Context lines that matter · External
  Seams · Acceptance Test Strategy · Rounds. No research / data-model / contracts / quickstart
  unless the plan cannot be understood without one.
- **M**: + Design section; research / data-model / contracts / quickstart only where the feature
  needs them (a new entity → data-model; a new endpoint → contracts).
- **L**: all that apply; research.md with decision → rationale → alternatives per real choice.
Design bigger than the tier (new seam, third layer) → STOP, ASK to raise it; on approval edit
the Size line, record the ruling.

## Sections that matter most
- **External Seams**: every DB function / view, HTTP contract, message, file format, external
  service — with what a read-only probe should query. Implement refuses a fixture without one.
- **Acceptance Test Strategy** (`spec-kit/references/acceptance.md` §2): per AC the level,
  harness, test file, environment (none / Docker / running stack), result source (TRX / JUnit
  path or command). A level with no harness yet → a Setup task, or ASK to change the level.
- **Security & Privacy** answers from the spec → where the check lives (policy, filter, validator,
  log scrubber) — one line each in Design.
- Constitution gates (simplicity, anti-abstraction, integration-first): violations justified in
  Complexity Tracking, never silently.

## Decisions
ASK the user for choices they would want to make (behaviour, scope, user-visible trade-offs);
no human → `decisions.md` assumption with the alternative not taken. Design choices inside the
plan's remit (which component, which helper, which test layout) are plan.md content — not
assumptions, not rulings.

## Bugfix mode
Per open bug: root cause from the code (not the report alone) → ONE dated round appended under
`## Rounds (ADR log)`: `### Round N — <date> — <BUG ids> — supersedes: <§ or nothing>` with
Context / Decision / Consequences / Plan Ref → set `Plan Ref` in `bugs.md`. Never edit earlier
rounds or `## Current Design` (the close regenerates it); a contradiction with the current
design → say so in *supersedes* and ASK. Then route `spec-kit-tasks` automatically.

## MCP, then commit
`mcp_spec_kit_update_artifact(plan.md)` · `mcp_spec_kit_advance_phase(from_phase=2)` ·
`mcp_spec_kit_lint_artifacts` · commit per `spec-kit/references/commits.md`.
