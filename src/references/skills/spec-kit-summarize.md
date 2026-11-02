# spec-kit-summarize — full procedure

> **Loaded on demand** — the one-screen SKILL.md is the entry point; this file holds only what it leaves out. Read the section you need.

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
`Implemented-by` from the history.md implement entries (or the tasks.md header when history is off) and the review label from review-final.md. No oracle → ❌
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

## Runbooks and changelog (optional — only what the project keeps)
```
RUNBOOKS = git-conventions runbooks_dir (absent → skip): grep the runbooks for commands, settings,
  endpoints, procedures the diff changed → targeted patch per statement, WAIT, apply approved
CHANGELOG = git-conventions changelog (absent → skip): under "## [Unreleased]" add ONE line in the
  right group (Added / Changed / Fixed / Removed / Security): "<one sentence> (<ticket>)" — never
  a feature narrative; the PR description already has that
```

## Design doc and epic row (optional — only what the project keeps)
```
DESIGN_DIR = git-conventions design_dir · EPICS_DIR = epics_dir   (absent → "none kept", skip)
FOR each module in plan.md **Modules**:  DOC = DESIGN_DIR/<module>.md
  missing → NOTE "no design doc for <module> — run 'spec-kit design <module>'" (never create it here)
  else → which sections does the diff make wrong? components (paths), data flow, seams /
         contracts, invariants & security, testing, known debt, Decisions (new ADRs)
         → targeted patch per section, WAIT, apply approved; append "- <date> <feature> — <what>"
         to the change log; bump Last patched
EPIC = spec.md **Epic**:  FILE = EPICS_DIR/<epic>/features.md
  missing → NOTE "spec names epic <epic> but <FILE> does not exist — run 'spec-kit epic <epic>'"
  else → set this feature's row: Status closed · PR · Health N% · ADRs; add the row if absent;
         epics_index on (default) → update the epic's row in EPICS_DIR/README.md (features closed / planned);
         every row closed or dropped → suggest "close epic <epic>"
RECORD both outcomes in the close document (Artifact State) and in the change record (Decisions / follow-ups)
```

## Change record
`spec-kit/templates/change-record-template.md` → `specs/[feature]/change-record.md`. Every field
filled from what exists (spec Security & Privacy, size ruling, history.md, acceptance round,
review round, decisions, ADRs) or written `pending` (PR reviewer, deployment approval) — never
blank. Timeline: history on → one row per history.md entry (date, phase, agent, evidence, commit
message); history off → `spec-kit/scripts/spec-kit-history.sh [feature]` (date · author · subject)
run on the branch now, before the squash. The record is the one page an auditor reads and the
one that survives the squash-merge.

## Reopen
Close doc exists → APPEND `## Reopened — <date>` (previous health → new health, changed
artifacts, new gaps, decisions); the original close is never edited. A requirement that went
from ✅ to worse → ASK: new entry (recommended) or overwrite.

## Finish
❌ Not Done gaps → `open` bugs (`mcp_spec_kit_next_id`). `mcp_spec_kit_update_artifact(close.md)` ·
`mcp_spec_kit_close_feature` (errors: open bugs, verified without oracle, review missing / NOT READY /
stale, no Architecture Decisions) · `mcp_spec_kit_lint_artifacts` · ONE commit
`spec(phase-6): [feature] close (health: N%)` after the history entry (preflight commit procedure). Report: mode,
health, tasks, bugs, patches, ADRs, AGENTS.md, change record. Then open THE PR (`spec-kit/references/commits.md`).
