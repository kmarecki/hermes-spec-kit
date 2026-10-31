# Feature Specification: [FEATURE NAME]

**Feature Branch**: [###-feature-name] · **Created**: [DATE] · **Status**: Draft
**Size**: [S | M | L] — [one-line reason; `spec-kit/references/sizing.md`]
**Input**: "[USER DESCRIPTION]"

> Size S (a single bugfix or a small enhancement): **a few lines** — one sentence of intent,
> 1–3 FRs, 1–2 ACs, one Security & Privacy line, 1 SC. Delete every other section.

## User Scenarios *(mandatory)*

### User Story 1 - [Title] (Priority: P1)

[The journey in plain language.] **Why this priority:** [value]. **Independent test:** [how].

**Acceptance Criteria** (`spec-kit/references/acceptance.md` — lowest level that proves it):
- **AC-001** (FR-001) Given [state], When [action], Then [outcome] — Verify: unit | integration | component
- **AC-002** (FR-002) Given [state], When [action], Then [outcome] — Verify: e2e ([why no lower level can prove it])

### User Story 2 - [Title] (Priority: P2)

[…] **Acceptance Criteria:** - **AC-003** (FR-003) Given …, When …, Then … — Verify: [level]

## Edge Cases

- [boundary condition] · [error scenario] — an edge case that matters is an AC too.

## Requirements *(mandatory)*

- **FR-001**: System MUST [specific, testable capability]
- **FR-002**: Users MUST be able to [key interaction]
- **FR-003**: System MUST [behaviour] [NEEDS CLARIFICATION: …] *(max 3 markers)*

**Key entities**: **[Entity]** — [what it represents, key attributes, relations] (domain only).

## Security & Privacy *(mandatory — "None — because …" is a valid answer)*

| Question | Answer |
|----------|--------|
| Authorization / tenant boundary — who may do this, and how is another tenant's data kept out? | |
| Personal data — collected, displayed, exported or logged? retention? | |
| New external surface — endpoint, file upload, integration, secret, dependency? | |
| Input reaching a sensitive operation — validated where? | |
| Audit / logging — what must be recorded, what must never be logged? | |

The pre-implement review checks this table; the final review verdicts it under §2.

## Success Criteria *(mandatory)*

- **SC-001**: [measurable outcome, e.g. "a 1 000-row import completes in < 10 s"]
- **SC-002**: [user or business metric]

## Assumptions

- [target users, scope boundaries, environment, dependencies on existing services]
