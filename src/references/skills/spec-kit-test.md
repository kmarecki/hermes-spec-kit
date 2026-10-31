# spec-kit-test — full procedure

> **Loaded on demand** — the one-screen SKILL.md is the entry point; this file holds only what it leaves out. Read the section you need. Hermes tools (`terminal`, `write_file`/`patch`, `read_file`, `search_files`, `skill_view`) map to Claude Code `Bash`, `Write`/`Edit`, `Read`, `Grep`/`Glob`, `Skill`; MCP `mcp_spec_kit_*` = `mcp__spec-kit__*`.

## Log before fix
ALWAYS write the bug to `bugs.md` first, then HALT. Do not fix, plan or read source code; the
user says `bugfix [feature]` to start the loop.

## Bug entry
```
### BUG-NNN: [summary]
- **Severity**: critical / major / minor / trivial   - **Area**: [spec section / component / AC-###]
- **Description**: observed vs expected              - **Steps to Reproduce**: 1. … 2. …
- **Actual Result** / **Expected Result**
- **Requires Clarification**: [ ] no / [ ] yes        - **Plan Ref**: (filled by plan)
- **Status**: open   - **Evidence**: (with claimed)   - **Verified-by**: (with verified)
```
Insert BEFORE the `---` that precedes `## Summary`; add the Summary row; fix the tallies.
Confirm each entry with the user. Status vocabulary and the oracle rule:
`spec-kit/references/evidence.md`.

## Accept mode — one round (`spec-kit/references/acceptance.md` §5–6)
```
PREREQ: every task [X]; spec.md has ACs; lint shows no "has no [TEST] [AC-###] task" error
N = rounds in acceptance.md + 1;  COMMIT = git rev-parse --short HEAD
COMMANDS = specs/merge-checklist.md acceptance_* (missing → add from the template, ASK once)
1. RUN acceptance_fast   (FULL unit + integration + component — also the regression)
2. E2E_SPECS = this feature's [TEST] [AC-###] e2e files; run acceptance_e2e only if
   acceptance_e2e_ready exits 0 — else those ACs are "deferred" (the final review handles them)
3. command / probe ACs → evidence/acceptance-r<N>-AC-###.txt ("RESULT: PASS|FAIL" first line)
4. console → evidence/acceptance-r<N>.txt (command + UTC time on top)
5. mcp_spec_kit_acceptance_status(feature, results=<globs>, round=N)
6. APPEND "## Round N — <UTC> — <agent>" to acceptance.md: Result, Commit, counts, matrix,
   regressions, frozen changes, Next
7. PASS → "route the final review" · STOPPED (frozen test changed) → ASK revert / refreeze
   FAIL → per fail / missing AC and regression: an existing open/claimed bug names it → back
   to open ("failed again in round N", append the new Actual); else a new bug — Severity major
   (critical for security/data ACs), Area AC-###, Steps = Given/When, Actual = first failing
   assertion, Expected = Then, Source: acceptance round N. No per-bug confirmation in the loop.
   STOP and ASK when: N == acceptance_max_rounds · same ACs + same first assertion as round N-1 ·
   the fix needs a spec or frozen-test change · the run could not execute twice.
   Else hand to spec-kit-workflow 'bugfix [feature]', which routes 'accept' again after implement.
```
Loop-fixed bugs stay `claimed` (`Evidence: output:evidence/acceptance-r<N>.txt`) until an oracle.

## Verify
Oracle required: the user's quoted words, a green `ci:<run-id>` on that commit, or
`review:<other-agent>`. The implementing agent's claim → refuse. Set `Status: verified` +
`Verified-by:`. All verified and (no ACs or latest round PASS) → "run `final review [feature]`".

## Commit
`mcp_spec_kit_lint_artifacts` → 0 errors · `spec(phase-5): [feature] bug log` (accept mode:
`spec(phase-5): [feature] acceptance round N (RESULT a/b)`) per `spec-kit/references/commits.md`.
