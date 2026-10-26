# Final Review: [FEATURE NAME]

> Merge-readiness review — phase 5.5, mandatory before close. One `## Round N` per run,
> appended, never edited. `close_feature` reads the LATEST round's Verdict and
> Reviewed-commit; any code commit after that sha makes the review stale.

## Round 1 — [YYYY-MM-DD] — [review:<agent> | self-review by <agent> (fresh context: yes/no)]

**Verdict**: READY | READY-WITH-FOLLOWUPS | NOT READY
**Reviewed-commit**: [short sha of HEAD when the review ran]
**Base**: [base branch] @ [merge-base sha] · **Size**: S | M | L · **Implemented-by**: [agent]
**Counts**: CRITICAL N · HIGH N · MEDIUM N · checklist failures N

### 1. Spec conformance — does the code do what the spec says?

| ID | Requirement (short) | Implemented in (`path:line`) | Proven by (test / evidence) | Verdict |
|----|---------------------|------------------------------|-----------------------------|---------|
| FR-001 | … | … | … | ✅ / ⚠️ partial / ❌ missing / ↔ deviates |
| SC-001 | … | … | … | |
| Edge: … | … | … | … | |

Contracts / data model vs code: [each contract and entity — matches / differs (how)].
Unplanned behaviour (code that no requirement asks for): [list or "none"].

### 2. Constitution & project rules

| Rule (source §) | Applies to this diff? | Verdict | Evidence (`path:line`) |
|-----------------|-----------------------|---------|------------------------|
| [constitution.md § / MUST statement] | yes / no — [why] | ✅ / ❌ | |
| [merge-checklist.md P1 / AGENTS.md rule] | | | |

### 3. Code quality & best practice

| ID | Severity | Category | `path:line` | Finding | Fix |
|----|----------|----------|-------------|---------|-----|
| Q1 | CRITICAL / HIGH / MEDIUM | architecture / error handling / security / data integrity / concurrency / duplication / complexity / API / tests | | | |

Best-practice check (stack research): [per technology the diff leans on — follows current guidance / deviates (source)].
Nitpicks omitted.

### 4. Tests

[Do the tests prove the requirements in §1? Edge cases? Fixtures match their `probe:` files?
RED/GREEN evidence present?]

### 5. Merge checklist

| # | Item | Result | Evidence |
|---|------|--------|----------|
| G1 | Merges cleanly | ✅ / ❌ | output:evidence/final-diff-scan.txt |
| G2 | Build | | output:evidence/final-build.txt |
| G3 | Full tests | | output:evidence/final-test.txt · ci:<id> |
| … | | | |

### 6. Outcome

- Bugs logged for CRITICAL/HIGH and blocking checklist failures: [BUG-NNN, … / none]
- Follow-ups (MEDIUM, non-blocking): [list / none]
- Deviations put to the user (spec ↔ code): [FR-NNN → decision / none]
- PR description draft: [below, or "see PR"]
