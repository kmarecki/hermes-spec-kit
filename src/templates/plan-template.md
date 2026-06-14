# Implementation Plan: [FEATURE]

**Branch**: [###-feature-name] | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from /specs/[###-feature-name]/spec.md

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

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