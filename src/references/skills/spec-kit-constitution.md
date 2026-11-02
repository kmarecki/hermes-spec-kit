# spec-kit-constitution — full procedure

**Task Persona**: Adopt the mindset of a project founder setting ground rules.
Constitutions should be principled but practical — they guide decisions without
being bureaucratic. Every rule must have a clear purpose. Always offer choice
with tradeoffs explained.

**Phase**: 0 (Project Foundation)

**Purpose**: Create or update the project constitution at `specs/constitution.md`.

Three input modes:
1. **Brownfield** (existing code): Auto-detects stack from project files —
   60+ detection patterns for language, framework, test runner, CI, database,
   and linting. Pre-fills ⭐-marked defaults.
2. **Free-text description** (new project): User describes the project in
   natural language (e.g. "React Native mobile app for fitness, small team,
   ship fast"). Agent maps description to purpose → architecture → tech →
   principle defaults automatically. User reviews and adjusts.
3. **Wizard** (guided, new project): Interactive 3-level decision tree
   (11 purposes × 44 architecture options + project traits). User picks at each level.
   Always presents 3 options per principle with pros and cons.

**When NOT to use**: This is a one-time setup per project. Do NOT re-run for
every feature — principles are project-wide.

**Prerequisites**: None. This is the first skill — run first for a new project.

**Artifacts**: `specs/constitution.md`

**Routing**: Load this skill when the user says "create constitution" or
"create project principles". If loaded directly (not via spec-kit-workflow),
consider loading the workflow first for prerequisite checks.

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Step 0: Check for existing constitution

```
IF specs/constitution.md EXISTS:
  LOAD existing constitution
  NOTE: "Constitution exists at v[VERSION]. Run 'amend constitution' to update."
  HALT — constitution is one-time setup, do not overwrite without user intent
```

### Step 0.5: Level 0 — context and rigor (both modes, asked first)

ASK who the project is for and what is at stake — hobby / learning · indie or solo product ·
startup or small team · established product or platform · regulated or safety-critical. Recommend
the rigor, doc scale and compliance from the Level 0 table in `spec-kit/references/rigor.md`
(recommendation first); a regulated / safety-critical trait found later forces strict. RECORD
rigor (written to git-conventions in Step 7). The rigor changes the principle defaults (Step 2c),
how many principles are asked (Step 3) and the engineering guidelines (Step 5).

### Step 1: Detect mode — brownfield vs greenfield

```
SCAN project root for these files to identify the tech stack:

LOAD `spec-kit/references/constitution-detection.md` (brownfield only — greenfield tables are not loaded)

  IF any project files detected:
    MODE = brownfield
    COMPILE a detection summary:
      "Detected [language] project with [framework].
       Test: [test_framework]. CI: [ci_platform]. DB: [database].
       Linting: [linter]. Formatting: [formatter]."

    INFER purpose (A–K), option and traits from the closest detection row; PRESENT them
    with the summary (the user corrects); record "not from the reference tables" when none fits.
    USE the detection to pre-fill ⭐ recommendations:
      - Testing: If pytest/Jest/Vitest/go test detected → ⭐ B (Pragmatic TDD)
                   If no test files found → ⭐ C (Test-After)
      - Linting: If ESLint/Ruff/RuboCop/clippy config exists → ⭐ A or B
                   If no lint config → ⭐ C (Minimal)
      - Git: If .github/workflows exists → ⭐ A (Trunk-Based) or B (Feature Branches)
               If Jenkinsfile → ⭐ C (Git Flow)
      - DB: If migrations detected → ⭐ A (Migration-First)
              If no DB files → SKIP Principle 10

  ELSE:
    MODE = greenfield
    NOTE: "No existing project detected. Would you like to:
           1. Describe your project in a sentence — I'll map it to purpose,
              architecture, tech, and principle defaults automatically
           2. Use the guided wizard — 3 levels of choices with tradeoffs at each step"
    
    ASK: "Which approach do you prefer? (1) Free-text description or (2) Guided wizard"
    
    RECORD: input_mode = [free-text | wizard]
```

### Step 2a / 2b: Greenfield — free-text or wizard

**Only for MODE=greenfield.** LOAD `spec-kit/references/constitution-greenfield.md` and follow
G1 (free-text: description → purpose, option, stack, traits → inference table → WAIT) or G2
(wizard: Level 1 purpose of 11 → monorepo → Level 1.5 traits → Level 2 architecture → Level 3
technology; "Other" when nothing fits). Brownfield never loads that file.

#### Step 2c: Default Mapping — Purpose to Principle Weights

Once purpose + architecture are chosen (or inferred by brownfield detection), pre-fill the 12
principles from this matrix (A/B/C = the option in `constitution-principles.md`; the user still
picks in Step 3). Architecture is always the Level 2 choice; `—` = skip (no database).

| Principle | A App | B Site | C Client | D Library | E Infra | F Game | G Ext. | H Data/ML | I Embedded | J Systems | K Platform |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 Testing | A/B | C | B | A | B | C | C | C (H4/H5: B) | C | A | B |
| 2 Linting | B | B | B | A | A | B | B | C | A | A | B |
| 4 Dependencies | B | B | B | A/B | A | C | A | C | A | A | B |
| 5 Git workflow | B | A | B | B | A | B | B | A | A | B | B |
| 6 Documentation | B | B | B | A | C | B | A | B | A | A | B |
| 7 Error handling | A | C | A | B | C | A | A | C | A | A | B |
| 8 Performance | B | C | B | B | A | A | A | C | A | A | B |
| 9 Code review | A/B | C | A | A | B | B | A | C | A | A | A |
| 10 Database | A (if DB) | — | — | — | — | — | — | A (H4) | — | — | — (vendor) |
| 11 Config/secrets | B | C | B | A | A | C | A | C | B | A | B |
| 12 Dev toolchain | B | B | C | B | C | C | B | A | C | C | B |

**Trait rules** (Level 1.5 / detected) — applied after the matrix, the stricter option wins:
safety-critical → Testing A, Review A, Documentation A, Error handling A, and suggest
`compliance: baseline` · health / finance / AI Act high-risk → Review A, Config A, suggest
`compliance: baseline` · personal data or multi-tenant SaaS → suggest `compliance: baseline`
· local-first → Database notes the sync model (CRDT / replication) · on-prem → versioned releases
and upgrade paths in Git workflow · prototype → Testing C and Documentation C allowed, say what
graduates it · modernization → characterisation tests first (Testing B), a strangler-fig target
on A2, and an ADR for the cut-over plan.

The why, per purpose (say it beside each ⭐): **A** reliability for real users (A5: evals are the
tests) · **B** no business logic, ship content fast · **C** crashes and store reviews are costly ·
**D** the public API is the product (D4: immutable once deployed) · **E** CLI responsiveness, static binaries · **F** frame budget,
playtesting dominates · **G** privileged APIs on every page · **H** exploration first, reproducibility
second · **I** no hotfix once flashed, hard memory limits · **J** memory safety, fuzzing, performance as a gate · **K** the vendor's limits and release cadence decide.

Present these as a summary table to the user:

```
  Based on your choices (Purpose: [name], Architecture: [name]), here are
  the recommended defaults for each principle:

  | Principle | Recommended | Why |
  |-----------|-------------|-----|
  | Testing   | ⭐ [option] | [reason] |
  | Linting   | ⭐ [option] | [reason] |
  | ...       |             |      |

```

Then proceed to Step 3 to let the user confirm or adjust each principle.

---

### Step 2d: Load the principles reference (both modes)

```
LOAD spec-kit/references/constitution-principles.md

This reference defines 12 principles, each with 3 options (A/B/C).
Each option has a rule, pros, and cons.

FOR each principle:
  READ the 3 options
  IF MODE == brownfield:
    SELECT the option that best matches detected project artifacts
    TAG it with ⭐ "detected"
  IF MODE == greenfield:
    USE the pre-filled mapping from Step 2c
    TAG the recommended option with ⭐ "recommended for [purpose]"
```

### Step 3: Present each principle with choice

**For each principle, present the 3 options as a formatted table.**
Always show pros and cons. Never skip the choice — even if a detected default
exists, the user may disagree. **Rigor lean**: present only Testing, Architecture, Git workflow
and Config / secrets; list the other 8 with their defaults in one table and open any the user
names — the rest are recorded as "default (lean)".

```
PRESENT for each principle:

  ## Principle N: [Name]

  | Option | Rule | Pros | Cons |
  |--------|------|------|------|
  | ⭐ A — [Name] *(detected)* | ... | ... | ... |
  | B — [Name] | ... | ... | ... |
  | C — [Name] | ... | ... | ... |

  The ⭐ marker means this was auto-detected from your project files.
  Pick A, B, or C (or type 'skip' to use detected default).

  USER picks: [A | B | C | skip]
  RECORD the chosen option
  ASK: "Any notes or rationale for this choice?" → RECORD as rationale
```

In greenfield mode, after showing the 3 options, include the purpose-based
recommendation from Step 2c instead of a generic guiding question:

```
  ⭐ This option is recommended for [purpose name] projects because
     [reason from Step 2c mapping].
  You can still pick A, B, or C — this is a recommendation, not a requirement.

  USER picks: [A | B | C]
  RECORD the chosen option
  ASK: "Any notes or rationale for this choice?" → RECORD as rationale
```

### Step 4: Handle principle exceptions

```
IF project has no database (no DB config, no ORM, no schema files):
  SKIP Principle 10 (Database & Schema)
  NOTE: "Skipping Database principle — no database detected."
```

### Step 5: Write the constitution

```
COPY spec-kit/templates/constitution-template.md → specs/constitution.md

ENGINEERING GUIDELINES (the template section) from stack + Level 2 option + rigor:
  lean      one line — "framework defaults; <formatter> on save"
  standard  layout and boundaries of the option (e.g. A2: modules own their data, no
            cross-module tables), the lint / format config to add, the testing shape of the
            purpose (A integration + Testcontainers · D unit + property · A5 evals · H4 data
            tests · G e2e in the host), coverage on changed core logic; each MUST → a P-item
            in specs/merge-checklist.md (create from the template) — WAIT
  strict    standard + architecture tests (ArchUnitNET / dependency-cruiser / import-linter),
            coverage ≥ 80 %, mutation testing optional

FILL each section with:
  - Chosen option letter and name
  - Full rule text from the reference
  - Recorded rationale
  - Rejected alternatives table with reasons

IF MODE == monorepo:
  FILL the Projects table at the top with each sub-project's:
    - Name, Purpose, Language/Framework, Architecture option
  SHARED principles apply to the PRIMARY sub-project
  NOTE per principle: "Applies to all sub-projects. Project-specific
    variations documented in the Projects section."

ELSE (single project):
  INCLUDE in the Tech Stack section:
    - Detected language/framework (brownfield) or "New project — TBD" (greenfield)
    - Test framework, CI, package manager
```

### Step 6: Version management
- **MAJOR** (1.x.x → 2.0.0): Backward-incompatible governance changes
- **MINOR** (x.1.x → x.2.0): New principles
- **PATCH** (x.x.1 → x.x.2): Clarifications


### Step 7: Project documents — scale, conventions, AGENTS.md

The constitution decides the rules; this step decides which living documents the project keeps
(document roles: ADR = why · design doc = how it works now · epic = what, in what order).

```
WRITE rigor: <lean|standard|strict>; lean + Principle 5 = A → blocked_branches: none (trunk).
SCALE follows Level 0 (hobby / indie / small team → small; platform / regulated → platform);
ASK only when Level 0 left it unclear (recommendation first):
  small     — one deployable, one team: no adr_dir / design_dir / epics_dir; the plan's
              Current Design is the design; ADRs only if a close finds one worth it
  ⭐ platform — several deployables, modules or teams (brownfield with > 1 project ⇒ platform):
              adr_dir docs/adr · design_dir docs/design · epics_dir specs/epics (+ epics_index on)
              · runbooks_dir / changelog only if they exist or the user wants them
RECORD in specs/git-conventions.md (create from the template; uncomment the chosen keys only).
AGENTS.md: missing → create from spec-kit/templates/AGENTS-template.md (stack + build commands
  from detection); exists (also CLAUDE.md) → patch only the <!-- SPECKIT --> block, WAIT.
EXISTING ADR / design dirs (brownfield) → point the keys at them; never move or rename files.
platform → NEXT: spec-kit-design map — system.md, the module split, module docs and the
  initial / retroactive ADRs (greenfield: target design + ADRs for the Level 2 / Level 3 picks).
```

### MCP state sync (optional, when MCP server is configured)

After writing the file and before committing, confirm it with the project-level
tool (the server checks that specs/constitution.md exists; it stores nothing):

```text
CALL mcp_spec_kit_project_set_constitution(status="present", principles='{"key": "value", ...}')
# principles is optional — echoed back after JSON validation
```

### Commit

The constitution is project-level: commit directly per `spec-kit/references/commits.md` — `spec(phase-0): constitution for [PROJECT]`.

## Completion
- Report: "Constitution ratified with [N] principles."
- Report mode: brownfield, free-text, or wizard (greenfield)
- If free-text mode: Show which purpose/architecture/tech were inferred from user's description
- List all chosen options (A/B/C per principle)
- List any principles skipped with reason
- Report the scale and the keys written; platform → propose `spec-kit design map` (then `spec-kit-specify`); small → propose `spec-kit-specify`.


## Common Pitfalls
1. **Skipping the choice dialog**: Always present ALL 3 options with pros/cons.
   The user needs to understand tradeoffs to make an informed decision.
2. **Burying detected defaults**: In brownfield mode, show ⭐ clearly but let the
   user override. Detection is guidance, not dictation.
3. **Assuming all 12 principles apply**: Skip Database principle for stateless
   projects. Skip Code Review for solo projects (but mentioning it is still useful).
4. **Overwriting an existing constitution**: Always check first. Constitution is
   one-time setup. If the user wants to amend, offer to add principles with
   version bump.

## Prerequisite Enforcement
**No prerequisites** — this is Phase 0.
