# Implementation Plan: [FEATURE]

**Branch**: [###-feature-name] | **Date**: [DATE] | **Spec**: spec.md | **Size**: [S | M | L]
**Modules**: [module names as in `design_dir` — the design docs the close will patch; delete when the project keeps none]

> Size S: keep Summary, Current Design, the Technical Context lines that matter, Seams,
> Acceptance Test Strategy, Rounds — delete the rest; no research / data-model / contracts /
> quickstart unless the plan cannot be understood without one.

## Summary

[Primary requirement + technical approach in a few sentences.]

## Current Design

> **Regenerated, never appended** — what is BUILT, ≤ 1 page; rewritten by the close (and by
> refresh). The rounds below are the dated history.

[Until the first close: "Not yet built — see the sections below."]

## Technical Context

Language/version · primary dependencies · storage · testing · target platform · performance
goals · constraints · scale — only the lines that matter; `NEEDS CLARIFICATION` where unknown.

## Constitution Check *(advisory gate)*

[Simplicity, anti-abstraction, integration-first — violations justified in Complexity Tracking.]

## External Seams

| Seam | Kind (DB function / HTTP contract / message / file / service) | Probe (what to query before writing the fixture) |
|------|------|------|

## Acceptance Test Strategy

| AC | Level | Harness | Test file | Needs | Result source |
|----|-------|---------|-----------|-------|---------------|
| AC-001 | integration | [e.g. WebApplicationFactory + Testcontainers] | [path] | Docker | TRX / JUnit path |

## Design *(M / L)*

Architecture, data flow, module boundaries, error handling, project structure decision.
Details in `research.md` (decision → rationale → alternatives), `data-model.md`, `contracts/`,
`quickstart.md` — only those the feature needs.

## Complexity Tracking *(only if the Constitution Check has violations)*

| Violation | Why needed | Simpler alternative rejected because |
|-----------|-----------|--------------------------------------|

## Rounds (ADR log)

> One dated section per bugfix / reopen round, appended, never edited. At close, rounds that
> pass the ADR bar become project ADRs.

### Round 1 — [YYYY-MM-DD] — [BUG-NNN, …] — supersedes: [§ or "nothing"]

- **Context**: [what was wrong, bug ids] · **Decision**: [what changes] ·
  **Consequences**: [what else moves] · **Plan Ref**: [the bugs.md Plan Ref value]
