# Constitution Principles Reference

This reference defines the canonical set of project principles, each with 3
options spanning conservative → pragmatic → minimal. The agent presents these
options to the user (or auto-selects based on brownfield detection) and writes
the chosen option into `specs/constitution.md`.

## How to Use

For each principle, present the 3 options as a table with pros and cons. Let
the user pick. In brownfield mode, mark the detected option with ⭐.

---

## Principle 1: Testing Philosophy

| Option | Rule | Pros | Cons |
|--------|------|------|------|
| **A — Strict TDD** | MUST write failing test before production code. Coverage MUST be ≥80%. | Catches regressions early, documented behavior, enables refactoring | Slower initial velocity, test maintenance cost, over-engineering simple things |
| **B — Pragmatic TDD** | Tests SHOULD be written first for core logic. Integration tests MUST cover critical paths. Simple code (getters, config) MAY skip tests. | Good coverage where it matters, faster for trivial code, balances speed and safety | Inconsistent coverage, "is this core logic?" debates, tests-after drift |
| **C — Test-After / Manual** | Manual QA preferred. Automated tests written for bug regressions only. | Fastest initial shipping, zero test debt, low barrier | No safety net, regressions go undetected, hard to refactor, no documentation of behavior |

---

## Principle 2: Code Quality & Linting

| Option | Rule | Pros | Cons |
|--------|------|------|------|
| **A — Strict** | Linter MUST pass. All warnings MUST be addressed. Type errors MUST be zero. Pre-commit hooks enforced. | Consistent codebase, catches bugs early, self-documenting | Slower commits, friction on prototypes, learning curve for strict rules |
| **B — Pragmatic** | Linter SHOULD pass. Warnings MAY be suppressed with inline comment (document why). Pre-commit hooks recommended but not enforced. | Good baseline quality, no blocked commits for minor style, team can iterate | Warning creep over time, inconsistent suppression quality, bikeshedding on rules |
| **C — Minimal** | No mandatory linting. Formatting conventions in README only. Code review catches style issues. | Zero friction, fastest iteration, complete team freedom | Inconsistent codebase, reviewer fatigue on style, onboarding friction |

---

## Principle 3: Architecture

| Option | Rule | Pros | Cons |
|--------|------|------|------|
| **A — Clean Architecture** | Layers MUST be explicit (domain → application → infrastructure). Dependency inversion required. Business logic MUST NOT depend on frameworks. | Highly testable, framework-independent, clear boundaries, scales well | Significant boilerplate, over-engineering for small projects, abstraction cost |
| **B — Modular Monolith** | Modules SHOULD have explicit boundaries but MAY share infrastructure. No circular dependencies. Patterns evolve with proven need. | Good separation without overhead, pragmatic for most projects, easy to start | Boundaries blur over time, hard to split later, requires discipline |
| **C — YAGNI / Flat** | Package by layer (models, services, controllers). Refactor only when patterns emerge. No abstractions before they're needed. | Fastest to build, minimal boilerplate, easy to understand for newcomers | Tight coupling over time, hard to test in isolation, costly refactors |

---

## Principle 4: Dependencies & Third-Party

| Option | Rule | Pros | Cons |
|--------|------|------|------|
| **A — Minimal** | Zero runtime dependencies unless absolutely necessary. Prefer stdlib. Pin exact versions. Regular audit (Dependabot/Renovate). | Low attack surface, no supply chain risk, stable builds | Reinventing wheels, more custom code to maintain, slower delivery |
| **B — Curated** | Dependencies MAY be used with justification. Prefer well-maintained libraries (1K+ GitHub stars, recent commits). Lock files committed. | Good balance of speed and safety, leverages community, standard patterns | Supply chain risk, upgrade burden, transitive dependency bloat |
| **C — Permissive** | Any dependency is acceptable. Latest version preferred. No lock file. | Fastest delivery, leverage best-in-class libraries, minimal custom code | Highest supply chain risk, breaking changes unexpectedly, builds not reproducible |

---

## Principle 5: Git Workflow

| Option | Rule | Pros | Cons |
|--------|------|------|------|
| **A — Trunk-Based** | Short-lived feature branches (<1 day). Direct merge to main. Feature flags for incomplete work. | Fastest CI, no merge hell, easy rollbacks, true continuous integration | Requires feature flags infrastructure, discipline on branch lifetime, not suitable for large teams |
| **B — Feature Branches** | Feature branches with linear history (rebase). PR review required. Squash merge to main. | Clean history, review gate, works at any team size, industry standard | Merge conflicts on long branches, squash loses granular commits, review bottleneck |
| **C — Git Flow** | `develop` + `main` + release/hotfix branches. Feature branches merge to develop. Releases branch from develop. | Structured releases, hotfix isolation, clear semantics, battle-tested | Heavy overhead, complex history, not needed for CI/CD, release cadence rigidity |

---

## Principle 6: Documentation

| Option | Rule | Pros | Cons |
|--------|------|------|------|
| **A — Exhaustive** | MUST update docs with every change. API docs, architecture decisions (ADR), changelog, inline comments for non-obvious code. | Onboarding is fast, decisions are recorded, API consumers understand without reading code | Significant maintenance burden, docs go stale, slows iteration, low ROI for stable APIs |
| **B — Critical-Only** | MUST document: public API surfaces, architecture decisions (lightweight ADR), setup/run steps. Code SHOULD be self-documenting. | High-value documentation without overhead, ADRs capture why decisions were made, setup docs prevent blockers | Internal logic undocumented, onboarding still requires code reading, "critical" is subjective |
| **C — Code-As-Docs** | Code IS documentation. README covers setup and one example. Type signatures and tests serve as documentation. | Zero documentation debt, always accurate, forces clean code | Hard onboarding for non-trivial projects, no design rationale captured, type system literacy required |

---

## Principle 7: Error Handling

| Option | Rule | Pros | Cons |
|--------|------|------|------|
| **A — Defensive** | EVERY external call MUST be wrapped in try/catch. User-facing errors MUST have friendly messages. Internal errors MUST be logged. Logging at every boundary. | No silent failures, great user experience for errors, full observability | Verbose code, error-handling boilerplate exceeds business logic, over-logging hides real issues |
| **B — Contract-Based** | External boundaries have error handling. Internal code uses Result types or panics for truly exceptional cases. Structured logging at service boundaries. | Clean business logic, errors where they matter, good observability | Requires Result type discipline, inconsistent if not enforced, edge cases fall through |
| **C — Minimal** | Errors propagate up. Top-level handler catches all. Minimal logging. | Least code, straightforward flow, maximum velocity | Poor debugging experience, user sees stack traces, failures may go unnoticed |

---

## Principle 8: Performance

| Option | Rule | Pros | Cons |
|--------|------|------|------|
| **A — Optimize-First** | Performance requirements MUST be defined upfront. All data structures and algorithms chosen for performance. Profiling before optimization. | Predictable performance, appropriate architecture from the start, no rewrites needed | Over-engineering for most use cases, premature optimization, slower delivery, complex code |
| **B — Profile-Then-Optimize** | Write clean code first. Profile to find bottlenecks. Optimize measured hotspots only. Performance budgets for critical paths. | Good-enough performance by default, effort spent where it matters, data-driven | Performance issues may be baked into architecture, late discovery of foundational problems, profiling infra needed |
| **C — Ignore-Until-Painful** | Ship first. If performance is unacceptable, optimize then. No performance requirements upfront. | Fastest to ship, simplest code initially, YAGNI applied | May require significant re-architecture, poor first impression, hard to predict when pain will hit |

---

## Principle 9: Code Review

| Option | Rule | Pros | Cons |
|--------|------|------|------|
| **A — Strict Review** | ALL code MUST be reviewed. At least 1 approval required. Reviewers MUST verify test coverage, error handling, and edge cases. No self-merge. | High quality bar, knowledge sharing, catches subtle bugs | Review bottleneck, slows delivery, reviewer fatigue, superficial reviews at scale |
| **B — Risk-Based Review** | Core/risk code MUST be reviewed. Trivial changes (typos, config, comments) MAY be self-merged. Review depth proportional to risk. | Good coverage where it matters, fast for trivial changes, focuses reviewer attention | "Is this trivial?" debates, inconsistent gate quality, risk assessment is subjective |
| **C — Post-Merge Review** | All changes merged immediately. Review happens after merge. Issues become bugs. | Fastest delivery, no blocking, encourages small frequent commits | Bugs reach production, no knowledge sharing before merge, culture of speed over quality |

---

## Principle 10: Database & Schema

| Option | Rule | Pros | Cons |
|--------|------|------|------|
| **A — Migration-First** | ALL schema changes MUST be additive migrations. No rollback — deploy forward. Migrations are code-reviewed separately. | Safe deployments, easy roll-forward, full change history | Migration file accumulation, no rollback strategy, complex state management |
| **B — State-Based** | Schema is defined as desired state. Tool computes diff. Migrations are auto-generated. Manual review before apply. | Less boilerplate, no manual migration files, clear desired state | Tool lock-in, auto-generated migrations may have edge cases, harder to review |
| **C — Ad-Hoc** | Schema changes applied directly. Backup before changes. No formal migration system. | Fastest for prototypes, zero migration tooling overhead | No change history, team coordination failures, production incidents from manual changes |

---

## Principle 11: Configuration & Secrets

| Option | Rule | Pros | Cons |
|--------|------|------|------|
| **A — Strict Isolation** | Secrets NEVER in code. Vault/external secret store required. Config per environment in dedicated files. Schema validated at startup. | Maximum security, no secret leaks in git, env isolation guaranteed | Higher setup cost, Vault operations overhead, startup fails on missing config |
| **B — Environment-Based** | Secrets via environment variables. Config files with env-specific overrides. `.env.example` committed, `.env` gitignored. | Simple setup, standard pattern, good-enough isolation | Secrets can leak via env dump, no rotation built-in, `.env` sprawl |
| **C — Config-In-Repo** | Config files committed with all values. Secrets use placeholder values with documented setup. | Simplest possible, everything in version control, new devs have zero config friction | Secrets eventually committed by accident, no isolation, compliance risk |

---

## Principle 12: Dependencies (Dev)

| Option | Rule | Pros | Cons |
|--------|------|------|------|
| **A — Minimal Dev Deps** | No dev tooling beyond language stdlib + test runner. No formatters, linters, task runners beyond what the ecosystem ships. | Zero dependency overhead, no tooling debates, CI stays fast | Manual formatting, inconsistent style, missing automated safety nets |
| **B — Standard Toolchain** | Standard formatter (Prettier/ruff/gofmt), linter (eslint/pylint/golangci-lint), and test runner. Task runner for common commands. | Consistent code, automated quality, team-wide standards, CI integration | Tooling config becomes a project, version disagreements, CI time overhead |
| **C — Full DX Pipeline** | Everything: formatter + linter + type checker + test runner + commit hook (husky/lefthook) + commit lint (commitlint) + changelog generator. | Maximum automation, enforced consistency, professional DX | Significant configuration debt, CI time, tooling churn, team must learn all tools |

Let the user pick for each principle. In brownfield mode, scan project files first
and mark detected preferences with ⭐.
