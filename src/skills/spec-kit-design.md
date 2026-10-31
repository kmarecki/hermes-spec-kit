---
name: spec-kit-design
description: >
  Load when the user says 'spec-kit design [module]', 'speckit design [module]', "write the design doc for [module]", "refresh the design doc for [module]", "how does [module] work" (when a design doc should answer it), or "document the architecture of [module]" — a living module design document (purpose, components, data flow, seams, invariants, security, testing, debt). Only for projects that keep `design_dir` in specs/git-conventions.md.
version: 1.0.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec-kit, design, architecture, module]
    related_skills: [spec-kit-plan, spec-kit-summarize, spec-kit-epic, spec-kit-refresh]
---

# spec-kit-design

**Phase**: cross-feature (standalone) · **Persona**: the architect who describes what is **built** — components, flows, seams, invariants — in ≤ 3–4 pages a new engineer or an auditor reads first; not a decision log (ADRs), not a plan (epic), not a feature (spec).
**Purpose**: create or refresh `[design_dir]/[module].md` (`spec-kit/templates/design-doc-template.md`) from the code. A module is **space**: a bounded part of the system that outlives every epic. Feature closes patch it; this skill writes or re-baselines it.
**Not for**: projects without `design_dir` (the plan's `## Current Design` is the design — say so and stop); recording a decision (→ an ADR at close); a feature's own design (→ `spec-kit-plan`).

## Before writing
- Preflight checks 1 and 4 (`spec-kit/references/preflight.md`). `design_dir` from `specs/git-conventions.md`; absent → **ASK** once whether to add it (default `docs/design`); declined → stop.
- Read the code first: directories, entry points, DI registrations, DB objects, contracts, tests. Then the constitution, the ADR index, AGENTS.md, closed specs whose plan names the module (`**Modules**:`).
- Existing doc → No Complete Overwrite: patch section by section with approval (refresh), never rewrite.

## Create
1. Boundary: what the module owns, what it does not, which services / projects / directories.
2. Components table (`path` per row), data flow (one request or event end to end), seams and contracts table (owner per seam).
3. **Invariants and security**: the tenant / authorization boundary (where the check is — `path:line`), personal data handled and what must never be logged, other invariants. Cite code, not intentions.
4. Testing (harnesses, goldens, probes), known debt (ticket / ADR per item), the ADRs that shaped it.
5. Status header `current`, owner, last-patched. Commit `docs(design): [module] design doc` (`spec-kit/references/commits.md`).

## Refresh
Diff the page against the code (`git log -- <module paths>` since *Last patched*): ≤ 5 discrepancies per session, "doc says … / code does … → patch?" **WAIT** each; append a change-log line; bump *Last patched*. Never bulk-apply.

## Done when
- [ ] Every section filled from the code with paths; security invariants cite `path:line`; ≤ 3–4 pages; status header present.
- [ ] Project ADR index and AGENTS.md point at the doc (propose the one-line patch, **WAIT**).

## Next
Feature closes keep it true (`spec-kit-summarize` step "design doc + epic row"); `spec-kit-epic` lists it under *Modules touched*.
