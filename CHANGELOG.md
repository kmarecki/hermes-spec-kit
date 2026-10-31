# Changelog

All notable changes to the Hermes Spec Kit project.

Format: [Keep a Changelog](https://keepachangelog.com/).

---

## [Unreleased]

### Added — epics and module design docs (opt-in)

- **`spec-kit-epic`** — an epic is one body of work in *time*, run through the same shape as
  a feature in `[epics_dir]/NNN-name/` (NNN = the tracker's epic number, e.g. the ADO epic;
  else `next_id kind="EPIC"`): **E1 specify** `epic.md` (goal, scope and non-goals,
  `EAC-###` epic acceptance criteria with how each is verified, cross-feature rules, epic-level
  Security & Privacy) → **E2 plan** `plan.md` (current state, target architecture, seams
  today → after, `ED-###` cross-feature decisions, sequencing, rollout / rollback, risks) →
  **E3 breakdown** `features.md` (the epic's tasks are features: ordered rows with size,
  depends-on, modules, EACs, status) → **E3.5 review** `review.md` (coverage, fit, sequencing
  + **devil's advocate**: the case against the epic and the ~80 % alternative, a six-month
  pre-mortem, system-level abuse cases, the riskiest assumption; verdict GO / GO-WITH-CHANGES
  / NO-GO, required before the first feature) → **E4 build** (features run the normal
  workflow; `specify` fills the row, each close flips it) → **E6 close** (every EAC verified
  with evidence, close review round, `ED-###` through the ADR bar).
- **`spec-kit-design`** — a living module design doc (`design-doc-template.md` in
  `design_dir`): one bounded part of the system in *space* — purpose, components, data flow,
  seams, invariants and security (`path:line`), testing, debt, ADRs; ≤ 3–4 pages, patched in
  place, never copied to `-v2`. The plan names the modules it touches (`**Modules**:`); the
  feature close patches the affected sections with approval.
- Both are **opt-in**: `epics_dir` / `design_dir` in `specs/git-conventions.md`. A small
  project sets neither and nothing is ever created unprompted; `lint_artifacts` warns when a
  spec or plan names an epic / module the project does not keep, and `project_status` hints
  when 3+ specs share an epic or 3+ closed features share a module without the dir.

### Changed — leaner tiers, the change record, devil's advocate

- **Size tiers are progressively leaner in workflow and artifact length — never in evidence**
  (`references/sizing.md`, `references/evidence.md`). S is for a single bugfix or a small
  enhancement: a few-line spec (1–3 FRs, 1–2 ACs, one Security & Privacy line), a half-page
  plan, a flat task list, one commit for spec+plan+tasks, no pre-implement review. M runs a
  **lite** pre-implement review (coverage, underspecification, codebase fit, design soundness
  + devil's advocate), L the full one. Every tier saves RED/GREEN files per phase and a probe
  per seam, and ends with an acceptance round that documents every AC — automated where a
  harness exists, `manual` with the user's quoted confirmation where none can.
- **`change-record.md` at close** (`change-record-template.md`) — the one page an auditor
  reads: ticket, branch/PR, size, what/why, Security & Privacy impact, data/config changes,
  implemented-by, reviewed-by (agent + human PR reviewer), verification, decisions, deployment
  approval, rollback, follow-ups, and the timeline from git. `close_feature` requires it.
- **Security & Privacy section in spec.md** (authorization / tenant boundary, personal data,
  new surface, input validation, logging) — "None — because …" is a valid answer; the plan
  answers each non-empty row, the pre-implement review checks it, the final review §2 verdicts it.
- **`history.md` is a project setting, default `history: large`** (git-conventions.md:
  `always | large | never`; spec.md `**History**: on | off` overrides per feature). Size L keeps
  the per-phase record (entry before every commit, `history_guard` enforces); S/M do not — the
  close builds the change record's timeline from the branch's git log
  (`scripts/spec-kit-history.sh`, before the squash) and `Implemented-by` lives in the tasks.md
  header. The MCP server stores nothing: the setting is in the files, so both agents and every
  machine see the same answer and it travels with the PR. `init_feature` writes history.md only
  under `always`; `lint_artifacts` requires it only when on. `references/commits.md` replaces
  `auto-commit.md`. Commit hashes are still never recorded.
- **Final review is exceptions-only** (`review-final-template.md`): §1 is one coverage line +
  rows for ⚠️ / ❌ / ↔ / 👤 (the AC matrix lives in acceptance.md, the FR map in tasks.md). New
  verdict **`AWAITING-OWNER`** — no defect, owner confirmations pending; a specs-only Round
  N+1 with the owner's quoted answers turns it READY without a bugfix cycle. `close_feature`
  names the owner instead of sending the feature to bugfix.
- **Devil's advocate pass in both reviews** (§4 of the final round; a section of the
  pre-implement report): strongest case against + simpler alternative, pre-mortem, abuse cases
  per seam, riskiest assumptions; concrete break attempts and "would this test still pass if
  the code were wrong?" after implementation. ≤ 5 objections, each answered (accepted /
  rebutted with evidence / deferred); unanswered blocks READY for L, where it runs as a separate
  sub-agent. The final review reads code and spec **before** decisions.md.
- **One close template.** `implementation-summary-template.md` is gone; `close-template.md`
  carries the gap table at the depth the tier needs (M exceptions, L "summarize" full).
  `implementation-summary.md` is still recognised as a legacy close document.
- **Deduplicated skills.** One-screen SKILL.md files are ≤ 60 lines; `references/skills/*.md`
  hold only the delta (clarify and refresh need none). `preflight.md` 173 → 40 lines; the
  workflow procedure 331 → 70; the tasks template is a legend plus one example, not a
  greenfield scaffold; the umbrella and workflow skills no longer trigger on phase commands.
  Whole skill set: ~85k → ~45k tokens; `test_skills.py` enforces the budget.
- `decisions.md` records only questions the **user** would want to decide; design choices
  within the plan's remit stay in plan.md (preflight check 6).
- Installers: `install.sh` moves unshipped top-level references aside (`references/local/`)
  and removes superseded full procedures; the Claude edition note block is four lines.

## [Previous unreleased]

### Added

- **Acceptance criteria and the automatic acceptance loop** (`references/acceptance.md`).
  spec.md criteria are `**AC-###** (FR-…) Given/When/Then — Verify: <level>`, the level being
  the lowest that proves it (unit · integration · component · e2e (reason) · command · probe ·
  manual (reason)). The plan maps each AC to a harness and test file; tasks tag the tests
  `[TEST] [AC-###]` and test names carry the id. Implement freezes the acceptance tests after
  their RED run (`acceptance_freeze`). After implement, `accept [feature]` (spec-kit-test
  accept mode) runs the full fast suites plus only this feature's e2e specs (only when the
  stack is up — else deferred), builds the AC matrix from JUnit/TRX (`acceptance_status`),
  logs every failure as a bug and auto-chains the bugfix loop, round after round, until PASS
  or a stop condition (5 rounds, no progress, spec or frozen-test change, run cannot
  execute). `acceptance.md` rounds (Result + Commit) gate the final review and the close.
- **Final review (phase 5.5) — mandatory merge gate.** `spec-kit-review` final mode replaces
  the optional post-implement review: requirement-by-requirement spec conformance (code
  `path:line` + proving test), every applicable constitution MUST / project rule verdicted,
  code quality and best practice, test quality, and a merge checklist
  (`specs/merge-checklist.md`, template `merge-checklist-template.md`) whose commands run with
  saved evidence. Output: `review-final.md` rounds with `**Verdict**` and `**Reviewed-commit**`.
  CRITICAL/HIGH findings become bugs. Prefers the other agent or a fresh-context sub-agent.
- **ADRs and AGENTS.md at close.** `spec-kit-summarize` harvests decisions (decisions.md
  rulings, plan rounds, research, review findings, deviations), applies the ADR bar, and
  writes / supersedes / amends project ADRs (project template, else `adr-template.md`),
  updates the ADR index, and proposes targeted AGENTS.md patches. Close documents carry an
  `## Architecture Decisions` table.
- **Size tiers S / M / L** (`references/sizing.md`): specify always asks, recommendation
  first; `**Size**:` in spec.md. S trims the templates and auto-chains specify → plan → tasks
  into one commit; L requires the pre-implement review. Evidence, history and the final-review
  gate do not shrink with the tier.
- MCP: `diff_scan` tool (merge conflicts, secrets, forbidden files, focused tests, TODOs,
  unplanned files); `next_id(kind="ADR")`; `get_feature_state` reports `size` and
  `final_review` (verdict, reviewed commit, stale); `advance_phase(5)` and `close_feature`
  require a fresh READY final review, `close_feature` an Architecture Decisions section;
  `lint_artifacts` checks review-final rounds, the Size line and the ADR section;
  `project_status` reports the merge checklist and ADR directory.
- git-conventions template: `## Documentation locations` (`adr_dir`, `adr_index`,
  `agents_file`, `merge_checklist`).

### Fixed

- **install.sh / uninstall.sh corrupted `~/.hermes/config.yaml`** when the
  `spec-kit` MCP block was written with `args:` as a YAML list (4 lines): the
  line-count `sed` left a dangling `- …server.py` line and appended a second
  `mcp_servers:` key. Replaced by `scripts/hermes-mcp-config.py`, which edits
  by indentation, keeps other servers, reuses an existing `mcp_servers:` key
  and backs the file up first.

### Changed

- **Hygiene.** (1) Assumptions log: `decisions-template.md` and preflight
  check 6 — an ASK that no human answered is recorded as an *assumption* with
  the alternative not taken, never as a self-made ruling; real rulings quote
  the user; reviews read `decisions.md` first and the close lists open
  assumptions. (2) `--no-verify` removed everywhere: hooks are the project's
  guardrails. (3) Commit granularity: one commit per phase carrying its
  status-only document changes; spec-before-code only for requirement or
  design-intent changes.

- **TDD rules that can be checked.** The "Iron Law" (delete code written
  before the test) is replaced by file-based rules: a `[TEST]` task's RED run
  is saved under `specs/[feature]/evidence/` before implementation; a `[SEAM]`
  task (database function, HTTP contract, file format, external service) starts
  with a read-only probe of the real system and its fixture must match the
  probe's shape; legacy code gets a characterisation test first; GREEN and the
  regression runs are saved too. tasks template documents `[TEST]`/`[SEAM]`;
  `lint_artifacts` warns on `[SEAM]` done without a probe file and `[TEST]`
  done without a RED file.

- **plan.md: Current Design + ADR rounds.** The plan template gains a
  `## Current Design` section (≤ 1 page, what is built; regenerated at every
  close and by refresh — the only replaced section) and a `## Rounds (ADR log)`
  section where each bugfix/reopen round appends one dated entry (Context /
  Decision / Consequences / Plan Ref) naming what it supersedes. Append-only
  plans no longer contradict themselves across rounds. `lint_artifacts` warns
  when a closed feature's plan lacks the section.

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
