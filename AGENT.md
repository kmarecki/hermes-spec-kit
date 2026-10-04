# Hermes Spec Kit — Agent Instructions

Project-level context for Hermes Agent when working on the **spec-kit** repository.
Read this file before making any changes. It covers architecture, conventions, phase
state machine, MCP integration, testing, and how skills/templates/references are
organized and maintained.

**This is the AI agent's working context — not a user-facing guide.**
For users, see `user-guide.md` (workflow docs) and `README.md` (quick start).

---

## Project Identity

| Field | Value |
|-------|-------|
| Repository | `kmarecki/hermes-spec-kit` |
| What it is | Spec-driven development (SDD) workflow for Hermes Agent — 12 skills + MCP server |
| License | MIT |
| Author | Hermes Agent |
| Maturity | Active development — `feat/mcp-orchestrator` branch |
| Source of truth for specs | `specs/` directory in consumer projects |
| Source of truth for state | `specs/.spec-kit/state.json` (MCP) OR filesystem artifact detection (fallback) |

---

## Architecture Overview

The system has three operational layers plus an optional MCP state layer:

```
┌──────────────────────────────────────────────────────────────┐
│             Workflow Orchestration Layer                      │
│  spec-kit-workflow — routes user intent → phase skill        │
│  Phase detection via artifact scan or MCP state              │
│  Session continuity detection for cross-session resumption   │
├──────────────────────────────────────────────────────────────┤
│              12 Phase Skills Layer                            │
│  One skill per phase + 2 supporting (refresh, review)        │
│  Each skill: preflight → phase work → history append → commit│
│  All skills loadable independently, none depend on each      │
│  other at runtime (only on artifact state)                   │
├──────────────────────────────────────────────────────────────┤
│              Artifact & Storage Layer                         │
│  Markdown files in specs/ — additive-only, never overwritten │
│  Templates in spec-kit/templates/ — 13 templates             │
│  References in spec-kit/references/ — 5 shared files         │
│  history.md — append-only process log per feature            │
├──────────────────────────────────────────────────────────────┤
│              MCP State Management Layer (optional)            │
│  FastMCP stdio server — 11 tools for deterministic state     │
│  State stored in specs/.spec-kit/state.json                  │
│  Fallback: filesystem-based artifact detection               │
│  All skills backward-compatible with or without MCP          │
└──────────────────────────────────────────────────────────────┘
```

### Key Architectural Principles

1. **Skills are self-contained** — each phase skill has full instructions for its
   phase, references preflight.md for shared checks, and never calls another skill.
2. **Routing is separate from execution** — `spec-kit-workflow` routes but never
   executes phase work. Phase skills execute but never route.
3. **Artifacts are the source of truth** — the filesystem (specs/ directory) is the
   primary state store. MCP server mirrors and enhances it with deterministic tools,
   but is optional.
4. **Additive-only mutation** — no spec artifact is ever overwritten. All edits are
   append, insert, or targeted patch. This is enforced at every phase.
5. **Phase 6 is mandatory** — a feature is not complete until Close/Summarize is
   done. This prevents feature accretion and ensures traceability.

---

## Three Development Modes

| Mode | When | Trigger | Phase Sequence | User Involvement |
|------|------|---------|---------------|-----------------|
| **Specify** (default) | New feature, low uncertainty | "Create a spec for..." | Constitution → Specify → [Clarify] → Plan → Tasks → [Review] → Implement → Test → Close | Manual — user says "plan", "implement", etc. |
| **Bugfix** | Working feature with known bugs | "bugfix [feature]" | Auto-chain: Plan → Tasks → Implement → Test → Close | Minimal — inner loop is automatic |
| **Reopen** | Closed feature needs more work | "reopen [feature]" | Creates bugfix branch from main, preserves original close, routes through bugfix loop | Additive-only edits; must close again |

### Bugfix vs Quickfix

- **bugfix** (default): separate commits per phase — plan commit, tasks commit,
  implementation commits. Full traceability.
- **quickfix** (user opt-in): one batch commit for trivial fixes (config typos,
  obvious one-liners). Plan ref and task entry still exist in docs.

---

## Phase Reference — Complete

| Phase | Skill | Artifact(s) | Prerequisite | Code Allowed? | Persona |
|-------|-------|-------------|-------------|---------------|---------|
| **Project** | `spec-kit-constitution` | `specs/constitution.md` | None (one-time project setup) | ❌ | Project designer |
| 1 | `spec-kit-specify` | `specs/NNN-name/spec.md` | None (creates first feature artifact) | ❌ | Product manager |
| 1.5 | `spec-kit-clarify` | `specs/NNN-name/clarify.md`, amends spec.md | spec.md | ❌ | Requirements analyst |
| 2 | `spec-kit-plan` | `plan.md`, `research.md`, `data-model.md`, `contracts/*`, `quickstart.md` | spec.md | ❌ | Architect |
| 3 | `spec-kit-tasks` | `specs/NNN-name/tasks.md` | plan.md + spec.md | ❌ | Tech lead |
| 3.5 | `spec-kit-review` | Review report (pre/post implement) | Pre: spec+plan+tasks / Post: spec+code | ❌ | Quality engineer |
| 4 | `spec-kit-implement` | Source code, `tasks.md` (completions), `bugs.md` (mark resolved) | tasks.md | ✅ | Developer |
| 5 | `spec-kit-test` | `specs/NNN-name/bugs.md` | Implement (or spec for bugfix) | ❌ | QA engineer |
| 6 | `spec-kit-summarize` | `close.md` or `implementation-summary.md`, patched spec/plan | Implement + Test (or bugs all verified) | ❌ | Reviewer |
| — | `spec-kit-refresh` | Patched spec/plan/data-model/contracts | Any (standalone) | ❌ | Archivist |

### Phase 6 — Mandatory Close

No feature enters Complete state without Phase 6. The close artifact includes:

- **Spec health score**: `(resolved + acknowledged) / total FRs * 100`
- **Gap analysis**: which FRs were deferred or only partially met
- **Deviation patching**: spec.md and plan.md patched to reflect intentional
  deviations
- **One commit**: `spec(phase-6): [feature] summary (health: N%)`

---

## Phase State Machine

### Artifact → Phase Mapping

| Artifacts Present | Implied Phase |
|------------------|---------------|
| constitution.md only (project root) | Project bootstrapped — ready to specify |
| spec.md exists | Specified (Phase 1) |
| clarify.md exists | Clarified (Phase 1.5) |
| plan.md exists (no tasks.md) | Planned (Phase 2) |
| tasks.md exists (no completions) | Tasked (Phase 3) |
| tasks.md with [X] completions | Implementing (Phase 4) |
| bugs.md with open bugs | Testing / Bugfix loop (Phase 5) |
| bugs.md all verified, no close.md | Testing complete — must close |
| close.md or implementation-summary.md exists | Complete (Phase 6) |
| close.md + bugs.md with open bugs | Reopened — bugfix in progress |

### Prerequisite Graph (enforced by MCP server and skills)

**Constitution is NOT a feature-level prerequisite.** It is project-level
bootstrap state, checked once by the workflow orchestrator before routing.
Features start at Phase 1 (specify) and have no constitution dependency.

```
Phase 1 (specify)      — no feature-level prereqs
       ↓
Phase 1.5 (clarify)    — needs spec.md
       ↓
Phase 2 (plan)         — needs spec.md
       ↓
Phase 3 (tasks)        — needs plan.md + spec.md
       ↓
Phase 3.5 (review)     — needs spec + plan + tasks (pre) or spec + code (post)
       ↓
Phase 4 (implement)    — needs tasks.md
       ↓
Phase 5 (test)         — needs implement (phase 4 done)
       ↓
Phase 6 (close)        — needs implement + test (phases 4 + 5)
```

### Phase Transitions via MCP

When the MCP server is active, every phase transition goes through
`mcp_spec_kit_advance_phase` which validates feature-level prerequisites,
updates artifact status, and records the transition timestamp.

**Rule**: Only the skill that OWNS a phase transition may call `advance_phase`.
The specify skill advances 1→2. The constitution skill does NOT call
`advance_phase` — it calls `project_set_constitution`. Never advance a phase
outside its owning skill context.

---

## MCP Server Integration

### Location
- Source: `spec-kit-mcp-server/server.py`
- Installed to: `~/.hermes/skills/spec-kit/mcp-server/server.py`
- State file: `specs/.spec-kit/state.json` (per-project)
- Framework: FastMCP (stdin/stdout transport)

### MCP Tools (prefixed `mcp_spec_kit_` in Hermes)

| Tool | Purpose | When to Call |
|------|---------|-------------|
| `init_feature` | Register new feature in state (starts at phase 1) | In specify skill when creating a new feature |
| `get_feature_state` | Get phase, artifacts, bugs for a feature | Phase detection, status queries |
| `get_next_actions` | Available actions from current phase | After any phase work, to show user what's next |
| `advance_phase` | Validate and transition to next phase | In the phase skill that owns the transition |
| `project_status` | Get project-level state (constitution status) | Workflow orchestrator bootstrap check |
| `project_set_constitution` | Mark constitution as present after creation | In constitution skill (NOT advance_phase) |
| `list_features` | List all registered features | Status queries, diagnostics |
| `reopen_feature` | Reopen closed feature | Reopen flow |
| `close_feature` | Mark feature closed | After Phase 6 close is written |
| `update_artifact` | Sync artifact status independently | After writing an artifact file |
| `auto_detect_features` | Scan specs/ dir, reconcile state. Detects project constitution from `specs/constitution.md` | First-use, drift recovery |

### Critical MCP Rules

- **`advance_phase`** — only call within the phase skill that owns the transition.
  Never advance a phase from outside its owning skill. Constitution uses
  `project_set_constitution`, not `advance_phase`.
- **`project_set_constitution`** — only call from `spec-kit-constitution` skill
  after writing the constitution file. Never call this from a feature-level skill.
- **Bug tracking is file-based** — `bugs.md` is the single source of truth. The
  MCP server has NO bug tools (removed in adc6b79): bug tools tempted the agent
  to bypass the bugs.md write and user-confirmation step. Bugfix/verify routing
  parses `bugs.md` directly in the skills.
- **Constitution is project state** — features never check or advance it. The
  `project_status` tool is read-only for all skills except `spec-kit-constitution`.
- **Fallback** — when MCP is not configured, all skills fall back to filesystem
  artifact detection. No code changes needed.

### MCP Error Handling

The server returns JSON with either `{"success": true, ...}` or
`{"error": "...", ...}`. Skills must check for `"error"` key before proceeding.
Common errors:
- `"Feature 'X' not found"` — call `init_feature` first
- `"Phase mismatch"` — feature is in a different phase than expected
- `"Feature 'X' is closed"` — must `reopen_feature` first
- `"Prerequisite not met"` — required artifact is absent

---

## Codebase Tour

```
hermes-spec-kit/
├── AGENT.md                          # ← This file — agent project context
├── README.md                         # User-facing quick start
├── user-guide.md                     # Full workflow documentation (1071+ lines)
├── design.md                         # Original system design document
├── automation.md                     # Cron job & automation config
├── migration.md                      # Migration notes (old → new formats)
├── .hermes/                          # Project-level Hermes config (if any)
│
├── src/
│   ├── skills/                       # 12 skill .md files (source of truth)
│   │   ├── spec-kit-workflow.md      # Orchestrator — routes to phase skills
│   │   ├── spec-kit-constitution.md  # Phase 0 — project principles
│   │   ├── spec-kit-specify.md       # Phase 1 — feature specification
│   │   ├── spec-kit-clarify.md       # Phase 1.5 — ambiguity resolution
│   │   ├── spec-kit-plan.md          # Phase 2 — implementation planning
│   │   ├── spec-kit-tasks.md         # Phase 3 — task breakdown
│   │   ├── spec-kit-review.md        # Phase 3.5 — quality review
│   │   ├── spec-kit-implement.md     # Phase 4 — TDD implementation
│   │   ├── spec-kit-test.md          # Phase 5 — bug tracking
│   │   ├── spec-kit-summarize.md     # Phase 6 — close/summary
│   │   ├── spec-kit-refresh.md       # Standalone — artifact reconciliation
│   │   └── spec-kit/
│   │       └── SKILL.md              # Umbrella skill — overview only
│   ├── templates/                    # 13 template files (*-template.md)
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   ├── tasks-template.md
│   │   ├── constitution-template.md
│   │   ├── bugs-template.md
│   │   ├── close-template.md
│   │   ├── implementation-summary-template.md
│   │   ├── data-model-template.md
│   │   ├── research-template.md
│   │   ├── history-template.md
│   │   ├── AGENTS-template.md
│   │   ├── git-conventions-template.md
│   │   └── gitignore-template.md
│   └── references/                   # 5 shared reference files
│       ├── preflight.md              # Pre-action self-check (branch, mode, workflow, history)
│       ├── auto-commit.md            # Standard commit patterns per phase
│       ├── history-tracking.md       # Process history design rationale
│       ├── constitution-principles.md # 12 principles × 3 options with pros/cons
│       └── constitution-tables.md    # Wizard tables and brownfield detection data
│
├── spec-kit-mcp-server/              # MCP server (Python, FastMCP)
│   ├── server.py                     # 11 tools, Python + mcp SDK (<2)
│   ├── test_workflow.py              # 11 MCP integration tests (state machine)
│   ├── test_skills.py                # 12 validation tests (skill file integrity)
│   ├── test_server.py                # Test runner entry point
│   └── README.md                     # MCP server docs
│
├── scripts/
│   ├── install.sh                    # Installs skills + templates + MCP to ~/.hermes/
│   └── uninstall.sh                  # Full clean uninstall
│
├── research/
│   └── sdd-2026.md                   # Industry research on SDD (June 2026)
│
└── specs/                            # Demo/test feature artifacts (not installed)
    ├── bug-life/
    ├── reopen-test/
    └── ...
```

---

## Installation & Testing

### Installing

```bash
./scripts/install.sh
# Then in Hermes: /reload-skills && /reload-mcp
```

The install script:
1. Copies each `src/skills/*.md` → `~/.hermes/skills/<name>/SKILL.md`
2. Copies umbrella `src/skills/spec-kit/SKILL.md` → `~/.hermes/skills/spec-kit/SKILL.md`
3. Copies templates to `~/.hermes/skills/spec-kit/templates/`
4. Copies references to `~/.hermes/skills/spec-kit/references/`
5. Copies MCP server to `~/.hermes/skills/spec-kit/mcp-server/server.py`
6. Auto-configures `~/.hermes/config.yaml` with MCP server entry
7. Cleans up old skill formats (flat `.md` files, renamed/obsolete directories)

### Testing

**MCP server workflow tests** (11 tests):
```bash
cd spec-kit-mcp-server
python3 test_workflow.py
```
Tests: happy path forward, prerequisite enforcement, wrong phase rejection,
duplicate feature, missing feature, reopen flow, reopen guard, update artifact,
next actions progression, auto-detect features.

**Skill validation tests** (12 checks):
```bash
python3 spec-kit-mcp-server/test_skills.py
```
Tests: all skills present, frontmatter YAML, phase coverage, reference/existence,
template existence, cross-skill references, preflight reference, trigger descriptions,
umbrella coverage, reference inventory, workflow diagram phases.

**Run both:**
```bash
cd spec-kit-mcp-server && python3 test_workflow.py && python3 test_skills.py
```

### After modifying skills/templates

Run validation tests before committing to catch:
- Broken YAML frontmatter
- Missing template/reference references
- Cross-skill link rot
- Phase number mismatches
- Missing preflight or workflow references

---

## Conventions & Rules

### File Naming

| Entity | Convention | Example |
|--------|-----------|---------|
| Feature ID | `NNN-kebab-case-name` | `003-user-auth` |
| Feature branch | `feat/NNN-name` or `fix/NNN-name` | `feat/003-user-auth` |
| Skill file | `spec-kit-<phase>.md` | `spec-kit-implement.md` |
| Skill directory | `<name>/SKILL.md` | `spec-kit-plan/SKILL.md` |
| Template | `<name>-template.md` | `spec-template.md` |
| Reference | `<name>.md` | `preflight.md` |
| State dir | `specs/.spec-kit/` | per-project |
| State file | `specs/.spec-kit/state.json` | per-project |

### Git Conventions

- **Design phases (0-3)**: Each phase commits immediately — no batch.
- **Implementation (Phase 4)**: One commit per implement sub-phase.
  All tests RED first, all code GREEN, then commit.
- **Bugfix sub-rounds**: Separate phase commits by default (`bugfix`);
  opt-in batch via `quickfix`.
- **Phase 6 close**: ONE commit — patched spec/plan + close.md.
- **--no-verify**: Always skip pre-commit hooks (they may block spec artifacts).
- **Commit messages**: Follow `auto-commit.md` patterns per skill.
  Template: `spec(phase-N): [feature] description` for spec phases,
  `feat:` / `fix:` for code phases.
- **Branch guardrails**: Block git operations on main/master. Preflight check #1
  enforces this.

### Additive-Only Rule (Universal, All Phases)

**Never overwrite a spec artifact that already has substantive content.**
Every modification must be additive (append new sections, insert new entries)
or targeted-edit (update specific lines/fields).

- **Allowed**: Append new FR-###, mark tasks [X], change bug status,
  insert new sections, patch specific lines.
- **Forbidden**: Delete existing entries, renumber IDs, reformat entire file,
  replace >50% of lines.
- **Exception**: First creation (file doesn't exist yet) — may write from template.
- **history.md is append-only**: Never edit or delete past entries.

Preflight.md section 3 enforces this with a 50-line threshold check.

### Template Path Convention

All skills reference templates as `spec-kit/templates/<name>-template.md` —
NOT bare paths like `templates/<name>.md`. This ensures correct resolution
regardless of Hermes profile or working directory.

### AGENTS.md Downstream Guidelines

When a consumer project uses spec-kit, their `AGENTS.md` should contain:
- Which spec-kit skills are available
- Active spec directories (features in progress)
- Project tech stack and build commands
- Project-specific conventions

AGENTS.md should NOT contain:
- Trigger phrase lists (belong in skill files)
- Routing tables (belong in workflow skill)
- Phase diagrams (belong in user guide)
- Bugfix loop mechanics (belong in skills)

The template at `src/templates/AGENTS-template.md` provides the starter.

---

## Key Design Decisions (with Rationale)

| Decision | Rationale |
|----------|-----------|
| **Constitution is mandatory bootstrap** (project-level), not per-feature | The constitution defines project-wide principles. Once it exists, all features implicitly operate under it. Per-feature blocking was a category error that caused the LLM to suggest running constitution mid-feature. |
| **Constitution is injected as guidance, enforced by review** | Phase skills receive constitution principles as context and use them as guidance. They never gate or block on constitution. The review skill is the designated enforcement point — it checks alignment and reports findings, but doesn't block. |
| **Phase 6 is mandatory** | Prevents feature accretion and half-finished work. Every feature gets a close audit. |
| **Additive-only artifacts** | Prevents AI from accidentally destroying work. The only safe mutation mode for AI-generated content. |
| **Design phases commit individually** | Each design decision is checkpointed. The user can review and amend per-phase without losing prior work. |
| **Phase-level TDD** | Scales TDD to feature level. One RED→GREEN cycle per implement sub-phase, not per function. |
| **TDD bypass at user request** | Not all features benefit from test-first. Pragmatic > dogmatic. |
| **One umbrella regression task** | Individual bugs would create noise. A single BF-REGRESSION-001 task covers the regression round. |
| **MCP is optional** | Keeps the skill set usable even without MCP infrastructure. The filesystem is always available. |
| **Project state separate from feature state in MCP** | Prevents the constitution from being treated as a per-feature phase. Clean separation of concerns between project bootstrap and feature lifecycle. |
| **9 purposes × 25 architectures** | Covers the full spectrum of project types while keeping the decision tree manageable. |
| **Free-text + guided + brownfield** | Three modes for three user contexts — fast (free-text), thorough (guided), or detected (brownfield). |
| **Separate workflow skill** | Prevents routing logic from mixing with phase execution logic. Each skill stays focused. |
| **history.md append-only** | Immutable process log. Every phase, every commit, every decision is traceable. |

---

## Working on This Repo — Common Tasks

### Adding a new template

1. Create `src/templates/<name>-template.md` with YAML frontmatter
2. Add the filename to `EXPECTED_TEMPLATES` in `test_skills.py`
3. Update relevant skills to reference the new template
4. Run validation tests
5. Run `./scripts/install.sh` to deploy

### Adding a new reference

1. Create `src/references/<name>.md` with relevant content
2. Add the filename to `EXPECTED_REFERENCES` in `test_skills.py`
3. Update skills to reference (`spec-kit/references/<name>.md`)
4. Run validation tests
5. Run `./scripts/install.sh` to deploy

### Modifying a skill

1. Edit `src/skills/<name>.md` — never edit `~/.hermes/skills/` directly
2. Update frontmatter version if making substantive changes
3. Run `test_skills.py` to validate cross-references and structure
4. Run `./scripts/install.sh` to deploy
5. Verify with `skill_view(name='<skill-name>')` in Hermes

### Modifying the MCP server

1. Edit `spec-kit-mcp-server/server.py`
2. Run `test_workflow.py` to verify state machine integrity
3. Run `test_skills.py` to verify no skill reference breakage
4. Run `./scripts/install.sh` to deploy
5. If adding tools: update the AGENT.md tool table AND the MCP section in
   `src/skills/spec-kit/SKILL.md` AND `spec-kit-mcp-server/README.md`

### Adding a new feature (for spec-kit itself)

Follow the spec-kit workflow! This repo uses its own skills:
1. Ensure constitution exists (`specs/constitution.md`)
2. Create spec (`specs/NNN-name/spec.md`)
3. Plan, task, implement, test, close
4. Branch: `feat/NNN-kebab-name`

---

## Important Guardrails (CAUTION)

1. **Never restructure existing working skills without explicit user consent.**
   One new file = one new file. Refactoring skills is a conversation, not an action.
2. **Never delete content from spec artifacts.** The additive-only rule is universal.
3. **Never run git operations on main/master.** Preflight check #1 enforces this.
4. **Never advance a phase outside its owning skill.** Only the phase skill that
   produces the transition artifact may call advance_phase.
5. **Never overwrite ~/.hermes/skills/ with partial installs.** Always run the
   full `./scripts/install.sh`.
6. **Never edit installed files in ~/.hermes/skills/.** Edit source files in
   `src/` and reinstall.
7. **Pre-flight self-check is not optional.** Branch, mode, workflow, history —
   run them before every action.
8. **When in doubt about the current state, run `get_feature_state` or
   `project_status` (MCP), or scan the artifact directory.** Do not guess.

---

## Communication Style

Concise. Show commands over explanations. Confirm before destructive operations.
Ask for clarification when blocked. When reporting errors from MCP or tests,
include the raw error message so the user can diagnose.

For downstream project AGENTS.md templates, keep routing mechanics out — only
project-specific context belongs there.
