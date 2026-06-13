<!-- SPECKIT START -->
This project uses spec-driven development via Hermes Agent's spec-kit skills.

Skills: constitution, specify, clarify, plan, tasks, implement, test, review, summarize, refresh, workflow

Development modes:
  - **Specify** (default): Constitution → Specify → [Clarify] → Plan → Tasks → Implement → Test → Close
  - **Bugfix**: Test → [Clarify] → Plan → Tasks → Implement → Test → Close (auto-chains inner loop)

Key behaviors:
  - Constitution is always optional
  - Phase 6 (Close/Summarize) is mandatory to complete a feature
  - All spec artifacts are batch-committed when Phase 4 begins (not per design phase)
  - Implementation uses phase-level TDD: all tests RED first, all code GREEN, then commit
  - TDD can be bypassed at user request during task generation
  - Spec health score (0-100%) computed at close
  - Regressions caught by final full-suite run → one umbrella fix task

Artifact paths:
  - Constitution: `specs/constitution.md`
  - Features: `specs/NNN-name/{spec,plan,tasks,bugs,close}.md`

Load `spec-kit-workflow` to start. Natural language triggers route to the correct phase.
<!-- SPECKIT END -->

# Project AGENTS.md

Fill in project-specific context below: tech stack, build commands, conventions, active specs.
