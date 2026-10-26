# Acceptance: [FEATURE NAME]

> One `## Round N` per acceptance run, appended, never edited. The gate reads the LATEST
> round: `**Result**: PASS` on a commit with no later code change. Procedure:
> `spec-kit/references/acceptance.md`.

## Round 1 — [YYYY-MM-DD HH:MM UTC] — [agent]

**Result**: PASS | FAIL | STOPPED
**Commit**: [short sha of HEAD when the run started]
**Counts**: pass N · fail N · missing N · deferred N · manual N · regressions N
**Runs**: fast `output:evidence/acceptance-r1.txt` · e2e [ran: specs … / deferred: stack down] · command/probe [evidence/acceptance-r1-AC-###.txt]

| AC | FRs | Level | Outcome | Tests (result) | Bug |
|----|-----|-------|---------|----------------|-----|
| AC-001 | FR-001 | integration | ✅ pass | RulesTests.AC001_rules_are_stored | — |
| AC-002 | FR-002 | unit | ❌ fail | OverdueTests.AC002_… — `Expected true, got false` | BUG-004 (new) |
| AC-003 | FR-001, FR-002 | e2e | ⏸ deferred | — (stack down) | — |
| AC-005 | FR-001 | manual | 👤 manual | — | — |

**Regressions** (failing tests without an AC id): [names → BUG-NNN / none]
**Frozen tests changed**: [paths → STOPPED / none]
**Next**: [PASS → final review · FAIL → bugfix chain, round 2 · STOPPED → asked the user: …]
