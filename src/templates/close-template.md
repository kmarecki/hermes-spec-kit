# Close: [FEATURE NAME]

**Feature**: specs/[###-feature-name]/ · **Date**: [DATE] · **Size**: S | M | L · **Mode**: close | summarize
**Spec Health**: N% = (resolved + acknowledged) / total · **TDD**: active / bypassed
**Change record**: `change-record.md` (the auditor's page — ticket, risk, approvals, rollback, timeline)

## Evidence

| Gate | Oracle | Reference |
|------|--------|-----------|
| Acceptance / regression | ci:<run-id> / output:evidence/acceptance-r<N>.txt | round N PASS @ <sha> / ❌ unverified |
| External seams | probe:<path> per seam | [list] |
| Bugs | Verified-by per bug | N verified · N claimed-unverified (listed below) |
| Final review | READY / READY-WITH-FOLLOWUPS @ <sha> · review:<agent> / self-review | review-final.md Round N |

## Artifact State

| Artifact | Status |
|----------|--------|
| `spec.md` / `plan.md` / `data-model.md` / `contracts/` | ✅ current / ⚠️ needs review / ❌ outdated — [patched at close: …] |
| `tasks.md` · `bugs.md` | ✅ all done · ✅ all verified / ⚠️ N claimed-unverified |
| `plan.md` Current Design | regenerated |

## Gaps *(M: exceptions only · L "summarize": every FR / story / entity / contract)*

| Item | Planned | Actual | Verdict | Rationale / follow-up |
|------|---------|--------|---------|------------------------|
| [FR-00N] | | | ✅ resolved / ⚠️ acknowledged / ❌ not done → BUG-NNN | |

Unverified claims: [bug ids / none]. Open questions / future work: [follow-ups from the final review].

## Architecture Decisions

> "None met the ADR bar" is a valid row — omitting the section is not.

| Decision | Source | ADR bar (why / why not) | Action | ADR |
|----------|--------|-------------------------|--------|-----|
| | decisions.md D-n / plan Round n / review Q-n | cross-feature / hard to reverse / re-litigable / contradicts ADR NNNN — or feature-local | new / supersedes NNNN / evidence appended / feature-local | docs/adr/NNNN-….md |

**ADR index**: updated / n/a · **AGENTS.md**: [updated — sections / no change needed — why]

## Reopened — [YYYY-MM-DD] *(appended on reopen, original close above untouched)*

Previous health N% → M%. [what changed; new gaps; decisions]
