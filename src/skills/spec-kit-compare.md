---
name: spec-kit-compare
description: Load when the user says 'spec-kit compare [feature]', 'speckit compare [feature]', 'spec-kit compare variants', 'speckit compare variants', "compare variants for [feature]", or "compare approaches for [feature]" — post-exploration decision matrix.
version: 1.2.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, compare, exploration, decision]
    related_skills: [spec-kit-explore, spec-kit-workflow]
---

# spec-kit-compare

**Task Persona**: Adopt the mindset of a thorough code auditor comparing alternatives. For each variant, verify implementation against spec and plan. Use web search to research best practices and patterns. Compare apples to apples — surface tradeoffs clearly with evidence. The user picks the winner; you provide the analysis.

**Phase**: N/A (post-exploration comparison)

**Purpose**: Load all variant artifacts from creative exploration, build a structured comparison matrix, guide the user to select a winning variant, and optionally cherry-pick features from rejected variants.

**When NOT to use**: When there's only one implementation path — just implement it directly.

**Routing**: Load this skill when the user says "compare [feature]" or "compare variants". Runs after explore mode completes.


**Prerequisites**: `specs/[feature]/variants/` must contain at least 2 variant directories. Worktrees from explore phase should still exist at `../<repo>-worktrees/explore-*/`.

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Load all variant artifacts
```
LOAD specs/[feature]/variants/<variant>/
  spec.md, plan.md, tasks.md, research.md, data-model.md
  (IF EXISTS) implementation-summary.md

LOAD worktree directory (IF EXISTS):
  ../<repo>-worktrees/explore-<variant>/
  (source code from each variant's full implementation)
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
  PROMPT: "Now promote variant code to the main feature branch.
           Choose a promotion method below."

IF user wants to cherry-pick:
  For each feature to cherry-pick:
    IDENTIFY source variant and target spec/plan
    UPDATE spec.md, plan.md, tasks.md accordingly
  NOTE: "Cherry-picked: [list of features merged from rejected variants]"
  PROMPT: "Now promote cherry-picked code to the main feature branch.
           Choose a promotion method below."

IF user rejects all variants:
  NOTE: "All variants rejected. Returning to specification phase."
  PROMPT: "Run 'spec-kit-specify' to refine requirements."
```

### Promote winning variant code to main feature branch

After the user picks a variant (or cherry-picks features), the winning
variant's code lives in a separate git worktree on branch
`{explore_prefix}/NNN-feature-<variant>`. It must be merged into the main feature
branch `{feature_prefix}/NNN-name`.

**Prerequisites**: The main feature branch `{feature_prefix}/NNN-name` must exist and
be up-to-date with the spec. Run this from the main repo (not the worktree).

**Step 1: Merge or cherry-pick the code**

```
IF user wants a full merge:
  RUN: git checkout {feature_prefix}/NNN-name
  RUN: git merge {explore_prefix}/NNN-feature-<winner> --no-ff
  COMMIT: Use the variant_promotion commit template from specs/git-conventions.md
          (default: "feat: [NNN-name] merge winning variant [variant-name]")

IF user wants selective cherry-pick (specific features only):
  For each cherry-picked feature:
    FIND commit(s) on {explore_prefix}/NNN-feature-<source> that implement it
    RUN: git checkout {feature_prefix}/NNN-name
    RUN: git cherry-pick <commit-hash>...
  COMMIT: Use the variant_promotion commit template from specs/git-conventions.md
          (default: "feat: [NNN-name] cherry-pick [features] from [variant]")

IF variants produced code in the main repo worktree but NOT on a separate branch:
  # Fallback: copy source files directly
  RUN: cp -r ../<repo>-worktrees/explore-<winner>/src/<relevant-dirs> ./
  COMMIT: "feat: [NNN-name] adopt code from [variant]"
```

**Step 2: Update spec artifacts**

After promotion:
```
IF spec/plan/tasks were copied from variant to specs/[feature]/:
  VERIFY: artifacts in specs/[feature]/ match what was merged
  UPDATE: any paths or references that changed during merge

APPEND to specs/[feature]/history.md:
- Phase: Compare → Promote
- Winner: [variant-name]
- Promotion method: merge / cherry-pick / file-copy
- Branch: {feature_prefix}/NNN-name (merged from {explore_prefix}/NNN-feature-<winner>)
```

**Step 3: Handle conflicts (if merge has conflicts)**

```
IF merge produces conflicts:
  NOTE: "Merge conflicts detected in: [list conflicted files]"
  REPORT: "Both the main branch and the variant branch modified these files.
           Review the conflict markers and resolve."
  PROMPT: "Resolve conflicts in the affected files, then:
           git add <resolved-files> && git merge --continue"
```

**Project-level path awareness**: The worktree path (`../<repo>-worktrees/`)
is relative to the project root. Detect the project root with
`git rev-parse --show-toplevel` and construct the full worktree path
as `<project-root>/../<repo>-worktrees/explore-<variant>/`.

**Branch name enforcement**: Both branches involved (`{feature_prefix}/NNN-name` and
`{explore_prefix}/NNN-feature-<variant>`) must follow the convention from
specs/git-conventions.md (read feature_prefix and explore_prefix).
Verify with `git branch --list` before any git operation.

### Generate comparison.md
Copy `spec-kit/templates/comparison-template.md` → `specs/[feature]/comparison.md`

### Cleanup
``` 
NOTE: "Variants preserved at specs/[feature]/variants/ for reference.
      Delete this directory when no longer needed."
NOTE: "Worktrees preserved at ../<repo>-worktrees/ in case you need
      to revisit a rejected variant. Clean up with:
      git worktree remove ../<repo>-worktrees/explore-<variant>
      git worktree prune"
```

## Transition Log
Append to `specs/[feature]/history.md` following `spec-kit/references/history-tracking.md`:
- Phase: Compare
- Artifacts: `comparison.md`

## Common Pitfalls
1. **Cherry-picking without verifying compatibility**: Features from different variants may conflict. Verify the combined spec/plan is coherent.
2. **Assuming the recommendation is correct**: Present the recommendation with rationale, then ask. The user may have priorities the agent doesn't know about.
3. **Deleting variants immediately**: Keep the variants/ directory until the implementation is well underway — the user might change their mind.
4. **Merge conflicts during promotion**: If both the main branch and the winning variant touched the same files, `git merge` will produce conflicts. Don't panic — it's expected when parallel agents work on the same spec. Step through each conflict file.
5. **Cherry-picked commits may depend on intermediate commits**: If you cherry-pick feature commits without their parent commits (dependency commits from the variant), the build may break. Prefer full merge unless you're certain the cherry-picked commits are self-contained.
6. **Worktrees not cleaned up**: After promotion, remove all variant worktrees with `git worktree remove <path>` and prune with `git worktree prune`. Leftover worktrees cause warnings and consume disk space.
