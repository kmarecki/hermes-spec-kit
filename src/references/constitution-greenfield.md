# Constitution — Greenfield (free-text and wizard)

Loaded by `spec-kit-constitution` **only when no project files are detected** (brownfield uses
`constitution-detection.md`). Refreshed 2026-11. ⭐ = the default to recommend when nothing in the
description argues otherwise. Purpose → principle defaults: the matrix in the full procedure.

## G1 — Free-text: description → purpose, option, stack

PROMPT for a few sentences (what, platform, team size, constraints) → infer → present the
inference table (purpose, option, language, traits, the ⭐ principles) → WAIT for "all good" or
corrections (record them as rationale). Vague → best guess, say so. "I want the wizard" → G2.

| Signal in the description | Purpose / option |
|---|---|
| web app, SaaS, dashboard, portal, API for our app | A — A2 (A1 if MVP / solo) |
| worker, queue, Kafka, event-driven, stream, batch job, integration hub | A — A6 |
| assistant, agent, copilot, RAG, LLM, chatbot | A — A5 |
| Lambda, Cloud Run, Container Apps, Workers, Firebase | A — A4 |
| microservices, many teams | A — A3 |
| blog, landing page, docs site, portfolio | B — B1 (B2 if editors) |
| iOS, Android, desktop app | C — C1 if one platform, else C2 |
| library, package, SDK | D — D2 |
| smart contract, Solidity, DeFi, on-chain | D — D4 |
| CLI, tool · Terraform, pipeline, CI | E — E1 · E4 |
| MCP server, tool for Claude / agents | E — E5 |
| game, Unity, Godot · VR, AR, visionOS, Quest | F — F1 · F4 |
| Chrome / Firefox extension | G — G3 |
| VS Code / JetBrains extension, Office add-in, Figma plugin, Slack / Teams bot | G — G4 |
| notebook, analysis, research | H — H2 |
| data warehouse, lakehouse, dbt, Spark, analytics engineering | H — H4 |
| train / fine-tune / serve a model, MLOps, feature store | H — H5 |
| firmware, sensor, ESP32 · Raspberry Pi, gateway · device fleet, OTA | I — I1 · I2 · I4 |
| kernel, driver, database engine, compiler, runtime, VM | J — J1 / J2 |
| simulation, HPC, MPI, CUDA, Fortran | J — J3 |
| Salesforce, Dynamics, Power Platform, SAP, ServiceNow, Shopify app | K — K1 / K2 / K3 |
| nothing fits | **Other** (G2 end) |

Also infer the traits (G2 Level 1.5) from words like "multi-tenant", "on-prem", "offline",
"patients", "payments", "safety", "prototype", "replace the legacy system".

## G2 — Wizard

**Level 1 — purpose.** ASK, present all 11 with what they weigh most:

| Purpose | Examples | Weighs most |
|---|---|---|
| **A** Applications & Services | SaaS, web / mobile backend, APIs, workers, AI apps | integration tests, architecture, defensive errors |
| **B** Content Site | marketing, blog, docs | speed of publishing, Core Web Vitals |
| **C** Native / Desktop Client | iOS, Android, desktop | UI tests, crash-free, store review |
| **D** Library / SDK | npm / PyPI / NuGet package, smart contract | public API, exhaustive tests, docs |
| **E** Infrastructure / CLI / DevOps | CLI, IaC, CI, MCP server | composability, static binaries |
| **F** Game / XR | 2D / 3D game, VR / AR | frame budget, playtesting |
| **G** Extensions & Integrations | browser extension, IDE plugin, Office add-in, chat bot | host APIs, permissions, store review |
| **H** Research, Data & ML | notebooks, data platform, model training | reproducibility, data quality, evals |
| **I** IoT / Embedded | firmware, embedded Linux, device fleets | no hotfix once flashed, hard limits |
| **J** Systems Software | kernel, driver, DB engine, compiler, HPC | memory safety, fuzzing, ABI, performance gates |
| **K** Business Platform | Salesforce, Dynamics / Power Platform, SAP, ServiceNow | the vendor's limits, release cadence, metadata deploys |

**Monorepo?** yes → name the sub-projects; run Levels 1–3 per sub-project; the constitution gets
a Projects table; shared principles follow the PRIMARY sub-project.

**Level 1.5 — project traits** (one multi-select question; they adjust the defaults, see the full
procedure's trait rules):

- **Runs where**: multi-tenant SaaS · single-tenant / dedicated · on-prem / customer-hosted · local-first / offline · edge
- **Regulated domain**: none · personal data · finance (DORA, PCI DSS) · health (IEC 62304, MDR, HIPAA) · safety-critical (ISO 26262, IEC 61508, DO-178C) · EU AI Act high-risk
- **Lifecycle**: prototype · product · modernization of a legacy system

**Level 2 — architecture** (tables below) → **Level 3 — technology** (brackets below), 3 options
per bracket (language · frameworks · pros · cons), the ⭐ option first.

**Other** — no purpose fits: take the closest purpose, write 3 options of your own with pros and
cons, mark them *(not from the reference tables)* in the constitution's Architecture section.

## Level 2 — Architecture options

**A — Applications & Services**

| Option | Name | Description | Pros | Cons |
|---|---|---|---|---|
| **A1** | Monolith | One deployable: server-rendered (Rails, Laravel, Django, ASP.NET Core + htmx / Hotwire) or full-stack (Next.js, Nuxt, SvelteKit, React Router 7). | Fastest, one deploy, one DB | Boundaries erode; all-or-nothing scaling |
| **A2** ⭐ | Modular Monolith | One deployable, modules (bounded contexts) owning their data, in-process contracts, vertical slices, architecture tests. | Microservice benefits without the network; extractable later | Boundaries need enforcement |
| **A3** | Microservices | Independent services and data, async messaging, a platform (containers, discovery, OpenTelemetry). | Independent scaling and release per team | Distributed failures, consistency, platform cost |
| **A4** | Serverless | Functions (Lambda, Azure Functions Flex, Workers) or scale-to-zero containers (Cloud Run, Container Apps, Fargate). | No servers, scale to zero, pay per use | Cold starts, limits, lock-in, local testing |
| **A5** | AI-native / Agentic | Model gateway (provider abstraction, retries, cost caps), retrieval (vector / hybrid), tools / MCP, optional agent orchestration, **an eval harness as the test suite**. | Capabilities plain code lacks | Non-determinism, eval cost, prompt injection, model drift, AI Act duties |
| **A6** | Event-driven / Workers | Consumers, schedulers and stream processors around a broker (Kafka, RabbitMQ, Service Bus, SQS); outbox, idempotent handlers, dead-letter queues; Flink / Kafka Streams for streams. | Decoupling, back-pressure, replay | Eventual consistency, ordering, harder tracing |

**B — Content Site**

| Option | Name | Description | Pros | Cons |
|---|---|---|---|---|
| **B1** ⭐ | Static / Islands | Astro, Hugo, 11ty; docs: Starlight, VitePress, Docusaurus. | CDN, near-zero cost, best Web Vitals | Rebuild on change |
| **B2** | Headless CMS + SSG | Sanity, Payload, Strapi, Storyblok, Contentful + SSG / ISR. | Editors without developers | CMS cost, preview plumbing |
| **B3** | Lightweight Backend | Hono, Express, Flask, PHP + htmx for a few dynamic routes. | Forms and auth without an app | A server to patch |

**C — Native / Desktop Client**

| Option | Name | Description | Pros | Cons |
|---|---|---|---|---|
| **C1** | Native | SwiftUI, Jetpack Compose, WinUI 3 / WPF, GTK / Qt. | Best performance and integration | One codebase per platform |
| **C2** ⭐ | Cross-Platform | Flutter, React Native (Expo), Compose Multiplatform, .NET MAUI, Avalonia, Tauri 2. | One codebase, near-native | Abstraction leaks, plugin gaps |
| **C3** | Web Wrapper | PWA, Capacitor, Electron, Blazor Hybrid. | Web reuse, instant updates | Heavier, non-native feel |

**D — Library / SDK**

| Option | Name | Description | Pros | Cons |
|---|---|---|---|---|
| **D1** | Zero-Dependency | Standard library only, minimal API. | No supply-chain exposure | More code to own |
| **D2** ⭐ | Curated | Few justified deps, ranges tested in CI, published with provenance (npm, PyPI trusted publishing, Sigstore) + SBOM. | Ecosystem leverage | Transitive risk |
| **D3** | Umbrella / Monorepo | pnpm + Turborepo / Nx, uv or Cargo workspaces, changesets. | Consumers take only what they need | Release overhead |
| **D4** | Smart Contracts | Solidity (Foundry, Hardhat), Move, Rust (Solana / CosmWasm); upgrade proxies or immutable. | Trustless execution | Immutable bugs, audits and formal verification, gas limits |

**E — Infrastructure / CLI / DevOps**

| Option | Name | Description | Pros | Cons |
|---|---|---|---|---|
| **E1** ⭐ | Single Binary | Go, Rust static binary. | Zero-install distribution | Flag sprawl |
| **E2** | Multi-Binary | Several binaries over shared libs. | Independent releases | Version coordination |
| **E3** | Plugin-Based | Core + WASM components (Wasmtime, Extism) or gRPC plugins. | Sandboxed community extension | Plugin API stability |
| **E4** | Declarative / Pipeline | OpenTofu / Terraform, Pulumi, Bicep, Ansible, CI YAML. | Reviewable, reproducible | Weak testing, state drift |
| **E5** | MCP Server / Agent Tool | MCP server (stdio / streamable HTTP + OAuth 2.1) or agent tool with typed tools / resources. | One integration, every MCP client | Tool poisoning, prompt injection, evolving protocol |

**F — Game / XR**

| Option | Name | Description | Pros | Cons |
|---|---|---|---|---|
| **F1** ⭐ | Engine-Centric | Unity, Unreal 5, Godot 4, Bevy (pre-1.0). | Tooling, asset pipelines, ports | Lock-in, licence terms |
| **F2** | Custom Engine | wgpu / Vulkan / SDL3, ECS. | Full control | Years of engine work |
| **F3** | Web | Phaser, PixiJS 8, Three.js / Babylon.js on WebGPU. | Zero install | Performance ceiling |
| **F4** | XR / Spatial | OpenXR via Unity / Unreal / Godot, visionOS (RealityKit), WebXR. | Immersive UX | Comfort (frame rate), device fragmentation |

**G — Extensions & Integrations**

| Option | Name | Description | Pros | Cons |
|---|---|---|---|---|
| **G1** | Simple Browser | One browser, MV3, content script + popup. | Fastest, small permissions | One store |
| **G2** | Full MV3 | Service worker, side panel, offscreen docs, Vite / CRXJS. | Full API | MV3 lifecycle limits |
| **G3** ⭐ | Cross-Browser | WXT (or Plasmo) for Chrome, Edge, Firefox, Safari. | Every store | Per-browser quirks |
| **G4** | Host Plugin / Bot | VS Code / JetBrains extension, Office add-in, Figma plugin, Slack / Teams app, SaaS marketplace app — the host's SDK, manifest and permission model. | Users where they work | Host API churn, store review, host sandbox limits |

**H — Research, Data & ML**

| Option | Name | Description | Pros | Cons |
|---|---|---|---|---|
| **H1** | Single Notebook | Jupyter, marimo, Quarto, Pluto.jl. | Zero setup | Hidden state, no reuse |
| **H2** ⭐ | Notebook + Modules | Notebooks for narrative, modules for logic, uv-locked env. | Reuse, reviewable | Environment discipline |
| **H3** | Package + Notebooks | Tested package, notebooks as examples, CI. | Reproducible, publishable | Slower research |
| **H4** | Data Platform | Warehouse / lakehouse (Snowflake, BigQuery, Databricks, Fabric, DuckDB), dbt, Dagster / Airflow, medallion layers, data contracts + quality tests. | Trusted shared data | Cost control, ownership, schema drift |
| **H5** | ML Training & Serving | Pipelines (Kubeflow, Vertex / Azure ML), experiment tracking (MLflow, W&B), feature store, model registry, serving (KServe, vLLM, Triton), drift monitoring. | Own models, own data | GPU cost, reproducibility, monitoring burden |

**I — IoT / Embedded**

| Option | Name | Description | Pros | Cons |
|---|---|---|---|---|
| **I1** | Bare-Metal / RTOS | Zephyr, FreeRTOS, ESP-IDF, Rust Embassy. | Lowest latency and power | No memory protection |
| **I2** | Linux Embedded | Yocto, Buildroot, Ubuntu Core, containers, A/B OTA. | Rich ecosystem | Footprint, patching duty |
| **I3** | High-Level Firmware | Arduino, MicroPython, CircuitPython. | Fastest prototype | Limited control |
| **I4** | Connected Fleet | Devices + cloud: provisioning and identity per device, MQTT / IoT hub (AWS IoT, Azure IoT Hub), signed OTA with rollback, telemetry pipeline. | Manageable at scale | Two systems to secure; update failures brick devices |

**J — Systems Software**

| Option | Name | Description | Pros | Cons |
|---|---|---|---|---|
| **J1** | Kernel / Driver | OS kernels, drivers, eBPF, hypervisors — C, Rust (Rust-for-Linux). | Platform capability | Crashes take the machine down; strict review |
| **J2** ⭐ | Engine / Runtime / Compiler | Database engines, VMs, compilers, language runtimes, storage — Rust, C++, Zig, Go. | Performance, control | Correctness at scale: fuzzing, property tests, benchmarks as gates |
| **J3** | Scientific / HPC | Simulations and numerics — C++, Fortran, Julia, CUDA / HIP, MPI, SLURM. | Cluster-scale compute | Reproducibility across hardware, numerical drift |

**K — Business Platform**

| Option | Name | Description | Pros | Cons |
|---|---|---|---|---|
| **K1** ⭐ | Configuration / Low-code | Declarative config and flows (Salesforce Flow, Power Apps / Automate, ServiceNow Flow Designer). | Fastest, vendor-supported upgrades | Hidden complexity, weak testing and diffing |
| **K2** | Platform Code | Apex / LWC, Power Fx + plugins (C#), ABAP / SAP BTP, ServiceNow scripts; source-tracked metadata, CI deploys. | Full platform power | Governor limits, vendor release cadence |
| **K3** | Marketplace App | AppExchange / AppSource / Shopify app: packaged, multi-org, security review. | Distribution through the vendor | Security review, multi-tenant packaging |

Devices, desktop clients and commercial libraries sold in the EU fall under the Cyber Resilience
Act (vulnerability reporting from 11 Sep 2026, full obligations from 11 Dec 2027) — note it in the
constitution when it applies.

## Level 3 — Technology brackets

```
A  A1 Rails 8, Laravel, Django, ASP.NET Core (Razor / Blazor SSR), Next.js / Nuxt / SvelteKit / React Router 7
   A2 ASP.NET Core modular monolith, Spring Boot + Spring Modulith, NestJS, Django apps, Phoenix contexts
   A3 Go, ASP.NET Core minimal APIs (+ .NET Aspire locally), Rust (Axum), Kotlin (Ktor)
   A4 TypeScript (Workers, Lambda, Vercel), Python / C# (Lambda, Azure Functions), containers on Cloud Run / Container Apps
   A5 Python (FastAPI + LangGraph / Pydantic AI), TypeScript (Vercel AI SDK, Mastra), C# (Microsoft.Extensions.AI);
      retrieval pgvector / Azure AI Search / Qdrant · evals promptfoo / Ragas / DeepEval · tracing OTel GenAI, Langfuse
   A6 Java / Kotlin (Spring Cloud Stream, Kafka Streams, Flink), C# (MassTransit, Wolverine), Go, Python (Faust / Bytewax)
B  B1 Astro, Hugo, 11ty, Starlight / VitePress · B2 Astro or Next.js + a headless CMS · B3 Hono, Flask, PHP + htmx
C  C1 Swift, Kotlin, C# (WinUI 3), C++ (Qt 6) · C2 Dart (Flutter), TS (React Native + Expo), Kotlin (CMP), C# (MAUI / Avalonia), Rust + TS (Tauri 2)
   C3 TypeScript (PWA, Capacitor, Electron), C# (Blazor Hybrid)
D  D1 Go / Python / Rust std, TS without runtime deps (npm + JSR) · D2 the ecosystem toolchain (uv, tsdown, cargo, Gradle, dotnet pack)
   D3 pnpm + Turborepo / Nx, uv / Cargo workspaces, changesets · D4 Solidity + Foundry, Move (Aptos / Sui), Rust (Anchor)
E  E1 Go (cobra), Rust (clap) · E2 Go, Rust · E3 Rust / Go host + WASM components · E4 OpenTofu / Terraform, Pulumi, Bicep, Ansible
   E5 TypeScript or Python MCP SDK (most mature), C#, Go; stdio locally, streamable HTTP + OAuth remotely
F  F1 C# (Unity), C++ (Unreal 5), GDScript / C# (Godot 4), Rust (Bevy) · F2 Rust (wgpu), C++ (SDL3, Vulkan), C# (MonoGame)
   F3 TypeScript (Phaser, PixiJS, Three.js / Babylon.js) · F4 Unity / Unreal + OpenXR, Swift (RealityKit), Three.js WebXR
G  G1 TS + plain manifest · G2 TS + Vite / CRXJS · G3 TS + WXT · G4 TS (VS Code API, Office.js, Figma, Bolt for Slack, Teams SDK), Kotlin (IntelliJ Platform)
H  H1 Python (Jupyter, marimo), Quarto, Julia (Pluto) · H2 Python + modules + uv, R + renv · H3 Python src layout + pytest, R package
   H4 SQL + dbt, Python (Dagster / Airflow, Polars, PySpark), DuckDB; tests: dbt tests / Great Expectations / Soda
   H5 Python (PyTorch, Hugging Face, MLflow, Kubeflow / Vertex / Azure ML), serving vLLM / KServe / Triton / BentoML
I  I1 C (Zephyr, FreeRTOS, ESP-IDF), Rust (Embassy, esp-hal) · I2 C / C++, Rust, Go, Python on Yocto · I3 C++ (Arduino), MicroPython
   I4 device as I1 / I2 + cloud: AWS IoT Core / Azure IoT Hub / EMQX, Mender / SWUpdate / RAUC for OTA
J  J1 C, Rust (Rust-for-Linux, eBPF with Aya / libbpf) · J2 Rust, C++20, Zig, Go · J3 C++ / Fortran + MPI / OpenMP, CUDA / HIP, Julia
K  K1 Salesforce Flow, Power Apps / Automate, ServiceNow · K2 Apex + LWC (sf CLI), Power Fx + C# plugins (pac CLI), ABAP / RAP, ServiceNow SDK
   K3 Salesforce 2GP managed packages, AppSource (Teams / Dynamics), Shopify (Remix app template)
```

**2026 baseline — present once after Level 3, as recommendations, never as gates:** OpenTelemetry
for traces, metrics and logs · dependency + secret scanning in CI and an SBOM per release · OIDC
sign-in with passkeys where users log in · IaC for anything deployed · lock files committed ·
AI coding agents governed by the constitution (what they may read, push, deploy).
