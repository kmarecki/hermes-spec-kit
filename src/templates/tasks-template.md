# Tasks: [FEATURE NAME]

**Input**: Design documents from /specs/[###-feature-name]/
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks grouped by user story to enable independent implementation and testing of each story.

**Format**: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

**Path Conventions**

- Single project: `src/`, `tests/` at repository root
- Web app: `backend/src/`, `frontend/src/`
- Mobile: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project — adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Setup database schema and migrations framework
- [ ] T005 [P] Implement authentication/authorization framework
- [ ] T006 [P] Setup API routing and middleware structure
- [ ] T007 Create base models/entities that all stories depend on
- [ ] T008 Configure error handling and logging infrastructure
- [ ] T009 Setup environment configuration management

**Checkpoint**: Foundation ready — user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - [Title] (Priority: P1) :star: MVP

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Implementation for User Story 1

- [ ] T010 [P] [US1] Create [Entity1] model in src/models/[entity1].py
- [ ] T011 [P] [US1] Create [Entity2] model in src/models/[entity2].py
- [ ] T012 [US1] Implement [Service] in src/services/[service].py (depends on T010, T011)
- [ ] T013 [US1] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T014 [US1] Add validation and error handling
- [ ] T015 [US1] Add logging for user story 1 operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Implementation for User Story 2

- [ ] T016 [P] [US2] Create [Entity] model in src/models/[entity].py
- [ ] T017 [US2] Implement [Service] in src/services/[service].py
- [ ] T018 [US2] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T019 [US2] Integrate with User Story 1 components (if needed)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Implementation for User Story 3

- [ ] T020 [P] [US3] Create [Entity] model in src/models/[entity].py
- [ ] T021 [US3] Implement [Service] in src/services/[service].py
- [ ] T022 [US3] Implement [endpoint/feature] in src/[location]/[file].py

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T0XX [P] Documentation updates in docs/
- [ ] T0XX Code cleanup and refactoring
- [ ] T0XX Performance optimization across all stories
- [ ] T0XX [P] Additional unit tests in tests/unit/
- [ ] T0XX Security hardening
- [ ] T0XX Run quickstart.md validation

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

User stories can proceed in parallel once Foundational phase completes (if team capacity allows).

### Parallel Opportunities

All Setup tasks marked [P] can run in parallel
All Foundational tasks marked [P] can run in parallel (within Phase 2)
Once Foundational phase completes, all user stories can start in parallel
All tasks for a user story marked [P] can run in parallel
Different user stories can be worked on in parallel by different team members