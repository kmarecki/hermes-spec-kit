# spec-kit-test — full procedure

> **Loaded on demand.** The one-screen `spec-kit-test` SKILL.md is the entry point; this file holds the complete
> procedure (every branch, template field and pitfall). Read the section you need, not the whole file.
> Tool names: Hermes (`terminal`, `write_file`, `patch`, `read_file`, `skill_view`) — Claude Code maps them to
> `Bash`, `Write`/`Edit`, `Read`, `Skill`; MCP tools are `mcp_spec_kit_*` / `mcp__spec-kit__*`.

**Task Persona**: Adopt the mindset of a QA engineer. Your primary deliverable is a detailed, structured bugs.md. Every bug must have: clear steps to reproduce, expected vs actual behavior, severity, environment context. Vague bug reports are worse than no report — they waste time. Be systematic, be thorough, be precise.

**Phase**: 5 (Testing)

**Purpose**: Log user-discovered bugs in `bugs.md` and orchestrate the bugfix loop. User reports bugs in natural language; agent formats them into structured entries.

**When NOT to use**: During implementation or before the full regression run (Step 7 of implement) completes.

**Routing**: Load this skill when the user says "test [feature]". If loaded directly, load spec-kit-workflow first to check prerequisites.

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Git Commit Guidelines
See `spec-kit/references/auto-commit.md`. Commits use `--no-verify`. Branch guard handled by preflight.md.


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

### Completion check
```
IF all bugs verified:
  REPORT: "All bugs verified — run 'close [feature]' to complete."
```

### MCP checks (optional, when MCP server is configured)
```text
CALL mcp_spec_kit_lint_artifacts(feature="[feature]")   # status vocabulary, Verified-by, summary table — 0 errors before commit
```

### Append to history.md and Commit

Follow the **Shared Commit Procedure** in `spec-kit/references/preflight.md`:
- Phase: Phase 5 — Testing
- Artifact: `specs/[feature]/bugs.md`
- Scope: `specs/[feature]/bugs.md`
- Message: `"spec(phase-5): [feature] bug log"`

## Common Pitfalls
1. **Fixing before logging**: Procedural lock. Log first, fix later. Violating this causes workflow corruption.
2. **Setting bugs to verified preemptively**: `verified` needs an oracle — the user, a CI run, or the other agent's review. The agent that fixed the bug may only set `claimed`.
3. **Skipping confirmation**: After each bug entry, confirm with user. They may have additional details.

## Prerequisite Enforcement
**ERROR** if: spec.md does not exist.
