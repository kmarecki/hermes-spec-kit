# Epic: [EPIC NAME]

**Id**: [epic-short-name] · **Status**: open | closed · **Owner**: [name] · **Opened**: [DATE] · **Closed**: —
**Goal**: [one sentence — the outcome, not the feature list]

> An epic is a body of work in time: many single-spec features towards one goal. It carries
> *what and in what order*; module design docs carry *how it works*; ADRs carry *why*.
> The close of every feature with `**Epic**: [epic-short-name]` in its spec updates its row.

## Scope

- In: [bounded list] · Out (non-goals): [explicit]
- Done when: [epic-level acceptance — measurable, e.g. "every RS-M tab serves from the reader; V1 reporting SPs unreferenced by V2"]

## Cross-feature rules

Rules every feature in this epic must obey — the pre-implement review and the final review §2
check them like constitution MUSTs.

- [e.g. "No new reader rollup without a golden file"] · [e.g. "V1 is frozen — ADR 0012"]

## Features

| # | Feature (spec dir) | Size | Status | PR | Health | ADRs | Note |
|---|--------------------|------|--------|----|--------|------|------|
| 1 | [NNN-name] | M | specified / implementing / closed | — | — | — | [sequencing: depends on #0] |

Order and dependencies: [#1 → #2 → (#3 ∥ #4) …]

## Decisions at epic level

| Date | Decision | Source | ADR |
|------|----------|--------|-----|

## Modules touched

[design_dir docs this epic changes — one line each, patched by the feature closes]

## Close *(appended when every row is closed)*

**Closed**: [DATE] · **Features**: N closed / N planned · **Health**: [min–max across features] ·
**ADRs**: [list] · **Design docs patched**: [list] · **Dropped from scope**: [features + why]
