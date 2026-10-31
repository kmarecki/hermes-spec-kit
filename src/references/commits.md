# Commits — the record is the commit

Every phase ends in ONE commit whose message carries the record. There is no separate
history file: `git log` is the history, and the close copies the timeline into
`change-record.md` (which survives a squash-merge). Project overrides: `specs/git-conventions.md`.

## Message shape

```
<type>(<scope>): [feature] <subject>

<body — optional, what and why, no narrative>

Phase: <label>                 # Phase 1 · Phase 4 — Core · BF-014 · Acceptance R2 · Phase 5.5 · Phase 6
Implemented-by: <agent>        # hermes | claude | <human> — read by the review's author check
Evidence: <refs or none>       # output:evidence/… ; probe:evidence/… ; ci:<id> ; review:<agent>
```

The three trailers are mandatory on every spec-kit commit. Git reads trailers only from the
**last paragraph** of the message, so they share ONE block with any attribution trailer
(`Co-Authored-By: …`) — no blank line between them. `Implemented-by` on a `feat:`/`fix:` commit
is what the final review reads to decide self-review vs `review:<agent>`.

## Per-skill messages

| Skill | Scope | Message |
|-------|-------|---------|
| constitution | `specs/constitution.md` | `spec(phase-0): constitution for [PROJECT]` |
| specify | `spec.md`, `decisions.md` | `spec(phase-1): [feature] spec` — size S: `spec(phase-1-3): [feature] spec, plan, tasks` |
| clarify | `clarify.md`, `spec.md` | `spec(phase-1.5): [feature] clarifications` |
| plan | plan artifacts | `spec(phase-2): [feature] plan` · bugfix: `spec(phase-2): [feature] bugfix plan (BUG-NNN, …)` |
| tasks | `tasks.md` | `spec(phase-3): [feature] tasks` · bugfix: `spec(phase-3): [feature] bugfix tasks (BUG-NNN, …)` |
| review (pre) | review report | `spec(review): [feature] review findings` |
| implement | code + `tasks.md` `[X]` + evidence | `feat: [feature] Phase N - [name]` · bugfix: `fix: [feature] BF-### - description` · quickfix: `fix: [feature] BF-### - description (plan+tasks+fix)` · regression: `fix: [feature] BF-REGRESSION-001 - fix regressions` |
| test | `bugs.md` | `spec(phase-5): [feature] bug log` |
| test (accept) | `acceptance.md`, evidence, `bugs.md` | `spec(phase-5): [feature] acceptance round N (RESULT a/b)` |
| review (final) | `review-final.md`, evidence, `bugs.md` | `spec(review): [feature] final review (verdict: X)` |
| summarize / close | close doc, change record, patched spec/plan, ADRs, AGENTS.md | `spec(phase-6): [feature] close (health: N%)` |
| refresh | patched artifacts | `spec(refresh): [feature] reconcile artifacts` |

## Rules

- **Intent before code.** A change to requirements or design intent (spec FRs, plan decisions)
  is committed before the code that follows it. Status-only edits (task `[X]`, bug status,
  evidence files) ride the phase's code commit — one commit per phase boundary.
- **Never `--no-verify`.** A hook that blocks a spec artifact is a hook to fix.
- Never commit a red suite during implement; no commits inside a RED sub-phase.
- Not a git repo → skip silently.
- Before every commit: `mcp_spec_kit_lint_artifacts` → 0 errors (no MCP: re-read ids and
  statuses by eye).

## Reading the history back

`spec-kit/scripts/spec-kit-history.sh <feature>` prints the feature's timeline from git
(date · phase · agent · subject · evidence). The close pastes it into `change-record.md`.
