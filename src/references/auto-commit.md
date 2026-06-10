# Auto-Commit Pattern

Skills that produce spec artifacts use a standard auto-commit pattern. Instead of repeating the 10-line `git rev-parse` block in every skill, reference this document.

Project-specific overrides: Create `specs/git-conventions.md` in your project root to customise commit message templates, branch naming, and merge behaviour. If the file doesn't exist, the defaults below apply.

## Standard Pattern

```bash
IF `git rev-parse --git-dir > /dev/null 2>&1`; THEN
  COMMIT_MSG="<message>"
  git add <paths>
  git commit -m "$COMMIT_MSG" --no-verify
  COMMIT_HASH=$(git rev-parse HEAD)
  NOTE: "Committed as $COMMIT_HASH"
  APPEND to workflow.md:
    ## [ISO_TIMESTAMP] | <phase> → Complete
    - **Commit**: $COMMIT_HASH
ELSE
  NOTE: "Not a git repository — skipping automatic commit"
```

## Per-Skill Usage

| Skill | Scope | Commit Message |
|-------|-------|---------------|
| spec-kit-constitution | `specs/constitution.md` | `spec(phase-0): constitution for [PROJECT]` |
| spec-kit-implement (batch) | All spec artifacts for feature | `spec: [feature] spec artifacts (spec, plan, tasks)` |
| spec-kit-implement (phase) | Source code per phase | `feat: [feature] Phase N - [Phase Name]` |
| spec-kit-implement (phase, bypass) | Source code per phase (no tests) | `feat: [feature] Phase N - [Phase Name]` |
| spec-kit-implement (regression) | Source code for regression fixes | `fix: [feature] BF-REGRESSION-001 - fix regressions` |
| spec-kit-implement (bugfix, per-task) | Source code per bugfix fix | `fix: [feature] BF-### - description` |
| spec-kit-test | `specs/[feature]/bugs.md` | `spec(phase-5): [feature] bug log` |
| spec-kit-summarize | Summary/close + patched spec/plan | `spec(phase-6): [feature] summary (health: N%)` |
| spec-kit-refresh | Patched spec artifacts | `spec(refresh): [feature] reconcile artifacts` |

## Rules

- Always `--no-verify` (pre-commit hooks may block spec artifacts)
- Hash is captured for workflow.md traceability
- Silently skip if not a git repo
- Never commit broken state during Implement (tests must pass first)
