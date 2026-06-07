---
name: spec-kit-specify
description: Create or update a feature specification. Phase 1 - defines WHAT users need and WHY, without implementation details.
version: 1.0.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, specification, requirements, features]
    related_skills: [spec-kit-constitution, spec-kit-clarify]
---

# spec-kit-specify

**Phase**: 1

**Purpose**: Create or update a feature specification at `specs/[feature]/spec.md`. Defines WHAT users need and WHY, not HOW to implement.

**Prerequisites**: `spec-kit-constitution` must be run first

**Artifacts**:
- `specs/[feature]/spec.md` (primary artifact)
- `specs/[feature]/checklists/requirements.md` (quality checklist)

## Execution

### Step 1: Validate prerequisites
```
IF specs/constitution.md NOT EXISTS:
  WARN: "No constitution found — proceeding without constitutional gates. Constitution is optional; run `spec-kit-constitution` later to add principles."
```

### Step 2: Parse user description
- Parse the feature description from user input
- If empty: ERROR "No feature description provided"
- Extract: actors, actions, data, constraints

### Step 3: Generate short name
Create 2-4 word short name:
- Use action-noun format: "user-auth", "oauth2-api-integration"
- Preserve technical terms: OAuth2, API, JWT
- Examples:
  - "I want to add user authentication" → "user-auth"
  - "Implement OAuth2 integration for the API" → "oauth2-api-integration"

### Step 4: Create feature directory
```
DETERMINE prefix:
  - Scan existing specs/ directories
  - Find next sequential number (001, 002, ...)
DIRECTORY: specs/[###]-[short-name]/
CREATE: mkdir -p specs/[feature]/checklists
```

### Step 5: Generate spec.md
COPY `spec-kit/templates/spec-template.md` → `specs/[feature]/spec.md`

Populate with:
- **User Scenarios**: P1/P2/P3 priority with Given/When/Then acceptance scenarios
- **Functional Requirements**: FR-001, FR-002, etc. — testable, technology-agnostic
- **Success Criteria**: Measurable outcomes (time, performance, volume)
- **Key Entities**: Domain objects without implementation details
- **Edge Cases**: Error conditions, boundary handling

### Step 6: Apply constraints
- Focus on WHAT users need and WHY
- **NO implementation details**: no tech stack, frameworks, APIs
- **MAX 3 [NEEDS CLARIFICATION] markers** — use only for critical decisions
- Prioritize: scope > security/privacy > user experience > technical details

### Step 7: Generate requirements checklist
COPY `spec-kit/templates/checklist-template.md` → `specs/[feature]/checklists/requirements.md`

Validate:
- No implementation details leaked
- All acceptance scenarios defined
- Success criteria measurable
- Max 3 [NEEDS CLARIFICATION] markers

### Step 8: Commit spec artifacts (auto)
```bash
IF `git rev-parse --git-dir > /dev/null 2>&1`; THEN
  COMMIT_MSG="spec(phase-1): [feature] specification"
  git add specs/[feature]/spec.md specs/[feature]/checklists/requirements.md
  git commit -m "$COMMIT_MSG" --no-verify
  COMMIT_HASH=$(git rev-parse HEAD)
  NOTE: "Committed as $COMMIT_HASH"
ELSE
  NOTE: "Not a git repository — skipping automatic commit"
```

## Completion

Report:
- Feature directory path
- Spec file path
- Checklist status
- List readiness for next phase
- **Commit**: `$COMMIT_HASH` (auto — `git log` for details)

## Next Skills

- Propose to the user: Run `spec-kit-clarify` for iterative clarification (optional but recommended)
- Propose to the user: Run `spec-kit-plan` when ready for technical planning

**Re-running this skill**:
1. LOAD existing `specs/[feature]/spec.md`
2. Compare user input against current spec
3. UPDATE only changed sections
4. PRESERVE unchanged content
5. PRESERVE branch name and feature number
6. PRESERVE completed checklist status

## Prerequisite Enforcement

**BLOCKED** if `spec-kit-constitution` has not been run:
```
CHECK: specs/constitution.md EXISTS
IF NOT:
  ERROR: "Run spec-kit-constitution first to establish project principles"
```

## Re-run Enforcement

After re-running `spec-kit-constitution`:
1. Re-validate spec against updated principles
2. UPDATE any sections that conflict with new principles
3. FLAG constitution violations as CRITICAL
