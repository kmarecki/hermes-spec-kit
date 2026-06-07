---
name: spec-kit-compare
description: Compare all parallel exploration variants — spec, plan, and implementation — and guide the user to choose a winner.
version: 1.0.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, compare, variants, decision, exploration]
    related_skills: [spec-kit-explore, spec-kit-workflow]
---

# spec-kit-compare

**Phase**: Comparison (Post-Exploration)

**Purpose**: After creative exploration completes, load all variant artifacts from `specs/[feature]/variants/`, build a structured comparison matrix across spec, plan, and implementation dimensions, and guide the user to select the winning variant. Optionally incorporate changes from rejected variants.

**When to use**: User says "compare [feature]" or "compare variants for [feature]" after running `spec-kit-explore`

**Prerequisites**: `spec-kit-explore` must have been run (variants/ directory must exist with at least 2 variants)

**Artifacts**:
- `specs/[feature]/comparison.md` (primary artifact — comparison report)

## Execution

### Step 1: Validate prerequisites

```
IF specs/[feature]/variants/ NOT EXISTS:
  ERROR: "No variants found. Run 'spec-kit-explore' first"

IF fewer than 2 variant directories found:
  ERROR: "Need at least 2 variants to compare. Run 'spec-kit-explore' with multiple variants"
```

### Step 2: Load all variant artifacts

```bash
SCAN: specs/[feature]/variants/*/
FOR EACH variant directory:
  LOAD: spec.md (if exists)
  LOAD: plan.md (if exists)
  LOAD: tasks.md (if exists)
  LOAD: bugs.md (if exists, means implementation was done)
  CHECK: git branch exists (explore/NNN-feature-<variant>)
  CAPTURE: git log --oneline for the variant branch
```

### Step 3: Build comparison matrix

For each dimension, analyze what each variant produced:

**A. Specification Comparison**
```
| Dimension | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Tech Stack | React + Tailwind | Vue 3 + PrimeVue | SvelteKit |
| Architecture | SPA | SPA | SSR |
| FRs covered | 8/8 | 8/8 | 7/8 |
| UI Approach | Component lib | Framework-native | Minimal |
```

**B. Plan Comparison**
```
| Dimension | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Complexity | High | Medium | Low |
| Dependencies | 12 | 8 | 3 |
| Data model entities | 5 | 4 | 5 |
| Contracts defined | Full REST | Full REST | REST + WS |
```

**C. Effort Comparison**
```
| Dimension | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Total tasks | 12 | 14 | 10 |
| Implemented | 12 | 14 | 8 |
| Test tasks | 4 | 5 | 3 |
| Estimated effort | 3 days | 4 days | 2 days |
```

**D. Implementation Comparison (if any variant reached implementation)**
```
| Dimension | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Implemented? | Yes | Yes | Partial |
| Tests passing | 45/47 | 52/52 | 30/32 |
| Bugs found | 2 | 0 | 1 |
| Branch | explore/... | explore/... | explore/... |
```

### Step 4: Synthesize recommendations

For each variant, summarize:
- **Strengths** — what this variant does best
- **Weaknesses** — trade-offs or limitations
- **Best for** — what scenario this variant would be ideal for
- **Notable features** — unique capabilities worth preserving

```
## Recommendations

### Variant A (React)
- **Strengths**: Rich ecosystem, best component library support
- **Weaknesses**: Heavier bundle size, more boilerplate
- **Best for**: Large teams with React expertise
- **Notable**: Excellent drag-and-drop implementation

### Variant B (Vue)
- **Strengths**: Simple and intuitive, lower learning curve
- **Weaknesses**: Smaller ecosystem for this domain
- **Best for**: Small teams, rapid prototyping
- **Notable**: Best test coverage (52/52 passing)
```

### Step 5: User selects the winner

Present the comparison and ask the user to choose:

```
PROPOSE: Based on the comparison, I recommend Variant B (Vue) for these reasons:
  - Highest test coverage
  - Fully implemented with zero bugs
  - Moderate complexity

Which variant do you want to pursue as the primary?
  [A] Variant A (React)
  [B] Variant B (Vue)  <-- recommended
  [C] Variant C (Svelte)
  [Custom] Incorporate selected features from multiple variants
```

If the user chooses **Custom** (incorporate from multiple):

```
FOR EACH feature the user wants to incorporate:
  IDENTIFY which variant has the best implementation
  INSTRUCT: cherry-pick from that branch
  Example: git cherry-pick <commit-hash>  # from explore/NNN-feature-react
```

### Step 6: Write comparison.md

Generate `specs/[feature]/comparison.md` with the full comparison matrix, user's decision, and any cherry-picked changes from rejected variants:

```markdown
# Comparison: [Feature]

**Date**: [ISO_TIMESTAMP]
**Variants compared**: [N]
**Winner**: [variant name]

## Decision Rationale
[User's stated reasons for choosing this variant]

## Comparison Matrix
[... full matrix from Step 3 ...]

## Features Incorporated from Rejected Variants
| Feature | Source Variant | How |
|---------|---------------|-----|
| Drag-and-drop UX | Variant A (React) | Cherry-picked abc1234 |
| Test pattern | Variant B (Vue) | Adopted manually |

## Recommendations Summary
[... from Step 4 ...]

## Next Steps
- Continue development on the winning branch
- Run `spec-kit-summarize` when complete
```

### Step 7: Set up the winning branch

```bash
IF user selected a single variant:
  NOTE: "Continue working on branch explore/NNN-feature-<winner>"
  PROPOSE: "Run spec-kit-implement to complete any remaining tasks, or spec-kit-test to verify"

IF user selected Custom (cherry-picks):
  FOR each cherry-pick:
    RUN: git cherry-pick <commit>
  NOTE: "Cherry-picked changes from rejected variants"
  PROPOSE: "Run tests to verify the merged changes"
```

## Done When

- [ ] Comparison matrix presented to user
- [ ] User selected winning variant
- [ ] comparison.md written to spec directory
- [ ] Cherry-picked changes from rejected variants applied (if any)
- [ ] User knows next steps

## Next Skills

- Propose to the user: Run `spec-kit-implement` to continue implementation on the winning branch
- Propose to the user: Run `spec-kit-test` to verify the winning implementation
- Propose to the user: Run `spec-kit-summarize` when complete
