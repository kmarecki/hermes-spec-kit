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

**Phase**: 1.5 (optional) · **Persona**: curious detail-gatherer — ambiguities hide assumptions that cause rework; ask precise questions, never for the sake of process.
**Purpose**: resolve underspecified areas of `spec.md` through a short Q&A; log it in `clarify.md`.
**Full procedure**: `spec-kit/references/skills/spec-kit-clarify.md`.
**Not for**: specs with no real ambiguity — go to `spec-kit-plan`.

## Before writing
- Run `spec-kit/references/preflight.md`. **BLOCK** if `spec.md` does not exist (run `spec-kit-specify`).
- Load `spec.md`; in bugfix mode also `bugs.md` (bugs flagged *Requires Clarification*).

## Steps
1. Scan: functional scope, domain model, UX flow, non-functional attributes, integrations, edge cases, terminology.
2. Max 5 questions per session, **one at a time**, each answerable by 2–5 options or a short answer.
3. For each: present → WAIT for the user → validate → record. If no human can answer (unattended run): do not invent an answer — record an **assumption** and move on.
4. After every answer: update `spec.md` immediately (replace `[NEEDS CLARIFICATION]` markers). `clarify.md` is the log; `spec.md` is the truth.
5. `clarify.md` format: `## Q1: …` / `**Answer**` / `**Resolution**` (how it was applied).

## Done when
- [ ] Every answered question applied to `spec.md`; unanswered ones left as markers, not guessed.
- [ ] history.md entry, then commit — Shared Commit Procedure in `spec-kit/references/preflight.md`: scope `clarify.md`, `spec.md`; message `spec(phase-1.5): [feature] clarifications`.

## Next
Propose `spec-kit-plan`.
