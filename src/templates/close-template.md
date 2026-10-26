[Close: FEATURE NAME]

**Feature**: specs/[###-feature-name]/
**Spec Health**: N%
**TDD Mode**: Active / Bypassed by user

## Intent Alignment
- Code matches spec intent: Yes / Partially / No
- Deviations: [1-2 sentences describing key differences between spec and code]

## Artifact State

| Artifact | Status |
|----------|--------|
| `spec.md` | ✅ current / ⚠️ needs review / ❌ outdated |
| `plan.md` | ✅ current / ⚠️ needs review / ❌ outdated |
| `tasks.md` | ✅ all complete / ⚠️ N remaining |
| `bugs.md` | ✅ all verified / ⚠️ N open / ⚠️ N claimed-unverified |
| `implementation-summary.md` | ✅ complete / ❌ not generated |
| `review-final.md` | ✅ READY @ <sha> / ⚠️ READY-WITH-FOLLOWUPS (N follow-ups) |

## Evidence

| Gate | Oracle | Reference |
|------|--------|-----------|
| Full regression | ci:<run-id> / output:<path> | [link or ❌ unverified] |
| Bug fixes | Verified-by per bug | [N verified / N claimed-unverified] |
| Final review | Verdict READY / READY-WITH-FOLLOWUPS @ <sha> · review:<agent> / self-review | review-final.md Round N |

## Architecture Decisions

> Harvested at close from decisions.md rulings, plan.md rounds, research decisions and review
> findings. Only decisions that pass the ADR bar become ADRs; the rest stay feature-local.
> "None met the ADR bar" is a valid row — omitting the section is not.

| Decision | Source | ADR bar (why / why not) | Action | ADR |
|----------|--------|-------------------------|--------|-----|
| [decision in one line] | [decisions.md ruling N / plan Round N / research D-n / review Q-n] | [cross-feature / hard to reverse / constrains future code / deviates from ADR NNNN — or "feature-local"] | new / supersedes NNNN / evidence appended to NNNN / feature-local | [docs/adr/NNNN-….md] |

**ADR index updated**: yes / n/a
**AGENTS.md**: [updated — sections touched / no change needed — why]

## Key Decisions
- **[Decision]**: [Rationale]

## Spec Health Calculation
- Resolved (implemented as planned or intentionally deviated): N
- Acknowledged (deferred with documented reason): N
- Not Done (missing without documented reason): N
- **Spec Health** = (resolved + acknowledged) / total * 100 = N%
