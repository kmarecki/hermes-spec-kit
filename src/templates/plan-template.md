# Implementation Plan: [FEATURE]

**Branch**: [###-feature-name] | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from /specs/[###-feature-name]/spec.md

> **Size S**: keep Summary, Current Design, Technical Context (only the lines that matter),
> the external seams and Rounds — delete the rest. No research.md / data-model.md /
> contracts/ / quickstart.md unless the plan cannot be understood without one.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Current Design

> **Regenerated, never appended.** This section describes what is BUILT, in at most one page.
> It is rewritten by `spec-kit-summarize` at every close (and may be refreshed by
> `spec-kit-refresh`); the original design and every bugfix round stay below as dated
> records. A reader who wants the truth reads this section; a reader who wants the
> history reads the rounds.

[Until the first close: "Not yet built — see the sections below for the intended design."]

## Technical Context

- **Language/Version:** [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]
- **Primary Dependencies:** [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]
- **Storage:** [if applicable, e.g., PostgreSQL, CoreData, files or N/A]
- **Testing:** [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]
- **Target Platform:** [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
- **Project Type:** [e.g., library/cli/web-service/mobile-app/compiler/desktop-app or NEEDS CLARIFICATION]
- **Performance Goals:** [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]
- **Constraints:** [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]
- **Scale/Scope:** [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

**GATE:** Must pass before Phase 0 research. Re-check after Phase 1 design.

[Insert specific gates from constitution: Simplicity, Anti-Abstraction, etc.]

## Project Structure

### Documentation (this feature)

specs/[###-feature-name]/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md         # Phase 1 output
└── contracts/           # Phase 1 output (API specs)

### Source Code

[Select and document the structure: Single Project / Web App / Mobile+API]

**Structure Decision:** [Document the selected structure]

## Complexity Tracking

Fill ONLY if Constitution Check has violations that must be justified.

| Violation | Why Needed | Simpler Alternative Rejected Because |
| :--- | :--- | :--- |
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## Rounds (ADR log)

> Feature-local decision records. At close, `spec-kit-summarize` promotes any round that
> passes the ADR bar to a project ADR (see the close document's Architecture Decisions).
> Every bugfix / reopen round appends ONE dated section here — never edits an earlier one.
> A round states what it supersedes, so a contradiction between sections is resolved by date.

### Round 1 — [YYYY-MM-DD] — [trigger: BUG-NNN, …] — supersedes: [§ names or "nothing"]

- **Context**: [what was wrong — one or two sentences, cite the bug ids]
- **Decision**: [what changes in the design]
- **Consequences**: [what else moves; what stays]
- **Plan Ref**: [the bugs.md Plan Ref value for each bug in this round]
