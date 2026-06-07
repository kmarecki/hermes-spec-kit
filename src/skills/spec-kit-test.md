---
name: spec-kit-test
description: Testing and bug tracking phase. Phase 5 - documents found bugs and routes back through the workflow for bugfixes.
version: 1.0.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, testing, bugs, qa]
    related_skills: [spec-kit-implement, spec-kit-workflow]
---

# spec-kit-test

**Phase**: 5 (Testing)

**Purpose**: Document discovered bugs in `specs/[feature]/bugs.md` and orchestrate the bugfix loop. Testing is manual — the user discovers and reports bugs. This skill creates the bug tracking document and routes bugs back through Clarify → Plan → Tasks → Analyze → Implement as needed.

## 🔒 SAFETY BLOCK: Bugs Must Be Logged Before Fixing

This is a **procedural lock**, not a suggestion. Violating it causes workflow corruption.

### The Rule
1. ALWAYS write the bug to `bugs.md` with Status: open
2. **HALT after logging.** Do NOT proceed to fix, plan, diagnose source code, or load implement/plan skills.
3. Only proceed when the user says **"bugfix [feature]"** — this is the trigger word.
4. Exception: User can edit bugs.md directly (that's documentation, not a code fix).

### Do NOT (after logging a bug)
- Load spec-kit-plan
- Load spec-kit-implement
- Read source files to understand the bug
- Propose a fix approach
- Apply any code change
- Chain to any other skill

Your only output after logging bugs is: a summary table and the phrase:
> "N open bugs found. Run 'bugfix [feature]' to begin the bugfix loop."

### Pre-flight Self-Check
Before any tool call in this skill:
```
IF I already wrote to bugs.md:
  CHECK: Am I about to read source code or edit files?
  IF YES: STOP. You are violating the safety block.
  Your job is done. Return control to the user.
```

**Prerequisites**: `spec-kit-implement` must have been run (or artifacts exist from prior phases)

**Artifacts**:
- `specs/[feature]/bugs.md` (primary artifact — bug log)

## Execution

### Step 1: Validate prerequisites
```
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first to establish the feature specification"
```

### Step 2: Check for existing bugs.md
```
IF specs/[feature]/bugs.md EXISTS:
  LOAD existing bugs.md
  REPORT current bug summary (open/in-progress/resolved/verified counts)
  ASK: "Add new bugs, continue bugfixing, or mark bugs as verified?"
ELSE:
  COPY `spec-kit/templates/bugs-template.md` → `specs/[feature]/bugs.md`
  REPORT: "Created specs/[feature]/bugs.md — add bugs manually using the template format"
  INSTRUCT: Each bug needs: ID, Severity, Area, Description, Steps to Reproduce,
            Actual Result, Expected Result, Requires Clarification flag, Status
```

### Step 3: User adds bugs manually
The user adds bugs to `bugs.md` in the following format:

```
### BUG-001: [Short title]

- **Severity**: [critical/major/minor/trivial]
- **Area**: [component or spec area affected]
- **Description**: [observed vs expected behavior]
- **Steps to Reproduce**:
  1. ...
- **Actual Result**: [what happens]
- **Expected Result**: [what should happen]
- **Requires Clarification**: [ ] no / [ ] yes
- **Plan Ref**:
- **Status**: open
```

### Step 4: Bug status validation
When user says they've finished logging bugs:
```
SCAN bugs.md for all bugs with Status: open
COUNT: total open bugs
IF count == 0:
  REPORT: "No open bugs — feature is complete!"
  SUGGEST: Continue to next feature or start new spec
ELSE:
  PRESENT summary table:
    | Bug ID | Severity | Area | Requires Clarification | Status |
    REPORT: "N open bugs found. Run 'bugfix [feature]' to begin the bugfix loop."
```

### Step 5: Bugfix routing
When user says "bugfix [feature]":

```
LOAD specs/[feature]/bugs.md

FOR EACH bug with Status: open or in-progress:
  IF Requires Clarification checkbox "yes" is checked:
    ROUTE: spec-kit-clarify (with bug context)
    AFTER clarify → AUTOMATICALLY route to spec-kit-plan
  ELSE:
    ROUTE: spec-kit-plan (with bugfix context)

AFTER plan completes → AUTOMATICALLY route to spec-kit-tasks
AFTER tasks completes → AUTOMATICALLY route to spec-kit-implement

DEFAULT ROUTING: spec-kit-plan → spec-kit-tasks → spec-kit-implement (automatic chain)
NOTE: No user choice between tasks and implement for bugfixes. Always chain all three.
```

### Step 6: Mark bugs as verified
When user indicates a bugfix is confirmed working:
```
FIND bug in bugs.md
SET Status: verified
REPORT: "[BUG-ID] marked as verified"
```

### Step 7: Completion check
```bash
SCAN bugs.md:
  COUNT bugs with Status: open
  COUNT bugs with Status: in-progress
  COUNT bugs with Status: resolved
  COUNT bugs with Status: verified

IF all bugs are verified:
  REPORT: "All bugs resolved and verified — feature is complete!"
ELSE:
  REPORT summary and recommend next steps
```

### Step 8: Commit bug log (auto)
```bash
IF `git rev-parse --git-dir > /dev/null 2>&1`; THEN
  COMMIT_MSG="spec(phase-5): [feature] bug log"
  git add specs/[feature]/bugs.md
  git commit -m "$COMMIT_MSG" --no-verify
  COMMIT_HASH=$(git rev-parse HEAD)
  NOTE: "Bug log committed as $COMMIT_HASH"
ELSE
  NOTE: "Not a git repository — skipping automatic commit"
```

## Bugfix Loop Flow

```
[Implement Complete]
       │
       ▼
 ┌─────────────┐
 │  TESTING    │  ◄── User discovers bugs, logs them in bugs.md
 │  (manual)   │
 └──────┬──────┘
        │ "bugfix [feature]"
        ▼
 ┌──────────────┐
 │ Needs        │
 │ Clarification│──yes──► spec-kit-clarify ──┐
 │  (per bug)?  │                            │
 └──────┬───────┘                            │
        │ no                                 │
        ▼                                    ▼
  ┌───────────┐                         ┌───────────┐
  │ spec-kit- │                         │ spec-kit- │
  │   plan    │◄────────────────────────│  clarify  │
  └─────┬─────┘                        └───────────┘
        │
        ▼
  ┌───────────┐
  │ spec-kit- │──► AUTOMATIC (no user choice)
  │   tasks   │
  └─────┬─────┘
        │
        ▼
  ┌──────────────┐
  │  spec-kit-   │──► (optional, only if user asks)
  │   analyze    │
  └──────┬───────┘
         │
         ▼
  ┌───────────┐
  │ spec-kit- │──► AUTOMATIC (no user choice)
  │ implement │
  └─────┬─────┘
        │
        ▼
  ┌─────────────┐
  │  TESTING    │  ◄── User retests, marks bugs verified
  │  (manual)   │      or discovers new bugs → repeat loop
  └─────────────┘
```

## Phase State Detection

| Artifacts Present | Interpretation |
|:-----------------|:-------------|
| `bugs.md` with open bugs | Testing — bugs found, awaiting bugfix |
| `bugs.md` with all verified | Testing complete |
| `bugs.md` + updated `plan.md` | Bugfix planned |
| `bugs.md` + updated `tasks.md` | Bugfix tasks defined |
| `bugs.md` + completion markers in tasks | Bugfix in progress |

## Routing Commands

- "Test [feature]" — loads this skill, creates/opens bugs.md
- "Add bug to [feature]" — guides adding a single bug entry
- "bugfix [feature]" — routes to bugfix workflow (plan → tasks → analyze → implement)
- "Verify [BUG-ID] in [feature]" — marks a bug as verified
- "Bug status [feature]" — shows current bug summary

## Done When

- [ ] All bugs logged in bugs.md have Status: verified
- [ ] No remaining open bugs
- [ ] User confirms feature is complete
- **Commit**: `$COMMIT_HASH` (auto — `git log` for details)

## Next Skills

- Propose to the user: Run `spec-kit-specify` to add new features
- Propose to the user: Run `spec-kit-workflow` to start a new feature cycle

**Re-running this skill**:
1. LOAD existing bugs.md
2. PRESERVE all existing bug entries and their statuses
3. APPEND new bugs at the end
4. UPDATE summary table
