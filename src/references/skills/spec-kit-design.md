# spec-kit-design — map mode (full procedure)

`design map` lays down a project's living documents in one pass: the system view, the module
split, a design doc per module and the ADRs. Brownfield recovers them **from the code**;
greenfield writes the **target** from the constitution. It runs after the constitution (Step 7,
scale = platform) or on its own on an existing project; re-running it refreshes, never rewrites.
Create / Refresh of a single module are in the one-screen SKILL.md.

## Preconditions

`design_dir` and `adr_dir` from `specs/git-conventions.md` (absent → ASK once, defaults
`docs/design`, `docs/adr`). Read `specs/constitution.md`, AGENTS.md / CLAUDE.md, the ADR index,
every file already in `design_dir`. Mode: source code present → brownfield, else greenfield.

## Brownfield

```
1. RECOVER (read-only; cite paths)
   deployables   solution / workspace files, projects, package manifests, Dockerfiles,
                 function hosts, IaC resources — what runs where
   entry points  Program.cs / main / handlers / routes / controllers / message consumers
   wiring        DI registrations, project references, imports between top-level folders
   data          stores, schemas and their owners (migrations, DB projects, which code writes
                 which tables), caches, queues, blobs
   edges         external systems, identity provider, third-party APIs, trust boundaries
                 (internet → app, app → DB, service → service, tenant boundary)
   existing docs ADRs, design / architecture docs, constitution inventories, READMEs

2. SYSTEM VIEW → [design_dir]/system.md (design-doc template, the `system` variant)
   containers table (service / store / external · technology · owner · trust boundary) +
   one context diagram; status current. PRESENT → WAIT → write.

3. MODULE SPLIT — PRESENT one table, WAIT, apply the user's edits:
   | Module | Paths | Responsibility | Owns (data) | Seams in → out | Evidence | Existing doc |
   rules  a module = one responsibility + the data it owns; a deployable is NOT automatically a
          module (one API can hold several; one module can span API + DB objects + jobs)
          · 5–12 modules; more → group, fewer → the project is small (say so)
          · shared "common" / god libraries → a Known-debt row on the modules that use them,
            not a module of their own (unless they own data or a contract)
          · evidence = project references, shared tables, call graphs — never names alone
          · name modules by domain (reporting, identity), not by layer (services, dal)

4. MODULE DOCS — per approved module the SKILL.md *Create* steps (boundary, components with
   paths, one data flow, seams, invariants and security citing path:line, testing, debt,
   ADRs). ≤ 3 modules per commit; WAIT per module. An existing doc covering the module:
   absorb (its facts move in, the old file gets a "> **Status:** superseded by <module>.md"
   line) · link (kept as a deep-dive, linked from Decisions/Testing) · keep (unrelated) —
   ASK per file; never delete or move.

5. ADRs — index first: every existing ADR → listed in the index, never duplicated.
   HARVEST de facto decisions the code embodies and no ADR records: platform and runtime,
   architecture style, data store and who owns the schema, auth / identity, messaging,
   hosting, multi-tenancy, logic location (e.g. business rules in stored procedures),
   the boundaries step 3 found. Apply the ADR bar (spec-kit-summarize full procedure);
   ≤ 10 per run, most constraining first. Each: Status `Accepted (retroactive)`, **Decided**
   = first commit that shows it (`git log --diff-filter=A --format=%as -- <path> | tail -1`)
   or "unknown", **Deciders** = "recorded by design map; original deciders unknown",
   Context / Decision / Consequences from the code, Evidence = paths. PRESENT → WAIT each.

6. INDEX + POINTERS
   [design_dir]/README.md from spec-kit/templates/design-index-template.md: the module map
   (module · paths · doc · status · owner) — the plan names `**Modules**:` from it and the
   close patches by it. AGENTS.md: one line pointing at system.md, the module map and the ADR
   index (WAIT). Constitution inventories of modules → propose a one-line pointer to the map
   (WAIT); never rewrite the constitution.
```

## Greenfield

```
1. system.md — status `target`: the containers the Level 2 architecture implies (app, stores,
   identity, external systems, trust boundaries); "planned" in the owner column.
2. MODULE MAP — [design_dir]/README.md with the planned modules (from the description and the
   architecture: A2 → bounded contexts; A3 → services; A5 → app, model gateway, retrieval, evals,
   tools); status `planned`, no module docs yet — a module doc is written when the first
   feature builds it (design docs describe what is built).
3. ADRs — 0001 Record architecture decisions · 0002 Architecture style (the Level 2 pick; the
   rejected options are the Alternatives) · 0003 Technology stack (Level 3) · one more per
   principle option that constrains code (e.g. database migration-first). Status Accepted,
   Deciders = the user, quoted from the constitution dialogue. WAIT each.
4. Optional: propose the first epic (spec-kit-epic E1, e.g. "MVP") when epics_dir is kept.
```

## Commits

`docs(design): system view and module map` · `docs(design): <module>[, …] design docs` ·
`docs(adr): NNNN–NNNN retroactive decisions` (greenfield: `initial decisions`) — per
`spec-kit/references/commits.md`, each after the user approved its content.

## Re-run

Same steps as *Refresh*: diff system.md / the map against the code; new deployables, modules or
undocumented decisions → propose patches (≤ 5 per session), WAIT each; append to the change log.
