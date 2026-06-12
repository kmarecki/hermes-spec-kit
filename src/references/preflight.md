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

5. HISTORY LOG CHECK — BEFORE creating or modifying any markdown document
   IF you are about to create or modify any markdown document in specs/[feature]/:
     ENSURE specs/[feature]/history.md EXISTS (create with header if missing)
     NOTE: "history.md is the process log for this feature. Every markdown
            change MUST be recorded here BEFORE the next commit."
```

## Quick summary for fast reference

- Not on main/master? ✓
- In bugfix mode? ✓ (if bugs.md open, route through workflow)
- Workflow loaded before code? ✓
- history.md exists for this feature? ✓ (created if missing)

## Post-Completion Requirements (MANDATORY)

After every skill completes that created or modified any markdown document:

1. **history.md is already ready** (pre-action check #5 already ensured it exists). Append an entry for each document created or modified:
   - Format: `## [ISO_TIMESTAMP] | [Phase Name] → Complete` with skill, artifacts, commit hash, notes
   - See `spec-kit/references/history-tracking.md` for the exact format
   - This is NOT optional — if you skip this, the process log will be missing

2. **PRE-COMMIT GUARD — Verify history.md is updated**
   BEFORE running `git add` and `git commit`:
   ```text
   READ specs/[feature]/history.md
   IF any markdown document created/modified in THIS skill run is NOT recorded:
     BLOCK: "Cannot commit — history.md is missing entries for [document(s)].
             Append entries first."
   ```
   Only proceed to commit after history.md is verified complete.
   - **Spec/plan changes that alter requirements or design intent** → MUST be committed BEFORE any related code. This preserves the causal chain: spec describes what → code implements it. Never commit spec changes as a side-effect of a code commit.
   - **Status-only updates** (bug verified, task marked [X], bug status changed) → CAN share a commit with code. These document what the code did, not what it should do.
   - **Bugfix sub-round documents** (new plan section for new bugs, new tasks for new bugs):
     - `bugfix` (default): plan gets its own commit, tasks get its own commit, implementation commits per fix.
     - `quickfix` (user opt-in): plan + tasks + fix batched in one commit. Plan ref and task entry ALWAYS exist.
   - **Phase 6 close** (patched spec/plan + close.md) → ONE commit. This is explicit intentional reconciliation.
   - **One change → one commit**. Multiple related changes in one logical action (e.g. clarify updates clarify.md + amends spec.md) → one commit.
   - Use commit template from specs/git-conventions.md (see auto-commit.md).
   - Skip silently if not a git repo.

3. **Additive-safe editing**. During design phases (0-3), you may freely iterate — rewrite, restructure, refactor spec/plan/tasks as needed. The review skill may propose changes freely. Each design phase skill commits its artifacts immediately (no batching).
   
   During implementation and bugfix phases (4+), the additive-safe rule tightens: never delete or reorder existing entries in bugs.md, tasks.md, plan.md, spec.md, clarify.md, close.md, or implementation-summary.md. You MAY modify existing entries — update status fields, amend text, correct inaccuracies — but the modification must be minimal (change only the specific field or section needed). Never restructure or refactor a document beyond what's required for the change. New entries (new bugs, tasks, plan sections) always append at the end. The goal: preserve every existing bug ID, task ID, and requirement — only update what the current change demands.
   
   If you return to modify spec/plan during test or bugfix phases: commit those changes immediately after editing, following the same per-document commit pattern.

4. **Ordering**: bugs.md entries must be ascending by BUG-NNN. tasks.md entries must be ascending by T###. New entries append with the next sequential ID.

## Enforcement

These checks are NOT optional. If you skip them and write to the wrong branch,
the result is workflow corruption. Stop and verify every time.
