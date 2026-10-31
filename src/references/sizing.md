# Size Tiers (S / M / L)

Ceremony follows the size of the change. `spec-kit-specify` **always asks** the tier,
recommendation first and marked "(Recommended)" with the signals that triggered it. The
answer is a ruling in decisions.md and `**Size**: S | M | L — <reason>` in spec.md. Unattended
→ the recommendation is recorded as an assumption. A spec without the line is treated as M.

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

## What each tier produces — progressively leaner

| Step | S | M | L |
|------|---|---|---|
| spec.md | one story, FRs, ACs, SCs, edge cases, **Security & Privacy** (one line allowed) | full | full |
| Clarify | only if markers remain | if markers remain | recommended |
| plan.md | Summary, Current Design, seams, Acceptance strategy, Rounds | full; research / data-model / contracts / quickstart only when needed | full + all that apply |
| Specify → Plan → Tasks | **auto-chained**, ONE commit `spec(phase-1-3)` | one commit per phase | one commit per phase |
| tasks.md | flat list | phases | phases |
| Pre-implement review (3.5) | skip | **lite**: coverage, underspecification, codebase fit, devil's advocate | **required, full** + devil's advocate by a separate sub-agent |
| **Implement evidence** | `probe:` per `[SEAM]` · no RED/GREEN files | `probe:` per `[SEAM]` · **RED per phase** · no GREEN files | `probe:` · RED **and** GREEN per phase |
| Acceptance loop | yes — its round output is the regression evidence | yes | yes |
| `ci:<id>` | when a pipeline exists | yes | yes |
| Final review (5.5) | §1 coverage line + exceptions, §2 rules, §5 checklist; no stack research | full, exceptions-only tables | full, by the other agent or a fresh-context sub-agent; devil's advocate separate |
| Close | `close` (one page) + `change-record.md` | `close` + change record; gap table exceptions only | `summarize` (full gap table) + change record |
| ADR / AGENTS.md step | yes ("none met the bar" is fine) | yes | yes |

What never shrinks: the probe per seam, the acceptance round, the oracle rule (your word is
not evidence), the final-review gate, the change record.

## Changing the tier

A bigger change than the tier (new seam, third layer): stop, say so, ask. On approval edit the
`**Size**:` line, add the missing artifacts additively, record the ruling. No downgrade once
higher-tier artifacts exist.
