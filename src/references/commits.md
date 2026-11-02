# Commits

Process level P1 (`rigor.md`): spec + plan + tasks in one commit `spec(phase-1-3)`, the implementation in one `feat: [feature] - [summary]`, on `main` when `blocked_branches: none`. Otherwise every phase ends in ONE commit, preceded by its `history.md` entry when history is on for the
feature (`history-tracking.md`: default size L only). Project overrides: `specs/git-conventions.md`.

## Per-skill messages

| Skill | Scope | Message |
|-------|-------|---------|
| constitution | `specs/constitution.md` | `spec(phase-0): constitution for [PROJECT]` |
| specify | `spec.md`, `decisions.md`, `history.md` | `spec(phase-1): [feature] spec` — size S: `spec(phase-1-3): [feature] spec, plan, tasks` |
| clarify | `clarify.md`, `spec.md` | `spec(phase-1.5): [feature] clarifications` |
| plan | plan artifacts | `spec(phase-2): [feature] plan` · bugfix: `spec(phase-2): [feature] bugfix plan (BUG-NNN, …)` |
| tasks | `tasks.md` | `spec(phase-3): [feature] tasks` · bugfix: `spec(phase-3): [feature] bugfix tasks (BUG-NNN, …)` |
| review (pre) | review report | `spec(review): [feature] review findings` |
| implement | code + `tasks.md` `[X]` + evidence + history | `feat: [feature] Phase N - [name]` · bugfix: `fix: [feature] BF-### - description` · quickfix: `fix: [feature] BF-### - description (plan+tasks+fix)` · regression: `fix: [feature] BF-REGRESSION-001 - fix regressions` |
| test | `bugs.md` | `spec(phase-5): [feature] bug log` |
| test (accept) | `acceptance.md`, evidence, `bugs.md` | `spec(phase-5): [feature] acceptance round N (RESULT a/b)` |
| review (final) | `review-final.md`, evidence, `bugs.md` | `spec(review): [feature] final review (verdict: X)` |
| summarize / close | close doc, change record, patched spec/plan, ADRs, AGENTS.md | `spec(phase-6): [feature] close (health: N%)` |
| refresh | patched artifacts | `spec(refresh): [feature] reconcile artifacts` |

## Rules

- **History first (when on).** The entry is appended (`mcp_spec_kit_append_history` or
  `spec-kit/scripts/spec-kit-log.sh`) and `mcp_spec_kit_history_guard` says ok before `git commit`;
  when off the guard answers ok and the close reads `spec-kit/scripts/spec-kit-history.sh`.
- **Intent before code.** A change to requirements or design intent (spec FRs, plan decisions)
  is committed before the code that follows it. Status-only edits (task `[X]`, bug status,
  evidence files, history entry) ride the phase's code commit — one commit per phase boundary.
- **Agent trailer.** Every commit names its agent: `git commit --trailer "Spec-Kit-Agent: <agent>"`
  (`hermes`, `claude`, …). Hermes adds `--trailer "Co-Authored-By: Hermes Agent <noreply@nousresearch.com>"`
  (`coauthor:` in git-conventions overrides); Claude Code keeps its own line. Implemented-by reads both.
- **One PR per feature**, opened after the close (an early merge = a 2nd PR).
- **Never `--no-verify`.** A hook that blocks a spec artifact is a hook to fix.
- Never commit a red suite during implement; no commits inside a RED sub-phase.
- No commit hashes in history entries (squash-merge kills them); the commit *message* is the link.
- Not a git repo → skip silently.
- Before every commit: `mcp_spec_kit_lint_artifacts` → 0 errors (no MCP: re-read ids and statuses).
