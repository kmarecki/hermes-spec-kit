---
name: spec-kit-refresh
description: Use when the user says 'refresh [feature]' or 'sync spec for [feature]' — standalone artifact reconciliation.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, refresh, alignment, reconciliation]
    related_skills: [spec-kit-summarize, spec-kit-workflow]
---

# spec-kit-refresh

**Phase**: N/A (standalone)

**Purpose**: Reconcile spec/plan artifacts with actual code without generating a summary or close document. For manual code changes or mid-stream alignment.

**When NOT to use**: To close a feature — use `spec-kit-summarize` instead.

**Routing**: Load this skill when the user says "refresh [feature]" or "sync spec for [feature]". Standalone — no prerequisite routing needed.
 To verify fresh implementation — the implement skill's batch commit already captures the design.

**Prerequisites**: `specs/[feature]/spec.md` must exist.

## Execution

### Load artifacts and code state
```
LOAD specs/[feature]/spec.md, plan.md (IF EXISTS), data-model.md, contracts/
RUN: git diff main --name-status
```

### Identify discrepancies
```
For each FR-###: compare spec description against actual code.
Classify: Match / Mismatch / Missing / Unplanned
```

### Present discrepancies to user (max 5 per session)
```
"spec.md says: [excerpt]"
"Code does:   [actual behavior]"
"→ Update spec to match code? (yes/no)"
```

### Refresh plan.md and data-model.md
Same per-item approval for architecture, data model, and contract discrepancies.

### Commit
See `spec-kit/references/auto-commit.md`:
- Scope: patched spec/plan/data-model files
- Message: `"spec(refresh): [feature] reconcile artifacts"`

## Key Difference from Summary

| Aspect | summarize | refresh |
|--------|-----------|---------|
| Output | summary/close document | In-place patches |
| Gap analysis | Full matrix | Per-item yes/no |
| Spec health | Computed | Not computed |
| When | End of feature | Mid-stream alignment |

## Common Pitfalls
1. **Using refresh instead of close**: Refresh doesn't generate a close document. The feature won't be marked complete.
2. **Bulk patching without user approval**: Each discrepancy needs explicit yes/no. Don't auto-approve.
