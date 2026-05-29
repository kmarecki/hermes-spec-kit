# Tasks: [Feature Name]

**Input**: Design documents from `/specs/NNN-feature-name/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: TDD approach - tests MUST be written before implementation.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create tests directory at `[path]`
- [ ] T002 [P] Configure `[tool]` at `[path]`
- [ ] T003 [P] Set up `[infrastructure]` at `[path]`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [ ] T004 [P] Implement `[utility]` at `[path]`
- [ ] T005 Extract `[logic]` into standalone module at `[path]`
- [ ] T006 [P] Create `[interface]` at `[path]`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - [Name] (Priority: P1) 🎯 MVP

**Goal**: [What this story achieves]

**Independent Test**: [How to verify this story works independently]

### Tests for User Story 1 ⚠️

- [ ] T007 [P] [US1] Write unit test for `[feature]` at `[path]` (Ensure it fails)
- [ ] T008 [P] [US1] Write integration test for `[feature]` at `[path]` (Ensure it fails)

### Implementation for User Story 1

- [ ] T009 [US1] Implement `[feature]` at `[path]`
- [ ] T010 [US1] Implement `[feature]` at `[path]`
- [ ] T011 [US1] Add `[supporting feature]` at `[path]`

**Checkpoint**: User Story 1 complete - verify independent test passes

---

## Phase 4: User Story 2 - [Name] (Priority: P2)

**Goal**: [What this story achieves]

**Independent Test**: [How to verify]

### Tests for User Story 2 ⚠️

- [ ] T012 [P] [US2] Write unit test for `[feature]` at `[path]` (Ensure it fails)
- [ ] T013 [P] [US2] Write integration test for `[feature]` at `[path]` (Ensure it fails)

### Implementation for User Story 2

- [ ] T014 [US2] Implement `[feature]` at `[path]`
- [ ] T015 [US2] Implement `[feature]` at `[path]`

**Checkpoint**: User Story 2 complete - verify independent test passes

---

## Phase 5: Polish & Integration

**Purpose**: Final integration, edge cases, and quality improvements

- [ ] T016 [P] Handle `[edge case]` at `[path]`
- [ ] T017 [P] Add `[error handling]` at `[path]`
- [ ] T018 Update documentation at `[path]`
- [ ] T019 Run full test suite and verify all pass

---

## Verification

- [ ] All tasks completed
- [ ] All tests passing
- [ ] Acceptance criteria met for each user story
- [ ] Documentation updated
- [ ] No regression in existing functionality
