# Specification Quality Checklist: [Feature Name]

**Purpose**: Optional validation of specification completeness and quality before planning.
**Created**: [DATE]
**Feature**: [Link to spec.md]

## Content Quality

- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

## Requirement Completeness

- [ ] No [NEEDS CLARIFICATION] markers remain (optional)
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

- These are optional guidelines, not blocking gates
- Incomplete items are suggestions for improving the spec, not requirements

---

# Implementation Readiness Checklist: [Feature Name]

**Purpose**: Optional readiness check before starting implementation.
**Created**: [DATE]
**Feature**: [Link to tasks.md]

## Planning Completeness

- [ ] plan.md exists
- [ ] research.md covers technical unknowns (optional)
- [ ] data-model.md defines entities (if applicable)
- [ ] quickstart.md documents integration (if applicable)

## Task Definition

- [ ] All phases covered in tasks.md
- [ ] Each task has a clear description
- [ ] File paths specified for each task
- [ ] Parallel tasks marked with [P]
- [ ] User story tags [US#] present
- [ ] Test tasks precede implementation tasks (TDD practice)

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

- These are optional guidelines, not blocking gates
- Incomplete items are suggestions for improving readiness, not requirements