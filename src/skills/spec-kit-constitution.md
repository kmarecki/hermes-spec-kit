---
name: spec-kit-constitution
description: >
  Load when the user says 'spec-kit constitution', 'speckit constitution', 'spec-kit principles', 'speckit principles', "create constitution", "create project principles", or "set up project principles" — Phase 0 project setup. Three modes: brownfield (auto-detect from existing code), free-text (describe your project in a sentence, agent maps to purpose/arch/principles), and guided wizard (decision tree with 11 purposes × 44 architecture options + project traits).
version: 2.2.0
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
**Purpose**: create `specs/constitution.md`. Modes: **brownfield** (detect the stack, pre-fill ⭐ defaults), **free-text** (describe the project → purpose/architecture/tech/principles inferred), **wizard** (11 purposes × 44 architectures + traits × tech brackets).
**Full procedure**: `spec-kit/references/skills/spec-kit-constitution.md` (purpose→principle matrix, trait rules, project documents). Reference data — load only the one the mode needs: `spec-kit/references/constitution-detection.md` (brownfield) · `spec-kit/references/constitution-greenfield.md` (free-text, wizard); always `spec-kit/references/constitution-principles.md` (12 principles × 3 options).
**Not for**: per-feature runs — principles are project-wide.

## Before writing
- `spec-kit/references/preflight.md`. `specs/constitution.md` exists → report its version and **HALT** (amend only on explicit request).

## Steps
0. **Level 0 — context, ASK first** (`spec-kit/references/rigor.md`): hobby · indie · team · platform · regulated → recommend the **rigor** (lean / standard / strict), the doc scale and compliance; record `rigor:` (written in step 6).
1. Detect mode: scan the project root with `constitution-detection.md`. Files found → brownfield summary ("Detected [language]/[framework]; tests …; CI …; DB …; lint …") + inferred purpose / option / traits for the user to correct. Nothing → **ASK**: free-text description or wizard (`constitution-greenfield.md`).
2. Free-text: map description → purpose (A–K) → architecture → tech → traits → principle defaults; present the inference table; **WAIT** for "all good" or corrections.
3. Wizard: Level 1 purpose (11, with what each weighs) → monorepo → Level 1.5 traits (runs where · regulated domain · lifecycle) → Level 2 architecture → Level 3 technology (3 options each); nothing fits → **Other** (closest purpose, own options, marked). Pre-fill the 12 principles: matrix → rigor → trait rules (stricter wins; lean may relax the matrix).
4. For **each** of the 12 principles (lean: only Testing, Architecture, Git, Config / secrets — list the other 8 as defaults the user may open) present the 3 options (rule, pros, cons) with the ⭐ default marked; **WAIT** for A/B/C/skip and an optional rationale. Skip Database for stateless projects.
5. Copy `spec-kit/templates/constitution-template.md` → `specs/constitution.md`: chosen option + rule text + rationale + rejected alternatives per principle; tech stack (or "TBD"); monorepo → Projects table; **Engineering guidelines** from the stack + option + rigor (lean: one line; standard / strict: each MUST → a `specs/merge-checklist.md` P-item, **WAIT**). Version 1.0.0 (MAJOR incompatible governance / MINOR new principle / PATCH clarification).
6. **Project documents** (full procedure Step 7): write `rigor:`; lean + Principle 5 A → `blocked_branches: none` (trunk); the scale follows Level 0 (**ASK** only if unclear) — small (no ADR / design / epic dirs) or ⭐ platform (`adr_dir`, `design_dir`, `epics_dir`; brownfield with > 1 deployable ⇒ platform); write the keys into `specs/git-conventions.md`; existing doc dirs → point at them; AGENTS.md missing → `spec-kit/templates/AGENTS-template.md`, exists → patch the spec-kit block only (**WAIT**).

## Done when
- [ ] Every principle chosen by the user (never silently); skipped ones listed with a reason.
- [ ] MCP (optional): `mcp_spec_kit_project_set_constitution(status="present")` (checks the file exists).
- [ ] Commit directly (`spec-kit/references/commits.md`): `spec(phase-0): constitution for [PROJECT]`.

## Next
Report mode, inferred items, chosen options, scale. Platform → `spec-kit-design` **map** (system.md, module split, module docs, initial / retroactive ADRs), then `spec-kit-specify`; small → `spec-kit-specify`.
