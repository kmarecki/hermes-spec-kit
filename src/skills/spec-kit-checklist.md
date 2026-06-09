---
name: spec-kit-checklist
description: Use when the user says 'generate checklist for [aspect]' or 'validation checklist' — any phase auxiliary.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, checklist, quality, validation]
    related_skills: [spec-kit-analyze, spec-kit-implement, spec-kit-workflow]
---

# spec-kit-checklist

**Phase**: Any (Auxiliary)

**Purpose**: Generate or update targeted checklists at `specs/[feature]/checklists/[name].md` for validating specific aspects of the workflow.

**When NOT to use**: Checklist items are advisory and never block phase advancement.

**Routing**: Load this skill when the user says "generate checklist" or "validation checklist". Standalone — no prerequisite routing needed.
 If the user wants to proceed without checking items, let them.

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Determine checklist type
Common types: requirements.md, test.md, security.md, implementation.md, architecture.md.

### Generate checklist
Format:
```markdown
# [Type] Checklist: [Name]
## [Category]
- [ ] CHK001 [Action with specific criteria]
- [x] CHK002 [Completed item]
```

### Number items
Format: CHK### prefix (CHK001, CHK002...), grouped by category.

### Provide validation guidance
Brief notes on how to verify each item and common failure modes.

## Completion
Report checklist path, item count by category, completion status.

## Common Pitfalls
1. **Using checklists as gates**: They are advisory. Never block phase advancement because a checklist item is unchecked.
2. **Too many items**: Keep focused. 5-10 items per checklist is enough. More than 20 and users will ignore them.
