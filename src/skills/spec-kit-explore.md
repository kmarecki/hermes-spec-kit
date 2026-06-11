---
name: spec-kit-explore
description: Load when the user says 'spec-kit explore [feature] with [variants]', 'speckit explore [feature] with [variants]', "explore [feature]", or "try different approaches for [feature]" — spawns parallel subagents for creative exploration.
version: 1.2.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, explore, parallel, variants]
    related_skills: [spec-kit-compare, spec-kit-workflow]
---

# spec-kit-explore

**Task Persona**: Adopt the mindset of a creative architect exploring the design space. Each variant is a legitimate approach — don't bias toward your favorite. Document tradeoffs so the user can make an informed choice.

**Phase**: N/A (parallel exploration)

**Purpose**: Spawn N parallel `delegate_task` subagents, each on its own branch (`{explore_prefix}/NNN-feature-<variant>`), running independent specify → clarify → plan → tasks → [implement] cycles. User compares variants with `spec-kit-compare`.

**When NOT to use**: For bounded, well-understood features with a single obvious approach — just implement directly.

**Routing**: Load this skill when the user says "explore [feature] with [variants]". Spawns parallel subagents — runs independently.


## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Validate variants
```
IF number of variants < 2:
  BLOCK: "Need at least 2 variants to explore. Provide different approaches."
IF number of variants > 3:
  REDUCE to 3 (delegate_task max per turn)
  WARN: "Limited to 3 variants. Picking the top 3 by diversity."
```

### Create variant directories
```
FOR each variant:
  CREATE specs/[feature]/variants/<variant>/
```

### Create branches and worktrees
```
FOR each variant:
  BRANCH_NAME="{explore_prefix}/NNN-feature-<variant>"
  WORKTREE_PATH="../<repo>-worktrees/explore-<variant>"

  git branch "$BRANCH_NAME"
  git worktree add "$WORKTREE_PATH" "$BRANCH_NAME"

  NOTE: "Worktree created at $WORKTREE_PATH for variant <variant>"
```

### Spawn subagents
```
FOR each variant:
  delegate_task(
    goal: "Implement variant <variant> for [feature]",
    context: "
      You are working in a git worktree at ../<repo>-worktrees/explore-<variant>.
      Branch: {explore_prefix}/NNN-feature-<variant>
      
      Work in the worktree directory, not the main repo:
      cd ../<repo>-worktrees/explore-<variant>
      
      Run: specify → clarify (if needed) → plan → tasks → [implement]
      
      Write spec artifacts to: specs/[feature]/variants/<variant>/
      (in the main repo, not the worktree)
      
      After complete, push the branch:
      git push origin {explore_prefix}/NNN-feature-<variant>
    ",
    toolsets: ["file", "terminal", "skills"]
  )

NOTE: "Spawned N variant subagents — they will run in parallel."
```

### After completion
```
NOTE: "All N variants completed."
NOTE: "Worktrees preserved at ../<repo>-worktrees/ for the compare phase."
NOTE: "Run 'compare [feature]' to review and select a winner."
```

### Append to history.md
Append to `specs/[feature]/history.md` following `spec-kit/references/history-tracking.md`:
- Phase: Explore
- Artifacts: specs/[feature]/variants/*/
- Worktrees: ../<repo>-worktrees/explore-*/

## Common Pitfalls
1. **Too many variants (3+):** Limited by `delegate_task.max_concurrent_children`. If user proposes 5, suggest grouping or prioritizing the top 3.
2. **Not providing enough context**: Each subagent has no conversation history. Put all relevant spec context in the goal/context fields.
3. **Assuming subagents completed successfully**: Verify by checking variant worktree directories exist before running compare.
4. **Branch must exist before `git worktree add`**: `git worktree add <path> <branch>` requires the branch to already exist. Always create the branch first with `git branch <branch>` then add the worktree. `git worktree add -b <branch> <path>` creates and checks out a new orphan-like branch but from HEAD — use explicit two-step to avoid ambiguity.
5. **Worktree cleanup after compare**: After the winning variant is selected and promoted, remove all worktrees with `git worktree remove <path>` and prune with `git worktree prune`. Worktrees left behind cause git operations warnings.
6. **Subagent pushes require remote**: Before subagents can push to the shared branch, the branch must exist on origin. Push the branch head before spawning: `git push origin {explore_prefix}/NNN-feature-<variant>` (after creation).
