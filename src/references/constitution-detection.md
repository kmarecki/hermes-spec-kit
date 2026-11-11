# Constitution — Brownfield Detection

Loaded by `spec-kit-constitution` **only when project files are detected** (greenfield uses
`constitution-greenfield.md`). Match the files below, pre-fill the ⭐ defaults, infer the purpose
and option (A1–K3) from the closest row, and the traits (Runs where / Regulated / Lifecycle)
from what the code shows (tenant filters, on-prem installers, a legacy stack → modernization).
No row fits → the closest purpose + *(not from the reference tables)*.

## Brownfield Detection Examples

| Language | File(s) | Detect framework by | Likely test framework | Typical CI | Recommended defaults |
|----------|---------|-------------------|----------------------|------------|---------------------|
| **TypeScript** | `package.json` + `next.config.*` | `next` in deps | Vitest/Jest | GitHub Actions | B (TDD), B (Lint), C (Arch), B (Deps), B (Git) |
| **TypeScript** | `package.json` + `vite.config.*` | `vite` + `vue`/`react`/`svelte` in deps | Vitest | GitHub Actions | B (TDD), B (Lint), C (Arch), B (Deps), B (Git) |
| **TypeScript** | `package.json` + `nuxt.config.*` | `nuxt` in deps | Vitest | GitHub Actions | B (TDD), B (Lint), B (Arch), B (Deps), B (Git) |
| **TypeScript** | `package.json` + `angular.json` | `@angular/core` | Vitest (Angular 21 default) / Karma (legacy) | GitHub Actions | B (TDD), A (Lint), A (Arch), B (Deps), B (Git) |
| **TypeScript** | `package.json` + `astro.config.*` | `astro` in deps | Vitest | GitHub Actions | B (TDD), B (Lint), C (Arch), B (Deps), B (Git) |
| **TypeScript** | `package.json` + `react-router.config.*` / `remix.config.*` | `@react-router` / `@remix-run` | Vitest | GitHub Actions | B (TDD), B (Lint), C (Arch), B (Deps), B (Git) |
| **TypeScript** | `package.json` + Express/Fastify/Nest | express/fastify/@nestjs | Jest | GitHub Actions | A (TDD), B (Lint), B (Arch), B (Deps), B (Git) |
| **TypeScript** | `package.json` (no framework) | plain lib/app | Jest/Vitest | — | B (TDD), B (Lint), C (Arch), B (Deps), B (Git) |
| **Serverless API** | `wrangler.toml` | Cloudflare Workers | Vitest | Cloudflare CI | B (TDD), B (Lint), A4 (Serverless), B (Deps), A (Git) |
| **Serverless API** | `serverless.yml` | Serverless Framework | Jest/Mocha | GitHub Actions | B (TDD), B (Lint), A4 (Serverless), B (Deps), A (Git) |
| **Serverless API** | `template.yaml` / `samconfig.toml` | AWS SAM | pytest | AWS CodeBuild | B (TDD), B (Lint), A4 (Serverless), B (Deps), A (Git) |
| **AI app / agent** | openai / anthropic / langgraph / pydantic-ai / `ai` / Microsoft.Extensions.AI in deps | LLM app | pytest/Vitest/xUnit + evals | GitHub Actions | B (TDD), B (Lint), A5 (AI-native), B (Deps), B (Git) |
| **MCP server** | `@modelcontextprotocol/sdk` / `mcp` / `ModelContextProtocol` in deps | MCP server | Vitest/pytest/xUnit | GitHub Actions | B (TDD), A (Lint), E5 (MCP), A (Deps), B (Git) |
| **AI/RAG Pipeline** | Python + langchain/llamaindex in deps, no server | AI data pipeline | pytest | — | C (TDD), B (Lint), E4 (Pipeline), C (Deps), A (Git) |
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
| **Python** | `uv.lock` / `pyproject.toml` (no framework) | uv-managed Python | pytest | — | B (TDD), B (Lint), C (Arch), B (Deps), B (Git) |
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
| **.NET Aspire** | `*.AppHost.csproj` / `Aspire.Hosting` | distributed .NET app | xUnit/TUnit | Azure DevOps / GitHub Actions | A (TDD), A (Lint), A2/A3 (by service count), B (Deps), B (Git) |
| **Azure Functions** | `host.json` + `*.csproj` / `function_app.py` | Azure Functions (isolated) | xUnit/pytest | Azure DevOps | B (TDD), A (Lint), A4 (Serverless), B (Deps), B (Git) |
| **SQL Server SSDT** | `*.sqlproj` | DACPAC database project | tSQLt | Azure DevOps | C (TDD), B (Lint), —, B (Deps), B (Git); DB principle A |
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
| **Bicep** | `*.bicep` | Azure IaC | — (what-if) | Azure DevOps / GitHub Actions | C (TDD), A (Lint), E4 (Declarative), A (Deps), A (Git) |
| **C / C++** | `CMakeLists.txt` / `meson.build` / `vcpkg.json` / `conanfile.*` | app or library | CTest / GoogleTest / Catch2 | GitHub Actions | B (TDD), A (Lint), B (Arch), A (Deps), B (Git) |
| **F#** | `*.fsproj` | F# app / library | Expecto / xUnit | — | A (TDD), A (Lint), B (Arch), B (Deps), B (Git) |
| **PowerShell** | `*.psd1` / `*.psm1` | PowerShell module | Pester | Azure DevOps | B (TDD), A (Lint), E4 (Pipeline), A (Deps), B (Git) |
| **Zig** | `build.zig` | Zig | zig test | — | A (TDD), A (Lint), E1 / J2, A (Deps), B (Git) |
| **Haskell / OCaml** | `*.cabal` / `stack.yaml` / `dune-project` | functional app / library | hspec / alcotest | — | A (TDD), A (Lint), B (Arch), A (Deps), B (Git) |
| **Julia** | `Project.toml` + `Manifest.toml` | Julia package | Test stdlib | — | B (TDD), B (Lint), H3 / J3, B (Deps), A (Git) |
| **Fortran / MPI** | `*.f90` + `CMakeLists.txt` / `mpirun` scripts | scientific code | pFUnit | — | C (TDD), B (Lint), J3 (HPC), A (Deps), B (Git) |
| **COBOL / mainframe** | `*.cbl` / `*.cpy` / JCL | legacy mainframe | — | — | C (TDD), C (Lint), —, A (Deps), C (Git); trait: modernization |
| **Kernel / eBPF** | `Kconfig` / `Kbuild` / `*.bpf.c` | kernel code | KUnit / kselftest | — | A (TDD), A (Lint), J1 (Kernel), A (Deps), B (Git) |
| **dbt** | `dbt_project.yml` | analytics engineering | dbt tests | — | B (TDD), B (Lint), H4 (Data platform), B (Deps), B (Git) |
| **Spark / Databricks** | `pyspark` in deps / `databricks.yml` | data platform | pytest + chispa | — | B (TDD), B (Lint), H4 (Data platform), B (Deps), B (Git) |
| **ML pipeline** | `MLproject` / `mlflow` / `kfp` / `azureml` in deps | ML training & serving | pytest + evals | — | B (TDD), B (Lint), H5 (ML), B (Deps), B (Git) |
| **Salesforce** | `sfdx-project.json` / `force-app/` | Salesforce DX | Apex tests / Jest (LWC) | — | B (TDD), B (Lint), K2 (Platform code), B (Deps), B (Git) |
| **Power Platform / Dynamics** | `solution.xml` / `*.cdsproj` / `pac` scripts | Dataverse solution | FakeXrmEasy / xUnit | Azure DevOps | B (TDD), B (Lint), K1 / K2, B (Deps), B (Git) |
| **VS Code extension** | `package.json` with `engines.vscode` | IDE extension | @vscode/test-electron | GitHub Actions | B (TDD), B (Lint), G4 (Host plugin), A (Deps), B (Git) |
| **Office add-in / Figma plugin** | `manifest.xml` (Office) / `manifest.json` with `figma` | host plugin | Vitest / Jest | — | B (TDD), B (Lint), G4 (Host plugin), A (Deps), B (Git) |
| **Smart contracts** | `foundry.toml` / `hardhat.config.*` / `Move.toml` | on-chain code | forge test / Hardhat | GitHub Actions | A (TDD), A (Lint), D4 (Contracts), A (Deps), B (Git) |
| **Kafka / stream workers** | Kafka / Flink / MassTransit / Spring Cloud Stream in deps, no HTTP host | event-driven service | integration tests (Testcontainers) | — | A (TDD), B (Lint), A6 (Event-driven), B (Deps), B (Git) |
| **Docker** | `Dockerfile` only | any language | — | — | C (TDD), C (Lint), C (Arch), A (Deps), B (Git) |
| **Nix** | `flake.nix` / `shell.nix` | nix language | — | — | C (TDD), A (Lint), B (Arch), A (Deps), A (Git) |
| **Unity Game** | `Assembly-CSharp*` / `.unity` files | Unity engine | Unity Test Runner / NUnit | Unity Cloud Build | C (TDD), B (Lint), F1 (Engine), C (Deps), B (Git) |
| **Unreal Game** | `.uproject` / `Source/*.Build.cs` | Unreal Engine | Unreal Automation Test | — | C (TDD), B (Lint), F1 (Engine), C (Deps), B (Git) |
| **Godot Game** | `project.godot` / `*.gd` | Godot engine | GDScript unit test addon | — | C (TDD), B (Lint), F1 (Engine), C (Deps), B (Git) |
| **Rust Game (Bevy)** | `Cargo.toml` (bevy in deps) | Bevy engine | cargo test | GitHub Actions | B (TDD), A (Lint), F1 (Engine), A (Deps), B (Git) |
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


---

## Brownfield File Detection Tables

```text
                    LANGUAGE / FRAMEWORK DETECTION
   package.json       → JavaScript/TypeScript
                       Check for: react, vue, next, nuxt,
                       svelte, solid, angular, express, fastify,
                       nest, remix, astro, qwik, htmx wrapper
                       hattip, hono, elysia, adonis

   pyproject.toml     → Python
                       Check for: django, fastapi, flask,
                       starlette, aiohttp, tornado, litestar,
                       sanic, asyncpg, sqlalchemy, streamlit

   setup.py /         → Python (legacy setup)
   setup.cfg             (fallback if no pyproject.toml)

   requirements.txt   → Python (no build system detected)

   go.mod             → Go + module path
                       Check for: gin, echo, fiber, chi,
                       gorilla/mux, buffalo, connect-go

   Cargo.toml         → Rust
                       Check for: actix, axum, rocket, tide,
                       warp, leptos, yew, dioxus, tauri

   Gemfile            → Ruby + framework
                       Check for: rails, sinatra, roda,
                       hanami, grape, rack

   build.gradle /     → Java / Kotlin
   build.gradle.kts      Check for: spring, micronaut, quarkus,
                          ktor, jooby, javalin, dropwizard

   pom.xml            → Java (Maven)
                       Check for: spring, hibernate, vaadin

   composer.json      → PHP
                       Check for: laravel, symfony, wordpress
                       (wp-content/), drupal, yii, cake,
                       codeigniter, phalcon, slim, magento

   *.csproj / *.sln   → C# / .NET
                       Check for: aspnet, blazor, maui,
                       wpf, winforms, webapi, minimal api

   pubspec.yaml       → Dart / Flutter

   Package.swift      → Swift (SPM) / iOS
                       Check for: vapor, hummingbird,
                       swiftui, uikit

   mix.exs            → Elixir
                       Check for: phoenix, nervesh, plug

   build.sbt          → Scala
                       Check for: play, http4s, zio-http, akka

   rebar.config /     → Erlang
   mix.exs              Check for: cowboy, ellierman

   deno.json /        → Deno
   deno.jsonc

   bun.lock           → Bun (alongside package.json)

   flake.nix /        → Nix language / NixOS
   shell.nix /
   default.nix

   *.tf               → Terraform / OpenTofu
   (any .tf files)

   CMakeLists.txt     → C / C++ (CMake)

   Makefile           → Generic build (C, C++, Go without
                        go.mod, or custom build system)

   Dockerfile         → Containerized app (any language)

                      TEST FRAMEWORK DETECTION
   Search for config files AND actual test files:

   jest.config.* /       → Jest (JS/TS)
   jest.setup.*
   vitest.config.*       → Vitest (JS/TS, Vite projects)

  | .mocharc.* / mocha    → Mocha (JS/TS)                        |
  | .cypress.* / cypress  → Cypress (F2E, JS/TS)                |
  | playwright.config.*   → Playwright (F2E, multi-lang)        |
  |                                                              |
   pytest.ini /        → pytest (Python)
   pyproject.toml [tool.pytest]

   unittest (std lib)  → unittest (Python, fallback)

   *_test.go files     → go test (Go, std lib)

   Rakefile / spec/    → RSpec (Ruby)

   minitest            → Minitest (Ruby, Rails default)

   PHPUnit config      → PHPUnit (PHP)
   (phpunit.xml*).*

   pest.php / Pest     → Pest (PHP, Laravel)

   *.Test.cs files     → xUnit / NUnit / MSTest (C#)
   .runsettings

   test_*.dart files   → flutter test (Dart)

   XCTest /            → XCTest (Swift/iOS)
   *_Tests.swift files

   ex_unit config      → ExUnit (Elixir)

   scalatest / specs2  → ScalaTest / specs2 (Scala)

   cargo test exists   → cargo test (Rust, std lib)

                   LINTING / FORMATTING DETECTION
   .eslintrc* /           → ESLint (JS/TS)
   eslint.config.*
   .prettierrc*           → Prettier (multi-lang)
   .biomerc / biome.json  → Biome (JS/TS, ESLint+Prettier alt)
   .oxlintrc*             → Oxlint (JS/TS, Rust-based)
   ruff config            → Ruff (Python, successor to flake8)
   pylintrc / .pylintrc   → Pylint (Python legacy)
   pyproject.toml          → mypy (type checker), ruff, black
     [tool.mypy/.ruff/       (modern Python toolchain)
      .black/.isort]
   .golangci.yml /        → golangci-lint (Go)
   .golangci.yaml
   rustfmt / clippy       → rustfmt + clippy (Rust, std tools)
   .rubocop.yml           → RuboCop (Ruby)
   .reek.yml              → Reek (Ruby)
   phpcs.xml*             → PHP_CodeSniffer (PHP)
   phpstan.neon*          → PHPStan (PHP static analysis)
   .php-cs-fixer.*        → PHP-CS-Fixer (PHP)
   .editorconfig          → EditorConfig (basic, multi-lang)

                        CI/CD DETECTION
   .github/workflows/*   → GitHub Actions
   .gitlab-ci.yml        → GitLab CI/CD
   Jenkinsfile           → Jenkins
   .circleci/config.yml  → CircleCI
   .travis.yml           → Travis CI
   azure-pipelines.yml   → Azure DevOps Pipelines
   bitbucket-pipelines   → Bitbucket Pipelines
                         → YAML in bitbucket-pipelines.yml
   buildkite             → Buildkite
                         → .buildkite/pipeline.yml
   .drone.yml            → Drone CI
   .woodpecker.yml       → Woodpecker CI
   cloudbuild.yaml       → Google Cloud Build
   buildspec.yml         → AWS CodeBuild
   codeship-*.yml        → CodeShip
   appveyor.yml          → AppVeyor
   wercker.yml           → Wercker

                     DATABASE / STORAGE DETECTION
   Search for ORM configs, migration dirs, schema files:

   migrations/ directory  → Has database migrations
   Prisma schema          → Prisma (JS/TS)
   (schema.prisma)
   Alembic config         → Alembic (Python, SQLAlchemy)
   (alembic.ini)
   Django migrations      → Django ORM (Python)
   (*/migrations/*.py)
   Entity Framework       → EF Core (C#)
   (Migrations/)
   Flyway / Liquibase     → Flyway/Liquibase (Java)
   configs
   Sequelize configs      → Sequelize (JS/TS)
   TypeORM config         → TypeORM (JS/TS)
   Drizzle config         → Drizzle (JS/TS)
   ActiveRecord           → ActiveRecord (Rails/Ruby)
   (db/migrate/)
   Ecto migrations        → Ecto (Elixir/Phoenix)
   (priv/repo/migrations/)
   Diesel / SeaORM        → Diesel/SeaORM (Rust)
   Hasura                 → Hasura metadata
   (metadata/)
   sqlite (file)          → SQLite (embedded)
   .db / .sqlite files

   IF NO database-related files found:
     mark as "stateless/no database"

                    DEPLOYMENT / INFRA DETECTION
   Dockerfile             → Docker container
   docker-compose.yml     → Docker Compose (multi-container)
   k8s/ / *.k8s.yaml      → Kubernetes manifests
   helm/ / Chart.yaml     → Helm charts
   serverless.yml         → Serverless Framework
   cdk.json / cdk*.ts     → AWS CDK
   Pulumi.yaml            → Pulumi
   Terraform files        → Terraform / OpenTofu
   (.tf, .tfvars)
   Ansible playbooks      → Ansible
   (*.yml in ansible/ or playbooks/)
   Nomad file             → Nomad
   (*.nomad)
   *.bicep / azure.yaml   → Bicep / Azure Developer CLI
   *.AppHost.csproj       → .NET Aspire (local orchestration)
   *.sqlproj              → SQL Server database project (SSDT / DACPAC)
```
