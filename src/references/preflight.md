# Pre-Action Self-Check

**Must be loaded and followed before ANY action in any spec-kit skill.**

Run these checks in order. If any check fails, stop and report before proceeding.

## Checks

```
1. BRANCH CHECK
   CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
   IF CURRENT_BRANCH == "main" OR CURRENT_BRANCH == "master":
     BLOCK: "On branch main/master. All spec-kit work must be on a
             feature branch. Run:
             git checkout -b feat/NNN-name
             (or bug/NNN-name for bugfix, explore/NNN-name for explore)"
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
     NOTE: Conventions override the defaults shown in each skill.

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

## Enforcement

These checks are NOT optional. If you skip them and write to the wrong branch,
the result is workflow corruption. Stop and verify every time.
