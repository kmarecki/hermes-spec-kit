# Auto-Commit Pattern

Skills that produce spec artifacts commit immediately after creating or updating markdown documents. This document lists the canonical commit scopes and message templates for each skill.

Project-specific overrides: Create `specs/git-conventions.md` in your project root to customise commit message templates, branch naming, and merge behaviour. If the file doesn't exist, the defaults below apply.

## Standard Pattern

```bash
IF `git rev-parse --git-dir > /dev/null 2>&1`; THEN
  COMMIT_MSG="<message>"
  git add <paths>
  git commit -m "$COMMIT_MSG"
  NOTE: "Committed"
ELSE
  NOTE: "Not a git repository — skipping automatic commit"
```

> **Do not capture the commit hash for history.md** — history entries record no
> commit hashes (feature branches are squash-merged; pre-merge hashes are dead
> data). The commit message itself (`spec(phase-N): [feature] ...`) is the
> traceability link.

## Per-Skill Usage

| Skill | Scope | Commit Message (use template from specs/git-conventions.md) |
|-------|-------|-------------------------------------------------------------|
| spec-kit-constitution | `specs/constitution.md` | Constitution template: `spec(phase-0): constitution for [PROJECT]` |
| spec-kit-specify | `specs/[feature]/spec.md` | Spec template: `spec(phase-1): [feature] spec` |
| spec-kit-clarify | `specs/[feature]/clarify.md`, `specs/[feature]/spec.md` | Clarify template: `spec(phase-1.5): [feature] clarifications` |
| spec-kit-plan | All plan artifacts | Plan template: `spec(phase-2): [feature] plan` |
| spec-kit-plan (bugfix sub-round) | `plan.md` (appended bugfix sections) | Bugfix plan template: `spec(phase-2): [feature] bugfix plan (BUG-NNN, ...)` |
| spec-kit-tasks | `specs/[feature]/tasks.md` | Tasks template: `spec(phase-3): [feature] tasks` |
| spec-kit-tasks (bugfix sub-round) | `tasks.md` (appended bugfix tasks) | Bugfix tasks template: `spec(phase-3): [feature] bugfix tasks (BUG-NNN, ...)` |
| spec-kit-implement (phase) | Source code per phase | Implement template: `feat: [feature] Phase N - [Phase Name]` |
| spec-kit-implement (regression) | Source code for regression fixes | Regression template: `fix: [feature] BF-REGRESSION-001 - fix regressions` |
| spec-kit-implement (bugfix, per-task) | Source code per bugfix fix | Bugfix template: `fix: [feature] BF-### - description` |
| spec-kit-implement (bugfix sub-round quickfix) | plan section + tasks entry + fix | Quickfix template: `fix: [feature] BF-### - description (plan+tasks+fix)` |
| spec-kit-test | `specs/[feature]/bugs.md` | Bug log template: `spec(phase-5): [feature] bug log` |
| spec-kit-test (accept mode) | `acceptance.md`, `evidence/acceptance-r<N>*`, `bugs.md` | `spec(phase-5): [feature] acceptance round N (PASS|FAIL a/b)` |
| spec-kit-review (pre-implement) | review report | Review template: `spec(review): [feature] review findings` |
| spec-kit-review (final) | `review-final.md`, `evidence/final-*`, `bugs.md`, approved spec/plan patches | Final review template: `spec(review): [feature] final review (verdict: X)` |
| spec-kit-specify (size S, chained) | `spec.md`, `plan.md`, `tasks.md` | `spec(phase-1-3): [feature] spec, plan, tasks` |
| spec-kit-summarize | Summary/close + patched spec/plan + ADR files/index + AGENTS.md patches | Summary template: `spec(phase-6): [feature] summary (health: N%)` |
| spec-kit-refresh | Patched spec artifacts | Refresh template: `spec(refresh): [feature] reconcile artifacts` |

## Rules

- **Never `--no-verify`.** Hooks are the project's guardrails; if one blocks a spec artifact, fix the hook (or its path filter), do not bypass it.
- **Spec before code only for intent.** A change to requirements or design intent (spec.md FRs, plan decisions) is committed before the code that follows it. Status-only document changes (task `[X]`, bug status, history entry, evidence files) ride the phase's code commit — one commit per phase boundary, documentation included.
- Silently skip if not a git repo
- Never commit broken state during Implement (tests must pass first)
- Additive-safe: never delete or reorder existing entries. Only append new, or modify specific fields minimally.
