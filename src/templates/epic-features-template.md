# Features: [EPIC NAME]

**Epic**: epic.md · **Plan**: plan.md · **Order**: [#1 → #2 → (#3 ∥ #4) → …]

> Stage E3 — the epic's "tasks" are features. One row per single-spec feature, ordered; every
> EAC covered by ≥ 1 feature. Rows are added before a spec exists and patched by
> `spec-kit-specify` (spec dir, size) and by every feature close (status, PR, health, ADRs).

| # | Feature | Spec dir | Size | Depends on | Modules | EACs | Status | PR | Health | ADRs | Note |
|---|---------|----------|------|------------|---------|------|--------|----|--------|------|------|
| 1 | [short name — one sentence of intent] | — | M? | — | [reader] | EAC-001 | planned | — | — | — | |
| 2 | | — | | #1 | | | planned | | | | |

**Status values**: planned · specified · implementing · closed · dropped (reason in Note)

## EAC coverage

| EAC | Features | Verified by (filled at epic close) |
|-----|----------|------------------------------------|
| EAC-001 | #1, #2 | |
