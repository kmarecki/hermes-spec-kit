---
name: spec-kit-review
description: Load when the user says 'spec-kit review [feature]', 'speckit review [feature]', "review [feature]", "quality check [feature]", or "analyze [feature]" — cross-artifact consistency check (pre-implement) and critical code quality review (post-implement).
version: 1.2.0
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

1. **Pre-implement** (after tasks.md, before code): Verify spec/plan/tasks are coherent **and** analyze the existing codebase structure to evaluate whether the planned approach fits the project architecture and follows current best practices. READ-ONLY — outputs a report, no file changes.

2. **Post-implement** (after tests green, before close): **Critical** code quality review — does the implementation match the constitution? Does it fulfill the spec? Is the architecture sound? Are there structural defects, security issues, or design debt introduced? Focuses on **important** findings; skips cosmetic/style nitpicks.

3. **Closed-review** (feature is already closed): Same checks as post-implement but does NOT update history.md. If issues are found, offers to add refactoring tasks to tasks.md and reopen the feature.|

**Prerequisites**:
- Pre-implement mode: `spec.md` + `plan.md` + `tasks.md` must exist
- Post-implement mode: `spec.md` + implemented code + passing tests

**Artifacts**: None (read-only analysis output)

**Routing**: Load this skill when the user says "review [feature]", "analyze [feature]", or "quality check [feature]". If loaded directly, load spec-kit-workflow first to check prerequisites.

**Task Persona**: Adopt the mindset of a senior architect doing a critical design review. You are not a style checker — you look for **structural problems, design flaws, security risks, and architectural misalignments** that would cause real pain if left unfixed. Every finding must be actionable and backed by evidence. Use web search to research current best practices for the project's tech stack when evaluating architecture or implementation quality. Ask yourself: *"Will this cause a problem in production? Will this be hard to maintain? Is there a simpler, more robust approach?"* If the answer to all three is no, the finding is probably a nitpick — skip it. Does this hold up under scrutiny?

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
    MODE = pre-implement (cross-artifact consistency + codebase architecture analysis)

  IF tests have passed AND writeable source code exists AND no close.md:
    MODE = post-implement (code quality review)

  IF both pre-implement and post-implement conditions match:
    ASK user: "Run pre-implement review (spec/plan/tasks), post-implement review (code quality), or both?"

  IF mode is still undetermined:
    ASK user: "Cannot auto-detect mode. Which review? (pre-implement / post-implement / closed-review)"
```

---

## Pre-Implement Mode: Cross-Artifact Consistency

### Review scope (feature-level only)
This review is scoped to the feature being examined. The following are
**IN SCOPE**:
- Spec/plan/tasks coherence and completeness
- Codebase architecture fit (does the plan fit the existing code?)
- Best-practice validation for the planned approach
- Design soundness (abstraction level, data flow, error handling)

The following are **OUT OF SCOPE** — do NOT flag or block on these:
- Missing project constitution — this is a project-level concern tracked
  separately. If the constitution exists, the review will note alignment.
  If it doesn't exist, that's not a feature issue.
- Missing project-level tooling (CI config, deployment pipeline, linting)
- Broad tech stack evaluations not specific to this feature
- Pre-existing code quality issues in unrelated parts of the codebase
- Personal stylistic preferences (see Nitpick Filter below)

If you discover a project-level issue during review, add it to a
"Project-Level Notes" section at the bottom of the report — do NOT
assign severity or block the feature.

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

**D. Constitution Alignment** (project-level — informational only)
WHEN specs/constitution.md EXISTS at project root:
  - Check feature artifacts for alignment with each applicable principle
  - Note any conflicts or gaps as informational findings
  - Do NOT assign CRITICAL severity — this is guidance, not a gate
WHEN specs/constitution.md does NOT exist:
  - SKIP this pass entirely
  - Add to Project-Level Notes: "Constitution not found — alignment
    check skipped. This is a project-level gap, not a feature issue."
  - Do NOT produce findings for missing constitution

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

**F. Codebase Architecture Analysis** (new — pre-implement)
- Scan the project's existing directory tree and module structure to understand current architecture patterns (layers, module boundaries, framework conventions, dependency injection style, testing patterns)
- Evaluate whether the planned architecture/design in plan.md fits the existing codebase — does it follow the same patterns or introduce new ones? If new patterns are proposed, is the justification compelling?
- Identify integration risk points — where the new feature connects to existing code. Are the interfaces clean? Are existing modules being modified in a way that could cause regressions?
- Check if the plan reuses existing abstractions or reinvents them. Is there already a utility, mixin, or service that does what the plan proposes?
- For each file path referenced in tasks.md: does the path follow the existing project layout conventions? Or does it introduce a new directory structure that doesn't match?

**G. Best Practice Validation** (new — pre-implement)
- For each major technology or pattern in the plan, briefly research (web search) current recommended practices. Example questions:
  - "Does framework X recommend this approach for Y in 2026?"
  - "Is this pattern considered best practice or is there a newer recommended alternative?"
  - "Are there known pitfalls or gotchas with this approach that the plan doesn't address?"
- Flag approaches that are:
  - Known anti-patterns (e.g., God objects, sequential async waterfalls, callback hell in modern frameworks)
  - Deprecated or superseded patterns (e.g., class components in a React project using function components)
  - Over-engineering for the problem size (e.g., adding a message queue for a single background job)
  - Under-engineering for the problem size (e.g., no error handling, no validation, no logging)
- Do NOT flag personal stylistic preferences or "one true way" debates (tabs vs spaces, semicolons vs no-semicolons). Only flag patterns with broad community consensus against them.

**H. Design Soundness**
- Does the plan reflect a solid understanding of the existing codebase, or does it feel like a generic solution?
- Are the proposed abstractions at the right level? Too abstract (over-general, YAGNI violation)? Too concrete (brittle, hard to extend)?
- Will the design scale with the next 2-3 likely features? Or is it a dead end that will need refactoring?
- Are there simpler approaches that would work with less complexity? Evaluate Occam's razor.
- Error handling strategy: does the plan have one? Or does it assume everything succeeds?
- Is the data flow coherent and traceable? Can you follow a request/event from entry to response without gaps?

### Step 5: Severity assignment
Use heuristic — **filter out nitpicks** at every level:

- **CRITICAL**: Requirement with zero task coverage blocking baseline, architectural integrity violation, security vulnerability, data integrity issue
- **HIGH**: Design flaw that will cause maintainability pain, pattern misalignment with existing codebase, missing error handling chains, duplicated logic across module boundaries
- **MEDIUM**: Terminology drift, missing non-functional task coverage, minor design concern that could degrade with future features
- **LOW**: SKIP — do not report. These are stylistic preferences, subjective opinions, or issues with no real-world impact. If you find yourself writing a LOW finding, ask: "Would the project be measurably worse if this were left as-is?" If no, delete the finding.

**NITPICK FILTER — Apply before reporting:**
- If a finding is about formatting, line length, naming preference (not correctness), comment style, or personal taste → DELETE it, do not report.
- If a finding is about a pattern that works but isn't your preferred approach → DELETE it.
- If a finding requires deep domain knowledge you don't have → flag as QUESTION, not finding.
- **Minimum bar**: every reported finding must have a demonstrable negative impact on correctness, security, performance, maintainability, or testability. If you cannot articulate which of these five is harmed, the finding is a nitpick — skip it.

### Step 6: Produce pre-implement report
OUTPUT:

```
# Pre-Implement Review: [Feature]

## Findings Table

| ID | Category | Severity | Location | Summary | Recommendation |
||----|----------|----------|----------|---------|----------------|
|| A1 | Duplication | HIGH | spec.md:L120-134 | Two similar requirements... | Merge phrasing |
|...

## Codebase Architecture Assessment

| Aspect | Assessment | Risk Level |
|--------|-----------|------------|
| Pattern fit | Plan aligns with existing MVC layout | ✅ Low |
| Integration points | New service connects via existing repository pattern | ✅ Low |
| Directory conventions | tasks.md references src/feature/ — matches project layout | ✅ Low |
| Pattern reuse | Plan creates new auth middleware — existing middleware in src/middleware/ not reused | ⚠️ Medium |

## Best Practice Validation

| Technology/Pattern | Research Finding | Status |
|--------------------|-----------------|--------|
| Next.js App Router auth | Next.js docs recommend middleware.ts for auth checks — plan uses getServerSession in each page | ⚠️ Consider middleware approach |
| JWT refresh pattern | Industry consensus: refresh token rotation + blacklist — plan uses long-lived tokens | ❌ High — security risk |

## Design Soundness Notes

[Key observations about abstraction level, scalability, simplicity, data flow]

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
- Codebase Fit: ✅ / ⚠️ / ❌
- Best Practice Alerts: N
- Design Soundness: ✅ / ⚠️ / ❌
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
**G. Code Quality** — Focus on **structural and substantive** issues. Skip cosmetic preferences.

- Architecture conformance — does the code structure match what plan.md described? Or did the implementation diverge in significant ways?
- Layer/model boundaries — are layers properly separated? Are there imports that cross layer boundaries (e.g., UI layer importing data access)?
- Error handling chains — are errors caught at appropriate boundaries? Or are there silent failures, bare excepts, or swallowed exceptions?
- Security — hardcoded secrets, injection vulnerabilities, missing authentication/authorization checks, unvalidated input flowing to sensitive operations
- Data integrity — are database operations transactional where needed? Race conditions? Missing validation before persistence?
- Duplication at the structural level — copy-pasted modules, repeated business logic across services, parallel hierarchies that should be unified
- Complexity hotspots — functions over 100 lines, modules over 500 lines, nested conditionals beyond 4 levels, excessive indirection (too many wrappers/delegates for what the code does)
- Dependency direction — do high-level modules depend on low-level modules, or is there dependency inversion? Are there circular dependencies?
- Public API surface — is the API/interface well-designed? Consistent naming, proper parameter validation, sensible defaults?
- Concurrency — thread safety, shared mutable state, async/await usage patterns, missing cancellation support for long operations

**NITPICK FILTER for post-implement** — Same rule as pre-implement (Step 5). Do NOT report:
- Line length, whitespace, formatting, comment style, import ordering
- Variable/function naming that is merely unconventional but clear
- Minor redundancy that doesn't affect maintainability (2-3 line patterns)
- Personal style preferences ("I would have written this differently")
- Missing edge cases that the spec doesn't require and are unlikely in practice
- Performance micro-optimizations with no demonstrated bottleneck

Ask: "Is this finding in the top 5 things that should change about this code?" If no, delete it.

**H. Test Quality** (if tests exist)
- Do tests actually test the behaviors described in spec.md?
- Are there tests for edge cases from the spec?
- Are tests meaningful (assert behavior, not implementation)?

### Step 4: Severity assignment
Same heuristic as pre-implement mode — **filter out nitpicks**:
- **CRITICAL**: Security vulnerability, data integrity issue, architecture violation, complete spec deviation
- **HIGH**: Structural defect, error handling gap, missing validation chain, concurrency bug
- **MEDIUM**: Minor design concern, documentation gap, test coverage gap on critical path
- **LOW**: SKIP — do not report (nitpicks only)

Apply the same **NITPICK FILTER** from pre-implement Step 5 before reporting any finding.

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

## Critical Findings (must fix)

| ID | Category | Severity | File | Finding | Suggestion |
|----|----------|----------|------|---------|------------|
| Q1 | Architecture | CRITICAL | src/auth/service.go:45 | Auth bypass possible — no middleware check on admin routes | Add middleware guard |
|...

## Advisory Findings (should fix)

| ID | Category | Severity | File | Finding | Suggestion |
|----|----------|----------|------|---------|------------|
| R1 | Error handling | HIGH | src/api/handler.go:120 | Database errors silently swallowed | Return 500 with error ID |
|...

[Nitpicks omitted — 0 reported]

## Architecture Conformance

| Plan Aspect | Implementation | Verdict |
|-------------|---------------|---------|
| Repository pattern | Data access via repository interfaces | ✅ Conforms |
| Middleware auth chain | Route-level middleware applied | ✅ Conforms |
| Layered separation | UI imports from services layer | ⚠️ UI imports data access directly in 2 places |

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

### Append to history.md and Commit

```text
IF mode == closed-review:
  NOTE: "Review on closed feature — history.md not updated."
ELSE:
  Follow the **Shared Commit Procedure** in `spec-kit/references/preflight.md`:
  - Phase: Phase 3.5 or Phase 5.5 (mode-dependent) — Review
  - Artifact: review report
  - Scope: review findings
  - Message: `"spec(review): [feature] review findings"`
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
- **NOTE**: constitution.md not found at project root — constitutional alignment
  checks skipped. This is a project-level gap, not a feature blocker.

Closed-review:
- **BLOCKED** if: `spec-kit-specify` has not been run (spec.md required)
- **BLOCKED** if: No implementation code detected
- **NOTE**: tasks.md will be modified only with user approval

## Key Constraint

**READ-ONLY on source code** — This skill does NOT modify source code files. It only outputs a report.
**Exception**: In closed-review mode, may append refactoring/remediation tasks to `tasks.md` with user approval.
