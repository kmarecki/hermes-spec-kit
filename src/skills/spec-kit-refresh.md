---
name: spec-kit-refresh
description: Lightweight artifact refresh — reconcile spec/plan artifacts with actual code without running a full summary. Useful for manual code changes or quick alignment.
version: 1.0.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, refresh, alignment, reconciliation]
    related_skills: [spec-kit-summarize, spec-kit-workflow]
---

# spec-kit-refresh

**Phase**: N/A (standalone — run at any time)

**Purpose**: Reconcile spec/plan artifacts with the actual codebase without generating a full implementation summary or close document. This is useful when:
- Code was changed outside the spec-kit workflow (manual edits, refactoring)
- User wants to bring spec artifacts up to date before a new bugfix/feature cycle
- Summary identified drift but user wants a guided reconcile, not an auto-patch

**When NOT to use**:
- After a completed feature with all bugs verified → use `spec-kit-summarize` (full) or "Close [feature]" (lightweight)
- To generate a gap analysis or close a feature → use `spec-kit-summarize`
- To start a new feature → use `spec-kit-workflow`

**Prerequisites**: `specs/[feature]/spec.md` (at least one artifact exists to reconcile)
**Artifacts**: Updated `spec.md`, `plan.md`, `data-model.md`, `contracts/*.md`

## Execution

### Step 1: Load artifacts and code state
```
LOAD specs/[feature]/spec.md
LOAD specs/[feature]/plan.md                    (IF EXISTS)
LOAD specs/[feature]/data-model.md              (IF EXISTS)
LOAD specs/[feature]/contracts/                 (IF EXISTS)
LOAD specs/[feature]/bugs.md                    (IF EXISTS)

RUN: git diff main --name-status
  OR: git status --short
  CAPTURE current code state
```

### Step 2: Identify discrepancies
```
FOR EACH requirement (FR-###) in spec.md:
  COMPARE against actual code:
    - Does the feature described in FR-XXX exist in the codebase?
    - Does its actual behavior match the spec description?
    - Are there new files with no corresponding FR?
  CLASSIFY:
    Match      — spec matches code, no change needed
    Mismatch   — spec description differs from code behavior
    Missing    — spec describes something not in code (code behind spec)
    Unplanned  — code does something not in spec (spec behind code)
```

### Step 3: Present discrepancies to user
```
FOR EACH mismatch, missing, or unplanned item:
  PRESENT:
    "spec.md says: [excerpt from spec]"
    "Code does:   [actual behavior from code analysis]"
    "→ Update spec to match code? (yes/no)"

  IF yes:
    patch spec.md to reflect actual behavior
  IF no:
    SKIP (mark as user-intentional — no change)

LIMIT: Present at most 5 discrepancies per session. If more exist,
  say "N discrepancies found — run 'spec-kit-refresh [feature]' again
  for the next batch."
```

### Step 4: Refresh plan.md and data-model.md
```
IF plan.md EXISTS:
  LOAD current plan.md
  COMPARE architecture, data model, API contracts against actual code
  FOR EACH discrepancy:
    PRESENT: "plan.md says [X], code does [Y]. Update plan?"
    IF yes: patch plan.md

IF data-model.md EXISTS:
  COMPARE entities/fields against actual codebase
  FOR EACH discrepancy:
    PRESENT: "data-model.md says [X], code has [Y]. Update data model?"
    IF yes: patch data-model.md
```

### Step 5: Record refresh
```
NOTE in output:
  - Artifacts checked: [spec.md, plan.md, data-model.md, ...]
  - Items updated: N
  - Items skipped (user declined): N
  - Items requiring user manual review: N (user declined but drift remains)
```

### Step 6: Commit (auto)
```bash
IF `git rev-parse --git-dir > /dev/null 2>&1`; THEN
  IF any artifacts were updated:
    COMMIT_MSG="spec(refresh): [feature] reconcile spec artifacts with code"
    git add specs/[feature]/spec.md     \
           specs/[feature]/plan.md      \
           specs/[feature]/data-model.md
    git commit -m "$COMMIT_MSG" --no-verify
    COMMIT_HASH=$(git rev-parse HEAD)
    NOTE: "Artifact refresh committed as $COMMIT_HASH"
  ELSE:
    NOTE: "No artifacts changed — nothing to commit"
ELSE
  NOTE: "Not a git repository — skipping automatic commit"
```

## Key Difference from spec-kit-summarize

| Aspect | spec-kit-summarize | spec-kit-refresh |
|--------|-------------------|------------------|
| Output | `implementation-summary.md` or `close.md` | No output file — patches artifacts in-place |
| Gap analysis | Full ✅/⚠️/❌ matrix | Per-item yes/no comparison |
| Spec health score | Computed and included | Not computed |
| Bugs from gaps | Created for ❌ Not Done | Not created |
| Spec/plan patches | Auto-patches with user confirmation | Manual per-item approval |
| When to use | End of feature, close, or full review | Mid-stream alignment, manual code changes |
| Complexity | Full pipeline (10 steps) | Lightweight (3 steps) |

## Routing Commands

- "Refresh [feature]" — loads this skill, reconciles spec artifacts with code
- "Sync spec for [feature]" — same
- "Align artifacts for [feature]" — same

## Done When

- [ ] All artifact discrepancies presented to user
- [ ] User-approved updates applied to spec.md, plan.md, data-model.md (as needed)
- [ ] User-declined items noted for manual review
- [ ] Report delivered with change summary
- [ ] Commit made (if changes applied)

## Next Skills

- Propose to the user: Run `spec-kit-summarize` to generate a full implementation summary
- Propose to the user: Run `spec-kit-workflow` to start a new feature cycle
