# spec-kit-implement — full procedure

> **Loaded on demand** — the one-screen SKILL.md is the entry point; this file holds only what it leaves out. Read the section you need. Hermes tools (`terminal`, `write_file`/`patch`, `read_file`, `search_files`, `skill_view`) map to Claude Code `Bash`, `Write`/`Edit`, `Read`, `Grep`/`Glob`, `Skill`; MCP `mcp_spec_kit_*` = `mcp__spec-kit__*`.

## The phase cycle
```
Phase N (Setup → Foundational → stories → Polish; S: the one flat list is one phase)
═══ RED ═══   for each [TEST] task: write it (one behaviour per test; real code, not mocks,
              unless unavoidable; behaviour, not implementation) → run it → it FAILS because
              the feature is missing (not a typo). M/L: tee → evidence/<phase>-red.txt
              then mcp_spec_kit_acceptance_freeze(feature)   # SHA of every [AC-###] test file
═══ SEAMS ═══ for each [SEAM] task: read-only probe of the real system/data FIRST
              → evidence/<TASK>-probe-<seam>.txt (command + result); the fixture has the SAME
              shape (columns, rows per key, types). A hand-built fixture without a probe is how
              a fix passes green and fails in production. All sizes.
═══ GREEN ═══ for each code task: the simplest code that passes (hardcode now, refactor in
              Polish). Then run ONLY this phase's tests (L: tee → evidence/<phase>-green.txt);
              run the build — TypeScript MUST compile (Vitest/Jest swallow type errors).
═══ CLOSE ═══ tasks [X] · fixed bugs → claimed + Evidence · mcp_spec_kit_lint_artifacts ·
              ONE commit "feat: [feature] Phase N - [name]" with the trailers
              (Phase: Phase 4 — <name> / Implemented-by: <agent> / Evidence: …)
```
- A frozen `[AC-###]` test that "needs" editing to go green means the code or the spec is wrong:
  STOP and ASK; a refreeze needs the user's ruling (`acceptance_freeze refreeze=true reason=…`).
- TDD bypassed (`tasks.md` header): implement and verify manually per task; the acceptance tests
  are written after the code and frozen at the first acceptance round.
- Legacy code without tests: characterisation test first (`evidence/<TASK>-characterisation.txt`),
  then change it. Untestable (visual, race, external) → note beside the task; the close flags it.
- Re-run: find the first incomplete phase, resume at its RED; keep earlier `[X]` marks.
- After compaction or at every sub-phase start: `mcp_spec_kit_get_next_actions` (the phase card).

## Bugfix mode (BF-### tasks)
```
0. READ  — the code of the bug area; cross-check the bugs.md Plan Ref against what the code
           really does. Contradiction → STOP, flag it. (Never fix from the report alone.)
1. RED   — a test that reproduces the bug; run → fails
2. GREEN — minimal fix; run → passes; evidence/BF-###-green.txt (all sizes — it is the claim);
           probe per seam touched → evidence/BF-###-probe-<seam>.txt
3. CLAIM — bugs.md Status: claimed + Evidence: … (never verified)
4. COMMIT "fix: [feature] BF-### - description" + trailers
```
New bug found mid-fix → log it (`mcp_spec_kit_next_id(kind="BUG")`, inserted before the
Summary separator), do not fix inline; say "BUG-NNN logged — address via 'bugfix' after this
round". Trivial test-only fixes (missing assertion, wrong fixture) may be fixed inline.
**Quickfix** (`quickfix [feature]`, explicit opt-in): plan section + task + fix in ONE commit
`fix: [feature] BF-### - description (plan+tasks+fix)`; the documents still exist; tests still written.

## After the last phase
- Spec has ACs → route `accept [feature]` (`spec-kit-test`): the full fast suites + this
  feature's e2e specs, failures → bugs → bugfix chain → accept again. Build verification first.
- Legacy spec without ACs → full suite → `evidence/regression-<date>.txt` + `ci:<run-id>` when a
  pipeline exists (no pipeline → "unverified claim"); failures → classify NEW vs PRE-EXISTING,
  one umbrella `BF-REGRESSION-001` task, fix, re-run, commit `fix: [feature] BF-REGRESSION-001 - fix regressions`.
- `mcp_spec_kit_advance_phase(from_phase=4)`.

## Guardrail
Code-editing tools (`write_file`, `patch`, `terminal` for builds) are allowed ONLY here
(including bugfix implementation). A bug mentioned by the user is logged (`spec-kit-test`)
before it is fixed — never fixed directly.
