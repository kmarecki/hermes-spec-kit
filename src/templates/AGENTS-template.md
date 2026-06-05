# Project Agent Instructions

This file provides project-level context and instructions for Hermes Agent. Always read and follow these guidelines when working on this project.

## Spec-Driven Development Workflow

This project uses spec-driven development (SDD). All features should follow the spec → plan → tasks → implement workflow unless the user explicitly requests otherwise.

## Workflow Phases

```
Constitution → Specify → Clarify → Plan → Tasks → Implement → Test
                                                              │
                                                              └── bugfix loop ──┐
                                                        ┌──────────────────────┘
                                                        ▼
                                                  Clarify → Plan → Tasks → [Analyze] → Implement → Test
```

The workflow has two paths:
- **Initial path**: Constitution → Specify → Clarify → Plan → Tasks → Implement → Test
- **Bugfix loop**: Test → [Clarify] → Plan → Tasks → [Analyze] → Implement → Test (repeat)

When the user requests a new feature:

1. **Specify**: "Create a spec for [feature description]" → produces `specs/NNN-feature-name/spec.md`
2. **Clarify (optional)**: "Clarify [feature]" → resolves ambiguities in spec
3. **Plan**: "Plan [feature]" → produces `specs/NNN-feature-name/plan.md`, `research.md`, `data-model.md`
4. **Tasks**: "Generate tasks for [feature]" → produces `specs/NNN-feature-name/tasks.md`
5. **Implement**: "Implement [feature]" → executes tasks with TDD
6. **Test**: "Test [feature]" — creates/opens bugs.md for tracking discovered bugs
7. **Bugfix**: "bugfix [feature]" — routes back through Plan/Tasks/Implement for each bug

## Spec Kit Skills

Load the appropriate skill for each phase:
- `spec-kit-workflow` — orchestration and phase detection
- `spec-kit-constitution` — project principles
- `spec-kit-specify` — feature specification
- `spec-kit-clarify` — ambiguity resolution
- `spec-kit-plan` — technical planning
- `spec-kit-tasks` — task breakdown
- `spec-kit-analyze` — optional quality review
- `spec-kit-checklist` — optional quality checklists
- `spec-kit-implement` — task execution
- `spec-kit-test` — testing & bug tracking

## Project Constitution

- The project constitution is at `specs/constitution.md` (or `.specify/memory/constitution.md` per official spec-kit convention).
- Read it before planning or implementing. All plans must address relevant principles.
- Check the **Constitution Check** section in `plan.md` when creating a plan.

## AGENTS.md SPECKIT Section

This section keeps track of current spec artifacts. Update it manually when specs are created or completed.

<!-- SPECKIT START -->
<!-- Add or remove entries as specs progress. Each line links to one key artifact. -->

<!-- SPECKIT END -->

## Spec Quality Standards

- Specifications must be technology-agnostic; technical decisions belong in plans
- Use Given/When/Then acceptance scenarios
- Define measurable success criteria
- Test tasks must precede implementation tasks
- Plans must include a Constitution Check

## Conventions

- Spec numbering: `NNN-feature-name` (sequential, 3 digits)
- Branch naming: `feature/NNN-feature-name` or `NNN-feature-name`
- Commit messages: `spec: [phase] - [feature name]`
- Tasks use format: `[ID] [P?] [Story] Description`
  - `[P]` = can run in parallel
  - `[Story]` = user story tag like US1, US2

## Project Context

<!--
Add project-specific information here:
- Tech stack (languages, frameworks, key libraries)
- Build/test commands
- Key directories and their purpose
- Coding standards
- Any existing conventions or patterns agents should follow
-->

[Describe your project's tech stack, build commands, key directories, etc.]

## Communication Style

<!--
Describe how you want the agent to communicate:
- Verbose vs concise
- Code vs explanation
- Confirmations vs proceed-without-asking
- When to ask for clarification
-->

[Communicate concisely. Show code and commands over explanations. Ask for clarification only when blocked.]

## Important Reminders

- This file is loaded fresh each message — changes take effect immediately
- Delete or clear any section you don't need
- Add custom sections as your project requires