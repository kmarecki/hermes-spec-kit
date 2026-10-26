# spec-kit-summarize — full procedure

> **Loaded on demand.** The one-screen `spec-kit-summarize` SKILL.md is the entry point; this file holds the complete
> procedure (every branch, template field and pitfall). Read the section you need, not the whole file.
> Tool names: Hermes (`terminal`, `write_file`, `patch`, `read_file`, `skill_view`) — Claude Code maps them to
> `Bash`, `Write`/`Edit`, `Read`, `Skill`; MCP tools are `mcp_spec_kit_*` / `mcp__spec-kit__*`.

**Phase**: 6 (Summary / Close — Mandatory)

**Task Persona**: Adopt the mindset of a thorough code auditor. Verify every claim against actual code — check spec.md, plan.md, and the git diff together. Use web search to research best patterns and practices when evaluating architecture decisions. Describe exactly what changed, why, and whether it matches the spec. No filler, no fluff. Detail is proportionate to actual work done.

**Purpose**: When implementation is complete, testing is done and the final review says READY, produce either a full `implementation-summary.md` or a lightweight `close.md`. Computes spec health score (0-100%), patches spec.md/plan.md for intentional deviations, **writes or updates the project's ADRs** for decisions that pass the ADR bar, and **keeps AGENTS.md current**. **Mandatory** before a feature can be marked complete.

**When NOT to use**: For mid-stream alignment — use `spec-kit-refresh` instead.

**Routing**: Load this skill when the user says "summarize [feature]" or "close [feature]". If loaded directly, load spec-kit-workflow first to check prerequisites.

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Git Commit Guidelines
See `spec-kit/references/auto-commit.md`. Commits run the project's hooks (never `--no-verify`). Branch guard handled by preflight.md.


**When to run**:
- **After bugfix loop completes** (all bugs verified) — suggested as mandatory close (user decides when to run it)
- User says: "Summarize [feature]" — full gap analysis
- User says: "Close [feature]" — lightweight close

**Prerequisites**: `spec-kit-implement` must have been run (tasks.md exists)
**Artifacts**:
- `specs/[feature]/implementation-summary.md` (full gap analysis report)
- `specs/[feature]/close.md` (lightweight close document)
- `specs/[feature]/spec.md` (auto-updated to reflect intentional deviations)
- `specs/[feature]/plan.md` (auto-updated to reflect intentional deviations)
- ADR files in the project's ADR directory + the ADR index (approved per ADR)
- `AGENTS.md` (and agent rule files that restate it) — targeted patches, approved per patch

## Execution

### Gate: the final review
```
READ specs/[feature]/review-final.md — the LATEST "## Round N" section
IF the file is missing:
  BLOCK: "No final review. Run the final review first ('final review [feature]' → spec-kit-review)."
IF its **Verdict** is NOT READY:
  BLOCK: "The final review says NOT READY — run 'bugfix [feature]', then the final review again."
IF code changed after its **Reviewed-commit**
   (git log <sha>..HEAD -- . ':(exclude)specs' is not empty, or the sha is unknown):
  BLOCK: "Code changed after the final review (Round N @ <sha>) — re-run the final review."
MCP: mcp_spec_kit_get_feature_state(feature).state.final_review gives the same answer.
READY-WITH-FOLLOWUPS → carry its follow-ups into the close document (Open Questions / Future Work).
```

### Determine Mode
```
IF user explicitly says "close [feature]":
  USE lightweight close mode → close-template.md
  NOTE: "Lightweight close — captures key decisions and state without deep gap analysis."

ELIF user explicitly says "summarize [feature]":
  USE full summary mode → implementation-summary-template.md
  RUN all steps below

ELIF all bugs in bugs.md have Status: verified:
  NOTE: "All bugs verified. Suggest running 'close [feature]' or 'summarize [feature]' to complete Phase 6 (mandatory)."
  PROMPT user for which mode: full summary or lightweight close
  USE the mode they selected

ELIF spec.md **Size** is S:
  USE lightweight close mode (spec-kit/references/sizing.md)
ELIF spec.md **Size** is L:
  USE full summary mode
ELSE:
  ASK the user: full summary or lightweight close (default: full summary)

OUTPUT RULE — applies to both modes:
  The length and detail of the summary MUST be proportional to the actual
  code changes made, not to the size of spec.md or tasks.md.
  
  GIT DIFF determines depth:
    - Few files changed → short, precise summary of what was touched
    - Many files / complex changes → thorough description per file/area
    - Single bugfix → one paragraph covering root cause + fix
  
  Always produce a precise, factual description of what code was changed
  and why. Avoid generic filler text. Every sentence should reflect a real
  change visible in the diff.
```

### Load artifacts and detect TDD mode
```
LOAD specs/[feature]/spec.md, plan.md, tasks.md
LOAD data-model.md, contracts/, research.md, quickstart.md, clarify.md (IF EXISTS)
LOAD bugs.md (IF EXISTS), constitution.md (IF EXISTS)

SCAN tasks.md for `> **TDD**: Bypassed by user request`
  IF found: SET tdd_bypassed = true
  IF not found: SET tdd_bypassed = false
```

### Analyze tasks.md completion
```
SCAN all tasks:
  COUNT total tasks
  COUNT completed tasks (marked [X])
  COUNT incomplete tasks (marked [ ])
  IDENTIFY remaining work from incomplete tasks

IF all tasks are complete:
  SET all task markers to [X]
  WRITE updated tasks.md
```

### Analyze bugs.md status
```
IF bugs.md EXISTS:
  SCAN all bugs:
    COUNT total bugs
    COUNT verified (with Verified-by)
    COUNT claimed (legacy resolved/fixed count as claimed)
    COUNT open / in-progress

  NEVER change a bug's status here — this skill has no oracle.
  IF any bug is open or in-progress:
    BLOCK: "Cannot close — N bugs still open. Run 'bugfix [feature]'."
  IF any bug is claimed without Verified-by:
    LIST them in the close document under "Unverified claims" and set the
    bugs.md row of the Artifact State table to ⚠️ N claimed-unverified.
    The feature may still close, but the close says so in plain words.
```

### Collect evidence (evidence.md)
```
FOR the full regression: find output:/ci: references in history.md and evidence/
FOR each external seam named in plan.md or touched per git diff: find its probe: file
FOR the review: read Implemented-by from history.md and the review report's label
  (review:<other-agent> counts; self-review does not)
FILL the Evidence table of the close/summary template.
A gate with no oracle is written as ❌ unverified — never omitted, never upgraded.
```

### Compare code against spec and plan (git diff)
*Skip in lightweight close mode*
```
RUN: git diff {branch_source} --name-status
  OR: git log --oneline --name-only HEAD..{branch_source}
  (branch_source from specs/git-conventions.md, default: main)
  CAPTURE list of files changed, added, deleted

FOR each file changed:
  MATCH to task descriptions in tasks.md
  MATCH to functional requirements in spec.md (FR-###)
  MATCH to architecture/data-model sections in plan.md

IDENTIFY:
  - Files that correspond to planned tasks → mark as implemented
  - Files that have NO corresponding task or requirement → flag as "unplanned change"
  - Requirements/FRs that have NO implementing files → flag as "gap — not implemented"
  - Plan sections (data-model entities, contracts) with no corresponding code → flag as "gap — deferred"
```

### Build gap analysis
*Skip in lightweight close mode*
```
FOR EACH requirement/story/entity/contract in spec.md and plan.md:
  VERDICT (a ✅ needs an evidence reference — output:/ci:/probe:/review:/user; without one the item is ⚠️ at best):
    ✅ Resolved  — implemented as planned (code exists, tests pass, evidence named)
    ✅ Resolved  — intentional deviation (code differs from plan, rationale documented)
    ⚠️ Acknowledged — deferred (not critical, tracked for future)
    ❌ Not Done  — missing with no documented reason (should be added to bugs.md or new spec)

FOR each gap marked "❌ Not Done":
  RECOMMEND: add a bug to bugs.md or create a follow-up spec
  WRITE: "Missing implementation: [requirement] — see implementation-summary.md gap analysis"

FOR each gap marked "⚠️ Acknowledged":
  NOTE: Reason for deferral, who decided, under what constraint
```

### Step 5.5: Detect previous close (reopen scenario)
```
IF specs/[feature]/close.md or specs/[feature]/implementation-summary.md EXISTS:
  LOAD previous health score from existing close document
  NOTE: "Previous spec health was N%. This close will append a new section,
         preserving the original close data."
  SET previous_health = N
  SET reopen_mode = true
ELSE:
  SET previous_health = None
  SET reopen_mode = false
```

### Step 6: Compute Spec Health Score
*Skip in lightweight close mode*
```
COUNT resolved: number of items with verdict ✅ Resolved
COUNT acknowledged: number of items with verdict ⚠️ Acknowledged
COUNT not_done: number of items with verdict ❌ Not Done
COUNT total = resolved + acknowledged + not_done

IF total == 0:
  SET spec_health = 100  (no requirements to compare — trivially aligned)
ELSE:
  spec_health = round((resolved + acknowledged) / total * 100)

INTERPRET:
  100%: Artifacts fully aligned — no action needed
  80-99%: Minor gaps tracked — acceptable
  50-79%: Significant drift — recommend spec-kit-refresh before refactoring
  <50%: Artifacts are misleading — run spec-kit-refresh before proceeding
```

### Step 7: Patch spec artifacts for intentional deviations

For each gap marked `✅ Resolved — intentional deviation`:
```
IDENTIFY the section of spec.md or plan.md that no longer reflects reality
  
CASE: FR requirement wording differs from implementation
  → patch spec.md: update requirement text to match actual behavior, keeping original intent
  → ADD note: "(Updated by implementation summary — see close.md or implementation-summary.md)"

CASE: Architecture/design detail differs from implementation
  → patch plan.md: update the relevant section to reflect what was built
  → ADD note: "(Updated by implementation summary — see close.md or implementation-summary.md)"

CASE: Data model entity or contract differs
  → patch plan.md or data-model.md: reflect current schema/contract
  → ADD note: "(Updated by implementation summary — see close.md or implementation-summary.md)"
```

**User confirmation**: Present each proposed patch as:
```
PROPOSE: "Update spec.md FR-XXX from [old] to [new]? (reason: [rationale])"
WAIT for user approval before applying.
```

If user rejects a proposed patch → mark that artifact as `⚠️ needs review` in the Spec State table (not auto-updated).

### Step 7b: Regenerate the plan's Current Design
```
REWRITE plan.md `## Current Design` (the ONLY section that is replaced, not appended):
  <= 1 page; what is built now — components, data flow, seams, the decisions that hold
  Source: the code (git diff), the rounds in `## Rounds (ADR log)`, the gap analysis
  Earlier rounds stay untouched; a round superseded by a later one is NOT edited —
  the Current Design simply no longer describes it
NOTE in the close document: "plan.md Current Design regenerated"
```

### Step 7c: Architecture decisions → project ADRs
*Both modes.*
```
LOCATE the ADR directory: adr_dir in specs/git-conventions.md, else
  mcp_spec_kit_next_id(feature, kind="ADR").adr_dir, else the first existing of
  docs/adr, docs/decisions, doc/adr, adr
  None exists → ASK the user whether to create one (default docs/adr/ + README.md index);
  declined → every candidate stays feature-local; say so in the close
LOCATE the ADR index (adr_index, else README.md / index.md in the ADR dir) and the
  project's ADR template (a "## Template" section in the index, else the shape of the newest
  ADR, else spec-kit/templates/adr-template.md). Read the index rules (numbering,
  immutability, status vocabulary) and follow them over the defaults below.

HARVEST candidates from:
  - decisions.md rulings (and assumptions the user confirmed)
  - plan.md design decisions and every "## Rounds (ADR log)" round
  - research.md decisions (decision → rationale → alternatives)
  - review findings (pre-implement and final) that changed the design
  - intentional deviations approved in Step 7
  - the diff itself: a new dependency, a new pattern, a new boundary nobody wrote down

THE ADR BAR — a candidate becomes a project ADR when ANY holds:
  1. it constrains code beyond this feature (other features must follow it)
  2. it is expensive to reverse (schema, public contract, data ownership, platform, dependency)
  3. it chooses between real alternatives that a future reader would re-litigate
  4. it changes, narrows or contradicts an existing ADR
  5. the constitution or AGENTS.md would otherwise state something no longer true
  Feature-local choices (a component name, an internal helper, a test layout) stay in plan.md.

CHECK existing ADRs for each passing candidate:
  - same decision already recorded → append to its Evidence / Related (allowed edit), no new ADR
  - contradicts / replaces an Accepted ADR → NEW ADR that "supersedes NNNN"; set the old ADR's
    status line to "Superseded by <new>" (the only edit an Accepted ADR receives)
  - narrows or extends it without contradiction → new ADR that "amends NNNN" (or the
    project's amendment convention, if its index defines one)
  - nothing related → new ADR

FOR each proposed ADR action:
  PRESENT: number (mcp_spec_kit_next_id kind="ADR"), title, the Decision paragraph,
           the action (new / supersedes / amends / evidence appended), the origin
  WAIT for approval. Approved → write it, Status "Accepted" with the date and the quoted
  ruling as Deciders (or "Proposed" if the user wants it reviewed by others);
  rejected → row "feature-local (declined by user)".
  Every number allocated, the file follows the template, Context cites path:line, Evidence
  names where the decision is visible in the code.

UPDATE the ADR index table (number, title, status, date) — and the old ADR's row when superseded.
FILL the close document's "## Architecture Decisions" table, one row per harvested candidate
  (including those that stayed feature-local, with the reason). No candidate passed →
  one row "none met the ADR bar". The section is never omitted — close_feature checks it.
```

### Step 7d: Keep AGENTS.md current
*Both modes.*
```
LOCATE agents_file (git-conventions, default AGENTS.md) and any file that restates or
  imports it (CLAUDE.md, .github/copilot-instructions.md, .claude/rules/*, .cursor/rules/*)
FOR each statement in those files, ask: does this feature's diff, a new/superseded ADR, or a
  resolved known-debt item make it WRONG or INCOMPLETE? Typical:
  - commands (build/test/run/deploy) added, renamed or changed
  - repository layout, projects/modules/services added or moved; service boundaries
  - tech stack versions, new dependencies an agent must know about
  - conventions/rules the feature introduced (a pattern every new endpoint follows)
  - "known debt" items this feature resolved, or new debt it knowingly left
  - the ADR list / "decisions" pointers (new or superseded ADRs)
  - spec-kit block (<!-- SPECKIT START/END -->): active features, artifact paths
DO NOT add feature narrative, changelog lines or anything derivable from the code alone;
  AGENTS.md is context for the next agent, not a history.
PROPOSE each change as a targeted patch (old → new, one section at a time); WAIT per patch;
  apply only approved ones. Never reformat or rewrite the file.
RECORD in the close document: "AGENTS.md: updated — <sections>" or
  "AGENTS.md: no change needed — <one-line reason>".
```

### Step 8: Collect implementation details
```
IDENTIFY:
  - Files changed (from plan file paths, tasks, and git diff)
  - Dependencies added
  - Architecture decisions made during implementation
  - Deviations from plan (with rationale — why they deviated)
  - Test results (pass/fail counts)
  - Known limitations or deferred work
```

### Step 9: Generate output document

**Full mode** (summarize):
```
IF reopen_mode AND specs/[feature]/implementation-summary.md EXISTS:
  APPEND to existing specs/[feature]/implementation-summary.md:
    - New section: "## Reopened Summary ([ISO date])"
    - Updated Spec Health Score
    - "Previous health: N% -> Current health: M%"
    - New gap analysis entries (additive only)
    - NOTE: "Original summary preserved above."
ELSE:
  COPY spec-kit/templates/implementation-summary-template.md -> specs/[feature]/implementation-summary.md

Populate with:
- Spec Health Score at top (from Step 6)
- **Previous vs Current**: IF previous_health exists: "Previous health: N% -> Current health: M%"
- Spec Health Scoring table
- All gap analysis sections
- Spec Artifact Refresh section listing what was patched (from Step 7)
- Spec State table
```

**Lightweight mode** (close):
```
IF reopen_mode:
  APPEND to existing `specs/[feature]/close.md`:
    - A new section header: "## Close (Reopened — [ISO date])"
    - Updated Spec Health Score from Step 6
    - "Previous health: N% → Current health: M%"
    - Updated Artifact State for artifacts changed during reopen
    - Key decisions made during reopen
    - NOTE: "Original close preserved above. This section documents the reopened cycle only."

ELSE (first close):
  COPY `spec-kit/templates/close-template.md` → `specs/[feature]/close.md`

Populate with:
- Spec Health Score (from Step 6, or simplified "100%" if skipped)
- Intent Alignment: Yes/Partially/No
- Artifact State: quick status of each artifact
- Key Decisions: notable decisions made
- Spec Health Calculation breakdown (if available)
```

**Reopen conflict check** (before writing either mode):
```
IF reopen_mode AND any requirement status changed from ✅/⚠️ to a worse status:
  For each changed requirement:
    PROMPT user: "FR-XXX was [original status] in previous close, now [new status].
                  This is a regression. How should I document it?
                  1. Add as new entry (preserves original close — recommended)
                  2. Update the original close entry (overwrite)"
  WAIT for user response before writing.
```

### Step 10: Update or create bugs from gaps
*Skip in lightweight close mode*
```
FOR each "❌ Not Done" gap:
  IF bugs.md EXISTS:
    APPEND a new bug entry:
    ### BUG-NNN: Missing: [requirement description]
    - Severity: [major/minor]
    - Description: Specified in spec.md but not implemented (see implementation-summary.md)
    - Requires Clarification: [ ] no / [ ] yes
    - Status: open
    WRITE updated bugs.md (append to end)
  PROMPT user: "N gaps found with ❌ Not Done — bugs added to bugs.md. Run 'bugfix [feature]' when ready."
```

### Step 11: Report completion
```bash
REPORT:
  - Mode: Full summary / Lightweight close
  - TDD mode: Active / Bypassed by user
  - Output: specs/[feature]/implementation-summary.md or specs/[feature]/close.md
  - Spec Health: N%
  - Task completion: N/Total
  - Bug resolution: verified/total
  - Artifacts patched: spec.md [yes/no], plan.md [yes/no]
  - Gap analysis (full mode): N resolved, N acknowledged, N not done
  - New bugs created (if any gap was ❌ Not Done)
  - ADRs: created / superseded / amended (numbers), or "none met the ADR bar"
  - AGENTS.md: sections updated, or "no change needed"
```


### MCP checks (optional, when MCP server is configured)

Before the final commit (the server derives and validates; it stores nothing):

```text
CALL mcp_spec_kit_update_artifact(feature="[feature]", artifact="close.md", status="present")
CALL mcp_spec_kit_close_feature(feature="[feature]")   # error if: a bug is open/in-progress or verified without Verified-by; the final review is missing, NOT READY or stale; the close doc lacks "## Architecture Decisions". Lists claimed_unverified
CALL mcp_spec_kit_lint_artifacts(feature="[feature]")
```

If MCP is not available, skip.

### Step 12: Append to history.md and Step 13: Commit (combined)

**Order is critical: history.md FIRST, then commit.**

1. **Append to history.md**:
   Append to `specs/[feature]/history.md` (create if missing):
   - Phase: Phase 6 — Complete
   - Artifact: `implementation-summary.md` or `close.md`, plus patched artifacts
   - Spec Health: N%

2. **PRE-COMMIT GUARD**:
   READ `specs/[feature]/history.md` — confirm the close/summary entry is recorded.
   If missing: BLOCK — must append before commit.

3. **Commit**:
   Follow `spec-kit/references/auto-commit.md`:
   - Scope: `implementation-summary.md` or `close.md`, plus patched `spec.md`, `plan.md`, `data-model.md`, the ADR files + ADR index, and the AGENTS.md / agent-rule-file patches
   - Message: `"spec(phase-6): [feature] summary (health: N%)"`

## Gap Analysis Detail

The Gap Analysis section answers the key question: **"Does the code match what was planned?"**

Sources for comparison:
- **spec.md**: Functional Requirements (FR-###), User Stories, Success Criteria
- **plan.md**: Data model entities, API contracts, architecture decisions
- **tasks.md**: Task descriptions and file paths
- **git diff / git log**: Actual files changed on the branch

Verdict definitions:
| Verdict | Meaning | Follow-up |
|---------|---------|-----------|
| ✅ Resolved | Implemented as planned, OR intentionally different with documented rationale | No action needed (spec/plan auto-updated in Step 7) |
| ⚠️ Acknowledged | Deferred by user; not implemented but tracked | Record reason; revisit if needed |
| ❌ Not Done | Missing with no documented reason | Create bug entry in bugs.md |

## State Transition

After this skill completes, the feature enters **Complete** state:
- All tasks marked [X]
- All bugs marked verified
- Unknown gaps resolved or acknowledged via gap analysis
- Spec/plan artifacts patched to reflect intentional deviations
- Summary (full or close) captures final state
- Bugs created for ❌ Not Done gaps (if any)
- No further phases required unless user initiates a new cycle

## Phase State Detection

| Artifacts Present | Interpretation |
|:-----------------|:-------------|
| `implementation-summary.md` exists | Feature complete — full summary generated |
| `close.md` exists | Feature closed — lightweight close document |
| `implementation-summary.md` or `close.md` + all bugs verified | Feature complete and verified |
| `spec.md` or `plan.md` patched (diff from prior commit) | Artifacts reconciled with code |
| `implementation-summary.md` with open gaps (❌) | Summary generated but gaps remain — new bugs created |
| `implementation-summary.md` with open tasks | Partial summary (run again after completion) |

## Routing Commands

- "Summarize [feature]" — loads this skill, generates full implementation summary
- "Close [feature]" — loads this skill, generates lightweight close document
- "Implementation summary for [feature]" — same as summarize
- "Status of [feature]" — checks if summary exists, reports state

## Mandatory Close (User-Initiated)

After the bugfix loop completes (all bugs in bugs.md marked Status: verified), the workflow suggests Phase 6 (Summarize/Close) — the user decides when to run it:

```text
CHECK: All bugs in bugs.md have Status: verified

ACTION:
  1. Suggest the user run Phase 6: "'close [feature]' or 'summarize [feature]'?"
  2. WAIT for user choice: full summary ('summarize') or lightweight close ('close')
  3. Run the chosen mode
  4. Present output to user

BLOCKER: A feature CANNOT enter Complete state without Phase 6 completing.
  - User says "feature is done" or tries to start a new feature
  - CHECK: implementation-summary.md or close.md exists?
  - IF NOT: Block with "Complete Phase 6 first: run 'summarize [feature]' or 'close [feature]'"
```

**Note**: The mandatory close is enforced by the workflow orchestrator (`spec-kit-workflow`). When `spec-kit-test` marks the last bug as verified, it should suggest "All bugs verified — run 'close [feature]' to complete."

## Done When

- [ ] Output generated: implementation-summary.md (full) or close.md (lightweight)
- [ ] Spec health score computed and included
- [ ] All tasks marked complete in tasks.md
- [ ] No bug open or in-progress; claimed-unverified bugs listed in the close document
- [ ] Evidence table filled; unverified gates written as ❌ unverified
- [ ] No bug status changed by this skill
- [ ] ✅ Resolved deviations patched into spec.md and plan.md (with user approval)
- [ ] ❌ Not Done gaps converted to new bug entries in bugs.md (if any, full mode only)
- [ ] Final review gate passed (latest round READY / READY-WITH-FOLLOWUPS, not stale)
- [ ] "## Architecture Decisions" table filled; approved ADRs written, superseded ADRs re-statused, ADR index updated
- [ ] AGENTS.md (and files restating it) patched where the change made them wrong — or "no change needed" recorded
- [ ] Report delivered to user with spec health score, artifact state, ADRs and AGENTS.md changes

## Next Skills

- Feature is now **Complete** — no further phases needed
- Propose to the user: Run `spec-kit-workflow` to start a new feature cycle
- Propose to the user: Run `spec-kit-specify` to add new features
- Propose to the user: Run `spec-kit-refresh` if artifacts show drift (for manual code changes)
- Propose to the user: Run `bugfix [feature]` if new gaps were added as bugs
