---
name: spec-kit-constitution
description: >
  Load when the user says 'spec-kit constitution', 'speckit constitution', 'spec-kit principles', 'speckit principles', "create constitution", "create project principles", or "set up project principles" — Phase 0 project setup. Three modes: brownfield (auto-detect from existing code), free-text (describe your project in a sentence, agent maps to purpose/arch/principles), and guided wizard (3-level decision tree with 9 purposes × 25 architecture options).
version: 2.1.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, constitution, principles, project-setup, brownfield, greenfield]
    related_skills: [spec-kit-specify, spec-kit-workflow]
---

# spec-kit-constitution

**Phase**: 0 (project foundation, one-time) · **Persona**: project founder setting ground rules — principled but practical; every rule has a purpose; always offer choices with trade-offs.
**Purpose**: create `specs/constitution.md`. Modes: **brownfield** (detect the stack, pre-fill ⭐ defaults), **free-text** (describe the project → purpose/architecture/tech/principles inferred), **wizard** (3-level tree: 9 purposes × 25 architectures × tech brackets).
**Full procedure**: `spec-kit/references/skills/spec-kit-constitution.md` (detection tables, inference mapping, purpose→principle defaults, monorepo mode). Reference data: `spec-kit/references/constitution-principles.md` (12 principles × 3 options), `spec-kit/references/constitution-tables.md`.
**Not for**: per-feature runs — principles are project-wide.

## Before writing
- Run `spec-kit/references/preflight.md`. `specs/constitution.md` exists → report its version and **HALT** (amend only on explicit request).

## Steps
1. Detect mode: scan the project root with the detection tables. Files found → brownfield summary ("Detected [language]/[framework]; tests …; CI …; DB …; lint …"). Nothing → **ASK**: free-text description or wizard.
2. Free-text: map description → purpose (A–I) → architecture → tech → principle defaults; present the inference table; **WAIT** for "all good" or corrections.
3. Wizard: Level 1 purpose (9 options with trade-offs) → monorepo question → Level 2 architecture → Level 3 technology bracket (3 options each). Pre-fill the 12 principles from the purpose mapping.
4. For **each** of the 12 principles present the 3 options (rule, pros, cons) with the ⭐ default marked; **WAIT** for A/B/C/skip and an optional rationale. Skip Database for stateless projects.
5. Copy `spec-kit/templates/constitution-template.md` → `specs/constitution.md`: chosen option + rule text + rationale + rejected alternatives per principle; tech stack (or "TBD"); monorepo → Projects table. Version 1.0.0 (MAJOR incompatible governance / MINOR new principle / PATCH clarification).

## Done when
- [ ] Every principle chosen by the user (never silently); skipped ones listed with a reason.
- [ ] MCP (optional): `mcp_spec_kit_project_set_constitution(status="present")` (checks the file exists).
- [ ] history.md is per feature — for the constitution, commit directly: `spec(phase-0): constitution for [PROJECT]` (`spec-kit/references/auto-commit.md`).

## Next
Report mode, inferred items, chosen options; propose `spec-kit-specify`.
