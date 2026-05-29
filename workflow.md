# Workflow Phases

The Hermes Spec Kit workflow consists of six phases, each with specific inputs, outputs, and validation criteria. Phases must be completed sequentially, with quality gates preventing progression until validation passes.

## Phase Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Constitution│────▶│  Specify    │────▶│  Clarify    │
│  (Project)  │     │  (Feature)  │     │ (Optional)  │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Implement  │◀────│    Tasks    │◀────│    Plan     │
│  (Execute)  │     │  (Breakdown)│     │  (Design)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Phase 0: Constitution

**Purpose**: Establish project-wide principles, constraints, and quality standards.

**When**: Once per project, or when making significant architectural changes.

**Inputs**:
- Project description
- Team requirements
- Technical constraints

**Process**:
1. Load `spec-kit-constitution` skill
2. Analyze existing project context (AGENTS.md, existing specs)
3. Define principles covering:
   - Architecture standards
   - Quality requirements
   - Security constraints
   - Performance targets
   - Testing standards

**Outputs**:
- `specs/constitution.md` - Project constitution document

**Validation**:
- All principles are actionable and measurable
- No contradictions between principles
- Covers all required domains (security, performance, etc.)

**Example Prompt**:
```
"Create the project constitution for our AI MUD visualizer"
```

## Phase 1: Specify

**Purpose**: Create a comprehensive feature specification focused on user value.

**When**: Starting a new feature or significant enhancement.

**Inputs**:
- Natural language feature description
- Project constitution
- Existing specs (for context)

**Process**:
1. Load `spec-kit-specify` skill
2. Create numbered spec directory: `specs/NNN-feature-name/`
3. Parse user description and extract:
   - Actors and user roles
   - Key actions and flows
   - Data entities involved
   - Constraints and edge cases
4. Generate spec.md with required sections
5. Create quality checklist at `checklists/requirements.md`
6. Validate spec against quality criteria

**Outputs**:
- `specs/NNN-feature-name/spec.md` - Feature specification
- `specs/NNN-feature-name/checklists/requirements.md` - Quality checklist

**Quality Criteria**:
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Success criteria are technology-agnostic
- [ ] All acceptance scenarios are defined
- [ ] Edge cases are identified
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

**Example Prompt**:
```
"Create a spec for multi-layered visualizer with 3D support"
```

## Phase 2: Clarify (Optional)

**Purpose**: Resolve ambiguities and de-risk uncertain decisions.

**When**: When spec contains [NEEDS CLARIFICATION] markers or significant uncertainties exist.

**Inputs**:
- Feature specification with ambiguities
- Stakeholder availability for questions

**Process**:
1. Load `spec-kit-clarify` skill
2. Identify ambiguities in spec.md (max 3 clarifications)
3. Prioritize by impact: scope > security > UX > technical
4. Generate structured questions
5. Await stakeholder responses
6. Update spec.md with resolved decisions

**Outputs**:
- `specs/NNN-feature-name/clarify.md` - Clarification questions and answers
- Updated `spec.md` with resolved ambiguities

**Rules**:
- Maximum 3 clarification questions per spec
- Each question must significantly impact the feature
- Document rationale for all decisions
- Update spec.md immediately after clarification

**Example Prompt**:
```
"Clarify the ambiguities in spec 006-multi-layered-visualizer"
```

## Phase 3: Plan

**Purpose**: Create detailed implementation plan with technical design.

**When**: After specification is complete and clarified.

**Inputs**:
- Feature specification (spec.md)
- Project constitution
- Existing codebase context

**Process**:
1. Load `spec-kit-plan` skill
2. Read spec.md and constitution.md
3. Execute sub-phases:

   **Phase 3.0: Research**
   - Identify technical unknowns
   - Research best practices and patterns
   - Evaluate technology choices
   - Generate `research.md` with findings

   **Phase 3.1: Design**
   - Extract entities from spec → `data-model.md`
   - Define relationships and constraints
   - Create state transitions if applicable

   **Phase 3.2: Contracts**
   - Generate API contracts from requirements
   - Create interface definitions
   - Output to `contracts/` directory

   **Phase 3.3: Integration**
   - Create `quickstart.md` for integration scenarios
   - Document setup and configuration
   - Include example usage

4. Update AGENTS.md with new spec references
5. Perform constitution check against design

**Outputs**:
- `specs/NNN-feature-name/plan.md` - Implementation plan
- `specs/NNN-feature-name/research.md` - Technical research
- `specs/NNN-feature-name/data-model.md` - Data models
- `specs/NNN-feature-name/contracts/` - API contracts
- `specs/NNN-feature-name/quickstart.md` - Integration guide
- Updated `AGENTS.md` with spec references

**Constitution Check**:
- Validate design against project principles
- Identify any violations with justification
- Ensure all quality gates are addressed

**Example Prompt**:
```
"Plan the implementation for 006-multi-layered-visualizer"
```

## Phase 4: Tasks

**Purpose**: Break down implementation into executable tasks.

**When**: After plan is complete and validated.

**Inputs**:
- Implementation plan (plan.md)
- Feature specification (spec.md)
- Research findings (research.md)
- Data models (data-model.md)

**Process**:
1. Load `spec-kit-tasks` skill
2. Analyze plan.md for implementation phases
3. Extract user stories from spec.md
4. Create task breakdown:
   - Phase 1: Setup (shared infrastructure)
   - Phase 2: Foundational (blocking prerequisites)
   - Phase 3+: User stories (parallel where possible)
5. Mark parallel tasks with [P]
6. Include exact file paths in descriptions
7. Create implementation checklist

**Outputs**:
- `specs/NNN-feature-name/tasks.md` - Task breakdown
- `specs/NNN-feature-name/checklists/implementation.md` - Implementation checklist

**Task Format**:
```markdown
## Phase N: [Phase Name]

**Purpose**: [What this phase accomplishes]

- [ ] TXXX [P] [US#] Task description with file path
- [ ] TXXX [P] [US#] Another task
```

**Task Rules**:
- Each task is independently completable
- Parallel tasks marked [P] have no dependencies
- User story tags [US#] link to spec requirements
- File paths are absolute and specific
- Test tasks precede implementation tasks (TDD)

**Example Prompt**:
```
"Generate tasks for 006-multi-layered-visualizer"
```

## Phase 5: Implement

**Purpose**: Execute implementation following the task plan.

**When**: After tasks are defined and validated.

**Inputs**:
- Task breakdown (tasks.md)
- Implementation plan (plan.md)
- All design artifacts
- Quality checklists

**Process**:
1. Load `spec-kit-implement` skill
2. Validate checklists are complete
3. Load implementation context:
   - tasks.md (required)
   - plan.md (required)
   - data-model.md (if exists)
   - contracts/ (if exists)
   - research.md (if exists)
4. Execute tasks phase-by-phase:
   - Complete each phase before proceeding
   - Respect task dependencies
   - Follow TDD approach
   - Validate at each checkpoint
5. Update task completion status
6. Run tests and verify acceptance criteria

**Outputs**:
- Implemented code changes
- Test results and coverage
- Updated tasks.md with completion status
- Verification against acceptance criteria

**Execution Rules**:
- Phase-by-phase execution only
- Sequential tasks must complete in order
- Parallel tasks [P] can run concurrently
- TDD: tests before implementation
- Validate checkpoints between phases
- Stop on test failures

**Example Prompt**:
```
"Implement the next tasks for 006-multi-layered-visualizer"
```

## Workflow State Machine

```
                    ┌──────────────┐
                    │   START      │
                    └──────┬───────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Phase 0: Constitution                        │
│  Input:  Project description                                    │
│  Output: constitution.md                                        │
│  Gate:   Principles defined and validated                       │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Phase 1: Specify                             │
│  Input:  Feature description                                    │
│  Output: spec.md + checklists/requirements.md                   │
│  Gate:   All quality criteria pass                              │
└─────────────────────────────────────────────────────────────────┘
                           │
                  ┌────────┴────────┐
                  │ Ambiguities?    │
                  └────────┬────────┘
                     Yes   │   No
                  ┌────────┴────────┐
                  ▼                 │
┌──────────────────────────┐        │
│  Phase 2: Clarify        │        │
│  Input:  Ambiguities     │        │
│  Output: clarify.md      │        │
│  Gate:  All resolved     │        │
└──────────────────────────┘        │
                  │                  │
                  └────────┬─────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Phase 3: Plan                                │
│  Input:  spec.md + constitution.md                              │
│  Output: plan.md, research.md, data-model.md, contracts/        │
│  Gate:   Constitution check passes                              │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Phase 4: Tasks                               │
│  Input:  plan.md + spec.md + research.md                        │
│  Output: tasks.md + checklists/implementation.md                │
│  Gate:   All tasks defined and validated                        │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Phase 5: Implement                           │
│  Input:  tasks.md + all design artifacts                        │
│  Output: Code changes + test results                            │
│  Gate:   All acceptance criteria met                            │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    COMPLETE  │
                    └──────────────┘
```

## Phase Validation

Each phase has specific validation criteria that must pass before proceeding:

### Constitution Validation
- [ ] All principles are actionable
- [ ] No contradictions between principles
- [ ] Covers security, performance, quality
- [ ] Approved by stakeholders

### Specification Validation
- [ ] No implementation details
- [ ] All requirements testable
- [ ] Success criteria measurable
- [ ] Edge cases identified
- [ ] Scope clearly bounded

### Plan Validation
- [ ] All technical unknowns resolved
- [ ] Data models defined
- [ ] Contracts specified
- [ ] Constitution check passed
- [ ] Integration scenarios documented

### Tasks Validation
- [ ] All phases covered
- [ ] Dependencies identified
- [ ] Parallel tasks marked
- [ ] File paths specified
- [ ] TDD approach enforced

### Implementation Validation
- [ ] All tasks completed
- [ ] Tests passing
- [ ] Acceptance criteria met
- [ ] Code reviewed
- [ ] Documentation updated

## Workflow Customization

The workflow can be customized for different project types:

### Library/SDK Projects
- Skip Clarify phase if API is well-defined
- Focus on contracts and data models
- Emphasize backward compatibility

### Web Applications
- Include UX design artifacts
- Add performance benchmarks
- Focus on user scenarios

### Data Pipelines
- Emphasize data models
- Include data quality checks
- Focus on throughput and latency

### Mobile Applications
- Include platform-specific considerations
- Add offline capabilities
- Focus on battery and network usage
