---
name: spec-kit
description: Spec-Driven Development (SDD) workflow mirroring github/spec-kit.
category: software-development
---

# Spec-Driven Development (SDD)

Spec-driven development for Hermes Agent. Specifications drive code, not the other way around.

## ⚠️ Critical Approach Rule: Read First, Build Second
**ALWAYS read the source repository design documents before implementing a skill or template that mirrors an existing system.** This prevents creating simplified approximations instead of faithful implementations.

**The pitfall to avoid:** Jumping to building before reading. When a user asks to implement parity with an existing system:
1. Read the actual source design docs, templates, and workflows FIRST
2. Analyze all commands, templates, and their exact structures
3. Only then build or update templates

**When this applies:** Any time implementing "parity" with, "mirroring," or "equivalent to" an existing system.

## Core Workflow

```text
                                            ┌── explore mode ──┐
                                            ▼                  │
Constitution → Specify → Clarify (opt) → Plan → Tasks → Implement → Test
                                                                      │
                                                                      └── bugfix loop ──┐
                                                                ┌──────────────────────┘
                                                                ▼
                                                          [Clarify] → Plan → Tasks → [Analyze] → Implement → Test → Close (mandatory)
```

The workflow has **three development modes**:

| Mode | Trigger | Behavior |
|------|---------|----------|
| **specify** (default) | "Create a spec for [feature]" | Full forward phase sequence. Forward phases are manual; user decides when to advance. |
| **bugfix** | "bugfix [feature]" | Reuses Plan → Tasks → Implement inner loop. Chains automatically — the user already committed by invoking bugfix mode. **Auto-chains to Close** when all bugs verified. |
| **explore** | "Explore [feature] with [variants]" | Spawns N parallel branches, each running its own independent phase sequence. User compares variants with `spec-kit-compare` and chooses a winner. |

**Constitution is always optional** in every mode. If `specs/constitution.md` doesn't exist, phases run without constitutional gates.

**Phase 6 (Close) is mandatory** to mark a feature complete. After the bugfix loop finishes or the user requests close, `spec-kit-summarize` runs in either full summary or lightweight close mode, computes spec health, and patches spec/plan artifacts to reflect intentional deviations.

**Explore mode** diverges into parallel branches:
```text
                      ┌── Variant A (branch: explore/NNN-feature-a)
                      │   └── Specify → Clarify → Plan → Tasks → [Implement]
Explore [feature] ────┼── Variant B (branch: explore/NNN-feature-b)          ──→ Compare → Pick winner → Close
                      │   └── Specify → Clarify → Plan → Tasks → [Implement]
                      └── Variant C (branch: explore/NNN-feature-c)
                          └── Specify → Clarify → Plan → Tasks → [Implement]
```

## Phase Reference

### Phase 0: Constitution
**Skill**: `spec-kit-constitution`
**When**: User says "create constitution" or "update constitution"

Establish project-level principles and constraints. Create once per project.

### Phase 1: Specification
**Skill**: `spec-kit-specify`
**When**: User says "create a spec for [description]" or "specify [feature]"

Define the WHAT and WHY — no implementation details.

### Phase 1.5: Clarify (Optional)
**Skill**: `spec-kit-clarify`
**When**: User says "clarify [feature]" or "resolve ambiguities in [feature]"

Resolve spec ambiguities. Run as many times as needed.

### Phase 2: Plan
**Skill**: `spec-kit-plan`
**When**: User says "plan [feature]" or "create plan for [feature]"

Define the HOW — research, data models, contracts, plan document.

### Phase 3: Tasks
**Skill**: `spec-kit-tasks`
**When**: User says "generate tasks for [feature]" or "break down [feature]"

Executable roadmap. Tests written before implementation (TDD approach).

### Phase 3.5: Analyze (Optional)
**Skill**: `spec-kit-analyze`
**When**: User says "analyze [feature]"

Non-destructive consistency and quality check.

### Phase 4: Implement
**Skill**: `spec-kit-implement`
**When**: User says "implement [feature]" or "start implementation"

Execute tasks from tasks.md. Update task status as completed.

### Phase 5: Test
**Skill**: `spec-kit-test`
**When**: User says "test [feature]" after implementation

Manual bug tracking. Creates `bugs.md` in the feature directory. User discovers and logs bugs.

### Phase 6: Summarize / Close (Mandatory)
**Skill**: `spec-kit-summarize`
**When**: 
- **Summarize**: User says "summarize [feature]" or "implementation summary" — full gap analysis
- **Close**: User says "close [feature]" — lightweight close document
- **Auto-trigger**: After bugfix loop completes (all bugs verified) — chains automatically

Post-implementation review and documentation of deviations. **Computes spec health score** (0-100%) and patches spec.md/plan.md to reconcile intentional deviations with user approval.

### Refresh (Standalone)
**Skill**: `spec-kit-refresh`
**When**: User says "refresh [feature]" or "sync spec for [feature]"

Lightweight artifact alignment for manual code changes or mid-stream reconciliation. Per-item user approval for each discrepancy. No close document generated.

### Explore Mode (Parallel)
**Skill**: `spec-kit-explore`
**When**: User says "explore [feature] with [variant descriptions]"

Spawn N parallel branches, each running independent specify → clarify → plan → tasks → [implement] cycles. Harnesses `delegate_task` for true parallelism. Branches are named `explore/NNN-feature-<variant>`.

### Compare Mode
**Skill**: `spec-kit-compare`
**When**: User says "compare [feature]" or "compare variants for [feature]"

After explore completes, load all variant artifacts, build a structured comparison matrix across spec/plan/implementation dimensions, and guide the user to select a winning variant. Optionally cherry-pick features from rejected variants.

**Bug tracking format**: Each bug has: ID (BUG-001), Severity (critical/major/minor/trivial), Area, Description, Steps to Reproduce, Expected vs Actual Result, Requires Clarification flag, Status (open/in-progress/resolved/verified).

### ⚠️ Bugfix Gate: Log Before Fix

When the user reports a bug, the first action is **always** to create or update `bugs.md` in the feature's spec directory. Do NOT make any code changes before the bug is logged.

**Always log the bug first, then route through the fix loop.** A user who says "stop" or "stop fixing" while you're changing code is telling you to step back and follow the proper procedure — not to give up on the task.

### Bugfix Loop

After bugs are logged in `bugs.md`, the workflow routes back through earlier phases:

```text
Test → [Clarify if needed] → Plan → Tasks → [Analyze] → Implement → Test (verify) → Close (mandatory)
```

- **"bugfix [feature]"** starts the loop
- **Default route**: Plan (for straightforward bugs)
- **With clarification**: 
  - *User-initiated*: user says "clarify [BUG-NNN]" — route through clarify step for that specific bug regardless of its Requires Clarification flag. The user may volunteer new details or corrections for any bug.
  - *Agent-initiated*: if a bug has `Requires Clarification: yes`, route through clarify step first.
- **Bugfix tasks**: Prefixed with `BF-###` and tagged `[BUGFIX]`
- **Bugfix task tracing**: When a bugfix task supersedes specific original (buggy) tasks, append `[T###-fix]` to trace the relationship (e.g. `BF-001 [BUGFIX] [T051-fix] Fix validate_cluster_shape`). This connects bugfix work back to the original tasks that need rework, useful during post-implementation review.
- **Verify**: User marks bug status as "verified" when fix is confirmed
- **Auto-close**: When all bugs are verified, the workflow auto-chains to Phase 6 (spec-kit-summarize) — either full summary or lightweight close depending on feature complexity
- **Repeat**: Loop until all bugs are verified and close is generated

### Phase 6 (Summarize/Close): Post-Implementation Review

The **canonical post-implementation review** is `spec-kit-summarize` (Phase 6). Run it with:
- "summarize [feature]" — full gap analysis: compares actual code against spec/plan/tasks, produces `implementation-summary.md` with ✅/⚠️/❌ verdicts, **computes spec health score**, **patches spec/plan artifacts** for intentional deviations, and creates bug entries for uncovered gaps.
- "close [feature]" — lightweight close mode: produces `close.md` with health score, artifact state, and key decisions. No deep gap analysis.

**Phase 6 is mandatory** to mark a feature complete. The workflow orchestrator blocks attempts to start new features or mark features done without running Phase 6 first.

Do NOT attempt a manual post-implementation review by following reference steps here. Load `spec-kit-summarize` and let it handle the analysis. The umbrella skill does not duplicate the summarization logic — refer to the skill file for execution details.

## AGENTS.md Conventions

AGENTS.md is **project-level context** — reference skills by name, don't replicate their routing logic or trigger phrases.

**Put in AGENTS.md**:
- Which skills are available
- Active spec directories and current artifacts
- Project-specific context (tech stack, build commands)
- Conventions unique to the project

**Keep out of AGENTS.md**:
- Trigger phrase lists or routing tables
- Workflow mechanics / phase descriptions / diagrams
- Any routing that already lives in a skill file

Routing logic, trigger phrases, and workflow mechanics belong in the skill files. When you add a new phase or routing rule, update the relevant skill — not AGENTS.md. This keeps AGENTS.md stable and skills as the source of truth.

## Checklists Are Optional

Quality checklists exist in `checklist-template.md` as guides. They do NOT block phase advancement. Use them when helpful, skip them when not needed. The user is always in control of when to advance.

## Workflow Tracking (Transition Log)

Every spec directory maintains `specs/NNN-name/workflow.md` — an append-only transition log. Each phase skill appends one entry when it completes. This gives:

- **Transition history** — when and why phases changed, survives context compression
- **Fast phase detection** — `grep '→ Complete' workflow.md | tail -1` is faster than scanning the directory
- **User visibility** — `cat workflow.md` shows the full history
- **No sync drift** — append-only entries can never disagree with reality

**Format** (appended by each phase skill on completion):
```markdown
## [ISO_TIMESTAMP] | Phase N → [Name] → Complete
- **Skill**: [skill-name]
- **Artifacts**: [files created/updated]
- **Notes**: [key decisions, user input, deviations]
```

**When created**: First transition (typically Phase 1: Specify) creates the file. If a user manually created `spec.md` before running a skill, the first skill run backfills entries for all completed phases.

**Phase detection shortcut**: Instead of scanning the spec directory for artifact files, load `workflow.md` and read the last `→ Complete` line. The phase name before the arrow is the current phase. Cross-check against artifact presence as a sanity check.

See `references/workflow-tracking.md` for full design rationale.

## Phase Enforcement

Phase transitions are **manual** but gated by artifact presence. Each phase skill checks whether its prerequisite documents already exist in `specs/NNN-feature-name/`. If a prerequisite is missing, the skill warns the user and suggests running the appropriate prior phase. No separate `.phase` marker files are used — phase state is determined solely by which markdown files are present in the spec directory.

**Phase 6 (Close) is mandatory** — a feature cannot enter Complete state without either `implementation-summary.md` or `close.md` present. This prevents silent drift accumulation.

| Artifacts Present | Current Phase |
|:-----------------|:-------------|
| `constitution.md` only | Ready to Specify |
| `spec.md` exists | Specified |
| `clarify.md` exists | Clarifying/Clarified |
| `plan.md` exists | Planning/Planned |
| `tasks.md` exists | Tasking/Tasked |
| `tasks.md` with completions | Implementing |
| `bugs.md` with open bugs | Testing (bugfix loop) |
| `bugs.md` all verified | Testing complete — **must close** |
| `implementation-summary.md` exists | Summarized — complete |
| `close.md` exists | Closed — complete |
| All tasks complete + all bugs verified + (implementation-summary.md or close.md) | **Complete** |
| `workflow.md` last entry | Current phase (fast lookup) |
| `variants/` directory exists with ≥2 entries | Exploring (creative mode) |
| `comparison.md` exists | Compared — decision made |

> **Tip**: `workflow.md` is the fastest phase detector. Read the last `→ Complete` line instead of scanning directory artifacts.

> **Drift detection**: When loading an existing feature that has `implementation-summary.md` or `close.md`, read its Spec State / Artifact State table. If any artifact is `⚠️ needs review` or `❌ outdated`, warn the user and suggest `spec-kit-refresh`.

## Phase Guardrails (Permission Matrix)

You MUST determine the current phase before any tool call. Each phase has strict limits on what files and tools are allowed:

| Phase | Allowed to Write | Code-Editing Tools (write_file/patch/terminal for build) |
|-------|-----------------|----------------------------------------------------------|
| **Constitution** | `constitution.md` only | **BLOCKED** |
| **Specify** | `spec.md`, `checklists/requirements.md` | **BLOCKED** |
| **Clarify** | `clarify.md`, `spec.md` (amend ambiguities) | **BLOCKED** |
| **Plan** | `plan.md`, `research.md`, `data-model.md`, `contracts/*.md`, `quickstart.md` | **BLOCKED** |
| **Tasks** | `tasks.md` only | **BLOCKED** |
| **Analyze** | None (read-only report) | **BLOCKED** |
| **Implement** | source code files, `tasks.md` (completions), `bugs.md` (mark resolved in bugfix loop) | **ALLOWED** |
| **Test** | `bugs.md` only | **BLOCKED** |
| **Explore** | `specs/[feature]/variants/*/` (variant artifacts) | ALLOWED (via delegate_task subagents) |
| **Compare** | `comparison.md` only | **BLOCKED** |
| **Summarize / Close** | `implementation-summary.md`, `close.md`, `spec.md` (patch deviations), `plan.md` (patch deviations), `tasks.md` (finalize), `bugs.md` (finalize) | **BLOCKED** |
| **Refresh** | `spec.md`, `plan.md`, `data-model.md`, `contracts/*.md` (per-item user approval) | **BLOCKED** |

**Bugfix loop**: reuses Plan, Tasks, and Implement — same permissions, just with `bugs.md` as additional input context.
**Summarize/Close exception**: May patch `spec.md` and `plan.md` to reconcile intentional deviations (with user approval per change).
**Refresh exception**: May patch spec artifacts with per-item user approval — code-editing tools remain BLOCKED.

### Enforcement Rules
- `write_file` / `patch` / `terminal` for compilation/builds → **ONLY** during Implement (including bugfix loop)
- Writing to spec artifacts → only during their respective phase
- **`workflow.md` (transition log)** — All phases may append to `workflow.md` on completion. This is the only file writable across all phases.
- Reading files, searching, loading skills → allowed in all phases
- If you cannot determine the phase → ASK the user
- If the user asks for code changes outside Implement → politely refuse and suggest the correct phase first

### Pre-Work Self-Check
Before ANY tool call:
1. **What phase am I in?** Detect from artifacts present (see Phase Enforcement table above)
2. **Open bugs lock**: Does `specs/[feature]/bugs.md` (for the target feature) have any bug with Status: open?
   - IF YES → You are in **Test** phase. Code tools (write_file, patch on source code, terminal for builds) are **BLOCKED**.
   - IF you are about to write code despite open bugs → **STOP**. You must route through "bugfix [feature]" first: plan → tasks → implement.
3. **Is this tool in the ALLOWED column for this phase?** Check the Permission Matrix
4. **Am I about to write code?** If YES and phase is NOT Implement → STOP. You are violating the guardrail.
5. **Am I starting a new feature or marking one complete?** If implementation-summary.md and close.md are both missing but bugs.md is all verified → BLOCK: Phase 6 (Close) required.
6. **Does an existing close/summary show drift?** If implementation-summary.md or close.md shows `⚠️ needs review` or `❌ outdated` artifacts → WARN: drift detected, suggest refresh.

## Migration from OpenCode Spec-Kit

Projects that previously used OpenCode's `.specify/` structure can migrate to Hermes spec-kit:

1. **Constitution**: copy `.specify/memory/constitution.md` → `specs/constitution.md`
2. **Install skills**: run `scripts/install.sh` from the hermes-spec-kit project
3. **Update AGENTS.md**: add spec-kit workflow section (see `AGENTS-template.md`)
4. **Verify**: existing `specs/NNN-feature-name/` directories are already compatible with Hermes skills

The canonical constitution path is `specs/constitution.md`. All Hermes spec-kit skills reference this path. The `.specify/` directory can be removed once migration is verified.

## Anti-Patterns to Avoid

- **Do NOT block on checklists.** If a user wants to advance, let them.
- **TDD is the default, not optional.** Test-first is enforced. The Iron Law says: NO production code without a failing test first. If you wrote code before the test, delete it and start over. The only exceptions require explicit user permission: throwaway prototypes, generated code, and configuration files. Without user permission, TDD is not optional — the agent cannot unilaterally skip it. This is consistent with the `test-driven-development` skill loaded during Phase 3 (Tasks) and Phase 4 (Implement).
- **Do NOT demand all artifacts exist before advancing.** Small features may skip Clarify or Plan entirely.
- **Do NOT use Cline/OpenCode command syntax** (e.g. `/speckit.specify`). Use natural language with skill names instead.
- **Do NOT fix bugs before logging them.** Bug reports always go into `bugs.md` first. Making code changes without a bug entry skips the workflow and causes user frustration. "Stop" / "stop fixing" means pause and follow the proper loop — never interpret it as permission to give up permanently.
- **Do NOT assume the fix approach before clarifying user intent.** When a user reports unexpected visual output (wrong colors, misaligned elements, oversized boxes, extra rendered elements), first CLARIFY whether they want the element fixed (adjusted/aligned) or removed entirely. Jumping to a sophisticated alignment fix when the user wants simple removal wastes time and causes frustration. A clarifying question like "Do you want this fixed in place or removed?" costs seconds and saves rework.
- **Do NOT ask for permission mid-bugfix-loop.** The bugfix inner loop (Plan → Tasks → Implement) chains automatically — do not ask "run spec-kit-tasks now?" or "proceed to implement?" when already in bugfix mode. The user committed to the path when they said "bugfix [feature]".
- **Do NOT set bug status to resolved/verified preemptively.** Only the user marks a bug verified — after they have tested the fix. Changing status to "resolved" before the user confirms is a workflow bypass. If you've applied a fix, set status to "in-progress" (or leave it at "open") and wait for the user to test and say it's fixed. The verify gate belongs to the user, not the agent.
- **Do NOT restructure existing working skills when adding new ones.** Adding one new skill (e.g. `spec-kit-test`) should only install that skill — do not convert existing flat `.md` files to directories, rename files, or change the install format. If the existing setup works, leave it alone.
- **Do NOT implement during Plan, Clarify, or Tasks phases — even for "obvious" fixes.** The bugfix loop requires Plan → Tasks → Implement in order. A one-line change (removing an arrowhead, adding a CSS class) still needs a plan and a task entry before code touches disk. Skipping phases is a phase guardrail violation, not a shortcut. If you catch yourself reaching for `write_file`/`patch` during the bugfix loop before reaching Implement, stop and run the correct phase skill first.
- **Do NOT pollute AGENTS.md with workflow mechanics.** AGENTS.md is project-level context: reference skills name, list active specs, document project conventions. Routing logic, trigger phrases, phase diagrams, and bugfix loop details belong in skill files. When you add a new phase or routing rule, update the relevant skill — not AGENTS.md.
- **Do NOT allow features to be complete without Phase 6.** A feature without `implementation-summary.md` or `close.md` is not complete, even if all bugs are verified. The mandatory close prevents silent drift accumulation. If a user insists a feature is done without closing, explain why close matters (spec health, drift prevention, future refactoring context) rather than bypassing the requirement.

## Spec Health Score

Spec health is a 0-100% score computed during Phase 6 (Summarize/Close). It indicates how well spec/plan artifacts align with actual code.

### Formula
```
spec_health = (resolved + acknowledged) / (resolved + acknowledged + not_done) * 100
```

Where:
- **resolved** = requirements implemented as planned OR intentionally deviated with documented rationale (spec/plan auto-updated)
- **acknowledged** = requirements deferred with documented reason
- **not_done** = requirements missing without documented reason

### Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 100% | Artifacts fully aligned with code | No action needed |
| 80-99% | Minor gaps tracked but not blocking | Acceptable — review at leisure |
| 50-79% | Significant drift | Run `spec-kit-refresh` before refactoring |
| <50% | Artifacts are misleading | Run `spec-kit-refresh` before proceeding |

### How Score is Used

- **At feature close**: The score is written into `implementation-summary.md` or `close.md`
- **On future feature load**: The workflow reads the score from the last close/summary. If <80%, warns the user about drift
- **On refresh**: Score is recalculated after refresh (though refresh does not produce an output document — the old score in close/summary remains stale until next close/summary)

## Template Path Convention

All skills reference templates using the canonical skill‑relative path:

```
spec-kit/templates/<name>-template.md
```

NOT bare paths like `templates/<name>.md`. This ensures templates resolve correctly regardless of which Hermes profile or working directory loaded the skill.

To load a template: use `skill_view(name='spec-kit', file_path='templates/<name>-template.md')` then copy the content to the target location.

## Project Structure

```
src/
  skills/                # Skill source files
    spec-kit-*.md
    spec-kit/            # Umbrella SKILL.md directory
      SKILL.md
  templates/             # Template source files
    *-template.md
scripts/
  install.sh             # Copies src/* to ~/.hermes/skills/
```

Skills and templates are maintained in the project directory and installed via `./scripts/install.sh`. Do not edit files in `~/.hermes/skills/` directly.

## Git Branch Naming Convention

Spec-kit produces feature directories like `specs/003-user-auth/`. The corresponding git branch should mirror the spec number and name for traceability:

```text
feature/NNN-short-name            # Normal forward development (specify mode)
fix/NNN-short-name                # Bugfix-only branch (standalone, not part of bugfix loop)
explore/NNN-feature-<variant>     # Creative exploration (one per variant)
```

Examples:
| Spec Directory | Branch Name |
|:---------------|:------------|
| `specs/001-user-auth/` | `feature/001-user-auth` |
| `specs/002-oauth2-api-integration/` | `feature/002-oauth2-api-integration` |
| `specs/003-data-export/` | `fix/003-data-export` (standalone bugfix) |
| `specs/004-taskify/variants/react/` | `explore/004-taskify-react` |
| `specs/004-taskify/variants/vue/` | `explore/004-taskify-vue` |

**During the bugfix loop**, the bugfix work happens on whatever branch the feature was implemented on. Do not create separate bugfix branches for individual bugfix loop iterations — the loop is part of the same feature branch.

**Post-Summarize**, if the user wants to squash or merge to main, follow the project's git workflow (rebase/merge). The branch naming itself lives in the umbrella skill, not in AGENTS.md, to keep AGENTS.md minimal.

## Git Integration

Git links phase progress to version history. Every phase transition automatically commits the spec artifacts, creating recoverable checkpoints and an audit trail without manual steps.

### Automatic Commit on Phase Completion

Every phase skill runs `git commit` as its final execution step. The commit captures all spec artifacts created during that phase:

```bash
# Automatically run by the phase skill on completion:
git add specs/[feature]/<artifacts>
git commit -m "spec(phase-N): [feature] description" --no-verify

# If not in a git repo, the step is silently skipped
```

The commit hash is captured and written to `workflow.md` for traceability. No user approval needed — the commit is part of the phase transition.

### Per-Phase Commit Convention

| Phase | Scope | Commit Message | Automatic? |
|-------|-------|----------------|------------|
| 0 — Constitution | `specs/constitution.md` | `spec(phase-0): constitution for [project]` | Yes |
| 1 — Specify | `specs/NNN-name/spec.md` | `spec(phase-1): [NNN-name] specification` | Yes |
| 1.5 — Clarify | `specs/NNN-name/clarify.md` | `spec(phase-1.5): [NNN-name] clarifications` | Yes |
| 2 — Plan | `specs/NNN-name/plan.md`, `research.md`, etc. | `spec(phase-2): [NNN-name] implementation plan` | Yes |
| 3 — Tasks | `specs/NNN-name/tasks.md` | `spec(phase-3): [NNN-name] task breakdown` | Yes |
| 4 — Implement | Source code per task | `feat: [NNN-name] T### - description` | Yes (per task) |
| 5 — Test / Bugs | `specs/NNN-name/bugs.md` | `spec(phase-5): [NNN-name] bug log` | Yes |
| 5 — Bugfix fix | Source code per bugfix task | `fix: [NNN-name] BF-### - description` | Yes (per fix) |
| 6 — Summarize | `specs/NNN-name/implementation-summary.md` or `close.md`, + patched spec/plan | `spec(phase-6): [NNN-name] implementation summary (health: N%)` | Yes |
| — Refresh | Patched spec/plan artifacts | `spec(refresh): [NNN-name] reconcile spec artifacts with code` | Yes |

### Commit Granularity Rules

- **Spec artifacts** (phases 0-3, 5-log, 6): One automatic commit per phase transition. The commit happens at the end of the skill's execution.
- **Phase 6 also commits spec.md and plan.md patches** (`git add specs/[feature]/spec.md specs/[feature]/plan.md`) alongside the summary/close document.
- **Implementation** (phase 4): Commit after each task (T###). Already handled by the TDD loop in `spec-kit-implement` / `writing-plans`. Each commit = one task's code + its tests.
- **Bugfix** (bugfix loop): Commit after each bugfix task (BF-###). Message references the BUG-ID.
- **Refresh**: Commit after all approved patches.
- **Never commit broken state**: Tests must pass before commit during Implement. Spec artifacts are always safe to commit (documentation, not code).
- **If not in a git repo**: The commit step is skipped silently. Phase transition logging to `workflow.md` still happens.

### Traceability Through Git History

Because every commit follows the `spec(phase-N)` or `feat/fix: [NNN-name]` convention, you can query git for the full lifecycle of a feature:

```bash
# Show all spec commits for a feature
git log --oneline --grep="003-user-auth" --all

# Show only phase boundaries (not implementation detail)
git log --oneline --grep="spec(phase-" --all

# Show when a feature entered implementation
git log --oneline --grep="spec(phase-3): 003-user-auth"

# Show all bugfixes for a feature
git log --oneline --grep="BF-" --all

# Show current phase across all features (latest spec commit per feature)
git log --oneline --grep="spec(phase-" --diff-filter=A --name-only --pretty=format: | sort -u
```

### workflow.md → Git History Linking

The transition log (`workflow.md`) captures the commit hash automatically:

```markdown
## 2026-06-07T12:00Z | Phase 6 → Summarize → Complete
- **Skill**: spec-kit-summarize
- **Artifacts**: specs/003-user-auth/implementation-summary.md, specs/003-user-auth/spec.md (patched), specs/003-user-auth/plan.md (patched)
- **Spec Health**: 92%
- **Commit**: abc1234
```

The agent runs `git rev-parse HEAD` after the commit and writes the hash into the workflow.md entry. No manual hash entry needed.

### Git Rules Summary

1. **Automatic commit on phase completion** — each phase skill commits before reporting done
2. **One commit per task** during Implement
3. **One commit per bugfix** — message references BUG-ID
4. **Phase 6 includes spec/plan patches** — the commit captures reconciled artifacts
5. **Tests pass before commit** in Implement phase (silent skip if not in a git repo)
6. **workflow.md captures commit hash** via `git rev-parse HEAD`

## Available Templates

Installed via `./scripts/install.sh`:
- `spec-template.md`: Feature specification with User Stories, FR-### requirements, Given/When/Then scenarios
- `plan-template.md`: Technical decomposition
- `tasks-template.md`: Task breakdown with parallel `[P]` markers
- `constitution-template.md`: Project principles template
- `checklist-template.md`: Optional quality checklists (not blocking)
- `research-template.md`: Technical research template
- `data-model-template.md` — Data model template
- `bugs-template.md` — Bug tracking template (BUG-### format)
- `implementation-summary-template.md` — Post-implementation review summary (Phase 6, via `spec-kit-summarize`)
- `close-template.md` — Lightweight close document (Phase 6 close mode, via `spec-kit-summarize`)
- `workflow-template.md` — Transition log template (appended by every phase skill on completion)
- `comparison-template.md` — Creative exploration comparison matrix template

## References

- `references/migration-from-opencode.md` — Migration guide from OpenCode spec-kit to Hermes spec-kit
- `references/spec-kit-commands.md` (if present): Command reference from github/spec-kit
- `references/visual-bug-triage.md` — Triage process for visual/layout bug reports when the agent cannot view screenshots (pixel analysis, DOM checks, clarification triggers)
- `references/phase-guardrails.md` — Quick-reference permission matrix and phase detection table
- `references/bugfix-css-debugging.md` — CSS/layout bug diagnosis workflow for the bugfix loop: Tailwind v4 syntax trap, computed-style inspection via browser console, flex layout diagnostics, and scope-discipline during cleanup
- `references/cluster-topology-validation.md` — Validating intra-cluster shape topology when cross-cluster transition edges exist: same-cluster filtering for degree computation, connectivity checks, and testing patterns
- `references/skill-consistency.md` — Cross-skill consistency checklist: phase numbering, template paths, auto-chaining reciprocity, installed-vs-source drift prevention
- `references/workflow-tracking.md` — Workflow transition log design and rationale (append-only workflow.md)
- `references/workflow-enforcement.md` — Three-layer bugfix enforcement architecture and propose-vs-execute semantics
- `references/transition-design.md` — Workflow transition design principles: propose vs auto-chain vs dead stop, optional phase marking, three-layer redundancy
