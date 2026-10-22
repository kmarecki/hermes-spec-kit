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

## Evidence

| Gate | Oracle | Reference |
|------|--------|-----------|
| Full regression | ci:<run-id> / output:<path> | [link or ❌ unverified] |
| Bug fixes | Verified-by per bug | [N verified / N claimed-unverified] |
| Review | review:<agent> / self-review | [report] |

## Key Decisions
- **[Decision]**: [Rationale]

## Spec Health Calculation
- Resolved (implemented as planned or intentionally deviated): N
- Acknowledged (deferred with documented reason): N
- Not Done (missing without documented reason): N
- **Spec Health** = (resolved + acknowledged) / total * 100 = N%
