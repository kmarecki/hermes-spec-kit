# Pre-Action Self-Check

Run before any action in any spec-kit skill; stop and report on a failure. After a context
compaction re-run 1–5 and re-read the phase card. Keep this file and the one-screen SKILL.md
in context; open `spec-kit/references/skills/<skill>.md` only for the step you are on.

```
1. BRANCH   git rev-parse --abbrev-ref HEAD ∈ blocked_branches (git-conventions.md)
            → BLOCK "feature branch required: git checkout -b {feature_prefix}/NNN-name"
2. MODE     specs/[feature]/bugs.md has Status: open | in-progress
            → bugfix mode: code only through 'bugfix [feature]' (plan → tasks → implement)
3. LOG BEFORE FIX   the user reports a bug with no BUG-NNN entry
            → BLOCK, route spec-kit-test, HALT
4. CONVENTIONS      specs/git-conventions.md missing → create from
            spec-kit/templates/git-conventions-template.md; `Conventions version:` < 1 → say so
5. PHASE CARD       MCP: mcp_spec_kit_get_next_actions(feature) — read it; no MCP: derive the
            phase from the files and state it in one line. Source code outside Implement → BLOCK
            history ON for this feature (phase card; history-tracking.md) and history.md missing
            → create it (spec-kit/templates/history-template.md)
6. ASSUMPTIONS      at every ASK / WAIT with no human answer: record an `assumption` in
            decisions.md (question, taken, alternative) — never an invented "ruling"; a human
            answer → `ruling` quoting them. Only questions the USER would want to decide (scope,
            behaviour, user-visible trade-offs) go here; a design choice inside the plan's remit
            is plan.md content, not an assumption.
```

## Commit procedure (every skill that writes artifacts)

```
1. history ON (phase card) → APPEND the history.md entry (history-tracking.md — fixed fields,
   real time, ≤ 60 words): mcp_spec_kit_append_history(feature, phase, skill, agent, artifacts,
   tests, evidence, commit, note)  |  no MCP: spec-kit/scripts/spec-kit-log.sh …
   history OFF → nothing to append (implement keeps **Implemented-by** in tasks.md instead)
2. mcp_spec_kit_history_guard(feature, phase) → ok · mcp_spec_kit_lint_artifacts → 0 errors
3. git add <scope>; git commit -m "<message from spec-kit/references/commits.md>"
   Hooks run — never --no-verify.
```
When on, `history.md` is the record that survives the squash-merge; a commit without its entry
is a gap an auditor will find. When off, the change record's timeline is built from git at close.

## No complete overwrite — every phase

Spec artifacts (`spec.md`, `plan.md`, `tasks.md`, `bugs.md`, `clarify.md`, `decisions.md`,
`acceptance.md`, `review-final.md`, close documents) are never rewritten: append sections,
insert entries, patch fields, flip status markers. Before any write, read the file. Forbidden:
copying a template over an existing file, deleting ids, reformatting, rewriting ≥ 50 % of the
lines. First creation is the only exception. Ids (`BUG-NNN`, `T###`, `BF-###`, `AC-###`, `D-###`)
are ascending and never reused.
