---
name: spec-kit-constitution
description: Create or update the project constitution. Phase 0 - establishes project-wide principles that govern all subsequent spec, plan, and task decisions.
category: software-development
---

# spec-kit-constitution

**Phase**: 0 (Foundation)

**Purpose**: Create or update the project constitution at `specs/constitution.md`. This defines core principles that govern all subsequent development.

**Prerequisites**: None. This is the first skill — run first for a new project.

**Artifacts**:
- `specs/constitution.md` (primary artifact)
- `.specify/memory/constitution.version` (version tracking)

## Execution

### Step 1: Check for existing constitution
```
IF specs/constitution.md EXISTS:
  LOAD existing constitution
  READ current version from header
ELSE:
  COPY templates/constitution.md → specs/constitution.md
  SET version to 0.1.0
```

### Step 2: Collect user input
- Parse user description for principle suggestions
- If user provides explicit principles, use them
- Otherwise infer from project context (README.md, docs/)

### Step 3: Identify placeholder tokens
Find all `[ALL_CAPS_IDENTIFIER]` tokens:
- `[PROJECT_NAME]`
- `[PRINCIPLE_1_NAME]`, `[PRINCIPLE_1_DESCRIPTION]`
- `[PRINCIPLE_N_NAME]`, `[PRINCIPLE_N_DESCRIPTION]`
- `[VERSION]`, `[RATIFICATION_DATE]`, `[LAST_AMENDED_DATE]`
- `[GOVERNANCE_RULES]`

### Step 4: Fill the constitution
Replace each placeholder with concrete text:
- Each principle must be declarative and measurable
- NO vague language ("should" → MUST/SHOULD)
- Preserve heading hierarchy

### Step 5: Version management
Increment version based on change type:
- **MAJOR** (1.x.x → 2.0.0): Backward-incompatible governance changes
- **MINOR** (x.1.x → x.2.0): New principles or expanded guidance
- **PATCH** (x.x.1 → x.x.2): Clarifications, wording fixes

### Step 6: Propagate changes
Read and update references in:
- `src/templates/plan-template.md` — Constitution Check section
- `src/templates/spec-template.md` — mandatory sections
- `src/templates/tasks-template.md` — principle-driven task types

## Completion

Report:
- New version and bump rationale
- List of modified principles
- Suggested commit message

## Next Skill

Run `spec-kit-specify` to create the first feature specification.

**Re-running this skill**:
1. LOAD existing constitution
2. Compare user input against current principles
3. UPDATE only changed sections
4. PRESERVE unchanged principles
5. Write Sync Impact Report to constitution header

## Prerequisite Enforcement

**No prerequisites** — this is Phase 0.

## Completion

Report:
- New version and bump rationale
- List of modified principles
- Files requiring manual follow-up
- Suggested commit message

## Next Skill

Run `spec-kit-specify` to create the first feature specification.