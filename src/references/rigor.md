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

Lean asks only Testing, Architecture, Git and Config / secrets; the other 8 are listed as
defaults the user may open.

## Ceremony

| Step | lean | standard | strict |
|---|---|---|---|
| Branch | trunk: commits on `main` (`blocked_branches: none`, Principle 5 = A) | feature branch | feature branch + PR |
| Size question | default S; ask only when a signal says M+ | ask | ask |
| spec.md | intent, FRs, 1–3 ACs (`manual` / `command` fine), Security & Privacy one line | template | template + compliance rows |
| TDD | **from Principle 1, never asked**: A/B → RED/GREEN, C → test-after | from Principle 1 (asked only if the constitution has none) | RED/GREEN every phase |
| Probe per `[SEAM]` | recommended | required | required |
| Commits | spec+plan+tasks one commit, implementation one commit | per phase | per phase |
| Acceptance | one recorded run **or** the user's quoted "works" in the final round | acceptance loop | loop + `ci:<id>` |
| Pre-implement review | never | by size | M lite, L full |
| Final review | **self-check round**: checklist commands + diff scan, one line per section, no devil's advocate | as today | other agent + devil's advocate; L: named human `**Approved-by**:` |
| Close | short `close.md`; change record optional; AGENTS.md patch; ADR only if obvious | as today | change record required |
| `history.md` (when `history:` is not set) | never | large (L) | always |
| Engineering guidelines (constitution) | one line: framework defaults | MUSTs → merge-checklist P-items | MUSTs → P-items + architecture tests |

## Floor — never below, at any rigor

A spec exists · something **not written by the agent** shows it works (test output, `ci:`, or the
user's quoted words — lean without `acceptance.md`: named in the final round, lint checks for it) ·
the diff scan (secrets, conflict markers) runs — on trunk it scans from the feature's spec commit ·
the close patches AGENTS.md. Strict + size L: `**Approved-by**:` a named human (gate).

## Test-after (Principle 1 = C, or TDD bypassed)

tasks.md header `> **TDD**: test-after (Principle 1 C)`; implement writes code, then the tests
for the phase's ACs and regressions; `evidence/<phase>-green.txt` only, no RED file;
`acceptance_freeze` after GREEN. Lint does not ask for RED files.
