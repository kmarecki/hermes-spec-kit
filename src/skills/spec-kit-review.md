---
name: spec-kit-review
description: Load when the user says 'spec-kit review [feature]', 'speckit review [feature]', "review [feature]", "quality check [feature]", or "analyze [feature]" — cross-artifact consistency check (pre-implement) and code quality review (post-implement).
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, review, quality, consistency, code-review]
    related_skills: [spec-kit-tasks, spec-kit-implement, spec-kit-workflow, spec-kit-constitution]
---

# spec-kit-review

**Phase**: 3.5 (Pre-implement optional gate) / 5.5 (Post-implement optional gate)

**Purpose**: Provides quality checks at two points in the workflow, plus a
third mode for reviewing already-closed features without altering history:

1. **Pre-implement** (after tasks.md, before code): Verify spec/plan/tasks are coherent and internally consistent. READ-ONLY — outputs a report, no file changes.

2. **Post-implement** (after tests green, before close): Review code quality — does the implementation match the constitution? Does it fulfill the spec? Are there deviations, quality issues, or technical debt introduced?

3. **Closed-review** (feature is already closed): Same checks as post-implement but does NOT update history.md. If issues are found, offers to add refactoring tasks to tasks.md and reopen the feature.|

**Prerequisites**:
- Pre-implement mode: `spec.md` + `plan.md` + `tasks.md` must exist
- Post-implement mode: `spec.md` + implemented code + passing tests

**Artifacts**: None (read-only analysis output)

**Routing**: Load this skill when the user says "review [feature]", "analyze [feature]", or "quality check [feature]". If loaded directly, load spec-kit-workflow first to check prerequisites.

**Task Persona**: Adopt the mindset of a thorough code auditor. Check every artifact against every other — spec vs plan vs tasks vs code. Use web search to research best patterns and practices when evaluating architecture or implementation quality. Every finding must be actionable and backed by evidence. Does this hold up under scrutiny?

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Determine mode
```
DETECT current artifacts:
  IF close.md or implementation-summary.md EXISTS:
    MODE = closed-review (post-close code quality check)
    NOTE: "Feature [feature] is closed. Review will NOT update history.md."

  IF tasks.md exists AND no implementation code exists:
    MODE = pre-implement (cross-artifact consistency check)

  IF tests have passed AND writeable source code exists AND no close.md:
    MODE = post-implement (code quality review)

  IF both pre-implement and post-implement conditions match:
    ASK user: "Run pre-implement review (spec/plan/tasks), post-implement review (code quality), or both?"

  IF mode is still undetermined:
    ASK user: "Cannot auto-detect mode. Which review? (pre-implement / post-implement / closed-review)"
```

---

## Pre-Implement Mode: Cross-Artifact Consistency

### Step 1: Validate prerequisites
```
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first"
IF specs/[feature]/plan.md NOT EXISTS:
  WARN: "No plan.md — analysis limited to spec only"
IF specs/[feature]/tasks.md NOT EXISTS:
  WARN: "No tasks.md — cannot verify task coverage"
```

### Step 2: Load artifacts
From **spec.md**:
- Functional Requirements (FR-###)
- Success Criteria (SC-###)
- User Stories
- Edge Cases

From **plan.md** (IF EXISTS):
- Architecture/Stack choices
- Data Model references
- Constitutional Gates
- Technical constraints

From **tasks.md** (IF EXISTS):
- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- File path references

From **constitution.md** (IF EXISTS):
- Principle names
- MUST/SHOULD statements

From **bugs.md** (bugfix mode only, IF EXISTS):
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
- Flag unresolved placeholders (TODO, TKTK, ???, <placeholder>)

**C. Underspecification**
- Requirements with verbs but missing object or measurable outcome
- User stories missing acceptance criteria alignment
- Tasks referencing undefined files/components

**D. Constitution Alignment**
- Any requirement or plan element conflicting with MUST principles
- Missing mandated sections or quality gates

**E. Naming Conventions** (pre-implement)
- Consistent naming patterns across spec, plan, and tasks
- File paths in tasks follow project conventions
- Terminology consistent between spec and plan

**F. Documentation Completeness** (pre-implement)
- Are all required spec sections present (FRs, edge cases, success criteria)?
- Does plan.md document architecture decisions?
- Are there TODOs or placeholders that should be resolved before coding?

**G. User-Defined Custom Gates** (pre-implement)
**H. Coverage Gaps** (only if tasks.md exists)
- Requirements with zero associated tasks
- Tasks with no mapped requirement/story
- Success Criteria requiring buildable work not in tasks

**I. Inconsistency**
- Terminology drift (same concept named differently)
- Data entities in plan but absent in spec
- Task ordering contradictions

**J. Bugfix Coverage (bugfix mode only)**
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

### Step 6: Produce pre-implement report
OUTPUT:

```
# Pre-Implement Review: [Feature]

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

### Step 7: Next actions (pre-implement)
```
IF CRITICAL issues exist:
  - Recommend resolving before spec-kit-implement
  - Suggest explicit remediation commands
  - In bugfix mode: Recommend fixing bug coverage gaps before implementing fixes

IF only LOW/MEDIUM:
  - User may proceed
  - Provide improvement suggestions
```

---

## Post-Implement Mode: Code Quality Review

### Step 1: Validate prerequisites
```
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first — cannot review without requirements"
IF no implementation code detected:
  ERROR: "No implementation found — run spec-kit-implement first"
```

### Step 2: Load context
```
LOAD specs/[feature]/spec.md (REQUIRED)
LOAD specs/[feature]/constitution.md (IF EXISTS)
LOAD specs/[feature]/plan.md (IF EXISTS)
LOAD specs/[feature]/tasks.md (IF EXISTS)

CAPTURE git diff or file list showing what was implemented
```

### Step 3: Code quality checks

**A. Architecture & Design**
- Does the code structure follow the plan's architecture?
- Are there architectural violations (layers bypassed, circular dependencies)?
- Is the code in the correct locations per the plan?

**B. Spec Fulfillment**
- For each FR-### in spec.md: does the implementation satisfy it?
- For each success criterion: is it demonstrably met?
- Are there edge cases from the spec that are unhandled?

**C. Constitution Alignment**
- Does the code respect MUST principles from constitution.md?
- Are there quality gates or standards that were skipped?

**D. Naming Conventions** (post-implement)
- Does the code follow project naming conventions?
- Are file/module/function names consistent with plan.md?
- Public API names match spec terminology?

**E. Documentation Completeness** (post-implement)
- Are there README, API docs, or inline docs that need updating?
- If this feature adds or changes a public interface, is it documented?
- Are there changelog entries or migration notes needed?

**F. User-Defined Custom Gates** (post-implement)
**G. Code Quality**
- Naming conventions — consistent and descriptive?
- Error handling — are failures caught and reported appropriately?
- Duplication — are there copy-paste patterns that should be extracted?
- Complexity — are there functions/modules that are too complex?
- Security — obvious vulnerabilities (hardcoded secrets, injection vectors)?

**H. Test Quality** (if tests exist)
- Do tests actually test the behaviors described in spec.md?
- Are there tests for edge cases from the spec?
- Are tests meaningful (assert behavior, not implementation)?

### Step 4: Severity assignment
Same heuristic as pre-implement mode.

### Step 5: Produce post-implement report
```
# Post-Implement Review: [Feature]

## Spec Fulfillment

| FR-ID | Status | Notes |
|-------|--------|-------|
| FR-001 | ✅ Fulfilled | Implemented as specified |
| FR-002 | ⚠️ Partial | Missing error handling for edge case |
| FR-003 | ❌ Missing | Not implemented |

## Constitution Alignment
[If any violations]

## Code Quality Findings

| ID | Category | Severity | File | Finding | Suggestion |
|----|----------|----------|------|---------|------------|
| Q1 | Duplication | MEDIUM | src/auth.py:45-60 | Repeated validation logic | Extract to helper |
...

## Metrics
- Requirements fulfilled: N/Total
- Code quality issues: N (Critical/High/Medium/Low)
- Constitution violations: N
- Test coverage adequacy: Satisfactory / Needs improvement / Not assessed
```
### Step 6: Next actions — deviation resolution (post-implement)

For each deviation found between code and spec/plan during post-implement review:

```
FOR each FR-### or plan section where code differs from spec/plan:
  PRESENT the discrepancy to the user:
    "FR-NNN in spec.md says: [original requirement]
     Implementation does: [what code actually does]
     
     Options:
     1. Update spec/plan to match implementation (intentional deviation — document it)
     2. Keep spec/plan as-is — change code to match (create a bugfix task)
     3. Skip for now (flag for Phase 6 close to resolve)"

  WAIT for user decision before proceeding to the next discrepancy.

  IF user picks 1:
    PATCH spec.md or plan.md to reflect what was implemented
    ADD note: "(Updated by post-implement review)"
    NOTE: "spec.md updated — deviation documented."
    These spec/plan patches will be committed by Phase 6 (summarize/close).

  IF user picks 2:
    ADD bug to bugs.md: "BUG-NNN: Implementation does not match spec FR-NNN"
    NOTE: "Bug logged — run 'bugfix [feature]' to align implementation with spec."

  IF user picks 3:
    NOTE: "Deferred to Phase 6 close."
```

### Step 7: Next actions (non-deviation)

```
IF mode == closed-review:
  PRESENT findings to user
  IF CRITICAL or HIGH issues exist:
    PROMPT: "N issues found. Options:
      1. Add refactoring tasks to tasks.md (no reopen)
      2. Add tasks and reopen the feature (reopen [feature])
      3. Note for future work, no changes"
    IF user picks 1 or 2:
      APPEND refactoring tasks to tasks.md for each issue
      NOTE: "Refactoring tasks added to tasks.md."
    IF user picks 2:
      NOTE: "Feature needs reopening. Run 'reopen [feature]' to start the fix loop."
    IF user picks 3:
      NOTE: "Issues noted for future work. No changes made."
  ELSE (only LOW/MEDIUM):
    NOTE: "Minor issues found. No code changes needed."

ELSE (normal pre/post-implement):
  IF CRITICAL issues exist:
    - Block: Resolve before closing feature
    - Recommend adding bugs to bugs.md
    - Proceed to bugfix cycle

  IF only LOW/MEDIUM:
    - User may proceed to close
    - Note improvement suggestions for future
```

### Append to history.md
```
IF mode == closed-review:
  NOTE: "Review on closed feature — history.md not updated."
  NOTE: "Run 'reopen [feature]' if issues need fixing."
ELSE:
  Append to `specs/[feature]/history.md` (create if missing):
  - Phase: Phase 3.5 or Phase 5.5 (mode-dependent) — Complete
  - Artifact: review report
```

## Completion

Report:
- Mode used: Pre-implement / Post-implement / Both
- Findings count by severity
- Coverage percentage (pre-implement)
- Spec fulfillment status (post-implement)
- Overall recommendation: Proceed / Fix critical issues first

## Next Skills

- Pre-implement mode: Propose `spec-kit-implement` when all CRITICAL issues resolved
- Post-implement mode: Propose `spec-kit-summarize` to close the feature
- Closed-review mode: Propose `reopen [feature]` if issues need fixing
- Either mode: Propose `spec-kit-specify` or `spec-kit-plan` to fix issues found
- In bugfix mode: Propose `spec-kit-tasks` to add missing bugfix tasks

**Re-running this skill**:
1. Re-run the relevant detection passes based on mode
2. COMPARE results against previous run
3. Report only changes/new findings
4. Preserve previous report for comparison

## Prerequisite Enforcement

Pre-implement:
- **BLOCKED** if: `spec-kit-specify` has not been run (spec.md required)
- **WARN** if: plan.md or tasks.md missing — analysis limited to what exists

Post-implement:
- **BLOCKED** if: `spec-kit-specify` has not been run (spec.md required)
- **BLOCKED** if: No implementation code detected
- **WARN** if: constitution.md missing — cannot check constitutional alignment

Closed-review:
- **BLOCKED** if: `spec-kit-specify` has not been run (spec.md required)
- **BLOCKED** if: No implementation code detected
- **NOTE**: tasks.md will be modified only with user approval

## Key Constraint

**READ-ONLY on source code** — This skill does NOT modify source code files. It only outputs a report.
**Exception**: In closed-review mode, may append refactoring/remediation tasks to `tasks.md` with user approval.
