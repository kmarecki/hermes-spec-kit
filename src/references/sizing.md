# Size Tiers (S / M / L)

The amount of ceremony follows the size of the change, not the template. `spec-kit-specify`
**always asks** the user for the tier — every time, never silently chosen — offering all three
with its recommendation listed first and marked "(Recommended)" plus the one-line reason
(the signals below that triggered it). The answer is a ruling in decisions.md (quote it) and is
written in `spec.md` as `**Size**: S | M | L — <reason>`. Unattended run (nobody to ask) →
the recommended tier is recorded as an *assumption*, not a ruling, and the next human touch
confirms it. The MCP server reads it (phase card,
`get_feature_state.size`); a spec without the line is treated as **M**.

## Choosing the tier

Pick the **highest** tier any row triggers.

| Signal | S | M | L |
|--------|---|---|---|
| Layers / components touched (UI, API, DB, infra, jobs…) | 1 | 2 | 3+ |
| Files expected to change | ≤ ~6 | ~7–25 | > 25 |
| New external seam (DB schema/migration, HTTP contract, message, file format) | none | one, additive | several, or a breaking change |
| New dependency / new pattern for the codebase | no | one, conventional | yes, or a new architectural pattern |
| Security, auth, money, data deletion, multi-tenant boundary | no | — | yes |
| Expected tasks | ≤ ~8 | ~9–25 | > 25 |
| Unknowns the plan must research | none | a few | many / spike needed |

Tiny unambiguous changes (typo, rename, config value) skip spec-kit entirely.

## What each tier produces

| Step | S | M | L |
|------|---|---|---|
| spec.md | one story, FRs, SCs, edge cases | full template | full template |
| Clarify | only if markers remain | if markers remain | recommended |
| plan.md | Summary, Current Design, seams, Rounds | full template | full template |
| research.md · data-model.md · contracts/ · quickstart.md | no (unless indispensable) | only those the feature needs | all that apply |
| tasks.md | flat list, TDD question still asked | phases | phases |
| Specify → Plan → Tasks | **auto-chained** after the user confirms the spec; ONE commit `spec(phase-1-3)` | one commit per phase | one commit per phase |
| Pre-implement review | skip | recommended | **required** before implement |
| Acceptance criteria (`AC-###`, verify level) | ≥ 1 per FR, mostly unit | ≥ 1 per FR | ≥ 1 per FR + edge cases |
| Implement (RED/GREEN evidence, seam probes, acceptance freeze) | same rules | same rules | same rules |
| Acceptance loop (`accept`) | yes | yes | yes |
| Final review (phase 5.5) | **required** — §1 spec conformance, §2 rules, §5 checklist; §3 without web research | **required**, full | **required**, full, by the other agent or a fresh-context subagent |
| Close | `close` (lightweight) by default | user's choice | `summarize` (full gap analysis) by default |
| ADR + AGENTS.md step at close | yes (usually "none met the bar") | yes | yes |

The evidence rules, history records, log-before-fix, the acceptance loop and the final-review gate do **not**
shrink with the tier — they are what makes the result trustworthy at any size.

## Changing the tier

Plan or implement discovers the change is bigger (a new seam, a third layer): stop, say so,
and ask. On approval, edit the `**Size**:` line (targeted edit), add the missing artifacts
additively, and record the ruling in decisions.md. Downgrading is not allowed once
artifacts for the higher tier exist.
