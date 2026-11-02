# Size Tiers (S / M / L)

Size works **inside the project's rigor** (`rigor.md`: lean / standard / strict — the table below is
`standard`; lean relaxes it, strict tightens it, the floor never moves). Ceremony follows the size of the change — the **workflow** and the **length of the artifacts**
shrink; the evidence does not. `spec-kit-specify` **always asks** the tier, recommendation first
and marked "(Recommended)" with the signals that triggered it. The answer is a ruling in
decisions.md and `**Size**: S | M | L — <reason>` in spec.md. Unattended → the recommendation is
recorded as an assumption. A spec without the line is treated as M.

**S is for a single bugfix or a small enhancement** — one layer, a handful of files, nothing
new at the boundary. Anything with a new seam, a second layer or a security / tenant / data
dimension is at least M.

## Choosing — the highest tier any row triggers

| Signal | S | M | L |
|--------|---|---|---|
| Layers touched (UI, API, DB, infra, jobs) | 1 | 2 | 3+ |
| Files expected to change | ≤ ~6 | ~7–25 | > 25 |
| New external seam (schema, HTTP contract, message, file format) | none | one, additive | several, or breaking |
| New dependency / new pattern | no | one, conventional | yes |
| Security, auth, money, deletion, tenant boundary, personal data | no | — | yes |
| Expected tasks | ≤ ~8 | ~9–25 | > 25 |
| Unknowns to research | none | a few | many / spike |

Typo, rename, config value → no spec-kit at all.

## What each tier produces — the workflow and the artifacts get leaner, the evidence stays

| Step | S | M | L |
|------|---|---|---|
| spec.md | **a few lines**: one sentence of intent, 1–3 FRs, **1–2 ACs**, the Security & Privacy line ("None — because …" allowed), 1 SC | full template | full template |
| Clarify | only if a marker remains | if markers remain | recommended |
| plan.md | **half a page**: Summary, Current Design, seams, the AC → test row(s), Rounds | full; research / data-model / contracts / quickstart only when needed | full + all that apply |
| Specify → Plan → Tasks | **auto-chained**, ONE commit `spec(phase-1-3)` | one commit per phase | one commit per phase |
| tasks.md | flat list, ≤ ~8 tasks | phases | phases |
| Pre-implement review (3.5) | skip | **lite**: coverage, underspecification, codebase fit, devil's advocate | **required, full** + devil's advocate by a separate sub-agent |
| Implement evidence | **same for every tier**: `probe:` per `[SEAM]`, RED and GREEN file per phase, AC tests frozen after RED | same | same |
| **Acceptance round** (`acceptance.md`) | **every tier**: automated ACs run and recorded; manual ACs carry the user's quoted confirmation | same | same |
| `ci:<id>` | when a pipeline exists | yes | yes |
| Final review (5.5) | §1 coverage line + exceptions, §2 rules, §4 devil's advocate (brief), §5 checklist; no stack research | full, exceptions-only tables | full, by the other agent or a fresh-context sub-agent; devil's advocate separate |
| Close | `close` (one page) + `change-record.md` | `close` + change record; gap table exceptions only | `summarize` (full gap table) + change record |
| ADR / AGENTS.md step | yes ("none met the bar" is fine) | yes | yes |
| `history.md` (default `history: large`; spec `**History**:` overrides) | off — timeline from git at close | off | **on** — entry before every commit |

**What never shrinks**: the RED/GREEN files, the probe per seam, the acceptance round that
documents every AC passing (automated where a harness exists, `manual` with the user's quoted
words where none can), the oracle rule (your word is not evidence), the final-review gate,
the change record. A small change still has to prove it works.

## Changing the tier

A bigger change than the tier (new seam, third layer): stop, say so, ask. On approval edit the
`**Size**:` line, add the missing artifacts additively, record the ruling. No downgrade once
higher-tier artifacts exist.
