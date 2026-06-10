---
name: spec-kit-test
description: Load when the user says 'spec-kit test [feature]', 'speckit test [feature]', 'spec-kit bug [feature]', 'speckit bug [feature]', 'spec-kit log [feature]', or 'speckit log [feature]' — Phase 5 bug tracking and manual testing.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, testing, bugs, qa, bug, error, failure, issue, problem]
    related_skills: [spec-kit-implement, spec-kit-workflow]
---

# spec-kit-test

**Task Persona**: Adopt the mindset of a QA engineer. Your primary deliverable is a detailed, structured bugs.md. Every bug must have: clear steps to reproduce, expected vs actual behavior, severity, environment context. Vague bug reports are worse than no report — they waste time. Be systematic, be thorough, be precise.

**Phase**: 5 (Testing)

**Purpose**: Log user-discovered bugs in `bugs.md` and orchestrate the bugfix loop. User reports bugs in natural language; agent formats them into structured entries.

**When NOT to use**: During implementation or before the final automated test run (Step 9 of implement) completes.

**Routing**: Load this skill when the user says "test [feature]". If loaded directly, load spec-kit-workflow first to check prerequisites.

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Git Commit Guidelines

> **Branch Guard**: Before any git operation, verify you are NOT on a blocked branch (from specs/git-conventions.md blocked_branches).
> If on a blocked branch, BLOCK and prompt: `git checkout -b {feature_prefix}/NNN-feature-name`
> (or `{bugfix_prefix}/NNN-bugfix-name` for bugfix work). See `spec-kit-workflow` for the full
> branch guard logic.

| Situation | Use commit template from specs/git-conventions.md |
|-----------|--------------------------------------------------|
| Bug log (Phase 5) | Bug log template (default: `spec(phase-5): [feature] bug log`) |

See `spec-kit/references/auto-commit.md`. Commits use `--no-verify`.


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

After each bug, confirm: "Logged BUG-NNN: [summary] — correct?"

### Bug status validation
When user finishes logging → count open bugs. If 0, feature complete. If >0, suggest "bugfix [feature]".

### Mark bugs as verified
```
FIND bug → SET Status: verified → REPORT
```

### Completion check
```
IF all bugs verified:
  REPORT: "All bugs verified — run 'close [feature]' to complete."
```

### Transition Log
Append to `specs/[feature]/history.md` following `spec-kit/references/history-tracking.md`:
- Phase: Phase 5
- Artifact: `specs/[feature]/bugs.md`

### Commit
See `spec-kit/references/auto-commit.md`:
- Scope: `specs/[feature]/bugs.md`
- Message: `"spec(phase-5): [feature] bug log"`

## Common Pitfalls
1. **Fixing before logging**: Procedural lock. Log first, fix later. Violating this causes workflow corruption.
2. **Setting bugs to resolved/verified preemptively**: Only the user marks a bug verified — after they test the fix.
3. **Skipping confirmation**: After each bug entry, confirm with user. They may have additional details.

## Prerequisite Enforcement
**ERROR** if: spec.md does not exist.
