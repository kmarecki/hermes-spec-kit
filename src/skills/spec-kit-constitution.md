---
name: spec-kit-constitution
description: Create or update the project constitution. Phase 0 - establishes project-wide principles that govern all subsequent spec, plan, and task decisions.
version: 1.0.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, constitution, principles, project-setup]
    related_skills: [spec-kit-specify]
---

# spec-kit-constitution

**Phase**: 0 (Foundation)

**Purpose**: Create or update the project constitution at `specs/constitution.md`. This defines core principles that govern all subsequent development.

**Prerequisites**: None. This is the first skill — run first for a new project.

**Artifacts**:
- `specs/constitution.md` (primary artifact)

## Execution

### Step 0: Check git availability
```bash
IF `git rev-parse --git-dir > /dev/null 2>&1`; THEN
  NOTE: "Git repository detected — spec artifacts will be committed automatically."
ELSE:
  WARN: "No git repository detected. Spec artifacts will be created but NOT versioned.
         Run 'git init' and optionally copy spec-kit/templates/gitignore-template.md → .gitignore
         to enable automatic commits on phase transitions."
```

### Step 1: Check for existing constitution
```
IF specs/constitution.md EXISTS:
  LOAD existing constitution
  READ current version from header
ELSE:
  COPY spec-kit/templates/constitution-template.md → specs/constitution.md
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
After updating constitution, re-run skills that depend on it:
- `spec-kit-specify` — re-validate spec against updated principles
- `spec-kit-plan` — re-validate gates against updated constitution

### Step 7: Commit spec artifacts (auto)
```bash
IF `git rev-parse --git-dir > /dev/null 2>&1`; THEN
  COMMIT_MSG="spec(phase-0): constitution for [PROJECT]"
  git add specs/constitution.md
  git commit -m "$COMMIT_MSG" --no-verify
  COMMIT_HASH=$(git rev-parse HEAD)
  NOTE: "Committed as $COMMIT_HASH"
ELSE
  NOTE: "Not a git repository — skipping automatic commit"
```

## Completion

Report:
- New version and bump rationale
- List of modified principles
- Suggested commit message
- **Commit**: `$COMMIT_HASH` (auto — see `git log` for details)

## Next Skill

Propose to the user: Run `spec-kit-specify` to create the first feature specification.

**Re-running this skill**:
1. LOAD existing constitution
2. Compare user input against current principles
3. UPDATE only changed sections
4. PRESERVE unchanged principles
5. Write Sync Impact Report to constitution header

## Prerequisite Enforcement

**No prerequisites** — this is Phase 0.
