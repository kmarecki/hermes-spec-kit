---
name: spec-kit-analyze
description: Cross-artifact consistency analysis across spec, plan, and tasks. Phase 3.5 - optional quality gate between tasks and implement.
category: software-development
---

# spec-kit-analyze

**Phase**: 3.5 (Optional Quality Gate)

**Purpose**: Perform a non-destructive consistency and quality analysis across the three core artifacts. **READ-ONLY** — outputs a report, does not modify files.
**Bugfix mode**: When bugs.md exists, also validates bugfix tasks against spec + plan + bugs.

**Prerequisites**: `spec-kit-constitution` + `spec-kit-specify` + `spec-kit-plan` + `spec-kit-tasks` must be run first

**Artifacts**: None (read-only analysis)

## Execution

### Step 1: Validate prerequisites
```
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first"
IF specs/[feature]/plan.md NOT EXISTS:
  ERROR: "Run spec-kit-plan first"
IF specs/[feature]/tasks.md NOT EXISTS:
  ERROR: "Run spec-kit-tasks first"
```

### Step 2: Load artifacts
From **spec.md**:
- Functional Requirements (FR-###)
- Success Criteria (SC-###)
- User Stories
- Edge Cases

From **plan.md**:
- Architecture/Stack choices
- Data Model references
- Constitutional Gates
- Technical constraints

From **tasks.md**:
- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- File path references

From **constitution.md**:
- Principle names
- MUST/SHOULD statements

From **bugs.md** (bugfix mode only):
- Bug IDs (BUG-###)
- Bugfix tasks (BF-###)
- Severity levels
- Requires Clarification flags

### Step 3: Build semantic models
Create internal representations:
- **Requirements inventory**: FR-### with imperative-phrase slug
- **User story inventory**: Discrete actions with acceptance criteria
- **Task coverage mapping**: Task → Requirement mapping
- **Constitution rule set**: Principles and normative statements

### Step 4: Detection passes

**A. Duplication Detection**
- Identify near-duplicate requirements
- Mark lower-quality phrasing for consolidation

**B. Ambiguity Detection**
- Flag vague adjectives (fast, scalable, secure, intuitive, robust)
- Flag unresolved placeholders (TODO, TKTK, ???, &lt;placeholder&gt;)

**C. Underspecification**
- Requirements with verbs but missing object or measurable outcome
- User stories missing acceptance criteria alignment
- Tasks referencing undefined files/components

**D. Constitution Alignment**
- Any requirement or plan element conflicting with MUST principles
- Missing mandated sections or quality gates

**E. Coverage Gaps**
- Requirements with zero associated tasks
- Tasks with no mapped requirement/story
- Success Criteria requiring buildable work not in tasks

**F. Inconsistency**
- Terminology drift (same concept named differently)
- Data entities in plan but absent in spec
- Task ordering contradictions

**G. Bugfix Coverage (bugfix mode only)**
- Bugs with no corresponding bugfix task (BF-###)
- Bugfix tasks not referencing a plan bugfix section
- Bugfix tasks without verification/regression test tasks
- Unclear mapping between bug and fix approach

### Step 5: Severity assignment
Use heuristic:
- **CRITICAL**: Violates constitution MUST, or requirement with zero coverage blocking baseline
- **HIGH**: Duplicate/conflicting requirement, ambiguous security/performance attribute
- **MEDIUM**: Terminology drift, missing non-functional task coverage
- **LOW**: Style/wording improvements, minor redundancy

### Step 6: Produce analysis report
OUTPUT:

```
# Specification Analysis Report: [Feature]

## Findings Table

| ID | Category | Severity | Location | Summary | Recommendation |
|----|----------|----------|----------|---------|----------------|
| A1 | Duplication | HIGH | spec.md:L120-134 | Two similar requirements... | Merge phrasing |
...

## Coverage Summary Table

| Requirement | Has Task? | Task IDs | Notes |
|-------------|-----------|----------|-------|
| FR-001 | Yes | T001, T002 | |
| FR-002 | No | --- | Missing coverage |
...

## Constitution Alignment Issues

[If any]

## Unmapped Tasks

[If any]

## Uncovered Bugs (bugfix mode)

[If any]

## Metrics

- Total Requirements: N
- Total Tasks: N
- Coverage %: X%
- Ambiguity Count: N
- Duplication Count: N
- Critical Issues: N
```

### Step 7: Next actions
IF CRITICAL issues exist:
- Recommend resolving before `spec-kit-implement`
- Suggest explicit remediation commands
- In bugfix mode: Recommend fixing bug coverage gaps before implementing fixes

IF only LOW/MEDIUM:
- User may proceed
- Provide improvement suggestions

## Completion

Report:
- Findings count by severity
- Coverage percentage
- Explicit remediation commands
- Recommend whether to proceed to `spec-kit-implement`

## Next Skills

- Run `spec-kit-specify` to fix spec issues
- Run `spec-kit-plan` to fix plan issues
- Run `spec-kit-tasks` to fix coverage gaps
- Run `spec-kit-implement` when all CRITICAL issues resolved
- In bugfix mode: Run `spec-kit-tasks` to add missing bugfix tasks

**Re-running this skill**:
1. Re-run all detection passes
2. COMPARE results against previous run
3. Report only changes/new findings
4. Preserve previous report for comparison

## Prerequisite Enforcement

**BLOCKED** if:
- `spec-kit-constitution` has not been run
- `spec-kit-specify` has not been run
- `spec-kit-plan` has not been run
- `spec-kit-tasks` has not been run

## Key Constraint

**STRICTLY READ-ONLY** — This skill does NOT modify any files. It only outputs a report.
