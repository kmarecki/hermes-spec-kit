---
name: spec-kit-constitution
description: Load when the user says 'spec-kit constitution', 'speckit constitution', 'spec-kit principles', 'speckit principles', "create constitution", "create project principles", or "set up project principles" — Phase 0 project setup. Three modes: brownfield (auto-detect from existing code), free-text (describe your project in a sentence, agent maps to purpose/arch/principles), and guided wizard (3-level decision tree with 9 purposes × 25 architecture options).
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
   (9 purposes × 25 architecture options). User picks at each level.
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

### Step 1: Detect mode — brownfield vs greenfield

```
SCAN project root for these files to identify the tech stack:

LOAD the brownfield file detection tables from `spec-kit/references/constitution-tables.md`

  IF any project files detected:
    MODE = brownfield
    COMPILE a detection summary:
      "Detected [language] project with [framework].
       Test: [test_framework]. CI: [ci_platform]. DB: [database].
       Linting: [linter]. Formatting: [formatter]."

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

### Step 2a: Free-Text — Description to Constitution

**Only for MODE=greenfield AND input_mode=free-text.**

The user provides a natural-language project description. The agent maps it
to a purpose (A-I), architecture (A1-I3), technology choices, and principle
defaults automatically. The user reviews the inferred choices and may accept
or adjust any of them.

```text
1. PROMPT: "Describe your project in a few sentences — what are you building,
   what platform/target, team size, and any key constraints?"

2. AWAIT user input (e.g. "React Native mobile app for fitness tracking,
   small two-person team, want to ship quickly, no backend — Firebase")

3. INFER from the description:

   MAP the description to a purpose code (A-I):
     - Look for keywords: "mobile app", "iOS", "Android", "desktop"
       → Purpose C (Native/Desktop Client)
     - "web app", "SaaS", "API", "dashboard", "full-stack"
       → Purpose A (User-Facing Application)
     - "library", "package", "SDK", "npm", "PyPI"
       → Purpose D (Library/SDK)
     - "CLI", "tool", "script", "pipeline", "Terraform"
       → Purpose E (Infrastructure/CLI/DevOps)
     - "game", "Unity", "Unreal", "Godot"
       → Purpose F (Game)
     - "extension", "browser add-on", "Chrome extension"
       → Purpose G (Browser Extension)
     - "notebook", "research", "analysis", "Jupyter"
       → Purpose H (Research/Notebook)
     - "firmware", "embedded", "IoT", "Arduino", "ESP32"
       → Purpose I (IoT/Embedded)
     - "portfolio", "blog", "landing page", "marketing site"
       → Purpose B (Content Site/Marketing)
     - If ambiguous: infer the closest match and note the uncertainty

   MAP architecture from implied stack:
     - "React Native", "Flutter", "Tauri" → C2 (Cross-Platform)
     - "iOS app (Swift)", "Android (Kotlin)" → C1 (Native)
     - "Electron", "PWA", "Capacitor" → C3 (Web Wrapper)
     - "Firebase", "Vercel", "Cloudflare" → A4 (Serverless)
     - "Unity", "Unreal", "Godot" → F1 (Engine-Centric)
     - "Rails", "Django", "Laravel" → A1 (Monolith)
     - "microservices", "distributed" → A3 (Microservices)
     - "Arduino", "sensor firmware" → I3 (MicroPython/Arduino)
     - "bare-metal", "RTOS", "FreeRTOS" → I1 (Bare-Metal/RTOS)
     - "single notebook", "analysis only" → H1 (Single Notebook)
     - "static site", "SSG" → B1 (Static Site Generator)
     - Default: use the most common architecture for the detected purpose

   MAP tech choices from explicit mentions:
     - "React Native" → TypeScript, React Native framework
     - "Flutter" → Dart, Flutter
     - "Firebase" → BaaS for auth/db
     - Extract any explicit language/framework mentions

   MAP principle defaults from inferred purpose using the Step 2c
   (Purpose-to-Principle) mapping table below.

4. PRESENT the inferred result as a table:

   | Inference | Value | Correct? |
   |-----------|-------|----------|
   | Purpose | C — Native / Desktop Client | ✅ / 🔄 |
   | Architecture | C2 — Cross-Platform (Flutter/React Native) | ✅ / 🔄 |
   | Language | TypeScript (React Native) | ✅ / 🔄 |
   | Testing | B — Pragmatic TDD (recommended for native apps) | ✅ / 🔄 |

   ASK: "Does this look right? You can say 'all good' to proceed with these
         defaults, or correct specific items. I'll then walk through the
         12 principles to confirm or adjust."

5. IF user says "all good" or confirms:
   PROCEED to Step 2c (Load principles reference) then Step 3

6. IF user corrects specific items:
   UPDATE the inferred values
   RECORD corrections as user rationale
   PROCEED to Step 3

7. IF user says "I want the wizard instead":
   SET input_mode = wizard
   ROUTE to Step 2b (Wizard mode below)

8. IF the description is too vague to map confidently:
   NOTE: "Description is quite broad. I'll use [purpose] as a starting point,
          but let me know if that doesn't fit."
   PROCEED with best-guess inference
```

**Inference examples:**

| User says | Inferred purpose | Inferred arch | Principle defaults |
|-----------|-----------------|---------------|-------------------|
| "iOS app with SwiftUI for habit tracking, solo dev" | C — Native | C1 — Native Platform | C defaults, Testing C (solo dev) |
| "React Native mobile app for fitness, small team, Firebase" | C — Native | C2 — Cross-Platform | C defaults, Testing B |
| "Django REST API for a SaaS dashboard" | A — User-Facing | A1 — Monolith | A defaults |
| "CLI tool in Go for managing Kubernetes clusters" | E — Infra/CLI | E1 — Single Binary | E defaults |
| "Three.js browser game, WebGL, casual" | F — Game | F3 — Web/Retro | F defaults |
| "Jupyter notebook analyzing stock market data" | H — Research | H1 — Single Notebook | H defaults |

---

### Step 2b: Wizard — 3-Level Decision Tree

**Only for MODE=greenfield AND (input_mode=wizard OR no input_mode set yet).**

Guide the user through three levels of decisions. Each level narrows the
options and pre-fills recommended defaults for the next level. Use the
brownfield detection examples table from `spec-kit/references/constitution-tables.md` for recommended defaults once
language + framework are chosen.

---

#### Level 1 — Highest-Level Purpose

Ask the user: *"What is this project's primary purpose?"*

Present these 9 options with their tradeoffs:

| Option | Type | Examples | Testing impact | Arch impact | Docs impact | Deps impact |
|--------|------|----------|---------------|-------------|-------------|-------------|
| **A — User-Facing Application** | Web/mobile API, frontend, full-stack app | SaaS, e-commerce, social app, dashboard, CMS | Needs integration + F2E tests. TDD pays off. | Architecture matters — will need to scale. | API docs, user docs, setup guide critical. | Framework deps expected (React, Django, etc.) |
| **B — Content Site / Marketing** | Static or lightly dynamic, no auth/DB | Portfolio, landing page, blog, documentation site, marketing site | Minimal. Visual checks + broken link checker. No business logic to test. | Simple — SSG, template-driven, or plain HTML/CSS. No backend needed. | Content IS the documentation. Readme for build/deploy. | SSG framework or plain HTML/CSS. Zero server deps. |
| **C — Native / Desktop Client** | Standalone client app, no backend to architect | iOS app, Android app, macOS app, Windows app, Linux desktop app, Electron app, Tauri app, Qt app | UI/snapshot tests, integration tests. Manual QA for visual polish. | Client-side architecture (MVC, MVVM, Redux, Composable). Platform SDK native or cross-platform framework. | User-facing help, API docs for local features, store listing. | Platform SDK, UI framework. Cross-platform framework for shared code. |
| **D — Library / SDK / Package** | Reusable code for other developers | npm package, PyPI lib, Go module, crate | Exhaustive unit tests essential. API surface must be tested. | Clean public API, minimal internal coupling. | API docs, README, examples, changelog mandatory. | Zero or minimal deps to avoid transitive bloat. |
| **E — Infrastructure / CLI / DevOps** | Automation, ops tools, platform | CLI tool, Terraform module, CI pipeline, daemon | Integration tests with real infra. Manual testing common. | Simple, composable. No over-engineering. | README + --help. Code that IS the documentation. | Minimal. Static binaries preferred. |
| **F — Game** | Interactive application with game loop, rendering, input | 2D platformer, 3D FPS, puzzle game, RPG, mobile game, WebGL game | Unit tests for game logic. Visual/playtest testing critical. Integration tests for netcode. | ECS, scene graph, component-based. Game loop, render pipeline, physics. | Design doc, mechanics doc, modding API docs. README + gameplay guide. | Engine dependency (Unity, Unreal, Godot, Bevy). Graphics, audio, physics libs. |
| **G — Browser Extension** | Browser add-on modifying/extending the browser | Chrome extension, Firefox add-on, Safari extension, Edge extension | Manual browser testing. Puppeteer/Playwright for F2E. | Content scripts, service worker (MV3), popup page, options page. Cross-browser API abstraction. | Store listing, permissions guide, feature docs, privacy policy. | Minimal — browser APIs. Polyfill for cross-browser support (webextension-polyfill). |
| **H — Research / Notebook** | Data exploration, academic research, one-off analysis | Jupyter notebook, R Markdown, Quarto doc, MATLAB script, experimental Python script | Minimal to none. Visual inspection of outputs. Assertions in cells. | Single notebook or notebook + reusable scripts. No deployment. No production infra. | Notebook cell comments, README with reproduction steps. Dataset provenance. | Permissive — pandas, numpy, matplotlib, torch, scipy, tidyverse. Whatever is needed. |
| **I — IoT / Embedded** | Firmware, device software, real-time systems | Sensor firmware, motor controller, smart home device, drone flight controller, RTOS application | Hardware-in-the-loop testing. Simulation for CI. Manual device testing essential. | HAL, RTOS tasks, driver layer. Memory-constrained. Real-time constraints. | Pinout docs, protocol specs, register maps. Datasheet references. | Minimal or zero std. Vendor SDKs. No dynamic allocation. Cross-compilation toolchain. |

```
ASK: "What kind of project are you building?"
RECORD: purpose = [A | B | C | D | E | F | G | H | I]
NOTE: purpose determines the weight of each principle below.
```

After the user picks their purpose, ask about monorepo:

```text
ASK: "Is this a multi-project monorepo with different purposes?
      (e.g., a repo containing a web app + mobile app + shared library)
      [yes | no]"

IF yes:
  NOTE: "Multi-project monorepo detected. The constitution will define
         each sub-project separately under a 'Projects' section."

  ASK: "How many sub-projects does this monorepo contain?"
  RECORD: sub_project_count = [N]

  FOR each sub-project (1 to N):
    ASK: "Sub-project [N] name? (e.g., 'frontend', 'mobile-app', 'shared-lib')"
    RECORD: sub_project_name = [name]

    RUN Levels 1-3 for this sub-project independently:
      ASK its purpose (can differ per sub-project)
      ASK its architecture (can differ)
      ASK its tech choices

  AFTER all sub-projects defined, the constitution will contain a
  'Projects' table at the top, and shared principles will be determined
  by the PRIMARY sub-project (the largest or most important one).

  IF monorepo:
    MODE = monorepo
    PRIMARY purpose = [chosen by user]

---

#### Level 2 — Architecture Approach

Based on the chosen purpose, present the architecture options:

LOAD the Level 2 architecture tables for each purpose from `spec-kit/references/constitution-tables.md`

```
ASK: "Given your purpose [A|B|C|D|E|F|G|H|I], which architecture approach fits?"
RECORD: architecture = [A1|A2|A3|A4 | B1|B2|B3 | C1|C2|C3 | D1|D2|D3 | E1|E2|E3|E4 | F1|F2|F3 | G1|G2|G3 | H1|H2|H3 | I1|I2|I3]
```

---

#### Level 3 — Technology Choices

Based on purpose + architecture, guide the user through technical choices.
For each choice, present 3 options using the project-type-aware defaults
from the tables below.

LOAD the Level 3 technology choice brackets for each purpose from `spec-kit/references/constitution-tables.md`

For each bracket, present the specific language options as follows:

```
  | Option | Language | Framework suggestions | Pros | Cons |
  |--------|----------|----------------------|------|------|
  | A | [lang] | [framework list] | [pros] | [cons] |
  | B | [lang] | [framework list] | [pros] | [cons] |
  | C | [lang] | [framework list] | [pros] | [cons] |

  USER picks: [A | B | C]
```

After the user picks language + framework, use the **Brownfield Detection
Examples table** from `spec-kit/references/constitution-tables.md` to find the matching row
and pre-fill recommended defaults for the remaining principles.

If the user's exact combination isn't in the table, infer from the closest
match:
- Same language + similar framework → use that row
- Same purpose category → use generic defaults for that purpose

---

#### Step 2c: Default Mapping — Purpose to Principle Weights

Once purpose + architecture are chosen, map them to recommended defaults
for the 12 principles. These are weighted suggestions — the user still
picks A/B/C in Step 3.

```
PURPOSE = A (User-Facing App):
  Testing → A or B (TDD important for reliability)
  Linting → B (Pragmatic — balance quality and speed)
  Architecture → user's choice from Level 2
  Dependencies → B (Curated — need frameworks)
  Git Workflow → B (Feature branches — standard)
  Documentation → B (Critical-only — API docs + setup)
  Error Handling → A (Defensive — user-facing app)
  Performance → B (Profile-then-optimize)
  Code Review → A or B (Strict or Risk-based)
  Database → A (Migration-first — if using DB)
  Config/Secrets → B (Environment-based)
  Dev Toolchain → B (Standard toolchain)

PURPOSE = B (Content Site / Marketing):
  Testing → C (Test-After — no business logic to test, visual QA only)
  Linting → B (Pragmatic — template code needs flexibility)
  Architecture → user's choice from Level 2
  Dependencies → B (Curated — SSG framework + maybe CMS client)
  Git Workflow → A (Trunk-based — content changes should ship fast)
  Documentation → B (Critical-only — build/deploy instructions + content guide)
  Error Handling → C (Minimal — static sites have no runtime errors)
  Performance → C (Ignore-until-painful — SSG output is inherently fast)
  Code Review → C (Post-merge — content edits shouldn't block)
  Database → SKIP (no database on content sites)
  Config/Secrets → C (Config-in-repo — build config is part of the source)
  Dev Toolchain → B (Standard toolchain — SSG, asset pipeline, CDN deploy)

PURPOSE = D (Library / SDK):
  Testing → A (Strict TDD — API surface must be tested)
  Linting → A (Strict — public API consistency)
  Architecture → user's choice from Level 2
  Dependencies → A or B (Minimal or Curated)
  Git Workflow → B (Feature branches)
  Documentation → A (Exhaustive — API docs mandatory)
  Error Handling → B (Contract-based — surface errors cleanly)
  Performance → B (Profile-then-optimize)
  Code Review → A (Strict — every change reviewed)
  Database → SKIP (libraries shouldn't dictate storage)
  Config/Secrets → A (Strict — secrets never in lib)
  Dev Toolchain → B (Standard toolchain)

PURPOSE = E (Infrastructure / CLI / DevOps):
  Testing → B (Pragmatic — integration-heavy)
  Linting → A (Strict — CLI UX consistency)
  Architecture → user's choice from Level 2
  Dependencies → A (Minimal — static binaries)
  Git Workflow → A (Trunk-based — fast iteration)
  Documentation → C (Code-as-docs — help text + README)
  Error Handling → C (Minimal — propagate, top-level catch)
  Performance → A (Optimize-first — CLI responsiveness)
  Code Review → B (Risk-based — config changes vs engine)
  Database → SKIP (infra tools shouldn't depend on DB)
  Config/Secrets → A (Strict — env + config files)
  Dev Toolchain → C (Full DX — automation matters)

PURPOSE = F (Game):
  Testing → C (Test-After — playtesting and visual QA dominant)
  Linting → B (Pragmatic — engine code needs flexibility)
  Architecture → user's choice from Level 2
  Dependencies → C (Permissive — engines, assets, middleware, audio libs)
  Git Workflow → B (Feature branches — asset changes need review)
  Documentation → B (Critical-only — design doc + mechanics + API)
  Error Handling → A (Defensive — game crashes ruin UX)
  Performance → A (Optimize-first — frame budget is hard limit)
  Code Review → B (Risk-based — gameplay logic vs asset changes)
  Database → SKIP (save systems are engine-managed or custom binary)
  Config/Secrets → C (Config-in-repo — game config is part of the game)
  Dev Toolchain → C (Full DX — asset pipeline, build chain, packaging)

PURPOSE = I (IoT / Embedded):
  Testing → C (Test-After — hardware testing dominates)
  Linting → A (Strict — firmware bugs are expensive, no OTA)
  Architecture → user's choice from Level 2
  Dependencies → A (Minimal — no stdlib, no heap, vendor SDK only)
  Git Workflow → A (Trunk-based — most constrained, fast iteration)
  Documentation → A (Exhaustive — pinouts, registers, protocols)
  Error Handling → A (Defensive — watchdog, brownout, fail-safe)
  Performance → A (Optimize-first — memory and cycles are hard limits)
  Code Review → A (Strict — hardware damage risk, no hotfix possible)
  Database → SKIP (no database on embedded devices)
  Config/Secrets → B (Environment-based — compile-time flags, EEPROM)
  Dev Toolchain → C (Full DX — cross-compiler, flashing, logic analyzer)

PURPOSE = C (Native / Desktop Client):
  Testing → B (Pragmatic — UI tests for critical paths, manual QA for visual)
  Linting → B (Pragmatic — platform SDKs have their own conventions)
  Architecture → user's choice from Level 2
  Dependencies → B (Curated — platform SDK + UI framework, minimize transitive)
  Git Workflow → B (Feature branches — release management matters)
  Documentation → B (Critical-only — user-facing help + setup + store listing)
  Error Handling → A (Defensive — app crashes cause user frustration)
  Performance → B (Profile-then-optimize — startup time, frame drops, memory)
  Code Review → A (Strict — app store review failures are costly)
  Database → SKIP (local storage is platform-managed: Core Data, Room, SharedPrefs)
  Config/Secrets → B (Environment-based — build flavors, feature flags, remote config)
  Dev Toolchain → C (Full DX — build pipeline, code signing, app store deploy)

PURPOSE = G (Browser Extension):
  Testing → C (Test-After — manual browser testing dominates)
  Linting → B (Pragmatic — content scripts need browser API flexibility)
  Architecture → user's choice from Level 2
  Dependencies → A (Minimal — browser APIs preferred, avoid bloating extension)
  Git Workflow → B (Feature branches — store release cycles)
  Documentation → A (Exhaustive — store listing, permissions, privacy policy mandatory)
  Error Handling → A (Defensive — broken extension in user's browser is invisible failure)
  Performance → A (Optimize-first — content script perf impacts every page user visits)
  Code Review → A (Strict — privileged API misuse can cause account/data theft)
  Database → SKIP (storage API is browser-provided)
  Config/Secrets → A (Strict — API keys, tokens must never be in extension code)
  Dev Toolchain → B (Standard toolchain — build, zip, upload to stores)

PURPOSE = H (Research / Notebook):
  Testing → C (Test-After — visual inspection of outputs, assertions in cells)
  Linting → C (Minimal — notebooks are exploratory, not production code)
  Architecture → user's choice from Level 2
  Dependencies → C (Permissive — use whatever lib the analysis needs)
  Git Workflow → A (Trunk-based — research is fast iteration, no release branches)
  Documentation → B (Critical-only — reproduction steps + dataset provenance)
  Error Handling → C (Minimal — errors are part of exploration, top-level catch)
  Performance → C (Ignore-until-painful — correct analysis first, optimize if needed)
  Code Review → C (Post-merge — notebooks are exploratory, not approval-gated)
  Database → SKIP (research uses files, not databases)
  Config/Secrets → C (Config-in-repo — dataset paths, API keys in .env.example)
  Dev Toolchain → A (Minimal — just a notebook runtime, no build pipeline)
```

Present these as a summary table to the user:

```
  Based on your choices (Purpose: [name], Architecture: [name]), here are
  the recommended defaults for each principle:

  | Principle | Recommended | Why |
  |-----------|-------------|-----|
  | Testing   | ⭐ [option] | [reason] |
  | Linting   | ⭐ [option] | [reason] |
  | ...       |             |      |

  Say 'bugfix [feature]' to start a new bugfix round.
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
exists, the user may disagree.

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

### Append to history.md and Commit

Follow the **Shared Commit Procedure** in `spec-kit/references/preflight.md`:
- Phase: Phase 0 — Constitution
- Artifact: `specs/constitution.md`
- Scope: `specs/constitution.md`
- Message: `"spec(phase-0): constitution for [PROJECT]"`

## Completion
- Report: "Constitution ratified with [N] principles."
- Report mode: brownfield, free-text, or wizard (greenfield)
- If free-text mode: Show which purpose/architecture/tech were inferred from user's description
- List all chosen options (A/B/C per principle)
- List any principles skipped with reason
- Propose: Run `spec-kit-specify` to create the first feature specification.

LOAD the Brownfield Detection Examples table from `spec-kit/references/constitution-tables.md`

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
