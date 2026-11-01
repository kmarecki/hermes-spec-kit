# Merge Checklist
# Checklist version: 1

Copy to `specs/merge-checklist.md` and edit. `spec-kit-review` (final mode) runs every
command below, saves each output under `specs/[feature]/evidence/final-<check>.txt`, and
judges every item. A failing **blocking** item makes the verdict NOT READY.

Empty command → the item is judged by reading the diff. Remove items that do not apply;
add the project's own (they are the project rules the final review enforces).

---

## Commands

```
base_branch:   main                        # defaults to branch_source in git-conventions.md
build:         [e.g. dotnet build -warnaserror | npm run build]
test:          [the FULL suite, e.g. dotnet test | npm test -- --watch=false]
lint:          [e.g. npm run lint]
format_check:  [e.g. dotnet format --verify-no-changes | npm run prettier:diff]
extra:         [any other command that must pass, e.g. architecture tests]

# Acceptance loop (spec-kit/references/acceptance.md) — results must be JUnit XML or TRX
acceptance_fast:          [the FULL unit + integration + component suites writing results, e.g.
                           dotnet test --logger "trx;LogFileName=acc.trx" && npm test -- --reporter=junit --outputFile=test-results/acc.xml]
acceptance_fast_results:  [comma-separated globs, e.g. **/TestResults/acc.trx, test-results/acc.xml]
acceptance_e2e:           [ONE feature's specs only — {specs} is replaced, e.g.
                           npx cypress run --spec {specs} --reporter junit --reporter-options mochaFile=test-results/e2e-[hash].xml]
acceptance_e2e_results:   [e.g. test-results/e2e-*.xml]
acceptance_e2e_ready:     [exit 0 when the stack is up, e.g. curl -sf http://localhost:4200 >/dev/null]
acceptance_max_rounds:    5

# Security scans — only with `compliance: baseline` (spec-kit/references/compliance.md); every final review.
# Exit 0 = pass, non-zero = finding. Check the tool really exits non-zero: `dotnet list package
# --vulnerable` exits 0 even with findings — filter its JSON. Legacy findings → an allowlist with
# reason + expiry (.trivyignore exp:, osv-scanner.toml ignoreUntil, checkov --baseline), or diff mode.
security_deps:     [.NET: dotnet list package --vulnerable --include-transitive --format json | jq -e '[.. | .vulnerabilities? // empty | .[] | select(.severity=="High" or .severity=="Critical")] | length == 0'
                    npm: npm audit --omit=dev --audit-level=high · Python: pip-audit --strict · Go: govulncheck ./...
                    any: trivy fs --scanners vuln --severity HIGH,CRITICAL --exit-code 1 .]
security_secrets:  [gitleaks git --redact --log-opts="<base>..HEAD"   (gitleaks < 8.19: gitleaks detect)]
security_sast:     [semgrep scan --error --config p/default --baseline-commit "$(git merge-base <base> HEAD)" | CodeQL / SonarQube new-code gate]
security_iac:      [checkov -d infra --compact --quiet | trivy config --severity HIGH,CRITICAL --exit-code 1 infra — delete when the project has no IaC]
```

## Generic gate (always checked)

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

## Security gate (only with `compliance: baseline`)

| # | Item | Blocking |
|---|------|----------|
| S1 | No known high/critical vulnerability in new or changed dependencies (`security_deps`) | yes |
| S2 | Secret scan clean on the branch range (`security_secrets`) | yes |
| S3 | Static analysis: no new high finding (`security_sast`) | yes |
| S4 | IaC scan: no new high finding (`security_iac`) | yes |
| S5 | Security high: threat model rows mitigated or accepted; `**Approved-by**` a named human | yes |

## Project rules (edit — these are this project's non-negotiables)

| # | Item | Blocking |
|---|------|----------|
| P1 | [e.g. "Module X must not reference module Y"] | yes |
| P2 | [e.g. "No new URLs in the frozen config file"] | yes |
