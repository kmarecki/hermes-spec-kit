# Git Conventions for this project
# Conventions version: 1
#
# A new version prompts projects to re-copy.

Copy to `specs/git-conventions.md` and edit; absent → the defaults shown.

---

## Branch naming

```
feature_prefix: feat          # e.g. feat/011-user-auth
bugfix_prefix: bug            # e.g. bug/011-login-crash
reopen_suffix: -bugfixing     # e.g. feat/011-user-auth-bugfixing
branch_source: main           # source branch for reopen (main, master, develop)
blocked_branches: main, master   # rigor lean + trunk: none (commits on main allowed)
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
| Acceptance round | `spec(phase-5): {feature} acceptance round {N} ({RESULT} {a}/{b})` |
| Final review | `spec(review): {feature} final review (verdict: {VERDICT})` |
| Close/Summary | `spec(phase-6): {feature} summary (health: {N}%)` |
| Refresh | `spec(refresh): {feature} reconcile artifacts` |

---

## Documentation locations

Used by the close (ADRs, AGENTS.md) and by the final review (merge checklist). Omit a key to
use the default.

```
# adr_dir: docs/adr             # set by the constitution (scale = platform); default: first existing of docs/adr, docs/decisions, doc/adr, adr
# adr_index: docs/adr/README.md # the ADR list to update; default: README.md / index.md in adr_dir
agents_file: AGENTS.md          # the agent context file kept current at close (also CLAUDE.md if it restates it)
merge_checklist: specs/merge-checklist.md
# rigor: standard             # lean | standard | strict — set by the constitution (Level 0); absent = standard (spec-kit/references/rigor.md)
# history: large              # always | large | never — keep specs/<feature>/history.md; absent → process level P3 only (rigor.md); spec.md `**History**: on|off` overrides
# design_dir: docs/design       # living module design docs (design-doc-template.md); ABSENT → plan.md's Current Design is the only design, nothing else is created
# epics_dir: specs/epics        # epics as specs/epics/NNN-name/{epic,plan,features,review}.md (NNN = tracker epic id, e.g. ADO); ABSENT → every feature is its own epic
# epics_index: on               # on | off — keep [epics_dir]/README.md, the roadmap table (one row per epic), maintained by spec-kit-epic
# changelog: CHANGELOG.md       # Keep-a-Changelog file the close adds an Unreleased line to; ABSENT → no changelog step
# runbooks_dir: docs/runbooks   # operational docs the close checks for statements the diff made wrong; ABSENT → skipped
# compliance: none            # none | baseline — baseline: per-feature security level, [SEC] tasks, security scans, human approver for high (spec-kit/references/compliance.md)
```

The commented keys are written by the constitution's scale question (small: none · platform: adr /
design / epics). Without `design_dir` / `epics_dir` nothing is created unprompted.

---

## Merge behaviour

```
always_push: true
push_remote: origin
```

---

## Customising

Edit the values; the skills follow them. Custom commit format: `style: custom` +
`commit_phase: "[{feature}] Phase {N}: {Phase Name}"`.
