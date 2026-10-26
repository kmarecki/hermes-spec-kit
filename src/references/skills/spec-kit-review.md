# spec-kit-review — full procedure

> **Loaded on demand.** The one-screen `spec-kit-review` SKILL.md is the entry point; this file holds the complete
> procedure (every branch, template field and pitfall). Read the section you need, not the whole file.
> Tool names: Hermes (`terminal`, `write_file`, `patch`, `read_file`, `skill_view`) — Claude Code maps them to
> `Bash`, `Write`/`Edit`, `Read`, `Skill`; MCP tools are `mcp_spec_kit_*` / `mcp__spec-kit__*`.

**Phase**: 3.5 (Pre-implement gate — optional for S/M, required for L) / 5.5 (Final merge-readiness review — **mandatory before close**)

**Purpose**: Provides quality checks at two points in the workflow, plus a
third mode for reviewing already-closed features without altering history:

1. **Pre-implement** (after tasks.md, before code): Verify spec/plan/tasks are coherent **and** analyze the existing codebase structure to evaluate whether the planned approach fits the project architecture and follows current best practices. READ-ONLY — outputs a report, no file changes.

2. **Final** (phase 5.5 — every task done, no open bug, before close): the merge gate. Does the code do what the spec says (requirement by requirement)? Does it obey the constitution and the project's rules? Is it good code by current practice? Is the branch mergeable (builds, full suite green, clean diff, conflict-free)? Writes a round to `specs/[feature]/review-final.md` whose **Verdict** and **Reviewed-commit** gate `close_feature`. Skips cosmetic nitpicks — but a broken explicit project rule is never a nitpick.

3. **Closed-review** (feature is already closed): Same checks as final but does NOT update history.md. If issues are found, offers to add refactoring tasks to tasks.md and reopen the feature.

**Prerequisites**:
- Pre-implement mode: `spec.md` + `plan.md` + `tasks.md` must exist
- Final mode: `spec.md` + implemented code, every task `[X]`, no bug `open`/`in-progress`

**Artifacts**: pre-implement — a report (the project may keep it as `review.md`); final — `specs/[feature]/review-final.md` (rounds appended), `evidence/final-*.txt`, bug entries in `bugs.md` for blocking findings

**Routing**: Load this skill when the user says "review [feature]", "analyze [feature]", or "quality check [feature]".

**Task Persona**: Adopt the mindset of a senior architect doing a critical design review. You are not a style checker — you look for **structural problems, design flaws, security risks, and architectural misalignments** that would cause real pain if left unfixed. Every finding must be actionable and backed by evidence. Use web search to research current best practices for the project's tech stack when evaluating architecture or implementation quality. Ask yourself: *"Will this cause a problem in production? Will this be hard to maintain? Is there a simpler, more robust approach?"* If the answer to all three is no, the finding is probably a nitpick — skip it. Does this hold up under scrutiny?

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Determine mode
```
DETECT current artifacts:
  IF close.md or implementation-summary.md EXISTS:
    MODE = closed-review (post-close code quality check)
    NOTE: "Feature [feature] is closed. Review will NOT update history.md."

  IF tasks.md exists AND no implementation code exists:
    MODE = pre-implement (cross-artifact consistency + codebase architecture analysis)

  IF every task is [X] AND implementation code exists AND no close doc:
    IF bugs.md has an open / in-progress bug:
      REFUSE: "BUG-NNN is open — finish the bugfix loop, then run the final review."
    MODE = final (merge-readiness review, phase 5.5)

  IF both pre-implement and final conditions match:
    ASK user: "Run the pre-implement review (spec/plan/tasks) or the final review (code + merge readiness)?"

  IF mode is still undetermined:
    ASK user: "Cannot auto-detect mode. Which review? (pre-implement / final / closed-review)"
```

---

## Pre-Implement Mode: Cross-Artifact Consistency

### Review scope (feature-level only)
This review is scoped to the feature being examined. The following are
**IN SCOPE**:
- Spec/plan/tasks coherence and completeness
- Codebase architecture fit (does the plan fit the existing code?)
- Best-practice validation for the planned approach
- Design soundness (abstraction level, data flow, error handling)

The following are **OUT OF SCOPE** — do NOT flag or block on these:
- Missing project constitution — this is a project-level concern tracked
  separately. If the constitution exists, the review will note alignment.
  If it doesn't exist, that's not a feature issue.
- Missing project-level tooling (CI config, deployment pipeline, linting)
- Broad tech stack evaluations not specific to this feature
- Pre-existing code quality issues in unrelated parts of the codebase
- Personal stylistic preferences (see Nitpick Filter below)

If you discover a project-level issue during review, add it to a
"Project-Level Notes" section at the bottom of the report — do NOT
assign severity or block the feature.

### Step 1: Validate prerequisites
```
IF specs/[feature]/spec.md NOT EXISTS:
  ERROR: "Run spec-kit-specify first"
IF specs/[feature]/plan.md NOT EXISTS:
  WARN: "No plan.md — analysis limited to spec only"
IF specs/[feature]/tasks.md NOT EXISTS:
  WARN: "No tasks.md — cannot verify task coverage"
```

### Step 2: Load artifacts
From **spec.md**:
- Functional Requirements (FR-###)
- Success Criteria (SC-###)
- User Stories
- Edge Cases

From **plan.md** (IF EXISTS):
- Architecture/Stack choices
- Data Model references
- Constitutional Gates
- Technical constraints

From **tasks.md** (IF EXISTS):
- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- File path references

From **constitution.md** (IF EXISTS):
- Principle names
- MUST/SHOULD statements

From **bugs.md** (bugfix mode only, IF EXISTS):
- Bug IDs (BUG-###)
- Bugfix tasks (BF-###)
- Severity levels
- Requires Clarification flags

### Step 3: Build semantic models
Create internal representations:
- **Requirements inventory**: FR-### with imperative-phrase slug
- **User story inventory**: Discrete actions with acceptance criteria
- **Task coverage mapping**: Task → Requirement mapping
- **Constitution rule set**: Principles and normative statements

### Step 4: Detection passes

**A. Duplication Detection**
- Identify near-duplicate requirements
- Mark lower-quality phrasing for consolidation

**B. Ambiguity Detection**
- Flag vague adjectives (fast, scalable, secure, intuitive, robust)
- Flag unresolved placeholders (TODO, TKTK, ???, <placeholder>)

**C. Underspecification**
- Requirements with verbs but missing object or measurable outcome
- User stories missing acceptance criteria alignment
- Tasks referencing undefined files/components

**D. Constitution Alignment** (project-level — informational only)
WHEN specs/constitution.md EXISTS at project root:
  - Check feature artifacts for alignment with each applicable principle
  - Note any conflicts or gaps as informational findings
  - Do NOT assign CRITICAL severity — this is guidance, not a gate
WHEN specs/constitution.md does NOT exist:
  - SKIP this pass entirely
  - Add to Project-Level Notes: "Constitution not found — alignment
    check skipped. This is a project-level gap, not a feature issue."
  - Do NOT produce findings for missing constitution

**E. Naming Conventions** (pre-implement)
- Consistent naming patterns across spec, plan, and tasks
- File paths in tasks follow project conventions
- Terminology consistent between spec and plan

**F. Documentation Completeness** (pre-implement)
- Are all required spec sections present (FRs, edge cases, success criteria)?
- Does plan.md document architecture decisions?
- Are there TODOs or placeholders that should be resolved before coding?

**G. User-Defined Custom Gates** (pre-implement)
**H. Coverage Gaps** (only if tasks.md exists)
- Requirements with zero associated tasks
- Tasks with no mapped requirement/story
- Success Criteria requiring buildable work not in tasks

**I. Inconsistency**
- Terminology drift (same concept named differently)
- Data entities in plan but absent in spec
- Task ordering contradictions

**J. Bugfix Coverage (bugfix mode only)**
- Bugs with no corresponding bugfix task (BF-###)
- Bugfix tasks not referencing a plan bugfix section
- Bugfix tasks without verification/regression test tasks
- Unclear mapping between bug and fix approach

**K. Codebase Architecture Analysis** (pre-implement)
- Scan the project's existing directory tree and module structure to understand current architecture patterns (layers, module boundaries, framework conventions, dependency injection style, testing patterns)
- Evaluate whether the planned architecture/design in plan.md fits the existing codebase — does it follow the same patterns or introduce new ones? If new patterns are proposed, is the justification compelling?
- Identify integration risk points — where the new feature connects to existing code. Are the interfaces clean? Are existing modules being modified in a way that could cause regressions?
- Check if the plan reuses existing abstractions or reinvents them. Is there already a utility, mixin, or service that does what the plan proposes?
- For each file path referenced in tasks.md: does the path follow the existing project layout conventions? Or does it introduce a new directory structure that doesn't match?

**L. Best Practice Validation** (pre-implement)
- For each major technology or pattern in the plan, briefly research (web search) current recommended practices. Example questions:
  - "Does framework X recommend this approach for Y in 2026?"
  - "Is this pattern considered best practice or is there a newer recommended alternative?"
  - "Are there known pitfalls or gotchas with this approach that the plan doesn't address?"
- Flag approaches that are:
  - Known anti-patterns (e.g., God objects, sequential async waterfalls, callback hell in modern frameworks)
  - Deprecated or superseded patterns (e.g., class components in a React project using function components)
  - Over-engineering for the problem size (e.g., adding a message queue for a single background job)
  - Under-engineering for the problem size (e.g., no error handling, no validation, no logging)
- Do NOT flag personal stylistic preferences or "one true way" debates (tabs vs spaces, semicolons vs no-semicolons). Only flag patterns with broad community consensus against them.

**M. Design Soundness** (pre-implement)
- Does the plan reflect a solid understanding of the existing codebase, or does it feel like a generic solution?
- Are the proposed abstractions at the right level? Too abstract (over-general, YAGNI violation)? Too concrete (brittle, hard to extend)?
- Will the design scale with the next 2-3 likely features? Or is it a dead end that will need refactoring?
- Are there simpler approaches that would work with less complexity? Evaluate Occam's razor.
- Error handling strategy: does the plan have one? Or does it assume everything succeeds?
- Is the data flow coherent and traceable? Can you follow a request/event from entry to response without gaps?

### Step 5: Severity assignment
Use heuristic — **filter out nitpicks** at every level:

- **CRITICAL**: Requirement with zero task coverage blocking baseline, architectural integrity violation, security vulnerability, data integrity issue
- **HIGH**: Design flaw that will cause maintainability pain, pattern misalignment with existing codebase, missing error handling chains, duplicated logic across module boundaries
- **MEDIUM**: Terminology drift, missing non-functional task coverage, minor design concern that could degrade with future features
- **LOW**: SKIP — do not report. These are stylistic preferences, subjective opinions, or issues with no real-world impact. If you find yourself writing a LOW finding, ask: "Would the project be measurably worse if this were left as-is?" If no, delete the finding.

**NITPICK FILTER — Apply before reporting:**
- If a finding is about formatting, line length, naming preference (not correctness), comment style, or personal taste → DELETE it, do not report.
- If a finding is about a pattern that works but isn't your preferred approach → DELETE it.
- If a finding requires deep domain knowledge you don't have → flag as QUESTION, not finding.
- **Minimum bar**: every reported finding must have a demonstrable negative impact on correctness, security, performance, maintainability, or testability. If you cannot articulate which of these five is harmed, the finding is a nitpick — skip it.

### Step 6: Produce pre-implement report
OUTPUT:

```
# Pre-Implement Review: [Feature]

## Findings Table

| ID | Category | Severity | Location | Summary | Recommendation |
||----|----------|----------|----------|---------|----------------|
|| A1 | Duplication | HIGH | spec.md:L120-134 | Two similar requirements... | Merge phrasing |
|...

## Codebase Architecture Assessment

| Aspect | Assessment | Risk Level |
|--------|-----------|------------|
| Pattern fit | Plan aligns with existing MVC layout | ✅ Low |
| Integration points | New service connects via existing repository pattern | ✅ Low |
| Directory conventions | tasks.md references src/feature/ — matches project layout | ✅ Low |
| Pattern reuse | Plan creates new auth middleware — existing middleware in src/middleware/ not reused | ⚠️ Medium |

## Best Practice Validation

| Technology/Pattern | Research Finding | Status |
|--------------------|-----------------|--------|
| Next.js App Router auth | Next.js docs recommend middleware.ts for auth checks — plan uses getServerSession in each page | ⚠️ Consider middleware approach |
| JWT refresh pattern | Industry consensus: refresh token rotation + blacklist — plan uses long-lived tokens | ❌ High — security risk |

## Design Soundness Notes

[Key observations about abstraction level, scalability, simplicity, data flow]

## Coverage Summary Table

| Requirement | Has Task? | Task IDs | Notes |
|-------------|-----------|----------|-------|
| FR-001 | Yes | T001, T002 | |
| FR-002 | No | --- | Missing coverage |

## Constitution Alignment Issues
[If any]

## Unmapped Tasks
[If any]

## Uncovered Bugs (bugfix mode)
[If any]

## Metrics
- Total Requirements: N
- Total Tasks: N
- Coverage %: X%
- Ambiguity Count: N
- Duplication Count: N
- Critical Issues: N
- Codebase Fit: ✅ / ⚠️ / ❌
- Best Practice Alerts: N
- Design Soundness: ✅ / ⚠️ / ❌
```

### Step 7: Next actions (pre-implement)
```
IF CRITICAL issues exist:
  - Recommend resolving before spec-kit-implement
  - Suggest explicit remediation commands
  - In bugfix mode: Recommend fixing bug coverage gaps before implementing fixes

IF only LOW/MEDIUM:
  - User may proceed
  - Provide improvement suggestions
```

---

## Final Mode: Merge-Readiness Review (phase 5.5)

The final review answers four questions, in this order, and writes the answers as one
round of `specs/[feature]/review-final.md` (`spec-kit/templates/review-final-template.md`):

1. Does the code do what the spec says?
2. Does it obey the constitution and the project's rules?
3. Is it good code by current practice for this stack?
4. Can it be merged now?

It is **mandatory**: `close_feature` and `advance_phase(5→6)` refuse a feature whose latest
round is missing, says `NOT READY`, or names a commit older than the last code change.

### Step 1: Reviewer and scope
```
READ Implemented-by from the implement entries of history.md
IF another agent is available (Hermes ↔ Claude Code): it runs this review → label review:<agent>
ELIF the harness can start a fresh-context sub-agent (Claude Code: the Agent tool):
  delegate the review to it with ONLY this procedure, the feature path and the base branch —
  never the implementation transcript → label "self-review by <agent> (fresh context)"
ELSE: label "self-review by <agent>"
The label goes in the round header and in the close's Evidence table. A self-review still
opens the merge gate, but it never counts as review:<agent> verification of a bug.

BASE = merge_checklist base_branch, else branch_source in specs/git-conventions.md, else main
SIZE = spec.md **Size** (absent → M)
REVIEWED_COMMIT = git rev-parse --short HEAD   # recorded before anything else
```

### Step 2: Load
```
LOAD spec.md (FR-###, SC-###, user stories + acceptance scenarios, edge cases),
     plan.md (Current Design / architecture / seams), tasks.md, data-model.md, contracts/,
     decisions.md (every assumption is a review item), bugs.md, evidence/ listing
LOAD specs/constitution.md — every MUST / SHOULD / numbered principle, and the
     per-component sections for the layers this diff touches
LOAD project rules: specs/merge-checklist.md (missing → create it from
     spec-kit/templates/merge-checklist-template.md, fill the commands from AGENTS.md /
     README / package scripts, ASK the user to confirm before using it), AGENTS.md and any
     agent rule files the project keeps (e.g. CLAUDE.md, .claude/rules/, .cursor/rules/),
     linters' configs
RUN git diff --stat BASE...HEAD and git diff BASE...HEAD -- . ':(exclude)specs'
```

### Step 3: Mechanical checks (evidence first, judgement after)
```
CALL mcp_spec_kit_diff_scan(feature, base=BASE)   # without MCP: run the same checks by hand —
   # git merge-tree --write-tree BASE HEAD, grep the added lines for secrets / conflict
   # markers / focused tests / TODO, list forbidden and > 1 MB files, list unplanned files
SAVE the result → evidence/final-diff-scan.txt (command + UTC time on top)
FOR each command in merge-checklist ## Commands (build, test = the FULL suite, lint,
    format_check, extra):
  RUN it; SAVE → evidence/final-<name>.txt; note pass/fail and NEW warnings in changed files
IF a CI pipeline exists: queue/locate the run for REVIEWED_COMMIT → record ci:<id> + result
```
A command that cannot run (missing tool, needs a service) is written as ❌ unverified with the
reason — never skipped, never assumed green.

### Step 4: §1 Spec conformance — requirement by requirement
```
IF spec.md defines **AC-###** criteria:
  READ the latest acceptance.md round: Result must be PASS and its Commit must cover the
    reviewed code (mcp_spec_kit_get_feature_state → acceptance.round.stale false) — else
    NOT READY with "run 'accept [feature]'"
  FOR each deferred e2e AC: run its spec now if the stack is up (save
    evidence/final-AC-###.txt), else ASK the user to run/confirm it — unverified blocks READY
  FOR each manual AC: ASK the user; quote the answer in the round — unconfirmed blocks READY
  Frozen tests: get_feature_state / lint must show no frozen_changed

FOR each FR-###, SC-###, acceptance scenario and edge case in spec.md:
  FIND the code that implements it (path:line) and the test that proves it
  VERDICT: ✅ implemented + proven
           ⚠️ partial / implemented but unproven (no test, or only a self-authored fixture
              where a probe: was required)
           ❌ missing                                   → CRITICAL
           ↔ implemented differently from the spec       → deviation (Step 8)
FOR each contract in contracts/ and entity in data-model.md: compare with the code
  (routes, status codes, payload fields, nullability, validation, persistence shape)
FOR each changed file the diff_scan lists as unplanned, and any behaviour no
  requirement asks for: in scope? (named by plan/tasks under another name) or scope creep
  (→ HIGH if it changes behaviour, MEDIUM otherwise)
```

### Step 5: §2 Constitution and project rules
```
MAP the changed files to the constitution's components / layers
FOR each MUST / principle / rule that applies to those layers, and each merge-checklist
    P-item, and each rule in AGENTS.md / agent rule files that the diff could touch:
  VERDICT ✅ respected / ❌ violated, with path:line evidence
  Rules that do not apply → one line "n/a — <why>" (so the reader sees they were considered)
A violated MUST or P-item = HIGH (CRITICAL when it is security, data integrity or a
non-negotiable the project marks as such). Rules are binding here — this is the place the
constitution is enforced; elsewhere it is guidance.
```

### Step 6: §3 Code quality & best practice, §4 Tests
Check, on the changed code only:

- Architecture conformance — the structure plan.md Current Design describes; layers not bypassed; dependency direction; no cycles
- Error handling chains — failures caught at the right boundary; nothing swallowed; user-facing errors leak no internals
- Security — secrets, injection, missing authentication/authorization, unvalidated input reaching sensitive operations, tenant/ownership checks
- Data integrity — transactions where needed, races, validation before persistence, migrations
- Concurrency — shared mutable state, async misuse, cancellation for long operations
- Structural duplication — repeated business logic, parallel hierarchies, re-implemented utilities the codebase already has
- Complexity hotspots — functions > ~100 lines, deep nesting, indirection that buys nothing
- Public API surface — naming consistent with the spec, validation, sensible defaults, backwards compatibility
- **Best practice** — for each framework/library the diff leans on, check current guidance (official docs, web search); flag deprecated APIs, known anti-patterns, over- and under-engineering. Skip the research for size S; still apply what you know.

§4 Tests: do they assert the behaviour §1 names (not implementation details)? Edge cases from the spec? For every external seam, does a `probe:` file exist and does the fixture match its shape (missing = HIGH)? RED/GREEN evidence present for each implement phase? Regression run present?

**NITPICK FILTER** — do NOT report: formatting, line length, import order, naming that is
unconventional but clear, 2–3 line repetition, personal style, micro-optimisations without a
measured problem, edge cases the spec does not require. Ask: "Is this in the top things that
must change before merge?" If not, delete it.

### Step 7: Severity, checklist, verdict
- **CRITICAL**: requirement missing, security vulnerability, data loss/corruption, architecture violation, a non-negotiable rule broken
- **HIGH**: violated constitution MUST / P-item, structural defect, error-handling gap, missing validation chain, concurrency bug, unprobed seam fixture, behaviour-changing scope creep
- **MEDIUM**: design concern that degrades with the next features, test gap on a non-critical path, doc gap
- **LOW**: do not report

Fill the §5 checklist table: every generic G-item and project P-item, each with ✅/❌ and its
evidence file. Then:

```
IF any CRITICAL or HIGH, or any blocking checklist item ❌:  VERDICT = NOT READY
ELIF any MEDIUM or non-blocking item ❌:                      VERDICT = READY-WITH-FOLLOWUPS
ELSE:                                                         VERDICT = READY
WRITE the round header: **Verdict**: <VERDICT> and **Reviewed-commit**: <REVIEWED_COMMIT>
```
An unverified blocking item (command could not run) is ❌ unless the user explicitly accepts
the risk — quote them in decisions.md and in the round.

### Step 8: Deviations, bugs, follow-ups
```
FOR each ↔ deviation from Step 4:
  PRESENT: "FR-NNN says: … / the code does: … — 1. update spec/plan (intentional),
            2. change the code (log a bug), 3. defer to the close"
  WAIT for the user. 1 → patch spec.md/plan.md now, note "(Updated by final review)";
  2 → bug; 3 → listed for the close.
FOR each CRITICAL / HIGH finding and each blocking checklist failure:
  LOG a bug in bugs.md using the spec-kit-test entry format (Severity, Area, Description
  observed vs expected, Steps, Status: open; id via mcp_spec_kit_next_id(kind="BUG")),
  reference the round and finding id; confirm each with the user
MEDIUM findings → §6 follow-ups (the close lists them; the user may log them as bugs)
DRAFT the PR description in §6: what / why / how verified (evidence + ci) / risks / rollback
```

### Step 9: Report
Report the verdict first, then: reviewer label, counts by severity, checklist failures,
requirement coverage (✅/total), rules verdicted, bugs logged. NOT READY → "run
`bugfix [feature]`, then the final review again (a new round)". READY / READY-WITH-FOLLOWUPS
→ "run `close [feature]` or `summarize [feature]`".

### Re-running
Every run appends `## Round N+1`; earlier rounds stay. A round may say "Rounds 1 findings
Q1–Q4 re-checked: fixed (evidence …)". Any code commit after the round's Reviewed-commit makes
the round stale — the close will refuse it.

---

## Closed-Review Mode

Same steps as the final mode, written as a report (not a round of review-final.md, no
history entry). CRITICAL / HIGH → offer: add refactoring tasks to tasks.md, add them and
reopen, or note for future work — only with the user's approval.

### Append to history.md and Commit

```text
IF mode == closed-review:
  NOTE: "Review on closed feature — history.md not updated."
ELIF mode == pre-implement:
  Follow the **Shared Commit Procedure** in `spec-kit/references/preflight.md`:
  - Phase: Phase 3.5 — Review
  - Artifact: review report
  - Message: `"spec(review): [feature] review findings"`
ELSE (final):
  CALL mcp_spec_kit_lint_artifacts(feature) — review-final.md rounds must carry Verdict + Reviewed-commit
  Follow the **Shared Commit Procedure** in `spec-kit/references/preflight.md`:
  - Phase: Phase 5.5 — Final review
  - Artifact: review-final.md, evidence/final-*.txt, bugs.md (if bugs were logged), patched spec/plan (approved deviations)
  - Message: `"spec(review): [feature] final review (verdict: <VERDICT>)"`
  This commit touches specs/ only, so it does not make the round stale.
```

## Completion

Report:
- Mode used: Pre-implement / Final / Closed-review
- Findings count by severity
- Coverage percentage (pre-implement) · requirement conformance ✅/total (final)
- Final: **Verdict**, Reviewed-commit, checklist failures, bugs logged
- Overall recommendation: Proceed / Fix first

## Next Skills

- Pre-implement mode: Propose `spec-kit-implement` when all CRITICAL issues resolved
- Final mode, READY / READY-WITH-FOLLOWUPS: Propose `spec-kit-summarize` (close)
- Final mode, NOT READY: Propose `bugfix [feature]`, then the final review again
- Closed-review mode: Propose `reopen [feature]` if issues need fixing
- In bugfix mode: Propose `spec-kit-tasks` to add missing bugfix tasks

**Re-running this skill**: pre-implement — compare with the previous report, report only
changes. Final — always a new round (see "Re-running" in the final mode).

## Prerequisite Enforcement

Pre-implement:
- **BLOCKED** if: `spec-kit-specify` has not been run (spec.md required)
- **WARN** if: plan.md or tasks.md missing — analysis limited to what exists

Final:
- **BLOCKED** if: spec.md missing, no implementation code, a task not `[X]`, or a bug open/in-progress
- **NOTE**: constitution.md missing → §2 checks project rule files and the merge checklist only; say so in the round

Closed-review:
- **BLOCKED** if: `spec-kit-specify` has not been run (spec.md required)
- **BLOCKED** if: No implementation code detected
- **NOTE**: tasks.md will be modified only with user approval

## Key Constraint

**READ-ONLY on source code** — This skill never modifies source code. It runs the project's
build/test/lint commands (read-only on the tree) and writes only: the report /
`review-final.md`, `evidence/final-*.txt`, bug entries in `bugs.md`, approved spec/plan
deviation patches, and `specs/merge-checklist.md` on first use (with the user's confirmation).
**Exception**: In closed-review mode, may append refactoring/remediation tasks to `tasks.md` with user approval.
