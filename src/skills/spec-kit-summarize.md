---
name: spec-kit-summarize
description: Load when the user says 'spec-kit summarize [feature]', 'speckit summarize [feature]', 'spec-kit close [feature]', 'speckit close [feature]', "summarize [feature]", "close [feature]", or "implementation summary for [feature]" — Phase 6 mandatory close with spec health score.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, summary, review, gap-analysis, close]
    related_skills: [spec-kit-test, spec-kit-workflow, spec-kit-refresh]
---

# spec-kit-summarize

**Phase**: 6 (Summary / Close — Mandatory)

**Task Persona**: Adopt the mindset of a thorough code auditor. Verify every claim against actual code — check spec.md, plan.md, and the git diff together. Use web search to research best patterns and practices when evaluating architecture decisions. Describe exactly what changed, why, and whether it matches the spec. No filler, no fluff. Detail is proportionate to actual work done.

**Purpose**: When implementation is complete and testing is done, produce either a full `implementation-summary.md` or a lightweight `close.md`. Computes spec health score (0-100%), patches spec.md/plan.md for intentional deviations. **Mandatory** before a feature can be marked complete.

**When NOT to use**: For mid-stream alignment — use `spec-kit-refresh` instead.

**Routing**: Load this skill when the user says "summarize [feature]" or "close [feature]". If loaded directly, load spec-kit-workflow first to check prerequisites.

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Git Commit Guidelines
See `spec-kit/references/auto-commit.md`. Commits use `--no-verify`. Branch guard handled by preflight.md.


**When to run**:
- **After bugfix loop completes** (all bugs verified) — suggested as mandatory close (user decides when to run it)
- User says: "Summarize [feature]" — full gap analysis
- User says: "Close [feature]" — lightweight close

**Prerequisites**: `spec-kit-implement` must have been run (tasks.md exists)
**Artifacts**:
- `specs/[feature]/implementation-summary.md` (full gap analysis report)
- `specs/[feature]/close.md` (lightweight close document)
- `specs/[feature]/spec.md` (auto-updated to reflect intentional deviations)
- `specs/[feature]/plan.md` (auto-updated to reflect intentional deviations)

## Execution

### Determine Mode
```
IF user explicitly says "close [feature]":
  USE lightweight close mode → close-template.md
  NOTE: "Lightweight close — captures key decisions and state without deep gap analysis."

ELIF user explicitly says "summarize [feature]":
  USE full summary mode → implementation-summary-template.md
  RUN all steps below

ELIF all bugs in bugs.md have Status: verified:
  NOTE: "All bugs verified. Suggest running 'close [feature]' or 'summarize [feature]' to complete Phase 6 (mandatory)."
  PROMPT user for which mode: full summary or lightweight close
  USE the mode they selected

ELSE:
  USE full summary mode (default)

OUTPUT RULE — applies to both modes:
  The length and detail of the summary MUST be proportional to the actual
  code changes made, not to the size of spec.md or tasks.md.
  
  GIT DIFF determines depth:
    - Few files changed → short, precise summary of what was touched
    - Many files / complex changes → thorough description per file/area
    - Single bugfix → one paragraph covering root cause + fix
  
  Always produce a precise, factual description of what code was changed
  and why. Avoid generic filler text. Every sentence should reflect a real
  change visible in the diff.
```

### Load artifacts and detect TDD mode
```
LOAD specs/[feature]/spec.md, plan.md, tasks.md
LOAD data-model.md, contracts/, research.md, quickstart.md, clarify.md (IF EXISTS)
LOAD bugs.md (IF EXISTS), constitution.md (IF EXISTS)

SCAN tasks.md for `> **TDD**: Bypassed by user request`
  IF found: SET tdd_bypassed = true
  IF not found: SET tdd_bypassed = false
```

### Analyze tasks.md completion
```
SCAN all tasks:
  COUNT total tasks
  COUNT completed tasks (marked [X])
  COUNT incomplete tasks (marked [ ])
  IDENTIFY remaining work from incomplete tasks

IF all tasks are complete:
  SET all task markers to [X]
  WRITE updated tasks.md
```

### Analyze bugs.md status
```
IF bugs.md EXISTS:
  SCAN all bugs:
    COUNT total bugs
    COUNT verified
    COUNT resolved
    COUNT open

  IF all bugs verified or resolved:
    SET any open bugs to Status: verified
    WRITE updated bugs.md
```

### Compare code against spec and plan (git diff)
*Skip in lightweight close mode*
```
RUN: git diff {branch_source} --name-status
  OR: git log --oneline --name-only HEAD..{branch_source}
  (branch_source from specs/git-conventions.md, default: main)
  CAPTURE list of files changed, added, deleted

FOR each file changed:
  MATCH to task descriptions in tasks.md
  MATCH to functional requirements in spec.md (FR-###)
  MATCH to architecture/data-model sections in plan.md

IDENTIFY:
  - Files that correspond to planned tasks → mark as implemented
  - Files that have NO corresponding task or requirement → flag as "unplanned change"
  - Requirements/FRs that have NO implementing files → flag as "gap — not implemented"
  - Plan sections (data-model entities, contracts) with no corresponding code → flag as "gap — deferred"
```

### Build gap analysis
*Skip in lightweight close mode*
```
FOR EACH requirement/story/entity/contract in spec.md and plan.md:
  VERDICT:
    ✅ Resolved  — implemented as planned (code exists, tests pass)
    ✅ Resolved  — intentional deviation (code differs from plan, rationale documented)
    ⚠️ Acknowledged — deferred (not critical, tracked for future)
    ❌ Not Done  — missing with no documented reason (should be added to bugs.md or new spec)

FOR each gap marked "❌ Not Done":
  RECOMMEND: add a bug to bugs.md or create a follow-up spec
  WRITE: "Missing implementation: [requirement] — see implementation-summary.md gap analysis"

FOR each gap marked "⚠️ Acknowledged":
  NOTE: Reason for deferral, who decided, under what constraint
```

### Step 5.5: Detect previous close (reopen scenario)
```
IF specs/[feature]/close.md or specs/[feature]/implementation-summary.md EXISTS:
  LOAD previous health score from existing close document
  NOTE: "Previous spec health was N%. This close will append a new section,
         preserving the original close data."
  SET previous_health = N
  SET reopen_mode = true
ELSE:
  SET previous_health = None
  SET reopen_mode = false
```

### Step 6: Compute Spec Health Score
*Skip in lightweight close mode*
```
COUNT resolved: number of items with verdict ✅ Resolved
COUNT acknowledged: number of items with verdict ⚠️ Acknowledged
COUNT not_done: number of items with verdict ❌ Not Done
COUNT total = resolved + acknowledged + not_done

IF total == 0:
  SET spec_health = 100  (no requirements to compare — trivially aligned)
ELSE:
  spec_health = round((resolved + acknowledged) / total * 100)

INTERPRET:
  100%: Artifacts fully aligned — no action needed
  80-99%: Minor gaps tracked — acceptable
  50-79%: Significant drift — recommend spec-kit-refresh before refactoring
  <50%: Artifacts are misleading — run spec-kit-refresh before proceeding
```

### Step 7: Patch spec artifacts for intentional deviations

For each gap marked `✅ Resolved — intentional deviation`:
```
IDENTIFY the section of spec.md or plan.md that no longer reflects reality
  
CASE: FR requirement wording differs from implementation
  → patch spec.md: update requirement text to match actual behavior, keeping original intent
  → ADD note: "(Updated by implementation summary — see close.md or implementation-summary.md)"

CASE: Architecture/design detail differs from implementation
  → patch plan.md: update the relevant section to reflect what was built
  → ADD note: "(Updated by implementation summary — see close.md or implementation-summary.md)"

CASE: Data model entity or contract differs
  → patch plan.md or data-model.md: reflect current schema/contract
  → ADD note: "(Updated by implementation summary — see close.md or implementation-summary.md)"
```

**User confirmation**: Present each proposed patch as:
```
PROPOSE: "Update spec.md FR-XXX from [old] to [new]? (reason: [rationale])"
WAIT for user approval before applying.
```

If user rejects a proposed patch → mark that artifact as `⚠️ needs review` in the Spec State table (not auto-updated).

### Step 8: Collect implementation details
```
IDENTIFY:
  - Files changed (from plan file paths, tasks, and git diff)
  - Dependencies added
  - Architecture decisions made during implementation
  - Deviations from plan (with rationale — why they deviated)
  - Test results (pass/fail counts)
  - Known limitations or deferred work
```

### Step 9: Generate output document

**Full mode** (summarize):
```
IF reopen_mode AND specs/[feature]/implementation-summary.md EXISTS:
  APPEND to existing specs/[feature]/implementation-summary.md:
    - New section: "## Reopened Summary ([ISO date])"
    - Updated Spec Health Score
    - "Previous health: N% -> Current health: M%"
    - New gap analysis entries (additive only)
    - NOTE: "Original summary preserved above."
ELSE:
  COPY spec-kit/templates/implementation-summary-template.md -> specs/[feature]/implementation-summary.md

Populate with:
- Spec Health Score at top (from Step 6)
- **Previous vs Current**: IF previous_health exists: "Previous health: N% -> Current health: M%"
- Spec Health Scoring table
- All gap analysis sections
- Spec Artifact Refresh section listing what was patched (from Step 7)
- Spec State table
```

**Lightweight mode** (close):
```
IF reopen_mode:
  APPEND to existing `specs/[feature]/close.md`:
    - A new section header: "## Close (Reopened — [ISO date])"
    - Updated Spec Health Score from Step 6
    - "Previous health: N% → Current health: M%"
    - Updated Artifact State for artifacts changed during reopen
    - Key decisions made during reopen
    - NOTE: "Original close preserved above. This section documents the reopened cycle only."

ELSE (first close):
  COPY `spec-kit/templates/close-template.md` → `specs/[feature]/close.md`

Populate with:
- Spec Health Score (from Step 6, or simplified "100%" if skipped)
- Intent Alignment: Yes/Partially/No
- Artifact State: quick status of each artifact
- Key Decisions: notable decisions made
- Spec Health Calculation breakdown (if available)
```

**Reopen conflict check** (before writing either mode):
```
IF reopen_mode AND any requirement status changed from ✅/⚠️ to a worse status:
  For each changed requirement:
    PROMPT user: "FR-XXX was [original status] in previous close, now [new status].
                  This is a regression. How should I document it?
                  1. Add as new entry (preserves original close — recommended)
                  2. Update the original close entry (overwrite)"
  WAIT for user response before writing.
```

### Step 10: Update or create bugs from gaps
*Skip in lightweight close mode*
```
FOR each "❌ Not Done" gap:
  IF bugs.md EXISTS:
    APPEND a new bug entry:
    ### BUG-NNN: Missing: [requirement description]
    - Severity: [major/minor]
    - Description: Specified in spec.md but not implemented (see implementation-summary.md)
    - Requires Clarification: [ ] no / [ ] yes
    - Status: open
    WRITE updated bugs.md (append to end)
  PROMPT user: "N gaps found with ❌ Not Done — bugs added to bugs.md. Run 'bugfix [feature]' when ready."
```

### Step 11: Report completion
```bash
REPORT:
  - Mode: Full summary / Lightweight close
  - TDD mode: Active / Bypassed by user
  - Output: specs/[feature]/implementation-summary.md or specs/[feature]/close.md
  - Spec Health: N%
  - Task completion: N/Total
  - Bug resolution: verified/total
  - Artifacts patched: spec.md [yes/no], plan.md [yes/no]
  - Gap analysis (full mode): N resolved, N acknowledged, N not done
  - New bugs created (if any gap was ❌ Not Done)
```

### Step 12: Append to history.md and Step 13: Commit (combined)

**Order is critical: history.md FIRST, then commit.**

1. **Append to history.md**:
   Append to `specs/[feature]/history.md` (create if missing):
   - Phase: Phase 6 — Complete
   - Artifact: `implementation-summary.md` or `close.md`, plus patched artifacts
   - Spec Health: N%

2. **PRE-COMMIT GUARD**:
   READ `specs/[feature]/history.md` — confirm the close/summary entry is recorded.
   If missing: BLOCK — must append before commit.

3. **Commit**:
   Follow `spec-kit/references/auto-commit.md`:
   - Scope: `implementation-summary.md` or `close.md`, plus patched `spec.md`, `plan.md`, `data-model.md`
   - Message: `"spec(phase-6): [feature] summary (health: N%)"`

## Gap Analysis Detail

The Gap Analysis section answers the key question: **"Does the code match what was planned?"**

Sources for comparison:
- **spec.md**: Functional Requirements (FR-###), User Stories, Success Criteria
- **plan.md**: Data model entities, API contracts, architecture decisions
- **tasks.md**: Task descriptions and file paths
- **git diff / git log**: Actual files changed on the branch

Verdict definitions:
| Verdict | Meaning | Follow-up |
|---------|---------|-----------|
| ✅ Resolved | Implemented as planned, OR intentionally different with documented rationale | No action needed (spec/plan auto-updated in Step 7) |
| ⚠️ Acknowledged | Deferred by user; not implemented but tracked | Record reason; revisit if needed |
| ❌ Not Done | Missing with no documented reason | Create bug entry in bugs.md |

## State Transition

After this skill completes, the feature enters **Complete** state:
- All tasks marked [X]
- All bugs marked verified
- Unknown gaps resolved or acknowledged via gap analysis
- Spec/plan artifacts patched to reflect intentional deviations
- Summary (full or close) captures final state
- Bugs created for ❌ Not Done gaps (if any)
- No further phases required unless user initiates a new cycle

## Phase State Detection

| Artifacts Present | Interpretation |
|:-----------------|:-------------|
| `implementation-summary.md` exists | Feature complete — full summary generated |
| `close.md` exists | Feature closed — lightweight close document |
| `implementation-summary.md` or `close.md` + all bugs verified | Feature complete and verified |
| `spec.md` or `plan.md` patched (diff from prior commit) | Artifacts reconciled with code |
| `implementation-summary.md` with open gaps (❌) | Summary generated but gaps remain — new bugs created |
| `implementation-summary.md` with open tasks | Partial summary (run again after completion) |

## Routing Commands

- "Summarize [feature]" — loads this skill, generates full implementation summary
- "Close [feature]" — loads this skill, generates lightweight close document
- "Implementation summary for [feature]" — same as summarize
- "Status of [feature]" — checks if summary exists, reports state

## Mandatory Close (User-Initiated)

After the bugfix loop completes (all bugs in bugs.md marked Status: verified), the workflow suggests Phase 6 (Summarize/Close) — the user decides when to run it:

```text
CHECK: All bugs in bugs.md have Status: verified

ACTION:
  1. Suggest the user run Phase 6: "'close [feature]' or 'summarize [feature]'?"
  2. WAIT for user choice: full summary ('summarize') or lightweight close ('close')
  3. Run the chosen mode
  4. Present output to user

BLOCKER: A feature CANNOT enter Complete state without Phase 6 completing.
  - User says "feature is done" or tries to start a new feature
  - CHECK: implementation-summary.md or close.md exists?
  - IF NOT: Block with "Complete Phase 6 first: run 'summarize [feature]' or 'close [feature]'"
```

**Note**: The mandatory close is enforced by the workflow orchestrator (`spec-kit-workflow`). When `spec-kit-test` marks the last bug as verified, it should suggest "All bugs verified — run 'close [feature]' to complete."

## Done When

- [ ] Output generated: implementation-summary.md (full) or close.md (lightweight)
- [ ] Spec health score computed and included
- [ ] All tasks marked complete in tasks.md
- [ ] All bugs marked verified in bugs.md
- [ ] ✅ Resolved deviations patched into spec.md and plan.md (with user approval)
- [ ] ❌ Not Done gaps converted to new bug entries in bugs.md (if any, full mode only)
- [ ] Report delivered to user with spec health score and artifact state
- **Commit**: `$COMMIT_HASH` (auto — `git log` for details)

## Next Skills

- Feature is now **Complete** — no further phases needed
- Propose to the user: Run `spec-kit-workflow` to start a new feature cycle
- Propose to the user: Run `spec-kit-specify` to add new features
- Propose to the user: Run `spec-kit-refresh` if artifacts show drift (for manual code changes)
- Propose to the user: Run `bugfix [feature]` if new gaps were added as bugs
