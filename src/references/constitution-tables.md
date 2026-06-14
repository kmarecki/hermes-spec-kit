# Constitution Reference Tables

Extracted wizard tables and detection tables from spec-kit-constitution.
Loaded by the constitution skill during wizard/brownfield mode.

---

## Level 2 — Architecture Approach Tables

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

## Level 3 — Technology Choice Brackets

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

---

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


---

## Brownfield File Detection Tables

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
