---
name: spec-kit-compare
description: Use when the user says 'compare [feature]' or 'compare variants' — post-exploration decision matrix.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, compare, exploration, decision]
    related_skills: [spec-kit-explore, spec-kit-workflow]
---

# spec-kit-compare

**Phase**: N/A (post-exploration)

**Purpose**: Load all variant artifacts from creative exploration, build a structured comparison matrix, guide the user to select a winning variant, and optionally cherry-pick features from rejected variants.

**When NOT to use**: When there's only one implementation path — just implement it directly.

**Routing**: Load this skill when the user says "compare [feature]" or "compare variants". Runs after explore mode completes.


**Prerequisites**: `specs/[feature]/variants/` must contain at least 2 variant directories.

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Load all variant artifacts
```
LOAD specs/[feature]/variants/<variant>/
  spec.md, plan.md, tasks.md, research.md, data-model.md
  (IF EXISTS) implementation-summary.md
```

### Build comparison matrix
Compare across these dimensions:
- **Tech Stack**: Languages, frameworks, dependencies
- **Functional Coverage**: Which FR-### requirements each variant satisfies
- **Architecture**: Structure, data model, contracts
- **Complexity**: Task count, estimated effort, parallelization potential
- **Test Coverage**: Test count, coverage approach
- **Risk**: Known limitations, unresolved questions

Format:
```
| Dimension | Variant A | Variant B | Variant C |
|-----------+-----------+-----------+-----------|
| Tech      | ...       | ...       | ...       |
```

### Present to user
```
SUMMARY:
- Variant A: [best for X]
- Variant B: [best for Y]
- Variant C: [best for Z]

Recommendation: [agent's recommendation with rationale]

ASK: "Which variant wins? Or should we cherry-pick from multiple?"
```

### Handle user decision
```
IF user picks ONE variant:
  COPY specs/[feature]/variants/[winner]/* → specs/[feature]/
  NOTE: "[Variant] selected as implementation baseline."

IF user wants to cherry-pick:
  For each feature to cherry-pick:
    IDENTIFY source variant and target spec/plan
    UPDATE spec.md, plan.md, tasks.md accordingly
  NOTE: "Cherry-picked: [list of features merged from rejected variants]"

IF user rejects all variants:
  NOTE: "All variants rejected. Returning to specification phase."
  PROMPT: "Run 'spec-kit-specify' to refine requirements."
```

### Generate comparison.md
Copy `spec-kit/templates/comparison-template.md` → `specs/[feature]/comparison.md`

### Cleanup
```
NOTE: "Variants preserved at specs/[feature]/variants/ for reference.
      Delete this directory when no longer needed."
```

## Common Pitfalls
1. **Cherry-picking without verifying compatibility**: Features from different variants may conflict. Verify the combined spec/plan is coherent.
2. **Assuming the recommendation is correct**: Present the recommendation with rationale, then ask. The user may have priorities the agent doesn't know about.
3. **Deleting variants immediately**: Keep the variants/ directory until the implementation is well underway — the user might change their mind.
