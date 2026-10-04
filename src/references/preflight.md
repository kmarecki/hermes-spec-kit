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
             (or {bugfix_prefix}/NNN-name for bugfix)"
     HALT
   
2. MODE DETECTION — STRICT
   IF specs/[feature]/bugs.md EXISTS with Status: open entries:
     BLOCK: "You are in bugfix mode. Cannot write code directly — bugs must go through the workflow.
             Route: 'bugfix [feature]' → plan → tasks → implement."
     HALT
   ELSE:
     MODE = feature

3. UNLOGGED BUG CHECK — before any code change
  IF the user reported a bug or issue (not a planned feature task):
    IF specs/[feature]/bugs.md NOT EXISTS OR the reported issue has no BUG-NNN entry:
      BLOCK: "Bug must be logged before it can be fixed. Run 'test [feature]' first to log the bug,
              then 'bugfix [feature]' to start the fix loop.
              Rule: Log Before Fix — ALWAYS."
      ROUTE to: spec-kit-test
      HALT

4. GIT CONVENTIONS
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
- Bug mode blocks code? ✓ (open bugs → BLOCK, route through bugfix)
- Bug logged before fix? ✓ (unlogged bug → BLOCK, route to spec-kit-test)
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

---

### Shared Commit Procedure (reference from every skill)

**Every skill that creates or modifies markdown artifacts MUST follow this procedure instead of re-implementing it.**

```text
1. APPEND to specs/[feature]/history.md:
   - Phase: [Phase Name]
   - Artifact: [comma-separated list of artifacts created/modified]

2. PRE-COMMIT GUARD:
   READ specs/[feature]/history.md
   IF the entry for this phase is NOT recorded:
     BLOCK: "Cannot commit — history.md is missing the [phase] entry. Append first."

3. COMMIT:
   Follow the auto-commit template for this phase:
   - Scope: [artifacts scope]
   - Message: [commit message template]
   git commit -m "[message]" --no-verify
```

Skills MUST replace their full "Append to history.md and Commit" section with:
```text
Follow the Shared Commit Procedure in spec-kit/references/preflight.md:
- Phase: [Phase Name]
- Artifact: [comma-separated list]
- Scope: [git scope for auto-commit.md]
- Message: "[commit message template]"
```

This ensures the 3-step pattern (append → guard → commit) is defined in ONE place, not copy-pasted across every skill. See each skill's section for the phase-specific phase name, artifacts, and commit message.

3. **No Complete Overwrite — Strict at EVERY phase**. No phase is exempt. Spec artifacts (constitution.md, spec.md, plan.md, tasks.md, bugs.md, clarify.md, close.md, implementation-summary.md, history.md) MUST never be completely overwritten. Every modification must be additive (append new sections, insert new entries) or targeted-edit (update specific fields).

   - **Before any write**: ALWAYS load the existing file first to check if it has substantive content (>=50 lines of spec content).
   - **If the file has substantive content**: NEVER copy a template over it, never rewrite it from scratch, never rewrite >=50% of its lines.
   - **Allowed**: Append new sections, insert new entries between existing ones, modify specific lines/fields, update status markers (e.g. marking a task [X], changing a bug status to verified).
   - **Forbidden**: Replacing all functional requirements, deleting existing task/bug IDs, reformatting the entire document, restructuring sections not relevant to the current change.
   - **history.md is append-only**: NEVER edit or delete past entries. Always append new entries.

   > This rule is UNIVERSAL. It applies during constitution, specify, clarify, plan, tasks, review, implement, test, and close phases. There is no "free iteration" phase. The only exception is first creation (file does not exist yet).

   If you return to modify spec/plan during test or bugfix phases: commit those changes immediately after editing, following the same per-document commit pattern.

4. **Ordering**: bugs.md entries must be ascending by BUG-NNN. tasks.md entries must be ascending by T###. New entries append with the next sequential ID.

## Enforcement

These checks are NOT optional. If you skip them and write to the wrong branch,
the result is workflow corruption. Stop and verify every time.
