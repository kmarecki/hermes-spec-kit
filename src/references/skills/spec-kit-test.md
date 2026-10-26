# spec-kit-test — full procedure

> **Loaded on demand.** The one-screen `spec-kit-test` SKILL.md is the entry point; this file holds the complete
> procedure (every branch, template field and pitfall). Read the section you need, not the whole file.
> Tool names: Hermes (`terminal`, `write_file`, `patch`, `read_file`, `skill_view`) — Claude Code maps them to
> `Bash`, `Write`/`Edit`, `Read`, `Skill`; MCP tools are `mcp_spec_kit_*` / `mcp__spec-kit__*`.

**Task Persona**: Adopt the mindset of a QA engineer. Your primary deliverable is a detailed, structured bugs.md. Every bug must have: clear steps to reproduce, expected vs actual behavior, severity, environment context. Vague bug reports are worse than no report — they waste time. Be systematic, be thorough, be precise.

**Phase**: 5 (Testing)

**Purpose**: Log user-discovered bugs in `bugs.md` and orchestrate the bugfix loop. User reports bugs in natural language; agent formats them into structured entries.

**When NOT to use**: During implementation or before the full regression run (Step 7 of implement) completes.

**Routing**: Load this skill when the user says "test [feature]".

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.


**Artifacts**: `specs/[feature]/bugs.md`

## Safety Block: Log Before Fix

**Rule**: ALWAYS write the bug to bugs.md first. HALT after logging. Do NOT fix, plan, or read source code. Only proceed when user says "bugfix [feature]".

## Execution

### Validate prerequisites
```
IF specs/[feature]/spec.md NOT EXISTS: ERROR "Run spec-kit-specify first"
```

### Check for existing bugs.md
```
IF bugs.md EXISTS:
  LOAD, report current summary
  ASK: "Add new bugs, continue bugfixing, or mark bugs as verified?"
ELSE:
  COPY spec-kit/templates/bugs-template.md → bugs.md
```

### User reports bugs — agent formats them
User describes in natural language. Agent structures into:
```
### BUG-NNN: [Summary]
- **Severity**: critical/major/minor/trivial
- **Description**: observed vs expected
- **Steps to Reproduce**: [numbered steps]
- **Requires Clarification**: [ ] no / [ ] yes
- **Status**: open
```

Status vocabulary and the oracle rule: `spec-kit/references/evidence.md` (open → in-progress → claimed → verified; legacy resolved/fixed = claimed).

**Id**: with MCP, `mcp_spec_kit_next_id(feature, kind="BUG")` gives the number; without MCP, highest existing + 1.

**Smart insert**: INSERT the new bug entry BEFORE the `---` separator that precedes `## Summary`. Then UPDATE the Summary table: add a row for the new bug, increment counts, and correct the open/in-progress/resolved/verified tallies. Never place new bugs after `---` or inside `## Summary`.

After each bug, confirm: "Logged BUG-NNN: [summary] — correct?"

### Bug status validation
When user finishes logging → count open bugs:
- **If 0 bugs**: Feature complete. Suggest close.
- **If >0 bugs**: Say \"bugfix [feature]\" to start the workflow. The bugfix workflow
  (spec-kit-tasks → spec-kit-implement) handles plan → tasks → implement.
  **Never fix bugs directly** — always route through the workflow.

### Mark bugs as verified
```
FIND bug
REQUIRE an oracle (evidence.md): the user says it is fixed (quote them),
  a CI run id with a green result, or a review report by the OTHER agent.
IF the only source is the implementing agent's own claim:
  REFUSE: "BUG-NNN is claimed, not verified — needs user / ci:<id> / review:<other-agent>."
ELSE:
  SET Status: verified
  SET Verified-by: user | ci:<run-id> | review:<agent>
  REPORT
```

### Accept mode — one round of the acceptance loop

Triggered by `accept [feature]`, or routed automatically after the last implement phase
(and after every bugfix round) when spec.md defines `**AC-###**` criteria. The full rules,
command keys and stop conditions: `spec-kit/references/acceptance.md`.

```text
PREREQUISITES: every task [X]; spec.md has ACs; tasks.md tags every automated AC
  (mcp_spec_kit_lint_artifacts → no "has no '[TEST] [AC-###]' task" errors)
N = (rounds in acceptance.md) + 1;  COMMIT = git rev-parse --short HEAD
COMMANDS = specs/merge-checklist.md acceptance_* keys
  missing → add them from spec-kit/templates/merge-checklist-template.md, filled from the
  project's test scripts; ASK the user to confirm once (then the loop runs unattended)

1. RUN acceptance_fast (the FULL unit + integration + component suites — also the regression)
2. E2E_SPECS = files on this feature's [TEST] [AC-###] tasks whose AC level is e2e
   IF E2E_SPECS AND acceptance_e2e_ready exits 0:
     RUN acceptance_e2e with {specs} = E2E_SPECS   (never the full e2e suite)
   ELSE: those ACs come back "deferred" — not a failure; the final review handles them
3. FOR each command / probe AC: run its check → evidence/acceptance-r<N>-AC-###.txt,
   first line "RESULT: PASS" or "RESULT: FAIL", then the command and output
4. SAVE the console output → evidence/acceptance-r<N>.txt (command + UTC time on top)
5. CALL mcp_spec_kit_acceptance_status(feature, results="<acceptance_*_results globs>", round=N)
6. APPEND "## Round N — <UTC> — <agent>" to acceptance.md (spec-kit/templates/acceptance-template.md):
   **Result**, **Commit**: COMMIT, counts, the matrix, regressions, frozen changes, Next

7. IF Result == PASS:  REPORT "Acceptance PASS (round N) — route the final review."
   IF Result == STOPPED (a frozen test changed): ASK — revert the test, or approve a refreeze
   IF Result == FAIL:
     FOR each fail / missing AC and each regression:
       IF an open / in-progress / claimed bug already names it (Area: AC-### or the test):
         SET it back to open — "failed again in acceptance round N" (append the new Actual)
       ELSE LOG a new bug (id: mcp_spec_kit_next_id kind="BUG"):
         Severity major (critical when it is a security/data AC), Area: AC-###,
         Description: observed vs the AC's Then, Steps: its Given/When, Actual: the first
         failing assertion, Expected: the Then, Source: acceptance round N, Status: open
       No per-bug confirmation inside the loop — the failing test is the evidence; the round
       lists every bug it logged so the user sees them.
     STOP CONDITIONS — ASK the user instead of continuing:
       - N == acceptance_max_rounds (default 5)
       - the same ACs failed with the same first assertion in rounds N-1 and N (no progress)
       - the fix would need a spec change or a frozen-test change
       - the run could not execute (build broken, service missing) twice in a row
     ELSE: REPORT "Acceptance FAIL (round N): BUG-… — bugfix chain next" and hand to
       spec-kit-workflow 'bugfix [feature]' (plan → tasks → implement), which routes
       'accept [feature]' again when implement finishes.
```

Bugs the loop fixed stay `claimed` (Evidence: `output:evidence/acceptance-r<N>.txt`); they
become `verified` only with an oracle — a green `ci:<run-id>` of the acceptance suite on that
commit, the user, or `review:<other-agent>`.

### Completion check
```
IF all bugs verified (or no bugs) AND (no ACs OR the latest acceptance round is PASS):
  REPORT: "Run 'final review [feature]', then 'close [feature]'."
```

### MCP checks (optional, when MCP server is configured)
```text
CALL mcp_spec_kit_lint_artifacts(feature="[feature]")   # status vocabulary, Verified-by, summary table — 0 errors before commit
```

### Append to history.md and Commit

Follow the **Shared Commit Procedure** in `spec-kit/references/preflight.md`:
- Phase: Phase 5 — Testing (accept mode: `Acceptance R<N>`)
- Artifact: `specs/[feature]/bugs.md` (accept mode: + `acceptance.md`, `evidence/acceptance-r<N>*`)
- Scope: `specs/[feature]/`
- Message: `"spec(phase-5): [feature] bug log"` (accept mode: `"spec(phase-5): [feature] acceptance round N (RESULT a/b)"`)

## Common Pitfalls
1. **Fixing before logging**: Procedural lock. Log first, fix later. Violating this causes workflow corruption.
2. **Setting bugs to verified preemptively**: `verified` needs an oracle — the user, a CI run, or the other agent's review. The agent that fixed the bug may only set `claimed`.
3. **Skipping confirmation**: After each bug entry, confirm with user. They may have additional details.

## Prerequisite Enforcement
**ERROR** if: spec.md does not exist.
