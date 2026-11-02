<!-- SPECKIT START -->
This project uses spec-driven development via Hermes Agent's spec-kit skills.

Skills: constitution, specify, clarify, plan, tasks, implement, test, review, summarize, refresh, workflow

Development modes:
  - **Specify** (default): Specify → [Clarify] → Plan → Tasks → [Review] → Implement → Test → Final review → Close
  - **Bugfix**: Test → [Clarify] → Plan → Tasks → Implement → Test → Final review → Close (auto-chains inner loop)
  - **Size tiers** (declared in spec.md): S = short spec/plan/tasks, auto-chained; M = default; L = full artifacts + pre-implement review

Key behaviors:
  - Constitution (`specs/constitution.md`) is project setup, checked once; the final review enforces its rules
  - Each design phase commits its own artifacts; implementation commits once per phase
  - The final review (`review-final.md`) must say READY on the current code before close
  - Phase 6 (Close/Summarize) is mandatory; it writes/updates ADRs and keeps this file current
  - Implementation uses phase-level TDD: all tests RED first, all code GREEN, then commit
  - TDD can be bypassed at user request during task generation
  - Spec health score (0-100%) computed at close
  - Regressions caught by final full-suite run → one umbrella fix task

Artifact paths:
  - Constitution: `specs/constitution.md`
  - Features: `specs/NNN-name/{spec,plan,tasks,bugs,review-final,close}.md`
  - Merge checklist: `specs/merge-checklist.md` · ADRs: [docs/adr/]

Load `spec-kit-workflow` to start. Natural language triggers route to the correct phase.
<!-- SPECKIT END -->

# Project AGENTS.md

Fill in project-specific context below: tech stack, build commands, conventions, active specs.
