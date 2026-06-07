---
name: spec-kit-explore
description: Creative exploration mode — spawn parallel branches with independent clarify, plan, tasks, and implementation for each variant.
version: 1.0.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, explore, creative, parallel, variants]
    related_skills: [spec-kit-compare, spec-kit-specify, spec-kit-plan, spec-kit-tasks, spec-kit-implement, spec-kit-workflow]
---

# spec-kit-explore

**Phase**: Explore (Parallel Development Mode)

**Purpose**: When you want to explore N different approaches in parallel — different tech stacks, architectures, or design patterns — this skill spawns independent branches, each running its own clarify/plan/tasks/implement cycle, then hands off to `spec-kit-compare` for the user to choose a winner.

**When to use**: User says "explore [feature] with [variant descriptions]" or "creative exploration for [feature]"

**Prerequisites**: `spec-kit-specify` must have been run first (or you provide a feature description)

**Artifacts**:
- `specs/[feature]/variants/[name]/spec.md` (per variant)
- `specs/[feature]/variants/[name]/plan.md` (per variant)
- `specs/[feature]/variants/[name]/tasks.md` (per variant)
- `specs/[feature]/variants/[name]/bugs.md` (per variant, if implemented)
- `specs/[feature]/comparison.md` (created by `spec-kit-compare`)

**Branch naming**: `explore/NNN-feature-<variant>`

## Development Modes Quick Reference

| Mode | Trigger | Behavior |
|------|---------|----------|
| **specify** | "Create a spec for [feature]" | Full forward phase sequence: Constitution (optional) → Specify → Clarify → Plan → Tasks → Implement → Test → Summarize |
| **bugfix** | "bugfix [feature]" | Bugfix loop: Test → [Clarify] → Plan → Tasks → Implement → Test (repeat) |
| **explore** | "Explore [feature]" | Parallel branches: spawn N variants, each runs its own phase sequence independently, then compare |

## Execution

### Step 1: Validate prerequisites

```
IF specs/[feature]/spec.md NOT EXISTS AND no feature description provided:
  ERROR: "Run spec-kit-specify first or provide a feature description"

IF fewer than 2 variants provided:
  ERROR: "Explore mode requires at least 2 variants to compare"
```

### Step 2: Parse variants

User provides N variant descriptions. Each variant must specify the distinguishing dimension:
- **Tech stack** (e.g., "React frontend vs Vue frontend")
- **Architecture** (e.g., "monolith vs microservices")
- **Design pattern** (e.g., "Redux vs Zustand for state management")
- **Approach** (e.g., "server-side rendering vs static generation")

Extract a short name (2-4 chars) for each variant and a description:

```
VARIANTS:
  react: "React with Tailwind CSS frontend"
  vue: "Vue 3 with PrimeVue frontend"
  svelte: "SvelteKit full-stack approach"
```

### Step 3: Create directory structure

```
CREATE: specs/[feature]/variants/
FOR EACH variant:
  CREATE: specs/[feature]/variants/[name]/
  NOTE: Variant artifacts will be populated by the parallel exploration
```

### Step 4: Spawn parallel exploration

For each variant, spawn a `delegate_task` subagent:

```python
delegate_task(
  tasks=[
    {
      "goal": f"Explore variant '{name}': {description}",
      "context": f"""
You are exploring variant '{name}' of feature '{feature}'.
Feature description: {feature_description}

Variant description: {description}

INSTRUCTIONS:
1. First, ensure you are on the correct branch. If the branch doesn't exist:
     git checkout -b explore/NNN-feature-{name}
   Otherwise:
     git checkout explore/NNN-feature-{name}

2. If specs/[feature]/variants/{name}/spec.md doesn't exist yet:
   - Create spec.md with the variant-specific approach. The spec should reflect
     the variant's unique characteristics (different tech, different UX, etc.)
     while addressing the same functional requirements.
   - Commit: git add specs/[feature]/variants/{name}/spec.md
            git commit -m "spec(phase-1): [feature] specification ({name} variant)"

3. Run through Clarify, Plan, Tasks, and Implement phases for this variant.
   Keep all variant artifacts under specs/[feature]/variants/{name}/.
   Implementation code goes in the main project source directories.
   Constitution is optional — skip if it doesn't exist.

4. After each phase, commit with the standard spec-kit message format.

5. Report back with:
   - Branch name
   - Tech stack / approach used
   - Key decisions made
   - Implementation status (complete / partial)
   - Number of tasks completed
   - Any notable trade-offs

IMPORTANT: Do NOT modify other variants' files. Work only in:
  - specs/[feature]/variants/{name}/
  - Project source code (shared, but your changes are on your branch)
""",
      "toolsets": ["terminal", "file", "web"]
    }
    for each variant...
  ]
)
```

Run all variants **in parallel**. Wait for all to complete.

### Step 5: Report exploration results

After all variants complete:

```
REPORT:
  - Total variants explored: N
  - Completed fully: N
  - Completed partially: N (note: implementation is optional)
  - Branches:
    - explore/NNN-feature-react (completed, 12 tasks)
    - explore/NNN-feature-vue (completed, 14 tasks)
    - explore/NNN-feature-svelte (partial, 8/10 tasks)

NEXT: Run `spec-kit-compare` for [feature] to compare all variants and choose a winner.
```

## Variant Implementation Rules

- **Implementation is optional**: Variants are valuable even at the spec/plan level. If a variant reaches implementation, it goes on its branch.
- **Branches are independent**: Each variant branch diverges from the common ancestor. No cross-branch interference.
- **Constitution is optional**: If `specs/constitution.md` exists, all variants inherit it. If not, each variant works without constitutional constraints.
- **Shared source**: Variant implementations write to the same source directories but on different branches. The merge/resolve step happens during comparison.
- **Time box**: Each variant subagent has a 5-minute timeout. Long-running implementation tasks should be noted as "partial" in the report.

## Completion

Report:
- Variant count and names
- Branch names
- Completion status per variant
- Key differentiators per variant
- Suggested next action: run `spec-kit-compare`

## Next Skills

- Propose to the user: Run `spec-kit-compare` for [feature] to compare all variants
- Propose to the user: Run `spec-kit-workflow` for normal forward development
