# Auto-Commit Pattern

Skills that produce spec artifacts commit immediately after creating or updating markdown documents. This document lists the canonical commit scopes and message templates for each skill.

Project-specific overrides: Create `specs/git-conventions.md` in your project root to customise commit message templates, branch naming, and merge behaviour. If the file doesn't exist, the defaults below apply.

## Standard Pattern

```bash
IF `git rev-parse --git-dir > /dev/null 2>&1`; THEN
  COMMIT_MSG="<message>"
  git add <paths>
  git commit -m "$COMMIT_MSG" --no-verify
  COMMIT_HASH=$(git rev-parse HEAD)
  NOTE: "Committed as $COMMIT_HASH"
ELSE
  NOTE: "Not a git repository — skipping automatic commit"
```

## Per-Skill Usage

| Skill | Scope | Commit Message (use template from specs/git-conventions.md) |
|-------|-------|-------------------------------------------------------------|
| spec-kit-constitution | `specs/constitution.md` | Constitution template: `spec(phase-0): constitution for [PROJECT]` |
| spec-kit-specify | `specs/[feature]/spec.md` | Spec template: `spec(phase-1): [feature] spec` |
| spec-kit-clarify | `specs/[feature]/clarify.md`, `specs/[feature]/spec.md` | Clarify template: `spec(phase-1.5): [feature] clarifications` |
| spec-kit-plan | All plan artifacts | Plan template: `spec(phase-2): [feature] plan` |
| spec-kit-tasks | `specs/[feature]/tasks.md` | Tasks template: `spec(phase-3): [feature] tasks` |
| spec-kit-implement (batch) | All spec artifacts for feature | Batch template: `spec: [feature] spec artifacts (spec, plan, tasks)` |
| spec-kit-implement (phase) | Source code per phase | Implement template: `feat: [feature] Phase N - [Phase Name]` |
| spec-kit-implement (regression) | Source code for regression fixes | Regression template: `fix: [feature] BF-REGRESSION-001 - fix regressions` |
| spec-kit-implement (bugfix, per-task) | Source code per bugfix fix | Bugfix template: `fix: [feature] BF-### - description` |
| spec-kit-test | `specs/[feature]/bugs.md` | Bug log template: `spec(phase-5): [feature] bug log` |
| spec-kit-summarize | Summary/close + patched spec/plan | Summary template: `spec(phase-6): [feature] summary (health: N%)` |
| spec-kit-refresh | Patched spec artifacts | Refresh template: `spec(refresh): [feature] reconcile artifacts` |

## Rules

- Always `--no-verify` (pre-commit hooks may block spec artifacts)
- Hash is captured for history.md traceability
- Silently skip if not a git repo
- Never commit broken state during Implement (tests must pass first)
- Additive-only: never delete existing content. Only append or modify specific fields.
