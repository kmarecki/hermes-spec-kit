---
name: spec-kit-epic
description: >
  Load when the user says 'spec-kit epic [name]', 'speckit epic [name]', "create an epic for [programme]", "epic status [name]", "close epic [name]", "plan epic [name]", "break down epic [name]", "review epic [name]", or "which features belong to [epic]" — an epic: one body of work made of many single-spec features, run through its own specify → plan → breakdown → review (with devil's advocate) → build → close. Only for projects that keep `epics_dir` in specs/git-conventions.md.
version: 1.0.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec-kit, epic, programme, roadmap]
    related_skills: [spec-kit-specify, spec-kit-summarize, spec-kit-design, spec-kit-workflow]
---

# spec-kit-epic

**Phase**: cross-feature (standalone) · **Persona**: delivery lead and architect one level up — one goal, the architecture across features, the features in order, the rules they all obey; never a feature's line-level design.
**Purpose**: run an epic through the same shape as a feature, in `[epics_dir]/[epic]/`: **E1 specify** `epic.md` → **E2 plan** `plan.md` → **E3 breakdown** `features.md` (the epic's tasks are features) → **E3.5 review** `review.md` (+ devil's advocate) → **E4 build** (features run the normal workflow) → **E6 close**. An epic is **time**; a module is **space** (`spec-kit-design`).
**Not for**: projects without `epics_dir` (every feature is its own epic — say so, stop); one feature (→ `spec-kit-specify`).

## Before writing
- Preflight checks 1 and 4 (`spec-kit/references/preflight.md`). `epics_dir` from `specs/git-conventions.md`; absent → **ASK** once (default `specs/epics`); declined → stop. Stage = the first missing file; an existing file is patched, never rewritten.
- Load constitution, ADR index, AGENTS.md, the module design docs (`design_dir`) the epic will touch.

## E1 Specify → `epic.md` (`spec-kit/templates/epic-template.md`)
Id `NNN-short-name` like a feature: **NNN = the tracker's epic number** (ADO / Jira — ASK for it, record the link as `**Tracker**:`), else `mcp_spec_kit_next_id(kind="EPIC")`; the directory is `[epics_dir]/NNN-short-name/`. Goal (one sentence); **problem and users (why now)**; **success metrics** (post-launch, lagging — today / target / how measured); **alternatives considered** (incl. do nothing); scope in / **out**, stakeholders; **EAC-###** epic acceptance criteria — measurable at the end, each with how it will be verified (feature ACs, probe, command, user); cross-feature rules; epic-level Security & Privacy; ≤ 3 clarification markers (more → ask first). **WAIT** for the owner's confirmation. `epics_index: on` (default) → add the row to `[epics_dir]/README.md` (create from `spec-kit/templates/epics-index-template.md`). Commit `spec(epic): [epic] specify`.

## E2 Plan → `plan.md` (`spec-kit/templates/epic-plan-template.md`)
Current state from the design docs and the code (paths); target architecture; seams today → after; cross-feature decisions `ED-###` (alternatives, why; ADR bar at close); sequencing constraints and parallelism; rollout / migration / rollback; risks with owners. `**Modules**:` names the design docs the features will patch. Commit `spec(epic): [epic] plan`.

## E3 Breakdown → `features.md` (`spec-kit/templates/epic-features-template.md`)
Ordered rows, one per single-spec feature: intent, size guess, depends-on, modules, EACs; parallel groups in the Order line. Every EAC → ≥ 1 feature; every feature → ≥ 1 EAC or it is scope creep. First row must deliver something testable. ≤ ~12 rows — more means two epics. Commit `spec(epic): [epic] breakdown`.

## E3.5 Review → `review.md` round (`spec-kit/templates/epic-review-template.md`) — required before the first feature
Coverage and scope (EAC ↔ features, non-goals, size realism) · fit (constitution, ADRs, design docs' current state true, rules checkable) · sequencing and risk. **Devil's advocate** (5+ features: a separate sub-agent, different model when available; else a separate pass): strongest case against the epic + the ~80 % alternative, pre-mortem at six months, system-level abuse cases, the riskiest assumption; ≤ 5 objections, each answered. Verdict **GO / GO-WITH-CHANGES / NO-GO**; changes patched into epic / plan / features with approval; NO-GO → new round. Prefer the other agent or a fresh-context sub-agent. Commit `spec(epic): [epic] review (verdict: X)`.

Every stage and every feature close that flips a row also updates the index row (status, features closed / planned, closed date).

## E4 Build — `status [epic]` at any time
Features run `spec-kit-specify` → … → `spec-kit-summarize` with `**Epic**: [epic]`; specify fills the row's spec dir and size, the close flips status / PR / health / ADRs. Status: refresh rows against `mcp_spec_kit_list_features()`; report stale rows, features naming the epic without a row, blocked order. A feature that cannot stay inside the plan → an `ED-###` amendment here, not a silent change.

## E6 Close — every row closed or dropped (reason)
Verify each **EAC** with evidence (feature ACs, a probe now, the owner's quoted words); fill *EAC coverage · Verified by*; close review round in `review.md` (verdict CLOSED / NOT-DONE, devil's advocate: "what does the goal look like unmet?"); harvest `ED-###` through the ADR bar (`spec-kit-summarize` rules); confirm the design docs were patched; Status → closed. **WAIT** for the owner; quote them. Commit `spec(epic): [epic] close`.

## Done when
- [ ] Stage file written, patched not rewritten; the owner's rulings quoted; every feature naming the epic has a row; the index row (when on) matches.

## Next
E1 → E2 → E3 → E3.5 → `spec-kit-specify` for row #1; each `spec-kit-summarize` updates its row; last row → E6.
