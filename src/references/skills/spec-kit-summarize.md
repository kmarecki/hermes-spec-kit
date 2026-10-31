# spec-kit-summarize — full procedure

> **Loaded on demand** — the one-screen SKILL.md is the entry point; this file holds only what it leaves out. Read the section you need. Hermes tools (`terminal`, `write_file`/`patch`, `read_file`, `search_files`, `skill_view`) map to Claude Code `Bash`, `Write`/`Edit`, `Read`, `Grep`/`Glob`, `Skill`; MCP `mcp_spec_kit_*` = `mcp__spec-kit__*`.

## Gate
```
review-final.md latest round: missing → BLOCK "run the final review"
  NOT READY → BLOCK "bugfix, then re-review" · AWAITING-OWNER → BLOCK "get the owner's answer, Round N+1"
  code changed after Reviewed-commit (git log <sha>..HEAD -- . ':(exclude)specs') → BLOCK "re-review"
bugs.md open / in-progress → BLOCK "bugfix"
mcp_spec_kit_get_feature_state → state.final_review / acceptance say the same
```
Mode: "close" / "summarize" as said; else S/M → close, L → summarize (full gap table). Output
depth follows `git diff {branch_source} --name-status`, not the size of the spec: few files →
short; a single bugfix → one paragraph (root cause + fix). Every sentence reflects the diff.

## Gap analysis
```
FOR each FR / story / SC / entity / contract (M: only the ones that are not ✅; L: all):
  ✅ Resolved — as planned (code + test + evidence named)  |  ✅ Resolved — intentional deviation (rationale)
  ⚠️ Acknowledged — deferred, reason and who decided        |  ❌ Not Done — missing, no reason → bug
health = round((resolved + acknowledged) / total × 100); total 0 → 100
Reuse review-final §1 rows and the acceptance matrix — do not re-derive them.
```
Deviations → propose each spec.md / plan.md / data-model.md patch ("(Updated at close)"); WAIT;
rejected → ⚠️ needs review in Artifact State. Regenerate `plan.md` → `## Current Design` (≤ 1
page, what is BUILT; rounds untouched).

## Evidence table
Acceptance / regression `output:` + `ci:`; a `probe:` per seam in the plan or the diff;
`Implemented-by` and the review label from the commits and review-final.md. No oracle → ❌
unverified — never omitted, never upgraded. `claimed` bugs without `Verified-by` → *Unverified
claims*; the feature may still close, saying so.

## ADRs
```
ADR_DIR = git-conventions adr_dir | mcp_spec_kit_next_id(kind="ADR").adr_dir | first of docs/adr,
          docs/decisions, doc/adr, adr | none → ASK to create (default docs/adr + README index);
          declined → every candidate feature-local
INDEX + TEMPLATE = the project's (README/index.md "## Template", else the newest ADR's shape,
          else spec-kit/templates/adr-template.md); follow the index's rules
HARVEST  decisions.md rulings (+ confirmed assumptions) · plan Rounds and design decisions ·
         research decisions · review findings that changed the design · approved deviations ·
         the diff (new dependency / pattern / boundary nobody wrote down)
BAR (any): constrains code beyond this feature · expensive to reverse (schema, contract, data
         ownership, platform, dependency) · chooses between real alternatives a reader would
         re-litigate · changes or contradicts an existing ADR · AGENTS.md / constitution would
         otherwise be wrong.   Feature-local (component name, helper, test layout) → plan.md.
PER candidate passing the bar: same decision exists → append Evidence / Related; contradicts an
         Accepted ADR → new ADR "supersedes NNNN" + the old status line "Superseded by <new>";
         narrows / extends → "amends NNNN"; else new. PRESENT (number, title, Decision, action,
         origin) → WAIT → write (Status Accepted + date + quoted ruling as Deciders, or Proposed)
         or "feature-local (declined)". Update the index. Fill the close's table; "none met the
         ADR bar" is a row — the section is never omitted (close_feature checks it).
```

## AGENTS.md
For AGENTS.md and files restating it (CLAUDE.md, .github/copilot-instructions.md, .claude/rules/*,
.cursor/rules/*): which statements does the diff, a new / superseded ADR, or resolved debt make
WRONG or INCOMPLETE — commands, layout, boundaries, versions, dependencies, conventions, known
debt, ADR list, the spec-kit block. No narrative, no changelog. Targeted patch per section →
WAIT → apply approved ones only. Record "updated — <sections>" or "no change needed — <why>".

## Change record
`spec-kit/templates/change-record-template.md` → `specs/[feature]/change-record.md`. Every field
filled from what exists (spec Security & Privacy, size ruling, commit trailers, acceptance round,
review round, decisions, ADRs) or written `pending` (PR reviewer, deployment approval) — never
blank. Timeline: paste `spec-kit/scripts/spec-kit-history.sh [feature]`. The record is the one
page an auditor reads; it survives the squash-merge that erases the phase commits.

## Reopen
Close doc exists → APPEND `## Reopened — <date>` (previous health → new health, changed
artifacts, new gaps, decisions); the original close is never edited. A requirement that went
from ✅ to worse → ASK: new entry (recommended) or overwrite.

## Finish
❌ Not Done gaps → `open` bugs (`mcp_spec_kit_next_id`). `mcp_spec_kit_update_artifact(close.md)` ·
`mcp_spec_kit_close_feature` (errors: open bugs, verified without oracle, review missing / NOT READY /
stale, no Architecture Decisions) · `mcp_spec_kit_lint_artifacts` · ONE commit
`spec(phase-6): [feature] close (health: N%)` per `spec-kit/references/commits.md`. Report: mode,
health, tasks, bugs, patches, ADRs, AGENTS.md, change record.
