---
name: spec-kit-summarize
description: Generate implementation summary and compare actual code with spec and plan. Phase 6 - run after testing complete.
category: software-development
---

# spec-kit-summarize

**Phase**: 6 (Summary)

**Purpose**: When implementation is complete and no more testing is needed, read all artifacts, compare actual code changes against the spec and plan, and produce a comprehensive `implementation-summary.md`. All gaps between what was planned vs what was built are either **resolved** (intentional deviation, acknowledged) or **tracked** (deferred for later bugs in bugs.md).

**When to run**:
- After testing is complete (all bugs verified)
- Or at any point to get a snapshot of current implementation state
- User says: "Summarize [feature]" or "implementation summary for [feature]"

**Prerequisites**: `spec-kit-implement` must have been run (tasks.md exists)
**Artifacts**:
- `specs/[feature]/implementation-summary.md` (primary artifact — generated report)

## Execution

### Step 1: Validate and load all artifacts
```
LOAD specs/[feature]/spec.md
LOAD specs/[feature]/plan.md
LOAD specs/[feature]/tasks.md
LOAD specs/[feature]/data-model.md          (IF EXISTS)
LOAD specs/[feature]/contracts/             (IF EXISTS)
LOAD specs/[feature]/research.md            (IF EXISTS)
LOAD specs/[feature]/quickstart.md          (IF EXISTS)
LOAD specs/[feature]/clarify.md             (IF EXISTS)
LOAD specs/[feature]/bugs.md               (IF EXISTS)
LOAD specs/constitution.md                  (IF EXISTS)
```

### Step 2: Analyze tasks.md status
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

### Step 3: Analyze bugs.md status
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

### Step 4: Compare code against spec and plan (git diff analysis)
```
RUN: git diff main --name-status
  OR: git log --oneline --name-only HEAD..main
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

### Step 5: Build gap analysis
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

### Step 6: Collect implementation details
```
IDENTIFY:
  - Files changed (from plan file paths, tasks, and git diff)
  - Dependencies added
  - Architecture decisions made during implementation
  - Deviations from plan (with rationale — why they deviated)
  - Test results (pass/fail counts)
  - Known limitations or deferred work
```

### Step 7: Generate implementation-summary.md
COPY `spec-kit/templates/implementation-summary-template.md` → `specs/[feature]/implementation-summary.md`

Populate with:
```
## Overview
[2-3 sentence summary]

## What Was Implemented
| Requirement | Status | Notes |

## Gap Analysis — Plan vs Implementation
| Category | Planned | Actual | Verdict | Notes |
|----------|---------|--------|---------|-------|
| FR-001   | ...     | ...    | ✅ Resolved | ...
| US-002   | ...     | ...    | ⚠️ Acknowledged | deferred, scope cut
| Entity X | ...     | —      | ❌ Not Done | missing, file never created

### Resolved Deviations
- list of intentional changes with rationale

### Acknowledged Gaps (Deferred)
- list of things cut/deferred

## Files Changed
| File | Type | Description |

## Known Issues & Bugs
| Bug ID | Severity | Status | Summary |

## Decisions Made
| Decision | Rationale | Alternatives |

## Spec State
| Artifact | Status | Action Needed |
```

### Step 8: Update or create bugs from gaps
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

### Step 9: Report completion
```
REPORT:
  - Summary: specs/[feature]/implementation-summary.md
  - Task completion: N/Total
  - Bug resolution: verified/total
  - Gap analysis: N resolved, N acknowledged, N not done
  - New bugs created (if any gap was ❌ Not Done)
  - Spec state recommendations per artifact
```

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
| ✅ Resolved | Implemented as planned, OR intentionally different with documented rationale | No action needed |
| ⚠️ Acknowledged | Deferred by user; not implemented but tracked | Record reason; revisit if needed |
| ❌ Not Done | Missing with no documented reason | Create bug entry in bugs.md |

## State Transition

After this skill completes, the feature enters **Complete** state:
- All tasks marked [X]
- All bugs marked verified
- Unknown gaps resolved or acknowledged via gap analysis
- Implementation-summary.md captures final state including any deviations
- Bugs created for ❌ Not Done gaps (if any)
- No further phases required unless user initiates a new cycle

## Phase State Detection

| Artifacts Present | Interpretation |
|:-----------------|:-------------|
| `implementation-summary.md` exists | Feature complete — summary generated |
| `implementation-summary.md` + all bugs verified | Feature complete and verified |
| `implementation-summary.md` with open gaps (❌) | Summary generated but gaps remain — new bugs created |
| `implementation-summary.md` with open tasks | Partial summary (run again after completion) |

## Routing Commands

- "Summarize [feature]" — loads this skill, generates implementation summary
- "Implementation summary for [feature]" — same
- "Status of [feature]" — checks if summary exists, reports state

## Done When

- [ ] implementation-summary.md generated with gap analysis
- [ ] All tasks marked complete in tasks.md
- [ ] All bugs marked verified in bugs.md
- [ ] ❌ Not Done gaps converted to new bug entries in bugs.md (if any)
- [ ] Report delivered to user with spec state recommendations

## Next Skills

- Run `spec-kit-workflow` to start a new feature cycle
- Run `spec-kit-specify` to add new features
- Run `bugfix [feature]` if new gaps were added as bugs
- No further phases needed for this feature
