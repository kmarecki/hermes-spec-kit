# Acceptance Criteria and the Acceptance Loop

Acceptance-test-driven development on top of the phase-level TDD: the spec's acceptance
criteria get ids and a verify level, their tests are ordinary `[TEST]` tasks tagged with
the id, and after implement an automatic loop runs them, logs failures as bugs, runs the
bugfix chain and runs them again — until every automated criterion passes or the loop stops.

## 1. Acceptance criteria (spec.md)

```
- **AC-003** (FR-002) Given a task due 4 days ago and grace 3, When the grid loads, Then it is flagged overdue — Verify: unit
```

- Ids are `AC-###`, ascending, never renumbered (`next_id kind="AC"`). Every FR is named by at
  least one AC (`lint_artifacts` warns otherwise). Edge cases that matter are ACs too.
- One observable outcome per AC, written as Given / When / Then.
- **Verify** names the LOWEST level that can prove it:

| Level | Proves | Typical harness | Speed |
|-------|--------|-----------------|-------|
| `unit` | a rule, a calculation, a validator, a handler with fakes | xUnit / NUnit, Vitest / Jest, pytest | seconds |
| `integration` | API contract, persistence, migrations applied, auth policy, tenant filter — real DB / HTTP in-process | WebApplicationFactory + Testcontainers, supertest | ~1 min |
| `component` | UI behaviour of one component/page with its services mocked | Vitest/Jest + Testing Library, Angular TestBed | seconds |
| `e2e` | a journey that needs the real UI + API + identity + DB together | Cypress, Playwright | minutes, needs the stack |
| `command` | build / infra / pipeline / config outcome | `terraform plan` no drift, `dotnet ef migrations script`, a pipeline dry-run | varies |
| `probe` | data or configuration in a real environment (read-only) | a SQL query, an HTTP GET | seconds |
| `manual` | what no tool can judge (visual fidelity, copy, UX feel) | the user | — |

- `e2e` and `manual` need a reason in parentheses: `Verify: e2e (needs the Keycloak redirect)`.
  Rule of thumb: ≤ 2 e2e ACs per feature; prefer an integration test of the API plus a component
  test of the UI over one e2e test of both.

## 2. Plan: the acceptance test strategy

`plan.md` → `## Acceptance Test Strategy`: one row per AC — level, harness, test file, the
environment it needs (none / Testcontainers / the running stack) and how its result is
produced (JUnit XML / TRX path, or the command). The plan decides where each test lives;
implement does not.

**Deployed-environment ACs** are settled here — one PR (`commits.md`), and shared environments
deploy after the merge: pre-merge run (branch deploy — ASK — or a local stack) · a lower level
in the PR · or a post-deploy SC on the ticket (never a task). A whole-suite AC is `command`.

## 3. Tasks: tag the tests

Every AC whose level is `unit`, `integration`, `component` or `e2e` has at least one
`[TEST] [AC-###]` task with the test file path (`lint_artifacts`: error otherwise). `command`
and `probe` ACs get a task that writes the check (script or query) — tagged the same way.

**Test names carry the id** so a result file maps back to the AC:

| Stack | Name |
|-------|------|
| xUnit / NUnit / MSTest | method `AC003_Late_task_is_flagged` or `[Fact(DisplayName = "AC-003 late task is flagged")]` |
| Vitest / Jest / Cypress / Playwright | `it('AC-003 late task is flagged', …)` |
| pytest | `def test_ac003_late_task_is_flagged()` |

Matching: `AC-003`, `AC003`, `AC_003`, `ac003` (case-insensitive, not inside a longer word or number).

## 4. Implement: RED, then freeze

Per implement phase, as today: the phase's `[TEST]` tasks (acceptance tests included) are
written and run RED (`evidence/<phase>-red.txt`), then the code goes GREEN. Right after the RED
run, call `acceptance_freeze(feature)` — it records the SHA-256 of every file named on a
`[TEST] [AC-###]` task in `evidence/acceptance-freeze.json` (additive: later phases add their
files). From then on a frozen test may only change with the user's approval
(`acceptance_freeze refreeze=true reason="<quoted ruling>"` + a decisions.md ruling) — this is
what stops a loop from "passing" by weakening the tests.

TDD bypassed: the acceptance tests are written after the code; freeze at the first
acceptance round; the final review notes the weaker guarantee.

## 5. The acceptance run (replaces implement's full-regression step)

Commands come from `specs/merge-checklist.md`:

```
acceptance_fast:          dotnet test --logger "trx;LogFileName=acc.trx" && npm test -- --reporter=junit --outputFile=test-results/acc.xml
acceptance_fast_results:  **/TestResults/acc.trx, test-results/acc.xml
acceptance_e2e:           npx cypress run --spec {specs} --reporter junit --reporter-options mochaFile=test-results/e2e-[hash].xml
acceptance_e2e_results:   test-results/e2e-*.xml
acceptance_e2e_ready:     curl -sf http://localhost:4200 >/dev/null     # exit 0 = the stack is up
acceptance_max_rounds:    5
```

1. **Fast** — the FULL unit + integration + component suites (this is also the regression run).
2. **e2e** — only this feature's specs (`{specs}` = the files named on its `[TEST] [AC-###]`
   e2e tasks), only when `acceptance_e2e_ready` exits 0. Never the full e2e suite. Stack down →
   those ACs are `deferred`, not failing; the final review lists them for a targeted run or the user.
3. **command / probe** — run each, save `evidence/acceptance-r<N>-AC-###.txt` whose first
   line is `RESULT: PASS` or `RESULT: FAIL`, then the command and its output.
4. `acceptance_status(feature, results="<the *_results globs>", round=N)` → the matrix:
   `pass` · `fail` · `missing` (automated, no result) · `deferred` (e2e not run) · `manual`,
   plus `regressions` (failing tests that carry no AC id) and `frozen_changed`.
   Result: `STOPPED` if a frozen test changed, `PASS` if nothing fails, is missing or regressed, else `FAIL`.
5. Append `## Round N` to `specs/[feature]/acceptance.md` (template
   `spec-kit/templates/acceptance-template.md`) with `**Result**:` and `**Commit**:` (HEAD
   when the run started) and the matrix. Save the console output as `evidence/acceptance-r<N>.txt`.

Matching is scoped to the files on the feature's `[TEST] [AC-###]` tasks (`foreign_ac_matches`).
Only specs/docs/evidence changed since a green `ci:<id>` → cite it (`**Runs**: ci:<id>`), no re-run.

## 6. The loop

```
round = 1
LOOP:
  acceptance run (§5) → round N in acceptance.md
  PASS                     → STOP: route the final review
  STOPPED (frozen change)  → STOP: ASK the user (revert, or approve a refreeze)
  FAIL:
    FOR each fail / missing AC and each regression:
      an open or claimed bug already names it → set it back to open ("failed again in
        acceptance round N"), else log a new bug (spec-kit-test entry format) with
        Area: AC-### · Steps: its Given/When/Then · Actual: the failing assertion ·
        Source: acceptance round N — no per-bug confirmation inside the loop (the failing
        test is the evidence); the round lists every bug it logged
    STOP and ASK instead of fixing when:
      - round == acceptance_max_rounds (default 5)
      - the SAME ACs failed with the SAME first assertion in two consecutive rounds (no progress)
      - the fix needs a spec change, or a frozen test change
      - the run itself cannot execute (build broken twice, a service missing)
    run the bugfix chain: spec-kit-plan → spec-kit-tasks → spec-kit-implement (bugfix mode)
    round += 1
```

**Failure outside the feature's files**: isolation re-run; passes → ASK; out of scope →
`flaky="<names>"` + `**Flaky**: <tests> — <file> — owner: "<quote>"`.

Inside the loop every question that cannot wait is an **assumption** in decisions.md
(preflight check 7), never an invented ruling. Bugs fixed by the loop are `claimed` with
`Evidence: output:evidence/acceptance-r<N>.txt`; they become `verified` only with an oracle
(`ci:<id>` running the acceptance suite on that commit, the user, or `review:<other-agent>`).

## 7. Gates

- `advance_phase(5→6)` and `close_feature` refuse a feature whose spec has ACs unless the
  latest acceptance round is `PASS` and no code commit follows its `**Commit**`.
- The final review's §1 reads the latest PASS round: `deferred` e2e and `manual` ACs must be
  verified there (a targeted run, or the user's quoted confirmation) or the verdict cannot be READY.
