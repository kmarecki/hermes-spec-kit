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

### Validate and determine variants
```
EXTRACT variant descriptions from user request
ENSURE at least 2 variants (otherwise explore mode is meaningless)
LIMIT to at most 3 variants (delegate_task concurrency cap)
```

### Create variants directory
```
CREATE: specs/[feature]/variants/
DETECT project root (git rev-parse --show-toplevel)
```

### Create git worktrees (isolated working directories)

Each variant needs a physically separate working directory so subagents don't
interfere with each other's source files. Git worktrees share the same `.git`
database but have independent working trees, indexes, and HEADs.

```
WORKTREE_BASE = ../<repo>-worktrees/   (relative to project root, gitignored)

FOR each variant (variant-a, variant-b, ...):
  BRANCH = {explore_prefix}/NNN-feature-<variant>
  WORKTREE_PATH = $WORKTREE_BASE/explore-<variant>

  # Create branch from conventions prefix (feature_prefix or explore_prefix)
  RUN: git branch $BRANCH  2>/dev/null || echo "branch exists"

  # Create worktree
  RUN: git worktree add $WORKTREE_PATH $BRANCH

  # Verify subagents can build in isolation
  IF specs/[feature]/plan.md has build commands:
    RUN: cd $WORKTREE_PATH && <build-smoke-test>  (e.g., npm install --frozen-lockfile)
    NOTE: "Build verified for variant <variant>"
```

> **Smoke test caveat**: Don't run the full suite — just verify the variant's
> dependencies resolve and it can produce its first change. Deep testing happens
> when that variant's subagent runs it.

Register each variant's worktree path:
```
VARIANTS[<variant>] = {
  "branch": "{explore_prefix}/NNN-feature-<variant>",
  "worktree": "<absolute-worktree-path>",
  "artifacts": "specs/[feature]/variants/<variant>/"
}
```

Worktree conventions:
- Directory: `../<repo>-worktrees/explore-<variant>/`
- Add `**/worktrees/` to `.gitignore` so worktree dirs are never committed
- Worktrees persist after subagents finish — compare phase reads them

### Spawn parallel subagents

```python
delegate_task(tasks=[
  {"goal": "Implement [feature] using [Variant A approach]",
   "context": "Spec: specs/[feature]/spec.md\n"
              "Worktree: <absolute-path-to-worktree-a>\n"
              "Branch: {explore_prefix}/NNN-feature-a\n"
              "Artifacts dir: specs/[feature]/variants/a/\n"
              "All work happens inside the worktree path — cd there first.",
   "toolsets": ["file", "terminal"]},
  {"goal": "Implement [feature] using [Variant B approach]",
   "context": "Spec: specs/[feature]/spec.md\n"
              "Worktree: <absolute-path-to-worktree-b>\n"
              "Branch: {explore_prefix}/NNN-feature-b\n"
              "Artifacts dir: specs/[feature]/variants/b/\n"
              "All work happens inside the worktree path — cd there first.",
   "toolsets": ["file", "terminal"]},
])
```

Each subagent receives:
- Feature spec and constitution for context
- Branch name: `{explore_prefix}/NNN-feature-<variant>`
- Worktree path: `<project>/../<repo>-worktrees/explore-<variant>/`
- Independent spec-artifact directory: `specs/[feature]/variants/<variant>/`

Subagent instructions for isolation:
1. `cd <worktree-path>` immediately on start
2. All file writes and git commands operate inside YOUR worktree only
3. Push changes to the shared branch: `git push origin {explore_prefix}/NNN-feature-<variant>`
4. Do NOT read or write files from other worktrees
5. Spec artifacts go to `specs/[feature]/variants/<variant>/` (in the main repo)

### After completion
```
NOTE: "All N variants completed."
NOTE: "Worktrees preserved at ../<repo>-worktrees/ for the compare phase."
NOTE: "Run 'compare [feature]' to review and select a winner."
Append to `specs/[feature]/history.md` following `spec-kit/references/history-tracking.md`:
- Phase: Explore
- Artifacts: specs/[feature]/variants/*/
- Worktrees: ../<repo>-worktrees/explore-*/
```

## Common Pitfalls
1. **Too many variants (3+):** Limited by `delegate_task.max_concurrent_children`. If user proposes 5, suggest grouping or prioritizing the top 3.
2. **Not providing enough context**: Each subagent has no conversation history. Put all relevant spec context in the goal/context fields.
3. **Assuming subagents completed successfully**: Verify by checking variant worktree directories exist before running compare.
4. **Branch must exist before `git worktree add`**: `git worktree add <path> <branch>` requires the branch to already exist. Always create the branch first with `git branch <branch>` then add the worktree. `git worktree add -b <branch> <path>` creates and checks out a new orphan-like branch but from HEAD — use explicit two-step to avoid ambiguity.
5. **Worktree cleanup after compare**: After the winning variant is selected and promoted, remove all worktrees with `git worktree remove <path>` and prune with `git worktree prune`. Worktrees left behind cause git operations warnings.
6. **Subagent pushes require remote**: Before subagents can push to the shared branch, the branch must exist on origin. Push the branch head before spawning: `git push origin {explore_prefix}/NNN-feature-<variant>` (after creation).
