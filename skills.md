# Skill Definitions

This document defines the complete set of Hermes Agent skills that implement the spec kit workflow. Each skill is self-contained with triggers, instructions, and validation logic.

## Skill Architecture

```
spec-kit-workflow (Master Orchestrator)
  │
  ├── spec-kit-constitution (Phase 0)
  ├── spec-kit-specify (Phase 1)
  ├── spec-kit-clarify (Phase 2)
  ├── spec-kit-plan (Phase 3)
  ├── spec-kit-tasks (Phase 4)
  └── spec-kit-implement (Phase 5)
```

## Master Orchestrator: spec-kit-workflow

**Category**: software-development
**Purpose**: Route user requests to appropriate phase skills and maintain workflow state.

### Triggers
- "spec kit"
- "spec-driven"
- "workflow"
- "what phase"
- "spec status"

### Skill Content

```markdown
---
name: spec-kit-workflow
category: software-development
---

# Spec Kit Workflow Orchestrator

This skill orchestrates the spec-driven development workflow.

## Workflow Phases

1. **Constitution** (spec-kit-constitution)
2. **Specify** (spec-kit-specify)
3. **Clarify** (spec-kit-clarify, optional)
4. **Plan** (spec-kit-plan)
5. **Tasks** (spec-kit-tasks)
6. **Implement** (spec-kit-implement)

## Routing Logic

When the user requests spec kit operations:

1. **New Feature**: "Create a spec for [description]"
   → Load spec-kit-specify

2. **Existing Feature Status**: "What phase is [feature] in?"
   → Analyze specs/NNN-feature-name/ directory structure
   → Report current phase and completion status

3. **Advance Phase**: "Plan [feature]" / "Generate tasks for [feature]" / "Implement [feature]"
   → Load appropriate phase skill

4. **Clarify Ambiguities**: "Clarify [feature]"
   → Load spec-kit-clarify

5. **Project Constitution**: "Create constitution" / "Update constitution"
   → Load spec-kit-constitution

## Status Detection

To determine the current phase of a feature, check for artifacts:

| Artifacts Present | Current Phase |
|-------------------|---------------|
| constitution.md only | Ready to Specify |
| spec.md exists | Specified |
| clarify.md exists | Clarifying/Clarified |
| plan.md exists | Planning/Planned |
| tasks.md exists | Tasking/Tasked |
| tasks.md with completions | Implementing |
| all tasks complete | Complete |

## Usage Examples

- "Create a spec for user authentication"
- "What phase is 006-multi-layered-visualizer in?"
- "Plan the implementation for 006-multi-layered-visualizer"
- "Generate tasks for 006-multi-layered-visualizer"
- "Implement the next tasks for 006-multi-layered-visualizer"
```

## Phase 0: spec-kit-constitution

**Category**: software-development
**Purpose**: Establish project-wide principles and constraints.

### Triggers
- "constitution"
- "project principles"
- "specify constitution"
- "project standards"

### Skill Content

```markdown
---
name: spec-kit-constitution
category: software-development
---

# Spec Kit Constitution Workflow

When asked to create or update the project constitution:

## Process

1. Check for existing `specs/constitution.md`
2. If updating, load existing constitution
3. Analyze project context:
   - Read AGENTS.md
   - Review existing specs for patterns
   - Check project structure and tech stack

4. Create/update `specs/constitution.md` with structure:

```markdown
# Project Constitution

## Identity
- **Project**: [Project Name]
- **Domain**: [Domain/Industry]
- **Version**: [Constitution Version]

## Principles

### Architecture
- [Principle]: [Description]
- [Principle]: [Description]

### Quality
- [Principle]: [Description]
- [Principle]: [Description]

### Security
- [Principle]: [Description]
- [Principle]: [Description]

### Performance
- [Principle]: [Description]
- [Principle]: [Description]

## Constraints

### Technical
- [Constraint]: [Reason]

### Regulatory
- [Constraint]: [Reason]

### Business
- [Constraint]: [Reason]

## Quality Gates

### Code Quality
- [Gate]: [Criteria]

### Testing
- [Gate]: [Criteria]

### Security
- [Gate]: [Criteria]

## Decision Record

| Date | Decision | Rationale | Impact |
|------|----------|-----------|--------|
| [Date] | [Decision] | [Why] | [Effect] |
```

5. Validate:
   - All principles are actionable and measurable
   - No contradictions between principles
   - Covers all required domains

6. Report constitution created/updated
```

## Phase 1: spec-kit-specify

**Category**: software-development
**Purpose**: Create comprehensive feature specifications.

### Triggers
- "specify"
- "create spec"
- "feature specification"
- "new spec"

### Skill Content

```markdown
---
name: spec-kit-specify
category: software-development
---

# Spec Kit Specify Workflow

When asked to create a feature specification:

## Process

1. **Create spec directory**: `specs/NNN-feature-name/`
   - NNN is the next sequential number
   - Check existing specs for numbering

2. **Parse user description** and extract:
   - Actors and user roles
   - Key actions and flows
   - Data entities involved
   - Constraints and edge cases

3. **Generate spec.md** using template:

```markdown
# Feature Specification: [Feature Name]

**Feature Branch**: `NNN-feature-name`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "[description]"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - [Name] (Priority: P1)

As a [role], I want [action] so that [benefit].

**Why this priority**: [Justification]

**Independent Test**: [How to verify independently]

**Acceptance Scenarios**:
1. **Given** [context], **When** [action], **Then** [outcome]
2. **Given** [context], **When** [action], **Then** [outcome]

---

### User Story 2 - [Name] (Priority: P2)
[Same structure]

---

## Edge Cases
- [Edge case]: [How handled]

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST [requirement]
- **FR-002**: System MUST [requirement]

### Non-Functional Requirements
- **NFR-001**: System MUST [performance/security/usability]

### Success Criteria
- **SC-001**: [Measurable outcome]
- **SC-002**: [Measurable outcome]

## Key Entities
- **[Entity]**: [Description], [Key attributes]

## Assumptions
- [Assumption]: [Rationale]

## Out of Scope
- [Item]: [Reason excluded]
```

4. **Create quality checklist** at `checklists/requirements.md`

5. **Validate spec** against quality criteria:
   - No implementation details leaked
   - All requirements testable
   - Success criteria measurable
   - Edge cases identified
   - Dependencies documented

6. **Report**: spec created with validation results
```

## Phase 2: spec-kit-clarify

**Category**: software-development
**Purpose**: Resolve ambiguities in feature specifications.

### Triggers
- "clarify"
- "resolve ambiguities"
- "needs clarification"

### Skill Content

```markdown
---
name: spec-kit-clarify
category: software-development
---

# Spec Kit Clarify Workflow

When asked to clarify ambiguities in a specification:

## Process

1. **Load spec.md** from feature directory

2. **Identify ambiguities**:
   - Look for [NEEDS CLARIFICATION] markers
   - Identify vague requirements
   - Find missing edge cases
   - Detect conflicting requirements

3. **Prioritize** (max 3 clarifications):
   - Scope impact (highest)
   - Security/privacy implications
   - User experience impact
   - Technical complexity

4. **Generate clarify.md**:

```markdown
# Clarification Questions: [Feature Name]

**Feature**: [Link to spec.md]
**Created**: [DATE]
**Status**: Pending/Resolved

## Questions

### Q1: [Question Title]
**Impact**: [Scope/Security/UX/Technical]
**Context**: [Relevant spec section]
**Question**: [Clear, specific question]
**Options**:
- A: [Option A]
- B: [Option B]
**Answer**: [Response]
**Decision**: [What was chosen]
**Rationale**: [Why chosen]

### Q2: [Question Title]
[Same structure]

### Q3: [Question Title]
[Same structure]

## Summary
- Questions asked: [N]
- Questions resolved: [N]
- Spec updated: Yes/No
```

5. **Update spec.md** with resolved decisions

6. **Remove** [NEEDS CLARIFICATION] markers

7. **Report**: clarifications resolved, spec updated
```

## Phase 3: spec-kit-plan

**Category**: software-development
**Purpose**: Create detailed implementation plan with technical design.

### Triggers
- "plan"
- "implementation plan"
- "create plan"
- "technical plan"

### Skill Content

```markdown
---
name: spec-kit-plan
category: software-development
---

# Spec Kit Plan Workflow

When asked to create an implementation plan:

## Process

1. **Load context**:
   - Read spec.md (required)
   - Read constitution.md (required)
   - Read clarify.md (if exists)

2. **Execute Phase 3.0: Research**
   - Identify technical unknowns from spec
   - Research best practices and patterns
   - Evaluate technology choices
   - Generate `research.md`:

```markdown
# Technical Research: [Feature Name]

**Feature**: [Link to spec.md]
**Date**: [DATE]

## Decisions

### Decision 1: [Topic]
**Decision**: [What was chosen]
**Rationale**: [Why chosen]
**Alternatives considered**: [What else evaluated]
**Trade-offs**: [Pros/cons]

### Decision 2: [Topic]
[Same structure]

## References
- [Resource]: [URL/Description]
```

3. **Execute Phase 3.1: Data Model**
   - Extract entities from spec
   - Define relationships and constraints
   - Create `data-model.md`:

```markdown
# Data Model: [Feature Name]

## Entities

### [Entity Name]
- **Purpose**: [What it represents]
- **Fields**:
  - `field_name`: [type] - [description]
- **Relationships**:
  - [Entity] → [Entity]: [relationship type]
- **Validation Rules**:
  - [Rule]: [Description]
- **State Transitions**:
  - [State] → [State]: [Trigger]
```

4. **Execute Phase 3.2: Contracts**
   - Generate API contracts from requirements
   - Create interface definitions in `contracts/`

5. **Execute Phase 3.3: Quickstart**
   - Create `quickstart.md` with integration scenarios

6. **Generate plan.md**:

```markdown
# Implementation Plan: [Feature Name]

**Branch**: `NNN-feature-name` | **Date**: [DATE] | **Spec**: [spec.md]

## Summary
[Brief description of implementation approach]

## Technical Context

**Language/Version**: [Tech stack]
**Primary Dependencies**: [Dependencies]
**Storage**: [Storage approach]
**Testing**: [Testing framework]
**Performance Goals**: [Targets]
**Constraints**: [Limitations]

## Constitution Check

*GATE: Must pass before Phase 0 research.*

- **[Principle]**: [PASS/FAIL] - [Justification]

## Project Structure

### Documentation
```
specs/NNN-feature-name/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code
[Expected source code structure]

## Implementation Phases

### Phase 1: Setup
[Shared infrastructure]

### Phase 2: Foundational
[Blocking prerequisites]

### Phase 3+: User Stories
[Feature implementation]
```

7. **Update AGENTS.md** with new spec references

8. **Perform constitution check** against design

9. **Report**: plan created with all artifacts
```

## Phase 4: spec-kit-tasks

**Category**: software-development
**Purpose**: Break down implementation into executable tasks.

### Triggers
- "tasks"
- "task breakdown"
- "create tasks"
- "generate tasks"

### Skill Content

```markdown
---
name: spec-kit-tasks
category: software-development
---

# Spec Kit Tasks Workflow

When asked to create task breakdown:

## Process

1. **Load context**:
   - Read plan.md (required)
   - Read spec.md (required)
   - Read research.md (if exists)
   - Read data-model.md (if exists)

2. **Analyze implementation phases** from plan.md

3. **Extract user stories** from spec.md

4. **Generate tasks.md**:

```markdown
# Tasks: [Feature Name]

**Input**: Design documents from `/specs/NNN-feature-name/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: TDD approach - tests MUST be written before implementation.

**Organization**: Tasks grouped by user story for independent testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create tests directory at [path]
- [ ] T002 [P] Configure [tool] at [path]

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure required before user stories

- [ ] T003 [P] Implement [utility] at [path]
- [ ] T004 Extract [logic] into [module] at [path]

**Checkpoint**: Foundation ready - user stories can begin in parallel

---

## Phase 3: User Story 1 - [Name] (Priority: P1) 🎯 MVP

**Goal**: [What this story achieves]

**Independent Test**: [How to verify]

### Tests for User Story 1 ⚠️

- [ ] T005 [P] [US1] Write test for [feature] at [path] (Ensure it fails)
- [ ] T006 [P] [US1] Write test for [feature] at [path] (Ensure it fails)

### Implementation for User Story 1

- [ ] T007 [US1] Implement [feature] at [path]
- [ ] T008 [US1] Implement [feature] at [path]

---

## Phase 4: User Story 2 - [Name] (Priority: P2)

[Same structure]

---

## Verification

- [ ] All tasks completed
- [ ] All tests passing
- [ ] Acceptance criteria met
- [ ] Documentation updated
```

5. **Create implementation checklist** at `checklists/implementation.md`

6. **Validate**:
   - All phases covered
   - Dependencies identified
   - Parallel tasks marked [P]
   - File paths specified
   - TDD approach enforced

7. **Report**: tasks generated with validation results
```

## Phase 5: spec-kit-implement

**Category**: software-development
**Purpose**: Execute implementation following the task plan.

### Triggers
- "implement"
- "execute tasks"
- "start implementation"
- "next task"

### Skill Content

```markdown
---
name: spec-kit-implement
category: software-development
---

# Spec Kit Implement Workflow

When asked to implement:

## Process

1. **Check checklists status**:
   - Scan all checklist files in checklists/
   - Count completed vs incomplete items
   - If incomplete, ask user: "Some checklists are incomplete. Proceed? (yes/no)"

2. **Load implementation context**:
   - tasks.md (REQUIRED)
   - plan.md (REQUIRED)
   - data-model.md (IF EXISTS)
   - contracts/ (IF EXISTS)
   - research.md (IF EXISTS)
   - quickstart.md (IF EXISTS)

3. **Parse tasks.md** and extract:
   - Current phase
   - Next incomplete task
   - Task dependencies
   - Parallel opportunities

4. **Execute tasks** following rules:
   - Phase-by-phase execution
   - Sequential tasks in order
   - Parallel tasks [P] can run together
   - TDD: test tasks before implementation
   - File-based coordination (same files = sequential)

5. **For each task**:
   a. Read task description and file path
   b. If test task: write failing test first
   c. If implementation task: implement to make test pass
   d. Verify task completion
   e. Update tasks.md with [X] completion

6. **Validation checkpoints**:
   - After each phase: verify all tasks complete
   - After each user story: run independent test
   - After implementation: verify acceptance criteria

7. **Report progress**:
   - Tasks completed: [N]/[Total]
   - Current phase: [Phase]
   - Next task: [Task ID]
   - Tests passing: [Yes/No]

## Implementation Rules

- NEVER skip test tasks
- NEVER implement without understanding the requirement
- ALWAYS verify file paths exist or create them
- ALWAYS run tests after implementation
- STOP on test failures and report
- Update tasks.md immediately after completion
```

## Skill Dependencies

```
spec-kit-workflow
  └── routes to all phase skills

spec-kit-constitution
  └── no dependencies (Phase 0)

spec-kit-specify
  └── spec-kit-constitution (for context)

spec-kit-clarify
  └── spec-kit-specify (requires spec.md)

spec-kit-plan
  └── spec-kit-specify (requires spec.md)
  └── spec-kit-constitution (for validation)

spec-kit-tasks
  └── spec-kit-plan (requires plan.md)
  └── spec-kit-specify (for user stories)

spec-kit-implement
  └── spec-kit-tasks (requires tasks.md)
  └── spec-kit-plan (for context)
```

## Installation

To install these skills in Hermes Agent:

1. Create skill files in `~/.hermes/skills/`:
   - `spec-kit-workflow.md`
   - `spec-kit-constitution.md`
   - `spec-kit-specify.md`
   - `spec-kit-clarify.md`
   - `spec-kit-plan.md`
   - `spec-kit-tasks.md`
   - `spec-kit-implement.md`

2. Each file should contain the YAML frontmatter and markdown content shown above.

3. Test by saying: "Create a spec for [feature]"
