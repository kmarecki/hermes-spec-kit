---
name: spec-kit-clarify
description: Load when the user says 'spec-kit clarify [feature]', 'speckit clarify [feature]', "clarify [feature]", or "resolve ambiguities in [feature]" — Phase 1.5 optional clarification of ambiguities in the spec.
version: 1.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, clarification, ambiguity, qa]
    related_skills: [spec-kit-specify, spec-kit-plan, spec-kit-workflow]
---

# spec-kit-clarify

**Phase**: 1.5 (optional) · **Persona**: precise questioner — ambiguities hide assumptions that cause rework; never ask for the sake of process.
**Purpose**: resolve underspecified areas of `spec.md` by a short Q&A logged in `clarify.md`.
**Not for**: specs with no real ambiguity → `spec-kit-plan`.

## Before writing
- `spec-kit/references/preflight.md`. **BLOCK** if `spec.md` is missing. Load `spec.md`; bugfix mode: also the bugs flagged *Requires Clarification*.

## Steps
1. Scan: scope, domain model, UX flow, non-functional attributes, integrations, edge cases, terminology, the Security & Privacy table.
2. ≤ 5 questions per session, **one at a time**, each answerable by 2–5 options or a short answer. Obvious from context → do not ask.
3. Present → WAIT → validate → record. No human (unattended) → record an **assumption** (preflight 6), never invent an answer.
4. After every answer update `spec.md` at once (replace the marker); `clarify.md` is the log (`## Q1: …` / `**Answer**` / `**Resolution**`), `spec.md` the truth.

## Done when
- [ ] Every answer applied; unanswered questions left as markers. history.md entry, then commit (`spec-kit/references/preflight.md` procedure): `spec(phase-1.5): [feature] clarifications`.

## Next
`spec-kit-plan`.
