# spec-kit MCP Server (v3 — derive and enforce)

A stateless MCP server for the spec-kit workflow, built on the official `mcp` Python SDK (FastMCP, stdio).
It keeps **no state of its own**: every call derives a feature's phase from the files under
`specs/<feature>/` at that moment and validates against them.

## Why no state file

v2 persisted `specs/.spec-kit/state.json`. In a real deployment 30 of 34 features had a stored
state that disagreed with the artifacts on disk, and the single shared JSON conflicted on every
merge. A state updated by voluntary calls from an agent that forgets after context compaction will
drift. The files are the only truth; the server reads them.

## What it is for

The things an LLM agent does badly and a script does perfectly:

| Need | Tool |
|------|------|
| Which phase am I in, what may I write, what is the next gate (also after compaction) | `get_next_actions` → ten-line **phase card** |
| Is this transition valid given the files on disk | `advance_phase`, `close_feature`, `update_artifact` |
| Next BUG-NNN / T### / BF-### / project ADR number | `next_id` |
| Is the branch mechanically mergeable (conflicts, secrets, forbidden files, focused tests, TODOs, unplanned files) | `diff_scan` |
| Has the final review said READY on the current code | `get_feature_state.final_review`, `close_feature` |
| Which acceptance criteria pass, fail, are missing or deferred — from JUnit/TRX results | `acceptance_status` |
| Have the acceptance tests been weakened since their RED run | `acceptance_freeze`, `acceptance_status.frozen_changed`, `lint_artifacts` |
| Are bugs.md / tasks.md / history.md well-formed (statuses, Verified-by, ids, summary counts) | `lint_artifacts` |
| What time is it (never type a timestamp from memory) | `timestamp` |
| Is there a fresh history entry for this phase since the last commit | `history_guard` |
| Append the history record with the real time and a word cap | `append_history` |

## Quick Start

```bash
./scripts/install.sh          # Hermes: copies the server to ~/.hermes/skills/spec-kit/mcp-server/ and configures config.yaml
./scripts/install-claude.sh   # Claude Code: claude mcp add -s user spec-kit … (same server file)
```

Hermes: `/reload-mcp`, then `/toolsets` should list `mcp_spec_kit_*`.
Claude Code: restart; tools appear as `mcp__spec-kit__*`.

## MCP Tools (16)

| Tool | Purpose | Writes |
|------|---------|--------|
| `init_feature` | Create `specs/<feature>/` with a history.md header; error if it exists | dir + history.md header |
| `get_feature_state` | Derived phase, status, size tier (S/M/L from spec.md), artifacts, task/bug counts, final review (verdict, reviewed commit, stale), phase card | — |
| `get_next_actions` | Available actions + phase card | — |
| `advance_phase` | Validate leaving `from_phase`: derived phase is `from_phase` or already `from_phase+1`, named artifacts and next prerequisites exist; 5→6 also needs a fresh READY final review | — |
| `project_status` | Constitution / git-conventions / merge-checklist present, ADR directory, feature count, legacy state file present? | — |
| `project_set_constitution` | Confirm `specs/constitution.md` matches the claimed status | — |
| `list_features` | Every feature's derived state | — |
| `reopen_feature` | Feature is closed on disk → branch hint; reopening is materialised by an open bug in bugs.md | — |
| `close_feature` | Close doc exists with `## Architecture Decisions`; latest `acceptance.md` round PASS and fresh (when spec.md has ACs); latest `review-final.md` round is READY / READY-WITH-FOLLOWUPS and no code commit follows its Reviewed-commit; no open/in-progress bug; verified bugs carry Verified-by; returns claimed-unverified list | — |
| `update_artifact` | Named artifact exists (present/verified) or does not (absent) | — |
| `auto_detect_features` | Derived state of all features; flags legacy `state.json` | — |
| `next_id` | Scan files, return next id for kind BUG / T / BF / AC; ADR → next 4-digit number in the project's ADR directory (`adr_dir` in git-conventions, else docs/adr, docs/decisions, …) | — |
| `acceptance_freeze` | SHA-256 of every file named on a `[TEST] [AC-###]` task → `evidence/acceptance-freeze.json`; additive; a changed frozen file is an error unless `refreeze=true` with the user's reason | evidence/acceptance-freeze.json |
| `acceptance_status` | AC matrix from spec.md (`**AC-###** … Verify: <level>`), tasks.md tags and JUnit/TRX result files (test names carry the id): pass / fail / missing / deferred (e2e) / manual, regressions (failing untagged tests), frozen tests changed → Result PASS / FAIL / STOPPED | — |
| `diff_scan` | Branch diff vs base (`branch_source`): merge conflicts (`git merge-tree`), conflict markers, private keys, secret assignments, AWS keys, focused tests, debugger, TODO/FIXME, forbidden files (.pfx/.pem/.key/.bacpac/.env), files > 1 MB, changed files not named in spec/plan/tasks; specs/ excluded | — |
| `lint_artifacts` | Schema lint: status vocabulary (open/in-progress/claimed/verified/superseded; legacy resolved/fixed = warning), Verified-by on verified, Evidence on claimed, ascending ids, summary rows and totals, history header, review-final.md rounds (Verdict + Reviewed-commit, numbering), spec.md Size line, close doc Architecture Decisions section | — |
| `timestamp` | UTC now, ISO 8601 | — |
| `history_guard` | A history.md entry mentioning `phase` exists and is newer than the last commit touching the feature | — |
| `append_history` | Append one fixed-field entry (timestamp \| phase \| skill \| agent; Artifacts, Tests, Evidence, Commit, Note ≤ 25 words; ≤ 60 words total) with the real UTC time | history.md |

> Hermes prefixes tools with `mcp_spec_kit_`; Claude Code with `mcp__spec-kit__`.

## Phase derivation

| Files under `specs/<feature>/` | Derived phase / status |
|---|---|
| no `spec.md` | 1 specify / `new` |
| `spec.md`, no `plan.md` | 2 plan |
| `plan.md`, no `tasks.md` | 3 tasks |
| `tasks.md` with pending tasks, no `bugs.md`, no close doc | 4 implement |
| all tasks `[X]` or `bugs.md` present, no close doc | 5 test |
| `close.md` / `implementation-summary.md`, no open bug | 6 / `closed` |
| close doc + `bugs.md` with open or in-progress bug | 5 / `reopened` |

## Bug tracking

File-based, deliberately. `bugs.md` is the single source of truth; only `spec-kit-test` writes it.
The server never edits bugs.md — it reads it for derivation, `next_id`, `lint_artifacts` and
`close_feature`. Status vocabulary and the oracle rule: `src/references/evidence.md`.

## Legacy state.json

Ignored. `project_status` and `auto_detect_features` report `legacy_state_file: true` when one
exists — delete it and add `specs/.spec-kit/` to `.gitignore` (the gitignore template does).

## Tests

```bash
cd spec-kit-mcp-server
python3 test_workflow.py   # derivation, validation, close/reopen, next_id, lint, timestamp, history_guard — in temp projects with real files
python3 test_skills.py     # skill/template/reference consistency, tool-name drift
```

Requires a Python with `mcp<2` and `pyyaml` (the repo's `.venv`).
