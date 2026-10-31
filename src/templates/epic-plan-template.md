# Epic plan: [EPIC NAME]

**Epic**: epic.md · **Date**: [DATE] · **Modules**: [names as in `design_dir` — the design docs this epic changes]

> Stage E2. HOW across features — the architecture the single features will implement
> piece by piece. Line-level design belongs to each feature's plan.md.

## Current state

[What exists today, from the module design docs and the code — 5–10 lines with paths. What
is wrong or missing that the goal needs.]

## Target architecture

[Components, boundaries, data flow at the end of the epic. Which modules change how; which
stay. One diagram or ≤ 1 page of prose.]

## Seams and contracts

| Seam | Today | After the epic | Owner feature |
|------|-------|----------------|---------------|

## Cross-feature decisions

| ID | Decision | Alternatives rejected | Why | ADR |
|----|----------|------------------------|-----|-----|
| ED-001 | | | | — / NNNN |

## Sequencing constraints and parallelism

[What must come first (shared infrastructure, a seam, a migration); what can run in parallel;
what can be dropped last if time runs out.]

## Rollout, migration, rollback

[Feature flags, data migration order, how the epic can stop halfway without harm, how to roll
back the whole thing.]

## Risks

| Risk | Impact | Mitigation | Owner |
|------|--------|------------|-------|
