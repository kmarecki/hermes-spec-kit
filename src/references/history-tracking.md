# Process History

Every spec feature directory maintains `specs/[feature]/history.md` — an append-only process history. Each phase skill appends one entry when it completes.

## Standard Entry Format

```markdown
## [ISO_TIMESTAMP] | [Phase Name] → Complete
- **Skill**: spec-kit-[skill-name]
- **Artifacts**: [comma-separated list of files created or modified]
- **Notes**: [optional — key decisions, deviations, or notable events]
```

## Example

```markdown
## 2026-06-08T10:00:00 | Phase 1 → Complete
- **Skill**: spec-kit-specify
- **Artifacts**: specs/001-user-auth/spec.md
- **Notes**: OAuth2 with JWT tokens, 3 user stories
```

> **No commit hashes**: history entries deliberately do NOT record commit hashes.
> Feature branches are squash-merged, so pre-merge hashes don't exist in the
> target branch's history — recording them is dead data. Traceability comes
> from the phase name + timestamp + commit message convention (`spec(phase-N): [feature] ...`),
> which survive the squash.

## How to Use

At the end of any phase skill, after all artifacts are written and committed, append to history.md:

```
FULL_PATH="specs/[feature]/history.md"

CREATE history.md IF NOT EXISTS with header:
  # Process History: [Feature]

APPEND entry:
  ## [$(date -u +"%Y-%m-%dT%H:%M:%SZ")] | [Phase] → Complete
  - **Skill**: spec-kit-[skill]
  - **Artifacts**: [files]
  - **Notes**: [summary of what was done]
```

## Phase Name Reference

| Skill | Phase Name |
|-------|-----------|
| spec-kit-constitution | Phase 0 |
| spec-kit-specify | Phase 1 |
| spec-kit-clarify | Phase 1.5 |
| spec-kit-plan | Phase 2 |
| spec-kit-tasks | Phase 3 |
| spec-kit-review (pre-implement) | Phase 3.5 |
| spec-kit-implement | Phase 4 (each sub-phase logged as Phase N) |
| spec-kit-implement | Phase 4 → Full Regression → Pass (after all phases, full suite passes) |
| spec-kit-implement | Phase 4 → Regression Fix → Complete (BF-REGRESSION-001 resolved) |
| spec-kit-implement | Phase 4 → Bugfix BF-### → Complete (per-bugfix during bugfix mode) |
| spec-kit-test | Phase 5 |
| spec-kit-review (post-implement) | Phase 5.5 |
| spec-kit-summarize | Phase 6 |
| spec-kit-refresh | Refresh |
| Reopen (workflow) | Reopen |

## Guard: history.md Before Every Commit

**history.md entries MUST be written before the corresponding git commit — never after.** Every commit in `spec-kit-implement` is preceded by a history.md entry:

1. **Per-phase commit**: Entry appended in step 4f — includes test pass count and task completion count.
2. **Bugfix commit (BF-###)**: Entry appended in bugfix mode step 3 — includes which BUG-NNN was fixed and test verification.
3. **Regression fix commit (BF-REGRESSION-001)**: Entry appended in regression fix flow — includes full suite pass confirmation.
4. **Full regression pass**: Entry appended in step 7 when all tests pass — standalone verification record (no commit, documents the checkpoint).

The PRE-COMMIT GUARD reads history.md and blocks the commit if the entry is missing. This ensures the process log is never behind the git log.
