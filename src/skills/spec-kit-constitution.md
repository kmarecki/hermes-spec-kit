---
name: spec-kit-constitution
description: Load when the user says 'spec-kit constitution', 'speckit constitution', 'spec-kit principles', 'speckit principles', "create constitution", "create project principles", or "set up project principles" — Phase 0 project setup. Handles both brownfield (existing codebase) and greenfield (new project) modes.
version: 2.0.0
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
Auto-detects project stack in brownfield mode, or guides the user through
principled choices in greenfield mode. Always presents 3 options per principle
with pros and cons.

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
  | .cypress.* / cypress  → Cypress (E2E, JS/TS)                |
  | playwright.config.*   → Playwright (E2E, multi-lang)        |
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
    NOTE: "No existing project detected — greenfield mode. I'll guide you through
           choosing principles for your new project."
```

### Step 2: Load the principles reference

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
    ASK the user about their intent or preference
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

In greenfield mode, after showing the 3 options, include a short guiding question:

```
  GUIDING QUESTION (greenfield only):
  "For a [project type], most teams pick [option]. This means [summary of tradeoff].
   Does that match your priorities?"
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
- Report mode: brownfield or greenfield
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
| **Terraform** | `*.tf` files | — | — | — | C (TDD), C (Lint), C (Arch), A (Deps), A (Git) |
| **Docker** | `Dockerfile` only | any language | — | — | C (TDD), C (Lint), C (Arch), A (Deps), B (Git) |
| **Nix** | `flake.nix` / `shell.nix` | nix language | — | — | C (TDD), A (Lint), B (Arch), A (Deps), A (Git) |

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
