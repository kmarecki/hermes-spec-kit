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

  ┌──────────────────────────────────────────────────────────────┐
  │                  LANGUAGE / FRAMEWORK DETECTION              │
  ├──────────────────────────────────────────────────────────────┤
  │ package.json       → JavaScript/TypeScript                   │
  │                     Check for: react, vue, next, nuxt,       │
  │                     svelte, solid, angular, express, fastify, │
  │                     nest, remix, astro, qwik, htmx wrapper   │
  │                     hattip, hono, elysia, adonis             │
  │                                                              │
  │ pyproject.toml     → Python                                  │
  │                     Check for: django, fastapi, flask,       │
  │                     starlette, aiohttp, tornado, litestar,   │
  │                     sanic, asyncpg, sqlalchemy, streamlit    │
  │                                                              │
  │ setup.py /         → Python (legacy setup)                   │
  │ setup.cfg             (fallback if no pyproject.toml)         │
  │                                                              │
  │ requirements.txt   → Python (no build system detected)       │
  │                                                              │
  │ go.mod             → Go + module path                        │
  │                     Check for: gin, echo, fiber, chi,        │
  │                     gorilla/mux, buffalo, connect-go         │
  │                                                              │
  │ Cargo.toml         → Rust                                    │
  │                     Check for: actix, axum, rocket, tide,    │
  │                     warp, leptos, yew, dioxus, tauri         │
  │                                                              │
  │ Gemfile            → Ruby + framework                        │
  │                     Check for: rails, sinatra, roda,         │
  │                     hanami, grape, rack                      │
  │                                                              │
  │ build.gradle /     → Java / Kotlin                           │
  │ build.gradle.kts      Check for: spring, micronaut, quarkus, │
  │                        ktor, jooby, javalin, dropwizard      │
  │                                                              │
  │ pom.xml            → Java (Maven)                            │
  │                     Check for: spring, hibernate, vaadin     │
  │                                                              │
  │ composer.json      → PHP                                     │
  │                     Check for: laravel, symfony, wordpress   │
  │                     (wp-content/), drupal, yii, cake,        │
  │                     codeigniter, phalcon, slim, magento      │
  │                                                              │
  │ *.csproj / *.sln   → C# / .NET                               │
  │                     Check for: aspnet, blazor, maui,         │
  │                     wpf, winforms, webapi, minimal api       │
  │                                                              │
  │ pubspec.yaml       → Dart / Flutter                          │
  │                                                              │
  │ Package.swift      → Swift (SPM) / iOS                       │
  │                     Check for: vapor, hummingbird,           │
  │                     swiftui, uikit                           │
  │                                                              │
  │ mix.exs            → Elixir                                  │
  │                     Check for: phoenix, nervesh, plug       │
  │                                                              │
  │ build.sbt          → Scala                                   │
  │                     Check for: play, http4s, zio-http, akka  │
  │                                                              │
  │ rebar.config /     → Erlang                                  │
  │ mix.exs              Check for: cowboy, ellierman            │
  │                                                              │
  │ deno.json /        → Deno                                    │
  │ deno.jsonc                                                      │
  │                                                              │
  │ bun.lock           → Bun (alongside package.json)            │
  │                                                              │
  │ flake.nix /        → Nix language / NixOS                    │
  │ shell.nix /                                                      │
  │ default.nix                                                      │
  │                                                              │
  │ *.tf               → Terraform / OpenTofu                    │
  │ (any .tf files)                                                │
  │                                                              │
  │ CMakeLists.txt     → C / C++ (CMake)                         │
  │                                                              │
  │ Makefile           → Generic build (C, C++, Go without       │
  │                      go.mod, or custom build system)         │
  │                                                              │
  │ Dockerfile         → Containerized app (any language)        │
  └──────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────┐
  │                    TEST FRAMEWORK DETECTION                  │
  ├──────────────────────────────────────────────────────────────┤
  │ Search for config files AND actual test files:               │
  │                                                              │
  │ jest.config.* /       → Jest (JS/TS)                         │
  │ jest.setup.*                                                    │
  │ vitest.config.*       → Vitest (JS/TS, Vite projects)        │
  │                                                              │
  | .mocharc.* / mocha    → Mocha (JS/TS)                        |
  | .cypress.* / cypress  → Cypress (F2E, JS/TS)                |
  | playwright.config.*   → Playwright (F2E, multi-lang)        |
  |                                                              |
  │ pytest.ini /        → pytest (Python)                        │
  │ pyproject.toml [tool.pytest]                                    │
  │                                                              │
  │ unittest (std lib)  → unittest (Python, fallback)            │
  │                                                              │
  │ *_test.go files     → go test (Go, std lib)                  │
  │                                                              │
  │ Rakefile / spec/    → RSpec (Ruby)                           │
  │                                                              │
  │ minitest            → Minitest (Ruby, Rails default)         │
  │                                                              │
  │ PHPUnit config      → PHPUnit (PHP)                          │
  │ (phpunit.xml*).*                                               │
  │                                                              │
  │ pest.php / Pest     → Pest (PHP, Laravel)                    │
  │                                                              │
  │ *.Test.cs files     → xUnit / NUnit / MSTest (C#)           │
  │ .runsettings                                                    │
  │                                                              │
  │ test_*.dart files   → flutter test (Dart)                    │
  │                                                              │
  │ XCTest /            → XCTest (Swift/iOS)                     │
  │ *_Tests.swift files                                            │
  │                                                              │
  │ ex_unit config      → ExUnit (Elixir)                        │
  │                                                              │
  │ scalatest / specs2  → ScalaTest / specs2 (Scala)             │
  │                                                              │
  │ cargo test exists   → cargo test (Rust, std lib)             │
  └──────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────┐
  │                 LINTING / FORMATTING DETECTION               │
  ├──────────────────────────────────────────────────────────────┤
  │ .eslintrc* /           → ESLint (JS/TS)                      │
  │ eslint.config.*                                                │
  │ .prettierrc*           → Prettier (multi-lang)               │
  │ .biomerc / biome.json  → Biome (JS/TS, ESLint+Prettier alt)  │
  │ .oxlintrc*             → Oxlint (JS/TS, Rust-based)          │
  │ ruff config            → Ruff (Python, successor to flake8)  │
  │ pylintrc / .pylintrc   → Pylint (Python legacy)             │
  │ pyproject.toml          → mypy (type checker), ruff, black   │
  │   [tool.mypy/.ruff/       (modern Python toolchain)          │
  │    .black/.isort]                                             │
  │ .golangci.yml /        → golangci-lint (Go)                  │
  │ .golangci.yaml                                               │
  │ rustfmt / clippy       → rustfmt + clippy (Rust, std tools)  │
  │ .rubocop.yml           → RuboCop (Ruby)                      │
  │ .reek.yml              → Reek (Ruby)                         │
  │ phpcs.xml*             → PHP_CodeSniffer (PHP)               │
  │ phpstan.neon*          → PHPStan (PHP static analysis)       │
  │ .php-cs-fixer.*        → PHP-CS-Fixer (PHP)                 │
  │ .editorconfig          → EditorConfig (basic, multi-lang)    │
  └──────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────┐
  │                      CI/CD DETECTION                         │
  ├──────────────────────────────────────────────────────────────┤
  │ .github/workflows/*   → GitHub Actions                       │
  │ .gitlab-ci.yml        → GitLab CI/CD                         │
  │ Jenkinsfile           → Jenkins                               │
  │ .circleci/config.yml  → CircleCI                              │
  │ .travis.yml           → Travis CI                             │
  │ azure-pipelines.yml   → Azure DevOps Pipelines               │
  │ bitbucket-pipelines   → Bitbucket Pipelines                  │
  │                       → YAML in bitbucket-pipelines.yml       │
  │ buildkite             → Buildkite                             │
  │                       → .buildkite/pipeline.yml              │
  │ .drone.yml            → Drone CI                              │
  │ .woodpecker.yml       → Woodpecker CI                         │
  │ cloudbuild.yaml       → Google Cloud Build                   │
  │ buildspec.yml         → AWS CodeBuild                        │
  │ codeship-*.yml        → CodeShip                              │
  │ appveyor.yml          → AppVeyor                              │
  │ wercker.yml           → Wercker                               │
  └──────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────┐
  │                   DATABASE / STORAGE DETECTION               │
  ├──────────────────────────────────────────────────────────────┤
  │ Search for ORM configs, migration dirs, schema files:        │
  │                                                              │
  │ migrations/ directory  → Has database migrations             │
  │ Prisma schema          → Prisma (JS/TS)                      │
  │ (schema.prisma)                                               │
  │ Alembic config         → Alembic (Python, SQLAlchemy)        │
  │ (alembic.ini)                                                 │
  │ Django migrations      → Django ORM (Python)                 │
  │ (*/migrations/*.py)                                           │
  │ Entity Framework       → EF Core (C#)                        │
  │ (Migrations/)                                                  │
  │ Flyway / Liquibase     → Flyway/Liquibase (Java)             │
  │ configs                                                       │
  │ Sequelize configs      → Sequelize (JS/TS)                   │
  │ TypeORM config         → TypeORM (JS/TS)                     │
  │ Drizzle config         → Drizzle (JS/TS)                     │
  │ ActiveRecord           → ActiveRecord (Rails/Ruby)           │
  │ (db/migrate/)                                                 │
  │ Ecto migrations        → Ecto (Elixir/Phoenix)               │
  │ (priv/repo/migrations/)                                        │
  │ Diesel / SeaORM        → Diesel/SeaORM (Rust)                │
  │ Hasura                 → Hasura metadata                     │
  │ (metadata/)                                                   │
  │ sqlite (file)          → SQLite (embedded)                   │
  │ .db / .sqlite files                                            │
  │                                                              │
  │ IF NO database-related files found:                          │
  │   mark as "stateless/no database"                            │
  └──────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────┐
  │                  DEPLOYMENT / INFRA DETECTION                │
  ├──────────────────────────────────────────────────────────────┤
  │ Dockerfile             → Docker container                    │
  │ docker-compose.yml     → Docker Compose (multi-container)    │
  │ k8s/ / *.k8s.yaml      → Kubernetes manifests               │
  │ helm/ / Chart.yaml     → Helm charts                         │
  │ serverless.yml         → Serverless Framework                │
  │ cdk.json / cdk*.ts     → AWS CDK                             │
  │ Pulumi.yaml            → Pulumi                              │
  │ Terraform files        → Terraform / OpenTofu               │
  │ (.tf, .tfvars)                                                │
  │ Ansible playbooks      → Ansible                             │
  │ (*.yml in ansible/ or playbooks/)                             │
  │ Nomad file             → Nomad                               │
  │ (*.nomad)                                                    │
  └──────────────────────────────────────────────────────────────┘

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
brownfield detection examples table (below) for recommended defaults once
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

**If purpose = A (User-Facing App):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **A1** | Monolith | Single deployable, shared everything. MVC or similar. | Fastest to build, simple deploy, single codebase | Hard to scale team, technology lock-in | MVPs, small teams, prototypes |
| **A2** | Modular Monolith | Bounded contexts in a shared runtime. Clear module boundaries. | Scales to medium teams, can extract services later, good separation | Requires discipline on boundaries | Growing teams, most web apps, medium complexity |
| **A3** | Microservices | Independent services, separate deploys, own data stores. | Independent scaling, team autonomy, technology flexibility | Operational complexity, distributed debugging, data consistency | Large teams, high-scale apps, multiple domains |
| **A4** | Serverless / FaaS | Individual functions deployed on-demand (Lambda, Cloudflare Workers, Vercel Functions, Google Cloud Functions). | Zero infrastructure management, auto-scale, pay-per-execution, fast deploys | Cold starts, execution time limits, vendor lock-in, testing complexity | APIs with variable traffic, event-driven, startups, Jamstack backends |

**If purpose = B (Content Site / Marketing):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **B1** | Static Site Generator | SSG (Astro, Hugo, 11ty, Jekyll, Next.js SSG). Build produces static HTML/CSS/JS. | Fastest possible hosting (CDN), no server costs, best SEO, instant load | No dynamic content without client JS, rebuild on content change | Portfolios, blogs, marketing sites, docs sites |
| **B2** | Headless CMS + SSG | Content managed in headless CMS (Strapi, Sanity, Contentful). SSG fetches at build time. | Non-developers edit content, structured content, revalidation possible | CMS hosting cost, build-time coupling, preview complexity | Team-maintained content sites, multi-author blogs, company sites |
| **B3** | Lightweight Backend | Simple server (Express, Flask, PHP) serving mostly static content with a few dynamic routes. | Easy dynamic features (forms, comments, auth), no SSG build step | Server costs, maintenance overhead, slower than CDN-hosted static | Sites needing a few dynamic features without full web-app complexity |

**If purpose = C (Native / Desktop Client):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **C1** | Native Platform | Platform-specific SDK (Swift/SwiftUI for iOS/macOS, Kotlin/Jetpack for Android, WinUI/WPF for Windows, GTK/Qt for Linux). | Best performance, full platform API access, native look-and-feel, smallest binary | Write once per platform, higher development cost, separate codebases to maintain | Performance-critical apps, platform-specific features, established products |
| **C2** | Cross-Platform Framework | Shared codebase (Flutter, React Native, Tauri, .NET MAUI, Kotlin Multiplatform). | Single codebase, faster development, shared business logic | Abstraction leaks, platform limitations, larger binary, debugging complexity | Most mobile/desktop apps, startups, resource-constrained teams |
| **C3** | Web Wrapper | Web tech packaged as client (Electron, PWA, Capacitor, Cordova, Tauri with web frontend). | Web skills transfer, fastest prototyping, easy updates, large ecosystem | Performance overhead, non-native UX, larger binary, limited platform API access | Internal tools, MVPs, cross-platform with limited native needs |

**If purpose = D (Library / SDK):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **D1** | Zero-Dependency | Stdlib only. Minimal API surface. No runtime deps. | Maximum compatibility, no supply chain risk, builds instantly | More custom code, reinventing wheels | Core libraries, security-sensitive, polyfills |
| **D2** | Curated | Few well-chosen deps with justification. Pin exact versions. | Faster delivery, standard patterns, community leverage | Transitive bloat, upgrade burden | Most libraries, SDKs for popular platforms |
| **D3** | Umbrella | Multi-package monorepo. Independent versioning per sub-package. | Clean separation, consumers pick what they need | Build complexity, tooling overhead, version coordination | Large SDKs (like AWS, Google Cloud clients) |

**If purpose = E (Infrastructure / CLI / DevOps):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **E1** | Single Binary | Everything compiled into one binary. No runtime deps. | Zero friction for users, simple distribution, easy CI | Monolithic code, feature flag complexity | CLIs, single-purpose tools, Terraform providers |
| **E2** | Multi-Binary | Separate binaries sharing common libs. | Independent releases, clear boundaries, composable | Distribution complexity, version coordination | Tool suites (like kubectl + plugins) |
| **E3** | Plugin-Based | Core binary + plugin system. Users extend without forking. | Extensible by community, clean core, pluggable | Plugin API stability burden, discovery UX | Framework-like tools, extensible CLIs |
| **E4** | Script / Declarative / Pipeline | Uncompiled scripts or declarative config (Python, shell, Terraform, Ansible). AI data pipelines (RAG, dataset prep, LLM eval) also fit here. | Fastest to iterate, no build step, easy to read, large ecosystem | No static binary, runtime deps needed, slower execution, harder to distribute | Data pipelines, AI/ML scripts, RAG ingestion, dataset prep, Terraform modules, Ansible playbooks, CI/CD configs |

**If purpose = F (Game):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **F1** | Engine-Centric | Built on existing engine (Unity, Unreal, Godot). Visual scripting + code. | Fastest prototyping, massive asset stores, mature tooling | Engine lock-in, license costs, bloated builds, hard to optimize | Most games, indie to AAA, cross-platform |
| **F2** | Custom Engine | Hand-rolled engine with ECS or scene-graph architecture. | Full control, no license fees, optimized for specific game | Massive upfront investment, no asset pipeline, constant engine work | Unique mechanics, competitive edge, learning exercise |
| **F3** | Web/Retro | Browser-based (WebGL, Canvas, Phaser) or retro-style (pixel art, 8-bit) | Zero install for players, nostalgic appeal, tiny asset sizes | Performance ceilings, limited complex rendering, browser compatibility | Casual games, jam games, mobile web, educational |

**If purpose = G (Browser Extension):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **G1** | Simple / Single-Browser | Single-purpose extension targeting one browser. Minimal architecture: content script + popup. | Fastest to build, minimal code, simple permissions, easy review | No cross-browser reach, limited capabilities, harder to scale features | One-off utilities, site-specific tweaks, internal tools |
| **G2** | Full MV3 | Manifest V3 with service worker, multiple pages (popup, options, side panel), background processing, storage API. | Full extension API access, service worker lifecycle, better security (MV3), can handle complex workflows | MV3 limitations (no background page, alarm-based wake), migration from MV2 complexity | Feature-rich extensions, productivity tools, developer tools |
| **G3** | Cross-Browser | WebExtension API with polyfill (webextension-polyfill). Built for Chrome + Firefox + Safari + Edge. | Maximum reach, single codebase, consistent API, store on all platforms | Polyfill overhead, browser-specific quirks, testing across 4+ browsers, longer review cycles | Public extensions, commercial products, wide-audience tools |

**If purpose = H (Research / Notebook):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **H1** | Single Notebook | One self-contained notebook (Jupyter, R Markdown, Quarto). All code and explanations in one file. | Zero setup, self-contained, easy to share, reproducible cell-by-cell | No reuse, hard to maintain at scale, no module boundaries | Exploratory analysis, teaching, one-off reports, data journalism |
| **H2** | Notebook + Scripts | Notebook for narrative + Python/R scripts for reusable logic. Shared utility modules. | Clean separation of concerns, reusable code, notebook stays readable | More files to manage, import path issues, needs documentation between cells and scripts | Research projects with shared preprocessing, analysis + paper, multi-notebook projects |
| **H3** | Package + Notebooks | Formal Python/R package with tests, notebooks as usage examples. Structured project with src/ layout. | Production-ready, testable, publishable, others can pip install | Significant overhead for research velocity, package management, CI setup | Research that becomes a product, reproducible academic research, team projects |

```
**If purpose = I (IoT / Embedded):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **I1** | Bare-Metal / RTOS | No OS or lightweight RTOS (FreeRTOS, Zephyr, Mbed). Direct hardware access. | Max performance, minimal latency, lowest power, no OS overhead | No memory protection, manual driver work, harder debugging, no standard libs | Sensor nodes, motor controllers, wearables, constrained devices |
| **I2** | Linux-Based Embedded | Runs on Linux (Yocto, Buildroot, Raspberry Pi OS). User-space + kernel modules. | Rich ecosystem, standard tooling, debugging easy, networking built-in | Larger footprint, higher power, boot time, real-time challenges | Smart home hubs, drones, gateways, cameras, robots |
| **I3** | MicroPython / Arduino | High-level firmware framework (Arduino, MicroPython, CircuitPython). Abstraction layer. | Fastest to prototype, huge community, beginner-friendly, extensive libraries | Limited performance, memory overhead, abstraction hides hardware issues | Prototypes, hobbyist, education, rapid IoT development |

ASK: "Given your purpose [A|B|C|D|E|F|G|H|I], which architecture approach fits?"
RECORD: architecture = [A1|A2|A3|A4 | B1|B2|B3 | C1|C2|C3 | D1|D2|D3 | E1|E2|E3|E4 | F1|F2|F3 | G1|G2|G3 | H1|H2|H3 | I1|I2|I3]
```

---

#### Level 3 — Technology Choices

Based on purpose + architecture, guide the user through technical choices.
For each choice, present 3 options using the project-type-aware defaults
from the tables below.

**Technology choice 1: Language and framework**

Present the user with relevant options based on purpose:

```
IF purpose == A (User-Facing App):
  RECOMMEND: web-optimized languages
  BRACKET by architecture:
    A1 (Monolith): Django, Rails, Laravel, Next.js, ASP.NET — batteries-included
    A2 (Modular): FastAPI, Express/Nest, Spring Boot, Phoenix — modular frameworks
    A3 (Microservices): Go, Rust, ASP.NET Minimal API, Fastify — lightweight, fast
    A4 (Serverless): TypeScript (Cloudflare Workers, Vercel Functions),
        Python (Lambda, Google Cloud Functions), Go (Lambda custom runtime),
        Rust (Lambda with wasm or custom runtime) — function-per-route

IF purpose == B (Content Site / Marketing):
  RECOMMEND: SSG-friendly or lightweight backend languages
  BRACKET by architecture:
    B1 (SSG): Astro, Hugo, 11ty, Jekyll, Next.js SSG — zero runtime JS if possible
    B2 (Headless CMS + SSG): Astro + Strapi/Sanity, Next.js + Contentful,
        Gatsby + WordPress headless — framework chosen by CMS ecosystem
    B3 (Lightweight Backend): Express (Node), Flask (Python), PHP (no framework),
        Sinatra (Ruby) — minimal server, mostly static responses

IF purpose == D (Library / SDK):
  RECOMMEND: ecosystem-specific languages
  BRACKET by architecture:
    D1 (Zero-Dep): Go stdlib, Rust no-std, Python stdlib, TypeScript with no deps
    D2 (Curated): Pick target ecosystem (Python, JS, Go, Rust, Java)
    D3 (Umbrella): TypeScript (monorepo with npm workspaces), Rust (workspaces)

IF purpose == E (Infra / CLI):
  RECOMMEND: systems languages
  BRACKET by architecture:
    E1 (Single bin): Go, Rust, Zig, C — compiles to static binary
    E2 (Multi-bin): Go (fast compile), Rust (safe), Python+PyInstaller
    E3 (Plugin): Go (plugin/pkg), Rust (wasm plugins), C (dlopen)
    E4 (Script / Pipeline): Python (langchain, llamaindex, torch, pandas,
        transformers), Shell (bash automation), HCL (Terraform), YAML
        (Ansible, CI/CD), Jupyter notebooks — no compilation, data-driven

IF purpose == F (Game):
  RECOMMEND: engine ecosystem + systems languages
  BRACKET by architecture:
    F1 (Engine-Centric): C# (Unity + script), C++ (Unreal BP+C++),
        GDScript (Godot), Rust (Bevy)
    F2 (Custom Engine): Rust (wgpu, winit, macroquad), C++ (SDL, OpenGL,
        Vulkan), C# (MonoGame, Stride), Zig (cross-compile for consoles)
    F3 (Web/Retro): TypeScript (Phaser, PixiJS, Three.js), Haxe
        (Heaps, OpenFL), Python (Pygame, Arcade), Lua (LÖVE)

IF purpose == I (IoT / Embedded):
  RECOMMEND: constrained languages + cross-compilation
  BRACKET by architecture:
    I1 (Bare-Metal / RTOS): C (de facto standard), C++ (with constraits),
        Rust (no-std, no-alloc), Zig (cross-compile natively)
    I2 (Linux Embedded): C, C++, Python, Rust, Go — whatever Linux supports
    I3 (MicroPython / Arduino): C++ (Arduino), Python (MicroPython,
        CircuitPython), Lua (eLua), JavaScript (Espruino)

IF purpose == C (Native / Desktop Client):
  RECOMMEND: platform SDKs and cross-platform frameworks
  BRACKET by architecture:
    C1 (Native): Swift (iOS/macOS), Kotlin (Android), C# (WinUI/WPF),
        C++ (Qt), Rust (GTK-rs, egui) — platform-specific
    C2 (Cross-Platform): Dart (Flutter), TypeScript (React Native),
        C# (.NET MAUI), Kotlin (KMP), Rust (Tauri) — shared codebase
    C3 (Web Wrapper): TypeScript (Electron, PWA, Capacitor),
        C# (Blazor Hybrid), Dart (Flutter Web) — web-first packaging

IF purpose == G (Browser Extension):
  RECOMMEND: WebExtension APIs and JS/TS ecosystems
  BRACKET by architecture:
    G1 (Simple): TypeScript/JavaScript with vanilla manifest.json,
        plain HTML/CSS for popup — minimal tooling
    G2 (Full MV3): TypeScript with build tool (Vite, WebExtension
        Vite plugin), React/Vue for complex UI, Chrome extensions
        CLI (chrome-ext-cli) — structured project
    G3 (Cross-Browser): TypeScript + webextension-polyfill,
        WXT framework (unified build for all browsers),
        Plasmo framework — multi-store deployment

IF purpose == H (Research / Notebook):
  RECOMMEND: data-science languages and notebook ecosystems
  BRACKET by architecture:
    H1 (Single Notebook): Python (Jupyter, JupyterLab), R (R Markdown,
        Quarto), Julia (Pluto.jl), Observable JS — zero setup
    H2 (Notebook + Scripts): Python + .py modules + Jupyter,
        R + .R scripts + R Markdown, Python + uv/poetry for deps
    H3 (Package + Notebooks): Python (src layout + pytest + notebooks),
        R (package structure + testthat + vignettes), Julia (Pkg +
        Pluto notebooks) — production-ready research
```

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
Examples table** (at the bottom of this skill) to find the matching row
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

**Order is critical: history.md FIRST, then commit.**

1. **Append to history.md**:
   Append entry to `specs/history.md` (create if missing):
   - Phase: Phase 0 — Complete
   - Artifact: `specs/constitution.md`

2. **PRE-COMMIT GUARD**:
   READ `specs/history.md` — confirm the constitution entry is recorded.
   If missing: BLOCK — must append before commit.

3. **Commit**:
   Follow `spec-kit/references/auto-commit.md`:
   - Scope: `specs/constitution.md`
   - Message: `"spec(phase-0): constitution for [PROJECT]"`

## Completion
- Report: "Constitution ratified with [N] principles."
- Report mode: brownfield, free-text, or wizard (greenfield)
- If free-text mode: Show which purpose/architecture/tech were inferred from user's description
- List all chosen options (A/B/C per principle)
- List any principles skipped with reason
- Propose: Run `spec-kit-specify` to create the first feature specification.

## Brownfield Detection Examples

| Language | File(s) | Detect framework by | Likely test framework | Typical CI | Recommended defaults |
|----------|---------|-------------------|----------------------|------------|---------------------|
| **TypeScript** | `package.json` + `next.config.*` | `next` in deps | Vitest/Jest | GitHub Actions | B (TDD), B (Lint), C (Arch), B (Deps), B (Git) |
| **TypeScript** | `package.json` + `vite.config.*` | `vite` + `vue`/`react`/`svelte` in deps | Vitest | GitHub Actions | B (TDD), B (Lint), C (Arch), B (Deps), B (Git) |
| **TypeScript** | `package.json` + `nuxt.config.*` | `nuxt` in deps | Vitest | GitHub Actions | B (TDD), B (Lint), B (Arch), B (Deps), B (Git) |
| **TypeScript** | `package.json` + `angular.json` | `@angular/core` | Jest/Karma | GitHub Actions | B (TDD), A (Lint), A (Arch), B (Deps), B (Git) |
| **TypeScript** | `package.json` + `astro.config.*` | `astro` in deps | Vitest | GitHub Actions | B (TDD), B (Lint), C (Arch), B (Deps), B (Git) |
| **TypeScript** | `package.json` + `remix.config.*` | `@remix-run` | Vitest/Jest | GitHub Actions | B (TDD), B (Lint), C (Arch), B (Deps), B (Git) |
| **TypeScript** | `package.json` + Express/Fastify/Nest | express/fastify/@nestjs | Jest | GitHub Actions | A (TDD), B (Lint), B (Arch), B (Deps), B (Git) |
| **TypeScript** | `package.json` (no framework) | plain lib/app | Jest/Vitest | — | B (TDD), B (Lint), C (Arch), B (Deps), B (Git) |
| **Serverless API** | `wrangler.toml` | Cloudflare Workers | Vitest | Cloudflare CI | B (TDD), B (Lint), A4 (Serverless), B (Deps), A (Git) |
| **Serverless API** | `serverless.yml` | Serverless Framework | Jest/Mocha | GitHub Actions | B (TDD), B (Lint), A4 (Serverless), B (Deps), A (Git) |
| **Serverless API** | `template.yaml` / `samconfig.toml` | AWS SAM | pytest | AWS CodeBuild | B (TDD), B (Lint), A4 (Serverless), B (Deps), A (Git) |
| **AI/RAG Pipeline** | Python + langchain/llamaindex in deps | AI data pipeline | pytest | — | C (TDD), B (Lint), E4 (Script), C (Deps), A (Git) |
| **Data Pipeline** | Python + pandas/airflow/prefect in deps | ETL / data pipeline | pytest | — | C (TDD), B (Lint), E4 (Script), C (Deps), A (Git) |
| **Terraform** | `*.tf` files | Terraform / OpenTofu | terraform test | GitHub Actions | C (TDD), A (Lint), E4 (Script), A (Deps), A (Git) |
| **Ansible** | `*.yml` in ansible/ or playbooks/ | Ansible | ansible-test | — | C (TDD), A (Lint), E4 (Script), A (Deps), A (Git) |
| **Astro Site** | `astro.config.*` / `src/pages/*` | Astro SSG | — | GitHub Pages / Netlify | C (TDD), B (Lint), B1 (SSG), B (Deps), A (Git) |
| **Hugo Site** | `hugo.toml` / `config.toml` / `content/` | Hugo SSG | — | Netlify / Cloudflare | C (TDD), B (Lint), B1 (SSG), B (Deps), A (Git) |
| **11ty Site** | `.eleventy.js` / `_config.js` | 11ty SSG | — | Netlify / GitHub Pages | C (TDD), B (Lint), B1 (SSG), B (Deps), A (Git) |
| **Jekyll Site** | `_config.yml` / `_posts/` | Jekyll SSG | — | GitHub Pages | C (TDD), B (Lint), B1 (SSG), B (Deps), A (Git) |
| **Next.js SSG** | `next.config.*` + `next export` or `output: export` | Next.js SSG mode | Vitest | Vercel | C (TDD), B (Lint), B1/B2 (SSG/CMS), B (Deps), A (Git) |
| **Python** | `pyproject.toml` + `manage.py` | Django | pytest | GitHub Actions | A (TDD), B (Lint), B (Arch), B (Deps), B (Git) |
| **Python** | `pyproject.toml` + `main.py` (FastAPI) | fastapi/starlette | pytest | — | A (TDD), B (Lint), B (Arch), B (Deps), B (Git) |
| **Python** | `pyproject.toml` + `app.py` (Flask) | flask in deps | pytest | — | B (TDD), B (Lint), C (Arch), B (Deps), B (Git) |
| **Python** | `pyproject.toml` + Streamlit | streamlit in deps | pytest | — | C (TDD), C (Lint), C (Arch), B (Deps), C (Git) |
| **Python** | `setup.py` / `requirements.txt` | legacy Python | pytest/unittest | — | B (TDD), B (Lint), C (Arch), B (Deps), C (Git) |
| **Go** | `go.mod` + `main.go` (Gin) | gin in go.mod | go test | GitHub Actions | A (TDD), A (Lint), A (Arch), A (Deps), B (Git) |
| **Go** | `go.mod` + `main.go` (Echo) | echo in go.mod | go test | GitHub Actions | A (TDD), A (Lint), A (Arch), A (Deps), B (Git) |
| **Go** | `go.mod` + `cmd/` (std lib) | no framework import | go test | — | A (TDD), A (Lint), A (Arch), A (Deps), B (Git) |
| **Rust** | `Cargo.toml` (Axum) | axum in deps | cargo test | GitHub Actions | A (TDD), A (Lint), A (Arch), A (Deps), B (Git) |
| **Rust** | `Cargo.toml` (Leptos/Yew) | leptos/yew in deps | cargo test | GitHub Actions | A (TDD), A (Lint), A (Arch), A (Deps), B (Git) |
| **Rust** | `Cargo.toml` (CLI tool) | clap in deps | cargo test | — | A (TDD), A (Lint), C (Arch), A (Deps), B (Git) |
| **Ruby** | `Gemfile` + `config/routes.rb` | Rails | RSpec/Minitest | GitHub Actions | B (TDD), B (Lint), B (Arch), B (Deps), B (Git) |
| **Ruby** | `Gemfile` (Sinatra) | sinatra in Gemfile | RSpec | — | B (TDD), B (Lint), C (Arch), B (Deps), B (Git) |
| **Kotlin** | `build.gradle.kts` (Spring) | spring in deps | JUnit 5 | — | B (TDD), A (Lint), A (Arch), B (Deps), B (Git) |
| **Kotlin** | `build.gradle.kts` (Ktor) | ktor in deps | JUnit 5 | — | B (TDD), A (Lint), B (Arch), B (Deps), B (Git) |
| **Java** | `pom.xml` (Spring Boot) | spring-boot-starter | JUnit 5 | Jenkins | B (TDD), A (Lint), A (Arch), B (Deps), C (Git) |
| **Java** | `pom.xml` (Quarkus) | quarkus in deps | JUnit 5 | — | B (TDD), A (Lint), A (Arch), B (Deps), B (Git) |
| **Java** | `build.gradle` (Micronaut) | micronaut in deps | JUnit 5 | — | B (TDD), A (Lint), A (Arch), B (Deps), B (Git) |
| **C# / .NET** | `*.csproj` + `Program.cs` (Web API) | Microsoft.AspNetCore | xUnit/NUnit | Azure DevOps | A (TDD), A (Lint), A (Arch), B (Deps), B (Git) |
| **C# / .NET** | `*.csproj` (Blazor) | Microsoft.AspNetCore.Components | xUnit | Azure DevOps | B (TDD), A (Lint), B (Arch), B (Deps), B (Git) |
| **C# / .NET** | `*.csproj` (MAUI) | Microsoft.Maui | xUnit | Azure DevOps | B (TDD), A (Lint), B (Arch), B (Deps), B (Git) |
| **PHP** | `composer.json` + `artisan` | Laravel | Pest/PHPUnit | GitHub Actions | B (TDD), B (Lint), B (Arch), B (Deps), B (Git) |
| **PHP** | `composer.json` + `bin/console` | Symfony | PHPUnit | — | B (TDD), B (Lint), B (Arch), B (Deps), B (Git) |
| **PHP** | `composer.json` + `wp-content/` | WordPress | — | — | C (TDD), C (Lint), C (Arch), B (Deps), C (Git) |
| **PHP** | `composer.json` + `core/drupal` | Drupal | PHPUnit | — | B (TDD), B (Lint), B (Arch), B (Deps), C (Git) |
| **Dart/Flutter** | `pubspec.yaml` | flutter in deps | flutter test | — | A (TDD), B (Lint), B (Arch), B (Deps), B (Git) |
| **Swift** | `Package.swift` (Vapor) | vapor in deps | XCTest | — | A (TDD), A (Lint), A (Arch), A (Deps), B (Git) |
| **Swift** | `Package.swift` (iOS app) | swiftui/uikit | XCTest | — | B (TDD), A (Lint), A (Arch), B (Deps), B (Git) |
| **Elixir** | `mix.exs` (Phoenix) | phoenix in deps | ExUnit | — | A (TDD), B (Lint), A (Arch), B (Deps), B (Git) |
| **Scala** | `build.sbt` (Play) | play in deps | ScalaTest | — | B (TDD), A (Lint), A (Arch), B (Deps), B (Git) |
| **Deno** | `deno.json` / `deno.jsonc` | deno std | deno test | — | B (TDD), B (Lint), C (Arch), A (Deps), B (Git) |
| **Docker** | `Dockerfile` only | any language | — | — | C (TDD), C (Lint), C (Arch), A (Deps), B (Git) |
| **Nix** | `flake.nix` / `shell.nix` | nix language | — | — | C (TDD), A (Lint), B (Arch), A (Deps), A (Git) |
| **Unity Game** | `Assembly-CSharp*` / `.unity` files | Unity engine | Unity Test Runner / NUnit | Unity Cloud Build | C (TDD), B (Lint), F1 (Engine), C (Deps), B (Git) |
| **Unreal Game** | `.uproject` / `Source/*.Build.cs` | Unreal Engine | Unreal Automation Test | — | C (TDD), B (Lint), F1 (Engine), C (Deps), B (Git) |
| **Godot Game** | `project.godot` / `*.gd` | Godot engine | GDScript unit test addon | — | C (TDD), B (Lint), F1 (Engine), C (Deps), B (Git) |
| **Rust Game (Bevy)** | `Cargo.toml` (bevy in deps) | Bevy engine | cargo test | GitHub Actions | B (TDD), A (Lint), E1/E2 (Engine/Custom), A (Deps), B (Git) |
| **Web Game** | `package.json` + canvas/Phaser | Phaser/PixiJS/Three.js | Vitest/Jest | — | C (TDD), B (Lint), F3 (Web/Retro), C (Deps), B (Git) |
| **Arduino** | `.ino` files / `platformio.ini` | Arduino framework | — | — | C (TDD), A (Lint), I3 (Arduino), A (Deps), B (Git) |
| **ESP-IDF** | `CMakeLists.txt` + esp-idf | ESP-IDF (Espressif SDK) | — | — | C (TDD), A (Lint), I1 (Bare-Metal), A (Deps), A (Git) |
| **STM32 / ARM MCU** | `Makefile` + linker script + CMSIS | Bare-metal / HAL / CubeMX | — | — | C (TDD), A (Lint), I1 (Bare-Metal), A (Deps), A (Git) |
| **Zephyr RTOS** | `CMakeLists.txt` + `prj.conf` | Zephyr RTOS | ztest | — | C (TDD), A (Lint), I1 (RTOS), A (Deps), A (Git) |
| **Raspberry Pi / Yocto** | `local.conf` / `*.bb` (Yocto) | Yocto / Buildroot / RPi OS | pytest | — | C (TDD), A (Lint), I2 (Linux), A (Deps), A (Git) |
| **MicroPython** | `boot.py` / `main.py` on MCU board | MicroPython / CircuitPython | — | — | C (TDD), B (Lint), I3 (MicroPython), A (Deps), A (Git) |
| **iOS App (Swift)** | `*.xcworkspace` / `*.xcodeproj` / `Package.swift` | Swift/SwiftUI | XCTest | Xcode Cloud / GitHub Actions | B (TDD), B (Lint), C1 (Native), B (Deps), B (Git) |
| **Android App (Kotlin)** | `build.gradle.kts` / `AndroidManifest.xml` | Kotlin/Jetpack | JUnit + Compose UI Test | GitHub Actions / Bitrise | B (TDD), B (Lint), C1 (Native), B (Deps), B (Git) |
| **Flutter App** | `pubspec.yaml` (flutter in deps) | Flutter/Dart | flutter test | GitHub Actions / Codemagic | B (TDD), B (Lint), C2 (Cross-Platform), B (Deps), B (Git) |
| **React Native App** | `package.json` + react-native in deps | React Native | Jest + Detox | GitHub Actions | B (TDD), B (Lint), C2 (Cross-Platform), B (Deps), B (Git) |
| **Electron App** | `package.json` + electron in deps | Electron/TypeScript | Vitest/Jest + Playwright | GitHub Actions | B (TDD), B (Lint), C3 (Web Wrapper), C (Deps), B (Git) |
| **Tauri App** | `src-tauri/Cargo.toml` + `tauri.conf.json` | Tauri/Rust+TS | cargo test + Vitest | GitHub Actions | A (TDD), A (Lint), C2/C3 (Cross-Platform/Web), A (Deps), B (Git) |
| **Chrome Extension** | `manifest.json` | Chrome Extension MV3 | Puppeteer/Playwright | — | C (TDD), B (Lint), G1/G2 (Simple/MV3), A (Deps), B (Git) |
| **Cross-Browser Extension** | `manifest.json` + webextension-polyfill | WebExtension | Puppeteer/Playwright | — | C (TDD), B (Lint), G3 (Cross-Browser), A (Deps), B (Git) |
| **Jupyter Notebook** | `*.ipynb` files | Python/Jupyter | — | — | C (TDD), C (Lint), H1 (Single Notebook), C (Deps), A (Git) |
| **R Markdown / Quarto** | `*.Rmd` / `*.qmd` files | R/R Markdown | — | — | C (TDD), C (Lint), H1/H2 (Notebook), C (Deps), A (Git) |
| **Research Package** | `pyproject.toml` + `src/` + notebooks/ | Python research pkg | pytest | — | C (TDD), C (Lint), H3 (Package), C (Deps), A (Git) |

Default options format: **Testing, Linting, Architecture, Dependencies, Git Workflow**.
Remaining principles (Documentation, Error Handling, Performance, Code Review, Database, Config, Dev Toolchain) 
use stock detection heuristics unless project-specific indicators override them.

**Database detection heuristics within each stack:**

| ORM/Schema detected | Language | Detected DB | Recommended DB principle |
|---------------------|----------|-------------|------------------------|
| Prisma (schema.prisma) | TS/JS | PostgreSQL/MySQL/SQLite | A (Migration-First) |
| Alembic (alembic.ini) | Python | PostgreSQL/MySQL | A (Migration-First) |
| Django ORM (migrations/) | Python | PostgreSQL/MySQL/SQLite | A (Migration-First) |
| EF Core (Migrations/) | C# | SQL Server/PostgreSQL | A (Migration-First) |
| Flyway/Liquibase | Java | Any SQL | A (Migration-First) |
| ActiveRecord (db/migrate/) | Ruby | PostgreSQL/MySQL | A (Migration-First) |
| Ecto (priv/repo/migrations/) | Elixir | PostgreSQL | A (Migration-First) |
| Diesel (diesel.toml) | Rust | PostgreSQL/SQLite | A (Migration-First) |
| Sequelize/TypeORM/Drizzle | TS/JS | PostgreSQL/MySQL | A (Migration-First) |
| No ORM, no migrations, no schema files | Any | Stateless | **SKIP** — no database principle needed |

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
