# Merge Checklist
# Checklist version: 1

Copy to `specs/merge-checklist.md`; the project owns it — every key, item and table may be
edited or dropped (absent key = the default shown). The final review runs each command
(`review_run`), saves the output as `evidence/final-<check>.txt` and judges every item; a
failing **blocking** item → NOT READY. Empty command → judged by reading the diff.

---

## Commands

```
base_branch:   main                        # defaults to branch_source in git-conventions.md
build:         [e.g. dotnet build -warnaserror | npm run build]
test:          [the FULL suite, e.g. dotnet test | npm test -- --watch=false]
lint:          [e.g. npm run lint]
format_check:  [e.g. dotnet format --verify-no-changes | npm run prettier:diff]
extra:         [any other command that must pass, e.g. architecture tests]

# Where the checks run (default local = every command above, on this machine)
review_run:    local                       # local | ci (CI jobs first, the rest locally)
ci_jobs:       [check=pipeline/job, …, e.g. test=Tests-BuildValidation/BffUnitTests, lint=Web/eslint]
ci_queue:      [e.g. az pipelines run --name {pipeline} --branch {branch} | gh workflow run {pipeline} --ref {branch}]
ci_status:     [per-job results + source commit, e.g. az pipelines runs show --id {run} | gh run view {run} --json headSha,jobs]

# Acceptance loop (spec-kit/references/acceptance.md) — results must be JUnit XML or TRX
acceptance_fast:          [the FULL unit + integration + component suites writing results, e.g.
                           dotnet test --logger "trx;LogFileName=acc.trx" && npm test -- --reporter=junit --outputFile=test-results/acc.xml]
acceptance_fast_results:  [comma-separated globs, e.g. **/TestResults/acc.trx, test-results/acc.xml]
acceptance_e2e:           [ONE feature's specs only — {specs} is replaced, e.g.
                           npx cypress run --spec {specs} --reporter junit --reporter-options mochaFile=test-results/e2e-[hash].xml]
acceptance_e2e_results:   [e.g. test-results/e2e-*.xml]
acceptance_e2e_ready:     [exit 0 when the stack is up, e.g. curl -sf http://localhost:4200 >/dev/null]
acceptance_max_rounds:    5
```

## Generic gate (default — edit, drop or add rows)

| # | Item | Blocking |
|---|------|----------|
| G1 | Branch merges cleanly into the base (`diff_scan` merge-conflict check) | yes |
| G2 | Build passes with no NEW warnings in changed files | yes |
| G3 | Full test suite passes; CI run on the reviewed commit recorded as `ci:<id>` when a pipeline exists | yes |
| G4 | Lint / format clean | yes |
| G5 | No secrets, keys, certificates, backups or `.env` files in the diff (`diff_scan`) | yes |
| G6 | No conflict markers, focused tests, debugger statements (`diff_scan`) | yes |
| G7 | New TODO/FIXME carry a ticket reference or are removed | no |
| G8 | Every changed file is in scope (`diff_scan` unplanned-change list explained) | yes |
| G9 | Schema/data migrations are included, ordered, and reversible or explicitly one-way | yes |
| G10 | Public API / contract changes are intentional and documented (breaking → called out) | yes |
| G11 | New dependencies: licence and version policy respected, lock file updated | yes |
| G12 | Config / infrastructure / environment changes documented for deploy | yes |
| G13 | User-facing docs, runbooks, AGENTS.md touched where the change makes them wrong | no |
| G14 | Commit messages follow `specs/git-conventions.md` | no |
| G15 | PR description drafted (what / why / how verified / risks / rollback) | no |

## Project rules (edit — these are this project's non-negotiables)

| # | Item | Blocking |
|---|------|----------|
| P1 | [e.g. "Module X must not reference module Y"] | yes |
| P2 | [e.g. "No new URLs in the frozen config file"] | yes |
