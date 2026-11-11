# Final Review: [FEATURE NAME]

> Merge-readiness review — phase 5.5, mandatory before close. One `## Round N` per run,
> appended, never edited. The close reads the LATEST round's Verdict and Reviewed-commit; a
> code commit after that sha makes the round stale. **Exceptions only**: the full AC → test
> matrix is in acceptance.md, the FR → task map in tasks.md — do not repeat them here.

> **Process level P1**: a self-check round ≤ 30 lines — Verdict, Reviewed-commit, one line per section, §5 results, the oracle (test output or the user's quoted words), §4 inline. P2 ≤ 80 lines, later rounds the delta only; P3 ≤ 150.

## Round 1 — [YYYY-MM-DD] — [review:<agent> | self-review by <agent> (fresh context: yes/no)]

**Verdict**: READY | READY-WITH-FOLLOWUPS | AWAITING-OWNER | NOT READY
**Reviewed-commit**: [short sha of HEAD when the review ran]
**Approved-by**: [`compliance: baseline` + Security high only — <human> — "<quoted words>"; delete otherwise]
**Base**: [branch] @ [merge-base sha] · **Size**: S | M | L · **Implemented-by**: [agent, from the history.md implement entries]
**Counts**: CRITICAL N · HIGH N · MEDIUM N · checklist failures N · awaiting owner N

### 1. Spec conformance

Coverage: FR [n/N] ✅ · SC [n/N] ✅ · edge cases [n/N] ✅ · acceptance round [N] PASS @ [sha] (frozen tests unchanged).
Rows for everything NOT ✅:

| ID | Requirement (short) | Verdict | Code / evidence | Why |
|----|---------------------|---------|-----------------|-----|
| [FR-00N] | … | ⚠️ partial / ❌ missing / ↔ deviates / 👤 awaiting owner | `path:line` · test | |

Contracts / data model vs code: [matches / differs — how]. Unplanned behaviour: [list / none].

### 2. Constitution, project rules, Security & Privacy

| Rule (source §) | Verdict | Evidence (`path:line`) |
|-----------------|---------|------------------------|
| [constitution MUST / merge-checklist P-item / AGENTS.md rule / spec Security & Privacy row] | ✅ / ❌ / n/a — why | |

### 3. Findings (code quality, best practice, tests)

| ID | Severity | Category | `path:line` | Finding | Fix |
|----|----------|----------|-------------|---------|-----|
| Q1 | CRITICAL / HIGH / MEDIUM | architecture / errors / security / data / concurrency / duplication / complexity / API / tests | | | |

Stack practice checked: [per framework the diff leans on — follows / deviates (source)] *(skip for S)*.
Tests: [prove §1 behaviour, not implementation; fixtures match `probe:` files; RED + GREEN file per phase].

### 4. Devil's advocate *(M: same reviewer, separate pass · L: separate sub-agent, code before decisions.md)*

| # | Objection (concrete input / scenario that breaks it) | Author's answer | Outcome |
|---|------------------------------------------------------|-----------------|---------|
| O1 | | | accepted → BUG-NNN / rebutted (evidence) / deferred (follow-up) |

≤ 5 objections. An unanswered objection blocks READY for size L.

### 5. Merge checklist

| # | Item | Result | Evidence |
|---|------|--------|----------|
| G1 | Merges cleanly | ✅ / ❌ | output:evidence/final-diff-scan.txt |
| G2 | Build | | output:evidence/final-build.txt |
| G3 | Full tests · `ci:<id>` | | output:evidence/final-test.txt |
| … | | | |

### 6. Outcome

- Bugs logged (CRITICAL / HIGH / blocking): [BUG-NNN, … / none] · Follow-ups (MEDIUM): [list / none]
- Awaiting the owner: [SC-00N manual check … / deviation FR-00N ruling … / none] → a specs-only Round N+1 turns AWAITING-OWNER into READY
- PR description: what / why / how verified (evidence + ci) / risks / rollback / strongest objections and how they were answered
