# Git Conventions for this project
# Conventions version: 1
#
# When this version is incremented, projects with existing specs/git-conventions.md
# will be prompted to re-copy. Skills check the version at startup.

Copy this file to `specs/git-conventions.md` in your project and edit.
Spec-kit skills load it automatically if it exists.
If it doesn't exist, built-in defaults (shown below) apply.

---

## Branch naming

```
feature_prefix: feat          # e.g. feat/011-user-auth
bugfix_prefix: bug            # e.g. bug/011-login-crash
reopen_suffix: -bugfixing     # e.g. feat/011-user-auth-bugfixing
branch_source: main           # source branch for reopen (main, master, develop)
blocked_branches: main, master
```

### Generated branch patterns

| Operation | Pattern |
|-----------|---------|
| New feature | `{feature_prefix}/{NNN}-{short-name}` |
| Bugfix | `{bugfix_prefix}/{NNN}-{short-name}` |
| Explore variant | `{explore_prefix}/{NNN}-{feature}-{variant}` |
| Reopen (from closed) | `{original_prefix}/{NNN}-{short-name}{reopen_suffix}` |

---

## Commit messages

```
style: conventional-commits    # conventional-commits | custom
```

### Per-operation templates

| Operation | Message |
|-----------|---------|
| Constitution | `spec(phase-0): constitution for {PROJECT}` |
| Spec + plan + tasks (size S) | `spec(phase-1-3): {feature} spec, plan, tasks` |
| Implement phase | `feat: {feature} Phase {N} - {Phase Name}` |
| Regression umbrella | `fix: {feature} BF-REGRESSION-001 - fix regressions` |
| Bugfix (per task) | `fix: {feature} BF-{###} - description` |
| Bug log | `spec(phase-5): {feature} bug log` |
| Final review | `spec(review): {feature} final review (verdict: {VERDICT})` |
| Close/Summary | `spec(phase-6): {feature} summary (health: {N}%)` |
| Refresh | `spec(refresh): {feature} reconcile artifacts` |

---

## Documentation locations

Used by the close (ADRs, AGENTS.md) and by the final review (merge checklist). Omit a key to
use the default.

```
adr_dir: docs/adr               # default: first existing of docs/adr, docs/decisions, doc/adr, adr
adr_index: docs/adr/README.md   # the ADR list to update; default: README.md / index.md in adr_dir
agents_file: AGENTS.md          # the agent context file kept current at close (also CLAUDE.md if it restates it)
merge_checklist: specs/merge-checklist.md
```

---

## Merge behaviour

```
always_push: true
push_remote: origin
```

---

## Customising for your project

1. Copy this file to `specs/git-conventions.md` in your project root
2. Edit the values to match your project's conventions
3. Spec-kit skills will automatically detect and follow them
4. No need to edit any skill files

### Examples

```yaml
# Project uses "feature/" prefix and "develop" as base branch:
feature_prefix: feature
branch_source: develop

# Project uses custom commit format:
style: custom
commit_phase: "[{feature}] Phase {N}: {Phase Name}"
```
