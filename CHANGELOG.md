# Changelog

All notable changes to the Hermes Spec Kit project.

Format: [Keep a Changelog](https://keepachangelog.com/).

---

## [Unreleased]

### Changed

- **history.md is a record, not a story.** Fixed-field entries (timestamp |
  phase | skill | agent; Artifacts, Tests, Evidence, Commit, Note ≤ 25 words;
  ≤ 60 words total), appended by the new `append_history` MCP tool or the
  shipped `spec-kit/scripts/spec-kit-log.sh` — both stamp the real UTC time.
  Narrative moves to implementation-summary.md. `history-tracking.md` and the
  template rewritten; the Shared Commit Procedure uses the appender.

- **Skill diet.** Every `src/skills/<skill>.md` is now a one-screen checklist
  (≈40 lines: phase, persona, purpose, before-writing, steps, done-when, next);
  the full procedure moved to `src/references/skills/<skill>.md` and is loaded on
  demand. Phase skills no longer ask to load `spec-kit-workflow` — preflight
  carries the guardrails and the MCP phase card carries the state. Per-phase
  instruction load drops from 6–10 k tokens to roughly 2.7 k (most of it the
  shared preflight). `test_skills.py`
  enforces the ≤ 110-line limit and the pointer to the full procedure; both
  installers ship `references/skills/`.

- **MCP server v3 — derive-and-enforce, no persisted state.** `state.json` was a
  second source of truth that drifted (30 of 34 features out of sync in one
  deployment) and conflicted on every merge. Every tool now derives the phase
  from `specs/<feature>/` on each call and writes nothing (`init_feature`
  creates the directory + history header only). `advance_phase`,
  `close_feature`, `update_artifact`, `project_set_constitution` validate
  against disk. New enforcement tools: `next_id`, `lint_artifacts`,
  `timestamp`, `history_guard`; `get_next_actions`/`get_feature_state` return a
  ten-line phase card to re-read after compaction. Legacy `state.json` is
  flagged and ignored; gitignore template ignores `specs/.spec-kit/`. Tests
  rewritten against real files in temp projects.

### Added

- **Evidence of Done** (`src/references/evidence.md`) — every gate needs an
  oracle the agent did not author (`user`, `ci:<run-id>`, `review:<other-agent>`)
  or evidence files (`output:`, `probe:` under `specs/[feature]/evidence/`).
  Bug status split `claimed` (agent's word) vs `verified` (+`Verified-by`);
  legacy `resolved`/`fixed` read as `claimed`. The implementing agent never
  sets `verified`; summarize never changes statuses and lists unverified
  claims. History records `Implemented-by`; review labels `review:<agent>` or
  `self-review`. External seams require a real-data `probe:` whose shape the
  test fixture must match.

- **Claude Code edition** (`scripts/install-claude.sh`) — installs the same
  skills for Claude Code from the same `src/skills/*.md` sources (generated
  `~/.claude/skills/<name>/SKILL.md` with Hermes tool names translated and a
  "Claude Code edition" header), symlinks `references/`, `templates/` and
  `mcp-server/` to the installed Hermes tree so both agents read identical
  shared files, and registers the spec-kit MCP server for Claude Code at user
  scope (`mcp__spec-kit__<tool>`). Enables dual-agent hand-offs on one `specs/`
  tree (e.g. Claude Code: specify → plan → tasks; Hermes: implement).
  `--no-mcp` and `--uninstall` flags.

## [2.0.0] — 2026-07-10

Version 2 adds an MCP server for deterministic workflow state management,
decouples the constitution from the per-feature phase cycle, and strengthens
the review skill with codebase architecture analysis and a nitpick filter.

### Added

- **MCP server** (`spec-kit-mcp-server/server.py`) — FastMCP stdio server with
  14 tools for deterministic workflow orchestration: `init_feature`,
  `get_feature_state`, `get_next_actions`, `advance_phase`, `project_status`,
  `project_set_constitution`, `list_features`, `reopen_feature`,
  `close_feature`, `update_artifact`, `auto_detect_features`.
  State stored in `specs/.spec-kit/state.json` per project.
- **Project-level state model** — `project {}` namespace in state separates
  constitution status from feature lifecycle. Features start at phase 1
  (specify). Constitution is tracked via `project_status` /
  `project_set_constitution` tools.
- **Workflow bootstrap gate** — `spec-kit-workflow` checks constitution once
  per session and routes to `spec-kit-constitution` if missing. No feature
  skill ever blocks on constitution.
- **Constitution context injection** — Workflow injects constitution principles
  as guidance (not gates) when routing to feature skills.
- **Review scope boundaries** — Pre-implement review has explicit IN/OUT
  scope rules. Project-level issues go to a "Project-Level Notes" section
  instead of blocking the feature.
- **Codebase architecture analysis** — Pre-implement review scans existing
  project structure to evaluate plan fit and integration risk.
- **Best-practice validation** — Pre-implement review researches current
  recommended practices for each technology in the plan.
- **Design soundness evaluation** — Pre-implement review assesses abstraction
  level, scalability, and data flow coherence.
- **Nitpick filter** — Both review modes explicitly skip cosmetic/style
  findings. Minimum bar: finding must harm correctness, security, performance,
  maintainability, or testability.
- **Workflow integration tests** (`test_workflow.py`) — 11 tests for happy
  path, prerequisite enforcement, reopen flow, project state, and error cases.
- **Skill validation tests** (`test_skills.py`) — 12 checks for frontmatter,
  phase coverage, reference/template existence, cross-skill links, preflight
  compliance.
- **CI workflow** — GitHub Action runs tests on every commit.
- **`uninstall.sh`** — full spec-kit removal including MCP config.
- **Auto-install** of `mcp` Python SDK in `~/.hermes-venv/` during setup.

### Changed

- **Constitution decoupled from features** — Was per-feature phase 0, is now
  project-level bootstrap. Skills no longer BLOCK/HALT/WARN on constitution.
  `advance_phase` refuses phase-0 transitions.
- **`init_feature` starts at phase 1** — No more per-feature constitution
  requirement.
- **Constitution skill uses `project_set_constitution`** — instead of
  `advance_phase(feature="[feature]", from_phase=0)`.
- **Review CRITICAL severity narrowed** — No longer includes constitutional
  alignment. Covers security, data integrity, architecture violations,
  and uncovered requirements only.
- **Review post-implement checks rewritten** — Focus on architecture
  conformance, layer boundaries, error handling chains, security,
  concurrency, structural duplication.
- **MCP server rewritten to FastMCP SDK** — replaces hand-rolled
  Content-Length framing with `mcp` Python SDK's stdio transport.
- **`install.sh` writes `config.yaml` directly** — avoids `hermes mcp add`
  timeout during headless install.
- **Auto-detection of legacy v1 state** — migrates to v2 format on load.

### Removed

- **`log_bug`, `set_bug_status`, `set_bug_plan_ref` MCP tools** — bug
  tracking is purely file-based (`bugs.md` is single source of truth).
  Determined redundant to file operations.
- **Constitution as per-feature prerequisite** — removed from all feature
  skills' prerequisite tables, validation blocks, and enforcement sections.
- **Per-skill constitution context sections** — removed from
  `spec-kit-specify.md` and `spec-kit-plan.md`. Workflow context injection
  handles this once at routing.
- **`spec_kit_` prefix from MCP tool names** — tools use bare names;
  Hermes adds `mcp_spec_kit_` at the client layer.

### Fixed

- LLM no longer suggests running `spec-kit-constitution` mid-feature in
  response to review findings.
- `install.sh` no longer corrupts `config.yaml` with `grep -v`.

---

## [1.0.0] — 2026-06-10

Version 1 is the full skill-based spec-driven development system without
MCP integration. 101 commits built the workflow over ~6 weeks.

### Skills (12)

| Skill | Phase | Purpose |
|-------|-------|---------|
| `spec-kit-workflow` | — | Orchestrator — routes to phase skills |
| `spec-kit-constitution` | 0 | Project principles (brownfield/free-text/wizard) |
| `spec-kit-specify` | 1 | Feature specification |
| `spec-kit-clarify` | 1.5 | Ambiguity resolution |
| `spec-kit-plan` | 2 | Implementation planning |
| `spec-kit-tasks` | 3 | Task breakdown |
| `spec-kit-review` | 3.5 / 5.5 | Quality gate (pre/post implement) |
| `spec-kit-implement` | 4 | Phase-level TDD execution |
| `spec-kit-test` | 5 | Bug tracking |
| `spec-kit-summarize` | 6 | Close/summary with health score |
| `spec-kit-refresh` | — | Artifact reconciliation |
| Umbrella `spec-kit/SKILL.md` | — | Overview and quick reference |

### Three Development Modes

- **Specify** (default): Constitution → Specify → [Clarify] → Plan →
  Tasks → [Review] → Implement → Test → Close
- **Bugfix**: Auto-chains Plan → Tasks → Implement → Test → Close
  (with separate per-phase commits or opt-in `quickfix` batching)
- **Reopen**: Bugfix branch from closed feature, preserves original close,
  additive-only edits, re-close required

### Constitution Decision Tree

- 3 modes: brownfield (auto-detect from 60+ patterns), free-text (describe
  project in a sentence), guided wizard (3-level interactive)
- 9 purpose types (A-I): User-Facing App, Content Site, Native/Desktop,
  Library/SDK, Infra/CLI, Game, Browser Extension, Research/Notebook,
  IoT/Embedded
- 25 architecture variants across all purposes
- 12 constitution principles with purpose-weighted defaults and 3 option
  levels (Strict/Pragmatic/Permissive)
- Monorepo support with per-sub-project purpose/architecture/tech

### Key Behaviors

- **Constitution mandatory** — specify and plan block without it
- **Design phases (0-3) commit individually** — each document change is
  checkpointed
- **Phase-level TDD** — all tests RED first, all code GREEN, one commit
  per phase (optional bypass)
- **Umbrella regression** — one BF-REGRESSION-001 task, not individual bugs
- **Additive-only editing** — spec artifacts never overwritten; mutations
  are append/insert/targeted-patch
- **Phase 6 mandatory** — feature cannot complete without close or summary
- **Spec health score** — computed at close: (resolved + acknowledged) /
  total FRs * 100
- **Branch guardrails** — blocks git operations on main/master
- **Pre-action self-check** (`preflight.md`) — branch, mode, workflow,
  history validation before every action
- **`history.md` append-only** — immutable process log per feature
- **Drift detection** — implementation-summary/close artifact state table
  flagged on stale artifacts
- **Natural language triggers** — skills respond to `spec-kit` prefix,
  `speckit` prefix, and plain NL phrases

### Templates (13)

spec, plan, tasks, constitution, bugs, close, implementation-summary,
data-model, research, history, AGENTS, git-conventions, gitignore.

### References (5)

preflight, auto-commit, history-tracking, constitution-principles,
constitution-tables.

### Filesystem State Detection

Phase determined by artifact presence in `specs/` directory (no MCP):

| Artifacts | Phase |
|-----------|-------|
| constitution.md | Ready to Specify |
| spec.md | Specified |
| clarify.md | Clarified |
| plan.md | Planned |
| tasks.md | Tasked |
| tasks.md with completions | Implementing |
| bugs.md with open bugs | Testing |
| bugs.md all verified | Must close |
| close.md / implementation-summary.md | Complete |

---

## Legend (skill versions)

| Skill | v1 | v2 |
|-------|----|----|
| spec-kit-constitution | 1.0.0 | 2.1.0 |
| spec-kit-implement | 1.0.0 | 1.2.0 |
| spec-kit-review | 1.0.0 | 1.2.0 |
| spec-kit-workflow | 1.0.0 | 1.1.0 |
| All other skills | 1.0.0 | 1.1.0 |
