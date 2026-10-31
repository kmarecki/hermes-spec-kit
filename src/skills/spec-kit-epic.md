---
name: spec-kit-epic
description: >
  Load when the user says 'spec-kit epic [name]', 'speckit epic [name]', "create an epic for [programme]", "epic status [name]", "close epic [name]", or "which features belong to [epic]" — an epic plan: one body of work made of many single-spec features (goal, scope, feature table with status, sequencing, cross-feature rules, epic-level done-when). Only for projects that keep `epics_dir` in specs/git-conventions.md.
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

**Phase**: cross-feature (standalone) · **Persona**: delivery lead — one goal, the features that reach it, their order, the rules they all obey; never design detail (that is the module design doc) and never a feature spec.
**Purpose**: create, report or close `[epics_dir]/[epic-short-name].md` (`spec-kit/templates/epic-template.md`). An epic is **time**: it opens, collects features, closes. A module is **space** (`spec-kit-design`).
**Not for**: projects without `epics_dir` (every feature is its own epic — say so and stop); a single feature (→ `spec-kit-specify`).

## Before writing
- Preflight checks 1 and 4 (`spec-kit/references/preflight.md`). `epics_dir` from `specs/git-conventions.md`; absent → **ASK** once whether to add it (default `specs/epics`); declined → stop.
- No Complete Overwrite: an existing epic file is patched (rows, decisions, close section), never rewritten.

## Create
1. Parse the description → goal (one sentence), scope in / out, **done-when** (measurable, epic-level), owner.
2. Feature table: the features already specified (`specs/*/spec.md` with `**Epic**: [name]`) plus the planned ones as rows without a spec dir yet; sequencing and dependencies in one line.
3. **Cross-feature rules** — the constraints every feature must obey (the reviews check them like constitution MUSTs). Modules touched → names as in `design_dir`.
4. Decisions that only make sense at epic level → the Decisions table (ADR bar applies at close).
5. Commit `spec(epic): [name] plan` (`spec-kit/references/commits.md`).

## Status
Read the feature table against `mcp_spec_kit_list_features()` (or the files): refresh Status / PR / Health per row; report rows out of date, features that name the epic but have no row, rows without a spec after their predecessors closed.

## Close
Every row closed or explicitly dropped (reason) → append `## Close` (date, N closed / N planned, health range, ADRs, design docs patched, dropped scope); Status → closed. **WAIT** for the owner's confirmation; quote it. Commit `spec(epic): [name] close`.

## Done when
- [ ] Goal, done-when, rules and the feature table filled; every feature naming the epic has a row.
- [ ] Features' `spec.md` carry `**Epic**: [name]` (added at specify; patched here for older specs with approval).

## Next
`spec-kit-specify` for the next feature in order (the spec's `**Epic**:` line links it); each feature close (`spec-kit-summarize`) updates its row.
