# Specification Quality Checklist: [Feature Name]

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: [DATE]
**Feature**: [Link to spec.md]

## Content Quality

- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

## Requirement Completeness

- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Success criteria are technology-agnostic (no implementation details)
- [ ] All acceptance scenarios are defined
- [ ] Edge cases are identified
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

## Feature Readiness

- [ ] All functional requirements have clear acceptance criteria
- [ ] User scenarios cover primary flows
- [ ] Feature meets measurable outcomes defined in Success Criteria
- [ ] No implementation details leak into specification

## Notes

- Items marked incomplete require spec updates before `/speckit.clarify` or `/speckit.plan`

---

# Implementation Readiness Checklist: [Feature Name]

**Purpose**: Validate implementation readiness before starting coding
**Created**: [DATE]
**Feature**: [Link to tasks.md]

## Planning Completeness

- [ ] plan.md exists and is complete
- [ ] research.md resolves all technical unknowns
- [ ] data-model.md defines all entities
- [ ] contracts/ defines all interfaces
- [ ] quickstart.md documents integration scenarios

## Task Definition

- [ ] All phases covered in tasks.md
- [ ] Each task has a clear description
- [ ] File paths are specified for each task
- [ ] Parallel tasks marked with [P]
- [ ] User story tags [US#] present
- [ ] Test tasks precede implementation tasks

## Test Strategy

- [ ] TDD approach defined
- [ ] Test frameworks identified
- [ ] Test locations specified
- [ ] Integration test strategy defined

## Risk Assessment

- [ ] Known risks documented
- [ ] Mitigation strategies defined
- [ ] Rollback plan exists

## Notes

- Items marked incomplete require updates before implementation begins
