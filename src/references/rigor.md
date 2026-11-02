# Rigor — lean / standard / strict (per project)

`ceremony = rigor (project) × size (feature, sizing.md)`. `rigor:` in `specs/git-conventions.md`,
set by the constitution (Level 0); absent → `standard` (the workflow as before). A spec may raise
it (`**Rigor**: strict`); lowering it needs a quoted ruling in `decisions.md`.

## Level 0 — context (constitution, asked first, both modes)

| Who / stakes | Rigor | Doc scale | Compliance |
|---|---|---|---|
| hobby · learning · experiment | **lean** | small | none |
| indie / solo product | **lean** (standard once it has paying users) | small | none · baseline with personal data |
| startup / small team (2–5) | **standard** | small or platform | baseline with personal data |
| established product / platform (6+, several deployables) | **standard** or **strict** | platform | baseline |
| regulated / safety-critical (trait) | **strict** — forced | platform | baseline |

## Principle defaults — purpose matrix → rigor → traits (the stricter wins; lean may relax the matrix)

| Principle | lean | standard | strict |
|---|---|---|---|
| 1 Testing | C (libraries: B) | matrix | A |
| 2 Linting | C — framework defaults | matrix | A |
| 3 Architecture | C / A1 — YAGNI | matrix ⭐ | matrix ⭐ + architecture tests |
| 5 Git workflow | A — trunk | matrix | B — branch + PR |
| 6 Documentation | C | matrix | A / B |
| 9 Code review | C | matrix | A |
| others | matrix | matrix | stricter of matrix and A |

## Process level — P1 light · P2 normal · P3 full (`ceremony = rigor × size`)

| Size | lean | standard | strict |
|---|---|---|---|
| S | P1 | P1 | P2 |
| M | P1 | P2 | P3 |
| L | P2 | P3 | P3 |

Phase card `process: P2`; compliance adds security evidence on top.

| Practice | P1 | P2 | P3 |
|---|---|---|---|
| Branch | lean: trunk (`blocked_branches: none`, Principle 5 = A) · else feature branch | feature branch | feature branch + PR |
| spec / plan / tasks | S shapes (sizing.md), auto-chained, one `spec(phase-1-3)` commit | template, one commit per phase | template (+ compliance rows), per phase |
| TDD | from Principle 1 (lean: never asked; C → test-after) | from Principle 1 | RED/GREEN every phase |
| RED evidence file | none — `<phase>-green.txt` (or `ci:`) | `<phase>-red.txt` only for a phase with an `[AC-###]` test or a `[SEAM]` | `<phase>-red.txt` + `-green.txt` per phase |
| Probe per `[SEAM]` | lean: recommended · else required | required | required |
| Commits | implementation in ONE commit; lint once before it | per phase; lint + history guard at phase end | per phase; lint before every commit |
| Pre-implement review | skip | lite | full |
| Devil's advocate | pre-implement: optional · final: **required** — the same reviewer, inline | pre-implement: **required** · final: optional | both **required**, by a **different agent** (the other agent, else a separate sub-agent) · objections never capped at any level |
| Acceptance | one recorded run **or** the user's quoted "works" in the final round | acceptance loop | loop + `ci:<id>` |
| Re-runs | one run, or cite CI | bugfix rounds re-run what the fix touched; the final review cites CI (`review_run`) | final review cites CI on the final commit; local only what CI did not run |
| Final review | self-check round ≤ 30 lines: checklist + diff scan, one line per section, the floor's oracle quoted | exceptions only, ≤ 80 lines; round N+1 records the delta | ≤ 150 lines; the other agent; strict L: named human `**Approved-by**:` |
| Close | short `close.md`, change record optional, AGENTS.md patch, ADR only if obvious; health = the server's | close + change record; health = the server's | `summarize` (full gap table) + change record |
| `history.md` (when `history:` is not set) | off | off — timeline from git at close | on |
| Cold at close (`archive_feature`) | history, verified bugs, earlier rounds → `*-archive.md` (forensics only) | same | same; lint warns at 40 KB live |
| Engineering guidelines | lean: one line · else MUSTs → merge-checklist P-items | MUSTs → P-items | + architecture tests |

Lint warns past the line caps and at 40 KB per live file; `next_id` reads the archives.

## Floor — never below, at any rigor

A spec exists · something **not written by the agent** shows it works (test output, `ci:`, or the
user's quoted words — P1 without `acceptance.md`: named in the final round, lint checks for it) ·
the diff scan (secrets, conflict markers) runs — on trunk it scans from the feature's spec commit ·
the close patches AGENTS.md. Strict + size L: `**Approved-by**:` a named human (gate).

## Test-after (Principle 1 = C, or TDD bypassed)

tasks.md header `> **TDD**: test-after (Principle 1 C)`; implement writes code, then the tests
for the phase's ACs and regressions; `evidence/<phase>-green.txt` only, no RED file;
`acceptance_freeze` after GREEN. Lint does not ask for RED files.
