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

**Persona**: router, not executor — check prerequisites, derive the phase, dispatch, enforce guardrails.
**Load for**: `bugfix`, `quickfix`, `reopen`, `accept`, `status` / "what phase is X in", and any `spec-kit …` command whose phase is unclear. Phase skills (`spec-kit-specify`, `spec-kit-clarify`, `spec-kit-plan`, `spec-kit-tasks`, `spec-kit-review`, `spec-kit-implement`, `spec-kit-test`, `spec-kit-summarize`, `spec-kit-refresh`, `spec-kit-constitution`) trigger themselves — do not load this skill for them.
**Full procedure**: `spec-kit/references/skills/spec-kit-workflow.md` (bugfix / quickfix / reopen rules, guardrail table).

## Before routing
- Preflight checks 1 and 4 (`spec-kit/references/preflight.md`). Feature named but `specs/[feature]/` missing → **BLOCK**, list specs. `specs/constitution.md` missing → route `spec-kit-constitution`, stop (once per session).
- Phase: `mcp_spec_kit_get_next_actions(feature)` / `mcp_spec_kit_list_features()`; no MCP: spec → plan → tasks → `[X]` tasks (implementing) → bugs open (bugfix loop) → all verified → acceptance PASS (ACs) → final review READY → close doc (complete); close doc + open bug = reopened.

## Routes
| State | Route |
|---|---|
| all tasks `[X]`, spec has ACs, no fresh PASS round | **accept** → `spec-kit-test` (accept mode) |
| no open bug, acceptance PASS (or no ACs), no fresh READY review | **final review** → `spec-kit-review` |
| final review READY / READY-WITH-FOLLOWUPS, fresh | **must close** → `spec-kit-summarize` |
| close doc with ⚠️/❌ artifact rows | warn "drift — run refresh" |

Inject constitution principles as guidance (not gates) when routing.

## Bugfix loop
`bugfix [feature]`: closed feature → say "use `reopen`". Every open bug needs a **Plan Ref** (else `spec-kit-plan` first). *Requires Clarification* → `spec-kit-clarify` first. Then **auto-chain** `spec-kit-plan` → `spec-kit-tasks` → `spec-kit-implement`; review only on request. `quickfix [feature]` (explicit opt-in): plan section + task + fix in one commit, documents still written.
- `accept [feature]` (also automatic after implement when spec.md has ACs): accept round → FAIL → auto-chain `bugfix` → accept again; no prompt between rounds; stop conditions → **ASK** (`spec-kit/references/acceptance.md`). PASS → final review. Never auto-close.
- Rigor (`spec-kit/references/rigor.md`, on the phase card): size × rigor → process level P1 / P2 / P3 on the phase card: P1 auto-chains specify → plan → tasks, no accept loop, final = self-check; P2 lite pre-implement review; P3 full pre-implement review, devil's advocate by a different agent, strict L a human approver.
- `reopen [feature]`: needs a close doc; bugfix branch per `specs/git-conventions.md`; the close appends.

## Guardrails
- Code-editing tools only in Implement (incl. bugfix). Spec artifacts only in their phase; summarize/close and refresh patch spec/plan with approval. Unknown phase → **ASK**. Code requested outside Implement → refuse, name the phase. Not done without a close doc.
