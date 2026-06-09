---
name: spec-kit-constitution
description: Use when the user says 'create constitution' or 'create project principles' — Phase 0 project setup.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, constitution, principles, project-setup]
    related_skills: [spec-kit-specify, spec-kit-workflow]
---

# spec-kit-constitution

**Phase**: 0 (Foundation)

**Purpose**: Create or update the project constitution at `specs/constitution.md`. Defines core principles that govern all subsequent development.

**When NOT to use**: This is a one-time setup per project. Do NOT re-run for every feature — principles are project-wide.

**Prerequisites**: None. This is the first skill — run first for a new project.

**Artifacts**: `specs/constitution.md`

**Routing**: Load this skill when the user says "create constitution" or "create project principles". If loaded directly (not via spec-kit-workflow), consider loading the workflow first for prerequisite checks.


## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Check git availability
```bash
IF `git rev-parse --git-dir > /dev/null 2>&1`; THEN
  NOTE: "Git repository detected — spec artifacts will be committed automatically."
ELSE:
  WARN: "No git repository detected. Run 'git init' and optionally copy .gitignore-template to enable auto-commits."
```

### Check for existing constitution
```
IF specs/constitution.md EXISTS:
  LOAD existing constitution, READ current version
ELSE:
  COPY spec-kit/templates/constitution-template.md → specs/constitution.md
  SET version to 0.1.0
```

### Collect user input
- Parse description for principle suggestions
- If none provided, infer from project context (README.md, docs/)

### Fill the constitution
Replace `[ALL_CAPS_PLACEHOLDER]` tokens with concrete text:
- Each principle must be declarative and measurable
- NO vague language ("should" → MUST/SHOULD)

### Version management
- **MAJOR** (1.x.x → 2.0.0): Backward-incompatible governance changes
- **MINOR** (x.1.x → x.2.0): New principles
- **PATCH** (x.x.1 → x.x.2): Clarifications

### Commit
Follow `spec-kit/references/auto-commit.md`:
- Scope: `specs/constitution.md`
- Message: `"spec(phase-0): constitution for [PROJECT]"`

## Completion
- Report new version and bump rationale
- Propose: Run `spec-kit-specify` to create the first feature specification.

## Common Pitfalls
1. **Constitution too vague**: Principles like "write clean code" are unmeasurable. Use MUST/SHOULD with specific criteria.
2. **Overloading per-feature**: Constitution is project-wide. Don't add feature-specific rules here.
3. **Skipping entirely for complex projects**: Constitution is optional, but for multi-developer projects it prevents conflicting assumptions.

## Prerequisite Enforcement
**No prerequisites** — this is Phase 0.
