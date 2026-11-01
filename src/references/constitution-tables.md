# Constitution Reference Tables

Extracted wizard tables and detection tables from spec-kit-constitution.
Loaded by the constitution skill during wizard/brownfield mode.

---

## Level 2 — Architecture Approach Tables

> Refreshed 2026-11. ⭐ = the default to recommend when nothing in the description argues otherwise.

**If purpose = A (User-Facing App):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **A1** | Monolith | One deployable: server-rendered (Rails, Laravel, Django, ASP.NET Core + htmx / Hotwire / Livewire) or a full-stack framework (Next.js, Nuxt, SvelteKit, React Router 7). | Fastest to build, one deploy, one database, easy to debug | Boundaries erode without discipline; scaling is all-or-nothing | MVPs, small teams, internal tools |
| **A2** ⭐ | Modular Monolith | One deployable, explicit modules (bounded contexts) that own their data and talk through in-process contracts; vertical slices inside a module; architecture tests guard the boundaries. | Most of the microservice benefits without the network; a module can be extracted later along a clean seam | Needs enforced boundaries (architecture tests, no shared tables) | The default for most web apps and SaaS, growing teams |
| **A3** | Microservices | Independently deployed services with their own data, async messaging, a platform underneath (containers, service discovery, OpenTelemetry). | Independent scaling and release per team | Distributed failure modes, data consistency, platform cost; premature for one team | Several autonomous teams, very different scaling or compliance needs per domain |
| **A4** | Serverless (functions / containers) | Functions (Lambda, Azure Functions Flex Consumption, Cloudflare Workers) or scale-to-zero containers (Cloud Run, Azure Container Apps, Fargate) behind managed services. | No servers to run, scale to zero, pay per use | Cold starts, execution limits, provider lock-in, harder local testing | Spiky or event-driven workloads, small ops capacity |
| **A5** | AI-native / Agentic App | An app whose core runs on LLM calls: a model gateway (provider abstraction, retries, cost limits), retrieval (RAG over a vector or hybrid index), tools / MCP servers, optional agent orchestration (LangGraph, Agent SDKs), and an **evaluation harness** (golden sets, LLM-as-judge) treated as the test suite. | Capabilities impossible with plain code; fast iteration on prompts | Non-deterministic outputs, eval cost, prompt injection, model drift and price changes, EU AI Act duties for some uses | Assistants, copilots, document understanding, workflow agents |

**If purpose = B (Content Site / Marketing):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **B1** ⭐ | Static / Islands | Static generation with islands of interactivity (Astro, Hugo, 11ty; docs: Starlight, VitePress, Docusaurus). | CDN hosting, near-zero cost, best Core Web Vitals | Rebuild on content change; dynamic bits need client JS or edge functions | Portfolios, blogs, marketing, documentation |
| **B2** | Headless CMS + SSG | Content in a headless CMS (Sanity, Payload, Strapi, Storyblok, Contentful); SSG or ISR fetches it. | Non-developers edit structured content; previews | CMS cost, build coupling, preview plumbing | Team-maintained sites, multi-author content |
| **B3** | Lightweight Backend | A small server or edge runtime for a few dynamic routes (Hono, Express, Flask, plain PHP), often with htmx. | Forms, auth, comments without a full app | A server to patch and monitor | Sites with a handful of dynamic features |

**If purpose = C (Native / Desktop Client):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **C1** | Native Platform | SwiftUI (iOS/macOS), Jetpack Compose (Android), WinUI 3 / WPF (Windows), GTK / Qt (Linux). | Best performance and platform integration | One codebase per platform | Platform-specific products, performance-critical apps |
| **C2** ⭐ | Cross-Platform | Flutter, React Native (New Architecture, Expo), Kotlin / Compose Multiplatform, .NET MAUI, Avalonia, Tauri 2 (desktop + mobile). | One codebase, shared logic, near-native UI | Abstraction leaks, plugin gaps, bridge debugging | Most mobile and desktop apps |
| **C3** | Web Wrapper | Web tech packaged as an app: PWA, Capacitor, Electron, Blazor Hybrid. | Web skills and code reuse, instant updates (PWA) | Heavier runtime, non-native feel, store limits for PWAs on iOS | Internal tools, MVPs, content-heavy apps |

**If purpose = D (Library / SDK):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **D1** | Zero-Dependency | Standard library only; minimal public API. | No supply-chain exposure, maximum compatibility | More code to own | Core primitives, security-sensitive libraries |
| **D2** ⭐ | Curated | Few justified dependencies, ranges tested in CI, published with provenance (npm provenance, PyPI trusted publishing, Sigstore) and an SBOM. | Faster delivery, ecosystem leverage | Transitive risk and upgrade work | Most libraries and SDKs |
| **D3** | Umbrella / Monorepo | Many packages, independent versions (pnpm workspaces + Turborepo / Nx, uv workspaces, Cargo workspaces, changesets). | Consumers take only what they need | Release and tooling overhead | Large SDKs, multi-language clients |

**If purpose = E (Infrastructure / CLI / DevOps):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **E1** ⭐ | Single Binary | One static binary (Go, Rust). | Zero-install distribution, simple CI | Grows into a monolith of flags | CLIs, single-purpose tools, providers |
| **E2** | Multi-Binary | Several binaries over shared libraries. | Independent releases | Version coordination | Tool suites |
| **E3** | Plugin-Based | Core + plugins (WASM components via Wasmtime / Extism, or gRPC plugins). | Community extension without forks; WASM plugins are sandboxed | Plugin API stability burden | Extensible tools and platforms |
| **E4** | Declarative / Pipeline | IaC and pipelines: OpenTofu / Terraform, Pulumi, Bicep, Ansible, CI YAML, data pipelines (dbt, Dagster, Airflow, Polars). | Reviewable, reproducible, no build step | Weak testing, state drift, runtime dependencies | Infrastructure, CI/CD, ETL, dataset preparation |
| **E5** | MCP Server / Agent Tool | A Model Context Protocol server (stdio or streamable HTTP) or agent tool exposing typed tools / resources to AI clients; official SDKs (TypeScript, Python, C#, Go, Kotlin). | One integration reaches every MCP client | Tool-poisoning and prompt-injection surface; auth (OAuth 2.1) for remote servers; protocol still evolving | Exposing an internal system to agents, developer tooling |

**If purpose = F (Game):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **F1** ⭐ | Engine-Centric | Unity, Unreal 5, Godot 4, Bevy (pre-1.0). | Tooling, asset pipelines, console ports | Engine lock-in, licence terms, build size | Most games |
| **F2** | Custom Engine | Own engine on wgpu / Vulkan / SDL3, ECS. | Full control, no licence | Years of engine work | Unusual tech, learning |
| **F3** | Web | Browser games (Phaser, PixiJS 8, Three.js / Babylon.js with WebGPU). | Zero install, instant sharing | Performance ceiling, browser quirks | Casual, jam, educational games |

**If purpose = G (Browser Extension):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **G1** | Simple | One browser, MV3 manifest, content script + popup, no build tooling. | Fastest, smallest permission set | Single store, little structure | Personal and internal utilities |
| **G2** | Full MV3 | Service worker, popup / options / side panel, storage, offscreen documents, a build tool (Vite / CRXJS). | Full API surface, structured project | MV3 constraints (no persistent background, alarm wake-ups) | Feature-rich extensions |
| **G3** ⭐ | Cross-Browser | One codebase for Chrome, Edge, Firefox and Safari via WXT (or Plasmo); Safari through the Xcode converter. | Every store, one codebase | Per-browser quirks, longer reviews | Public and commercial extensions |

**If purpose = H (Research / Notebook):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **H1** | Single Notebook | Jupyter, marimo (reactive, stored as .py), Quarto, Pluto.jl. | Zero setup, shareable | No reuse; hidden state (Jupyter) | Exploration, teaching, one-off reports |
| **H2** ⭐ | Notebook + Modules | Notebooks for narrative, importable modules for logic, uv-locked environment. | Reuse, reviewable diffs | Import-path and environment discipline | Research with shared preprocessing |
| **H3** | Package + Notebooks | A tested package (src layout, pytest / testthat), notebooks as examples, CI. | Reproducible, publishable | Slower research velocity | Research that becomes a product |

**If purpose = I (IoT / Embedded):**

| Option | Name | Description | Pros | Cons | Best for |
|--------|------|-------------|------|------|----------|
| **I1** | Bare-Metal / RTOS | Zephyr, FreeRTOS, ESP-IDF, or async Rust (Embassy). | Lowest latency and power | No memory protection, manual drivers | Sensors, controllers, wearables |
| **I2** | Linux Embedded | Yocto, Buildroot, Ubuntu Core; containerised apps; A/B OTA updates. | Rich ecosystem, networking | Footprint, boot time, patching duty | Gateways, cameras, robots |
| **I3** | High-Level Firmware | Arduino, MicroPython, CircuitPython. | Fastest prototype | Limited performance and control | Prototypes, education, hobby |

Devices, desktop apps and commercial libraries sold in the EU fall under the Cyber Resilience Act
(vulnerability reporting from 11 Sep 2026, full obligations from 11 Dec 2027) — note it in the
constitution when it applies.

```
ASK: "Given your purpose [A|B|C|D|E|F|G|H|I], which architecture approach fits?"
RECORD: architecture = [A1–A5 | B1–B3 | C1–C3 | D1–D3 | E1–E5 | F1–F3 | G1–G3 | H1–H3 | I1–I3]
```

---

## Level 3 — Technology Choice Brackets

Present 3 options per bracket (language · frameworks · pros · cons), the ⭐ architecture's first.

```
A  A1: Rails 8, Laravel, Django, ASP.NET Core (Razor / Blazor SSR), Next.js / Nuxt / SvelteKit / React Router 7
   A2: ASP.NET Core modular monolith, Spring Boot + Spring Modulith, NestJS, Django apps, Phoenix contexts
   A3: Go, ASP.NET Core minimal APIs (+ .NET Aspire for local orchestration), Rust (Axum), Kotlin (Ktor)
   A4: TypeScript (Workers, Lambda, Vercel), Python (Lambda, Azure Functions), C# (Azure Functions isolated), containers on Cloud Run / Container Apps
   A5: Python (FastAPI + LangGraph / Pydantic AI), TypeScript (Vercel AI SDK, Mastra), C# (Microsoft.Extensions.AI, Semantic Kernel);
       retrieval: PostgreSQL + pgvector, Azure AI Search, Qdrant; evals: promptfoo, Ragas, DeepEval; tracing: OpenTelemetry GenAI conventions, Langfuse
B  B1: Astro, Hugo, 11ty; docs: Starlight, VitePress, Docusaurus
   B2: Astro or Next.js + Sanity / Payload / Storyblok / Contentful
   B3: Hono (Node, Bun, Workers), Flask, PHP — + htmx
C  C1: Swift (SwiftUI), Kotlin (Compose), C# (WinUI 3), C++ (Qt 6)
   C2: Dart (Flutter), TypeScript (React Native + Expo), Kotlin (Compose Multiplatform), C# (.NET MAUI / Avalonia), Rust + TS (Tauri 2)
   C3: TypeScript (PWA, Capacitor, Electron), C# (Blazor Hybrid)
D  D1: Go stdlib, Rust no-std, Python stdlib, TypeScript without runtime deps (publish to npm + JSR)
   D2: the target ecosystem's standard toolchain (uv / hatch, tsup / tsdown, cargo, Gradle)
   D3: pnpm workspaces + Turborepo / Nx, uv workspaces, Cargo workspaces; changesets for releases
E  E1: Go (cobra), Rust (clap) · E2: Go, Rust · E3: Rust / Go host + WASM components
   E4: OpenTofu / Terraform, Pulumi (TS / Python / C#), Bicep, Ansible; data: Python + uv, Polars, DuckDB, dbt, Dagster
   E5: TypeScript or Python MCP SDK (most mature), C# MCP SDK, Go; stdio for local tools, streamable HTTP + OAuth for remote
F  F1: C# (Unity), C++ (Unreal 5), GDScript / C# (Godot 4), Rust (Bevy)
   F2: Rust (wgpu, winit), C++ (SDL3, Vulkan), C# (MonoGame)
   F3: TypeScript (Phaser, PixiJS 8, Three.js / Babylon.js), Lua (LÖVE)
G  G1: TypeScript + plain manifest · G2: TypeScript + Vite / CRXJS, React / Svelte / Vue UI · G3: TypeScript + WXT (or Plasmo)
H  H1: Python (Jupyter, marimo), R / Python (Quarto), Julia (Pluto) · H2: Python + modules + uv, R + scripts + renv
   H3: Python (src layout, pytest, uv), R (package, testthat, vignettes), Julia (Pkg)
I  I1: C (Zephyr, FreeRTOS, ESP-IDF), Rust (Embassy, esp-hal), C++ (constrained)
   I2: C / C++, Rust, Go, Python on Yocto / Buildroot · I3: C++ (Arduino), Python (MicroPython, CircuitPython)
```

**2026 baseline — present once after Level 3, as recommendations, never as gates:** OpenTelemetry
for traces, metrics and logs · dependency + secret scanning in CI and an SBOM per release · OIDC
sign-in with passkeys where users log in · IaC for anything deployed · lock files committed ·
AI coding agents governed by the constitution (what they may read, push, deploy).

---

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
