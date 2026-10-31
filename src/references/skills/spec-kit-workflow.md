# spec-kit-workflow — full procedure

> **Loaded on demand** — the one-screen SKILL.md is the entry point; this file holds only what it leaves out. Read the section you need. Hermes tools (`terminal`, `write_file`/`patch`, `read_file`, `search_files`, `skill_view`) map to Claude Code `Bash`, `Write`/`Edit`, `Read`, `Grep`/`Glob`, `Skill`; MCP `mcp_spec_kit_*` = `mcp__spec-kit__*`.

Routing only — never execute a phase here. "bugfix" → the Bugfix section, not specify.

## Bootstrap and phase detection
`specs/constitution.md` missing → route `spec-kit-constitution`, HALT (once per session; features
never check it again). Constitution principles are injected into phase skills as guidance, not gates.

| Artifacts | Phase |
|-----------|-------|
| spec.md | Specified (1) · clarify.md → clarified |
| plan.md | Planned (2) · tasks.md → tasked (3) · tasks with `[X]` → implementing (4) |
| bugs.md with open bugs | bugfix loop (5) · only `claimed` → awaiting an oracle |
| all tasks done, ACs, no fresh PASS round | **accept due** |
| no open bug, acceptance PASS (or no ACs), no fresh READY round | **final review due** · AWAITING-OWNER → the owner's answers |
| review-final READY / READY-WITH-FOLLOWUPS, fresh | **must close** |
| close.md / implementation-summary.md | complete · + open bugs → reopened |

Drift: a close doc with ⚠️ / ❌ artifact rows → "run `refresh [feature]`".

## Prerequisites per skill
specify none · clarify spec · plan spec · tasks spec + plan · review (pre) spec + plan + tasks ·
review (final) every task `[X]`, no open bug, acceptance PASS · implement tasks · test spec ·
summarize tasks + fresh READY final review · refresh spec.

## Bugfix
```
bugfix [feature]:
  close doc exists → "use reopen [feature]"
  each open bug: Plan Ref missing → spec-kit-plan first (user confirms)
                 Requires Clarification = yes → spec-kit-clarify first
  AUTO-CHAIN spec-kit-plan → spec-kit-tasks → spec-kit-implement (no user choice; review on request)
  implement done, spec has ACs → accept [feature] automatically
quickfix [feature]: explicit opt-in only — plan section + task + fix in ONE commit; docs still exist
test [feature]: logs and STOPS; new bugs mid-round wait for the next round
accept [feature]: spec-kit-test accept mode → FAIL → bugfix (auto) → accept again … until PASS
  or a stop condition (max rounds, no progress, spec / frozen-test change, run cannot execute) → ASK
all bugs verified (oracle each) → suggest the final review, then close — never auto-close
```

## Reopen
Needs a close doc. Branch `{original_prefix}/NNN-name{reopen_suffix}` per `specs/git-conventions.md`
(default `-bugfixing`); `bugs.md` created if missing; the bugfix loop runs; the close APPENDS a
dated section. A requirement that went from ✅ to ❌ → ASK before writing.

## Guardrails
| Phase | May write | Code tools |
|-------|-----------|------------|
| Specify / Clarify | spec.md, clarify.md, decisions.md | no |
| Plan / Tasks | plan artifacts / tasks.md | no |
| Review | report · review-final.md, evidence/final-*, bugs.md entries, merge-checklist.md (first use), approved spec/plan patches | runs build/test/lint only |
| Implement (incl. bugfix) | source, tasks.md `[X]`, bugs.md → claimed, evidence/ | **yes** |
| Test | bugs.md, acceptance.md, evidence/acceptance-* | no |
| Summarize / Close | close.md, change-record.md, spec/plan/data-model patches (approved), ADRs + index, AGENTS.md patches, bugs.md gap bugs | no |
| Refresh | spec/plan/data-model/contracts patches (per-item approval) | no |

Unknown phase → ASK. Code outside Implement → refuse, name the phase. "[feature] is done" without
a close doc → BLOCK "run close [feature]".
