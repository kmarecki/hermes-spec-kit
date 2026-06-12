# Pre-Action Self-Check

**Must be loaded and followed before ANY action in any spec-kit skill.**

Run these checks in order. If any check fails, stop and report before proceeding.

## Checks

```
1. BRANCH CHECK
   CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
   IF CURRENT_BRANCH == blocked_branches (from git-conventions.md, step 3):
     BLOCK: "On a blocked branch. All spec-kit work must be on a
             feature branch. Run:
             git checkout -b {feature_prefix}/NNN-name
             (or {bugfix_prefix}/NNN-name for bugfix, {explore_prefix}/NNN-name for explore)"
     HALT
   
2. MODE DETECTION
   IF specs/[feature]/bugs.md EXISTS with Status: open entries:
     MODE = bugfix
     NOTE: "You are in bugfix mode for [feature]. Must route through
            spec-kit-workflow before any code changes."
   ELSE:
     MODE = feature

3. GIT CONVENTIONS
   IF specs/git-conventions.md EXISTS in the project root:
     LOAD and apply for branch naming, commit messages, and merge behaviour.
     CHECK version: read `Conventions version:` line from the file
       IF version < 1: NOTE "Your git-conventions.md is outdated. Re-copy from spec-kit/templates/git-conventions-template.md."
     NOTE: Conventions override the defaults shown in each skill.
   ELSE:
     CREATE specs/git-conventions.md from spec-kit/templates/git-conventions-template.md
     NOTE: "Created specs/git-conventions.md with default conventions. Edit to customise for this project."

4. WORKFLOW LOAD CHECK — code-writing phase only
   IF you are about to call write_file, patch, or terminal(build/test):
     IF spec-kit-workflow is NOT loaded:
       BLOCK: "Must load spec-kit-workflow first for branch guardrails
               and phase routing. Run: skill_view(name='spec-kit-workflow')"
       HALT
```

## Quick summary for fast reference

- Not on main/master? ✓
- In bugfix mode? ✓ (if bugs.md open, route through workflow)
- Workflow loaded before code? ✓

## Post-Completion Requirements (MANDATORY)

After every skill completes that created or modified any markdown document:

1. **Append to history.md**: Every markdown file created or modified MUST be recorded in `specs/[feature]/history.md`. Create the file if it doesn't exist.

2. **Commit**: Commit changed markdown documents immediately.
   - One change → one commit
   - Multiple related changes in one logical action (e.g. clarify updates clarify.md + amends spec.md) → one commit
   - Use commit template from specs/git-conventions.md (see auto-commit.md)
   - Skip silently if not a git repo

3. **Additive-only editing**: NEVER delete, overwrite, or reorder existing content in bugs.md, tasks.md, plan.md, spec.md, clarify.md, close.md, or implementation-summary.md. Always append new entries at the end. If modifying an existing entry (e.g. updating bug status), change only the specific field — never remove the row.

4. **Ordering**: bugs.md entries must be ascending by BUG-NNN. tasks.md entries must be ascending by T###. New entries append with the next sequential ID.

## Enforcement

These checks are NOT optional. If you skip them and write to the wrong branch,
the result is workflow corruption. Stop and verify every time.
