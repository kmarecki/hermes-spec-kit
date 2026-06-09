---
name: spec-kit-explore
description: Use when the user says 'explore [feature] with [variants]' — spawns parallel subagents for creative exploration.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, explore, parallel, variants]
    related_skills: [spec-kit-compare, spec-kit-workflow]
---

# spec-kit-explore

**Phase**: N/A (parallel exploration)

**Purpose**: Spawn N parallel `delegate_task` subagents, each on its own branch (`explore/NNN-feature-<variant>`), running independent specify → clarify → plan → tasks → [implement] cycles. User compares variants with `spec-kit-compare`.

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
```

### Spawn parallel subagents
```python
delegate_task(tasks=[
  {"goal": "Implement [feature] using [Variant A approach]",
   "context": "Spec: specs/[feature]/spec.md\nBranch: explore/NNN-feature-a\n...",
   "toolsets": ["file", "terminal"]},
  {"goal": "Implement [feature] using [Variant B approach]", ...},
])
```

Each subagent receives:
- Feature spec and constitution for context
- Branch name: `explore/NNN-feature-<variant>`
- Independent directory: `specs/[feature]/variants/<variant>/`

### After completion
```
NOTE: "All N variants completed. Run 'compare [feature]' to review and select."
```

## Common Pitfalls
1. **Too many variants (3+):** Limited by `delegate_task.max_concurrent_children`. If user proposes 5, suggest grouping or prioritizing the top 3.
2. **Not providing enough context**: Each subagent has no conversation history. Put all relevant spec context in the goal/context fields.
3. **Assuming subagents completed successfully**: Verify by checking variant directories exist before running compare.
