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

## Project rules (edit — these are this project's non-negotiables)

| # | Item | Blocking |
|---|------|----------|
| P1 | [e.g. "Module X must not reference module Y"] | yes |
| P2 | [e.g. "No new URLs in the frozen config file"] | yes |
