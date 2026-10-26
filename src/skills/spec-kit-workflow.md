---
name: spec-kit-workflow
description: >
  Load when the user says 'spec-kit bugfix [feature]', 'speckit bugfix [feature]', 'spec-kit fix [feature]', 'speckit fix [feature]', 'spec-kit reopen [feature]', 'speckit reopen [feature]', 'spec-kit implement [feature]', 'speckit implement [feature]', 'spec-kit plan [feature]', 'speckit plan [feature]', 'spec-kit close [feature]', 'speckit close [feature]', 'spec-kit specify [feature]', 'speckit specify [feature]', 'spec-kit status [feature]', 'speckit status [feature]', or any 'spec-kit ...' or 'speckit ...' workflow routing command. Also triggers on natural phrases: "fix bugs in [feature]", "bugfix [feature]", "bugfixing [feature]", "continue bugfixing", "reopen [feature]", "implement [feature]", "plan [feature]", "close [feature]", "create a spec", "specify [feature]", "what phase is [feature] in". Routes to the correct phase skill.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec-kit, workflow, orchestrator, routing]
    related_skills: [spec-kit-constitution, spec-kit-specify, spec-kit-clarify, spec-kit-plan, spec-kit-tasks, spec-kit-review, spec-kit-implement, spec-kit-test, spec-kit-summarize, spec-kit-refresh]
---

# Spec Kit Workflow Orchestrator

**Persona**: router, not executor — check prerequisites, derive the phase, dispatch to the phase skill, enforce guardrails before handing over.
**Load for**: `bugfix`, `quickfix`, `reopen`, `close`, `status` / "what phase is X in", and any `spec-kit …` command whose phase is unclear. Phase skills do **not** need this skill loaded — their preflight carries the guardrails.
**Full procedure**: `spec-kit/references/skills/spec-kit-workflow.md` (routing table, phase-detection table, guardrail matrix, reopen and quickfix rules).

## Before routing
- Preflight checks 1 and 4 (`spec-kit/references/preflight.md`): feature branch, git conventions.
- Feature named but `specs/[feature]/` missing → **BLOCK**, list available specs.
- Bootstrap gate, once per session: `specs/constitution.md` missing → route `spec-kit-constitution` and stop.
- Phase: MCP `mcp_spec_kit_get_next_actions(feature)` (phase card) or `mcp_spec_kit_list_features()`; without MCP derive from files: spec → plan → tasks → tasks with `[X]` (implementing) → bugs.md open (bugfix loop) → all verified (**must close**) → close doc (complete); close doc + open bug = reopened. All tasks done, spec has ACs and no fresh PASS round in acceptance.md → **accept**; then no READY final review → **final review**; close doc with ⚠️/❌ artifact rows → warn "drift — run refresh".

## Routes
| Phase | Skill | Needs |
|---|---|---|
| 1 specify · 1.5 clarify | `spec-kit-specify` · `spec-kit-clarify` | — · spec |
| 2 plan · 3 tasks | `spec-kit-plan` · `spec-kit-tasks` | spec · spec+plan |
| 3.5 pre-implement review (L: required) | `spec-kit-review` | spec+plan+tasks |
| 5 accept (spec has ACs) | `spec-kit-test` (accept mode) | all tasks `[X]` |
| **5.5 final review (mandatory)** | `spec-kit-review` | all tasks `[X]`, no open bug, acceptance PASS |
| 4 implement · 5 test | `spec-kit-implement` · `spec-kit-test` | tasks · spec |
| 6 summarize / close (mandatory) | `spec-kit-summarize` | tasks |
| refresh (standalone) | `spec-kit-refresh` | spec |

Inject constitution principles as guidance (not gates) when routing to specify, plan, implement, test, review.

## Bugfix loop
`bugfix [feature]`: load bugs.md → closed feature → say "use `reopen`". Every open bug needs a **Plan Ref** (else route `spec-kit-plan` first, user confirms). Bug *Requires Clarification* → `spec-kit-clarify` first. Then **auto-chain** `spec-kit-plan` → `spec-kit-tasks` → `spec-kit-implement`; review only on request. `quickfix [feature]` (explicit opt-in): plan section + task + fix in one commit, documents still written.
- `test [feature]` logs and stops. New bugs mid-round → logged, fixed next round.
- **Acceptance loop** — `accept [feature]` (also routed automatically after implement when spec.md has ACs): `spec-kit-test` accept round → FAIL → auto-chain `bugfix` (plan → tasks → implement) → accept again; no user prompt between rounds. Stops on PASS (→ final review) or a stop condition (max rounds, no progress, spec/frozen-test change, run cannot execute) → **ASK**. `spec-kit/references/acceptance.md`.
- No open bug and (spec has ACs) the latest acceptance round PASS → route the **final review**; READY → suggest `close [feature]`; NOT READY → its bugs start a new round. Never auto-close.
- Size (spec.md `**Size**`, `spec-kit/references/sizing.md`): S auto-chains specify → plan → tasks; L requires the pre-implement review before implement.
- `reopen [feature]`: needs a close doc; bugfix branch per `specs/git-conventions.md`; close appends, never overwrites.

## Guardrails
- Code-editing tools only in Implement (incl. bugfix implementation). Spec artifacts only in their own phase; summarize/close and refresh may patch spec/plan with approval.
- Unknown phase → **ASK**. Code requested outside Implement → refuse, name the right phase.
- A feature is not "done" without `close.md` / `implementation-summary.md`.
