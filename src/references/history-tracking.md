# Process History — the record, not the story

`specs/[feature]/history.md` is an append-only **record**: one fixed-field entry per phase
completion, bugfix, regression run or close. It exists so that an agent (or a human) can read
in ten seconds what was done, when, with what evidence, and by whom — and so the pre-commit
guard can prove the entry was written before the commit.

It is **not** the place for narrative. Decisions, rationale and what-went-wrong belong in
`close.md` / `change-record.md` (phase 6), `decisions.md` (assumptions) or the commit body.
It is the record that survives the squash-merge; the close copies its timeline into `change-record.md`.
In one deployment history files reached 215 KB with 1 600-word entries and invented
timestamps — nobody read them. The format below is capped and machine-appended.

## Entry format

```markdown
## <UTC ISO timestamp> | <Phase label> | <skill> | <agent>
- Artifacts: <comma-separated files created or modified>
- Tests: <command> → <N passed, M failed>   (or "none")
- Evidence: <output:…; probe:…; ci:…; review:…>   (or "none — unverified")
- Commit: <commit message that follows>
- Note: <≤ 25 words — the one fact a reader needs; nothing else>
```

Rules:
- **Timestamp from the clock**, never from memory: `mcp_spec_kit_timestamp()` or `date -u +%Y-%m-%dT%H:%M:%S+00:00`.
- `<agent>` is `hermes`, `claude`, or the human's name — this is the `Implemented-by` the review and evidence rules read.
- Whole entry ≤ 60 words after the header. The appender refuses longer notes.
- Append only. Never edit or delete a past entry; a correction is a new entry.
- No commit hashes (branches are squash-merged; the commit *message* is the traceability link).

## How to append

With the MCP server (preferred — it stamps the real time and enforces the cap):

```text
CALL mcp_spec_kit_append_history(feature="[feature]", phase="Phase 2", skill="spec-kit-plan",
     agent="claude", artifacts="plan.md, research.md", tests="none",
     evidence="none", commit="spec(phase-2): [feature] plan", note="HQ-currency resolution deferred to F")
```

Without MCP — the shipped script does the same from the shell:

```bash
~/.hermes/skills/spec-kit/scripts/spec-kit-log.sh <feature> "<Phase label>" <skill> <agent> \
    --artifacts "plan.md, research.md" --tests "none" --evidence "none" \
    --commit "spec(phase-2): [feature] plan" --note "HQ-currency resolution deferred to F"
```
(Claude Code: the same path under `~/.claude/skills/spec-kit/scripts/`.)

If neither is available, write the entry by hand in the exact format, taking the time from `date -u`.

## Phase labels

| Skill | Phase label |
|-------|-------------|
| spec-kit-specify | `Phase 1` |
| spec-kit-clarify | `Phase 1.5` |
| spec-kit-plan | `Phase 2` (bugfix round: `Phase 2 — bugfix round N`) |
| spec-kit-tasks | `Phase 3` (bugfix round: `Phase 3 — bugfix round N`) |
| spec-kit-review | `Phase 3.5` / `Phase 5.5` |
| spec-kit-implement | `Phase 4 — <sub-phase name>` · `BF-###` · `Regression` · `Regression fix` |
| spec-kit-test | `Phase 5` |
| spec-kit-summarize | `Phase 6` |
| spec-kit-refresh | `Refresh` |
| workflow reopen | `Reopen` |

The constitution is project-level and has no feature history.

## Guard: history before every commit

Every commit touching `specs/[feature]/` or the feature's code is preceded by an entry.
`mcp_spec_kit_history_guard(feature, phase)` checks that an entry mentioning the phase label is
newer than the last commit touching the feature; the Shared Commit Procedure in `preflight.md`
calls it. Without MCP, read the last entry's header before `git commit`.
