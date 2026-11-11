# spec-kit-review — full procedure

> **Loaded on demand** — the one-screen SKILL.md is the entry point; this file holds only what it leaves out. Read the section you need.

## Mode detection
```
close doc exists                                  → closed-review (report only, no round)
tasks.md exists AND no implementation code        → pre-implement
every task [X] AND code AND no close doc          → bugs.md open/in-progress? REFUSE ("bugfix first") : final
both match → ASK which; undetermined → ASK
```
SIZE from spec.md. REVIEWED_COMMIT = `git rev-parse --short HEAD` before anything else.
BASE = merge-checklist `base_branch`, else `branch_source` in git-conventions, else main.

## Reviewer
`Implemented-by` = every implementing agent (`spec-kit/references/evidence.md`); you among them →
self-review. Another agent not among them available → it reviews → `review:<agent>`. Else (Claude Code: the Agent tool) a
**fresh-context sub-agent** given ONLY this procedure, the feature path, BASE and the project
rule files — never the implementation transcript → `self-review by <agent> (fresh context: yes)`.
Else `self-review by <agent>`. A self-review opens the merge gate; it never verifies a bug.
**Order of reading for the final review**: diff and spec first, acceptance.md, then plan, then
`decisions.md` last — so the author's rationale does not anchor the verdict.

## Pre-implement (3.5)
Scope: this feature only. Out of scope (note under "Project-level notes", no severity): missing
constitution or CI, pre-existing debt elsewhere, broad stack opinions, taste.

| Pass | M (lite) | L |
|------|----------|---|
| Coverage: every FR / story / SC / AC → a task; tasks → a requirement | ✓ | ✓ |
| Underspecification: verbs without measurable objects; vague adjectives; placeholders | ✓ | ✓ |
| Codebase fit: existing patterns, abstractions reused, integration points, paths match layout | ✓ | ✓ |
| Design soundness: abstraction level, data flow traceable, error-handling strategy, next 2–3 features | ✓ | ✓ |
| Security & Privacy: each spec row has a design answer in the plan | ✓ | ✓ |
| Duplication, ambiguity, naming drift, completeness, inconsistency | | ✓ |
| Best practice: research current guidance for each major technology / pattern | | ✓ |
| Bugfix coverage (bugfix mode): every open bug → BF task + verifying test | ✓ | ✓ |

**Devil's advocate** (P1: optional · P2: required, a separate pass by the same reviewer · P3:
required, a different agent — the other agent, else a separate sub-agent, another model when
available — briefed with the plan and the code, not the review so far):
1. the strongest case against the plan, and the simplest alternative delivering ~80 % of the value;
2. pre-mortem — "it is three months later and this failed in production; why?";
3. abuse cases per new seam: another tenant's id, unauthorized role, oversized / malformed input,
   data exposure in a response or a log, replay / concurrency;
4. the riskiest assumptions in decisions.md — which would hurt most if wrong.
Every objection with a concrete scenario, never capped; the author answers every one (accepted →
task / spec change; rebutted with evidence; deferred → follow-up). Unanswered → the report says so.

Severity: CRITICAL (zero coverage, architecture violation, security, data integrity) · HIGH
(maintainability pain, pattern misalignment, missing error chain) · MEDIUM (drift, non-functional
gap) · LOW → do not report. Report: findings table, coverage table, codebase-fit assessment,
devil's-advocate table, metrics. CRITICAL → resolve before implement.

## Final (5.5)
```
LOAD spec (FR/SC/ACs/edge cases), plan (Current Design, seams), tasks, data-model, contracts,
     acceptance.md (latest round), bugs.md, evidence/, constitution (MUSTs for the touched
     layers), specs/merge-checklist.md (missing → from the template, ASK to confirm), AGENTS.md
     + agent rule files, linter configs; decisions.md LAST
RUN  git diff --stat BASE...HEAD; git diff BASE...HEAD -- . ':(exclude)specs'
MECHANICAL  mcp_spec_kit_diff_scan(feature, base=BASE) → evidence/final-diff-scan.txt
            (no MCP: git merge-tree, grep the added lines for secrets / conflict markers /
            focused tests / TODO, list forbidden and > 1 MB files, unplanned files)
            every merge-checklist command → evidence/final-<name>.txt; a command that cannot
            run = ❌ unverified with the reason, never assumed green; ci:<id> for REVIEWED_COMMIT; code unchanged since a green ci:<id> → cite it
CI RUN      review_run (merge-checklist; default local) — branch pushed (not → ASK); ci → ci_queue
            each pipeline of ci_jobs, ci_status until done · pr → read pr_checks, nothing queued,
            nothing re-run. Source commit ≠ REVIEWED_COMMIT → not evidence. Per check (ci_jobs
            maps it): succeeded → final-<check>.txt = the status lines, evidence ci:<run>/<job>
            · skipped / not run → local · failed → ❌. Local always: diff_scan, probes, rulings.
            No CLI / auth / timeout → all local, said in the round. A required approval may be
            the PR's: `**Approved-by**: <name> — pr:<id>` (the approval read, never assumed).
§1  spec has ACs → latest acceptance round PASS and not stale (else NOT READY: "run accept");
    frozen tests unchanged. Deferred e2e → run now if the stack is up (evidence/final-AC-###.txt)
    else 👤; manual ACs → the user's quoted words or 👤.
    For each FR / SC / edge case: find the code (path:line) and the proving test — write ONLY
    the rows that are not ✅ (⚠️ partial / unproven · ❌ missing = CRITICAL · ↔ deviates · 👤).
    Contracts and data-model vs code; unplanned files / behaviour → scope creep (HIGH if it
    changes behaviour).
§2  every applicable constitution MUST, merge-checklist P-item, AGENTS.md / rule-file rule and
    each non-empty spec Security & Privacy row → ✅ / ❌ with path:line; n/a rows one line.
    Violated MUST = HIGH; CRITICAL when security, data or a declared non-negotiable.
§3  on the changed code: architecture conformance, error chains (nothing swallowed, no internals
    leaked), security (secrets, injection, authz, tenant / ownership, unvalidated input),
    data integrity (transactions, races, migrations), concurrency, structural duplication,
    complexity (> ~100-line functions, deep nesting), API surface. Stack practice: M/L.
    Tests: assert §1 behaviour; edge cases; every [SEAM] fixture matches its probe (missing = HIGH);
    RED + GREEN file per implement phase; acceptance round present with every AC's outcome
    (manual ACs → the user's quoted confirmation, else 👤).
§4  devil's advocate (final): concrete break attempts — another tenant's id, empty / stale /
    boundary period, concurrent edit, failing dependency, unauthorized role, oversized input;
    "would this test still pass if the code were wrong?"; argue the opposite verdict.
    P1: required, inline · P2: optional · P3: required, a different agent that reads the code and
    the spec, not this round. Objections never capped, each answered (accepted → bug / rebutted
    with evidence / deferred); unanswered blocks READY at P3. Round N+1 (P2+) = the delta since N.
§5  checklist: every G-item and P-item with ✅ / ❌ and its evidence file.
VERDICT  CRITICAL / HIGH or blocking ❌           → NOT READY
         no defect, owner confirmations pending   → AWAITING-OWNER   (👤 rows, ↔ rulings)
         only MEDIUM / non-blocking ❌             → READY-WITH-FOLLOWUPS
         else                                     → READY
§6  bugs for CRITICAL / HIGH / blocking failures (spec-kit-test format, mcp_spec_kit_next_id,
    confirm each with the user); MEDIUM → follow-ups; ↔ deviations → WAIT: patch spec/plan
    (intentional) / log a bug / defer to close; PR description: what / why / how verified /
    risks / rollback / strongest objections and how they were answered
```
An unverified blocking item is ❌ unless the user accepts the risk in writing (quote in
decisions.md and the round). A code commit after Reviewed-commit makes the round stale; a
specs-only commit (the owner's answers, Round N+1) does not.

**Nitpick filter**: formatting, import order, naming that is clear, 2–3-line repetition,
micro-optimisations without a measured problem, edge cases the spec does not require → delete.
"Is this in the top things that must change before merge?" — if not, it is not a finding.

## Closed-review
Same checks as final, written as a report; no round, no commit. CRITICAL / HIGH → offer:
refactoring tasks in tasks.md + `reopen`, or note for future work — with the user's approval.

## Commit
History entry first (preflight commit procedure; closed-review: none). Pre: `spec(review): [feature]
review findings`. Final: `mcp_spec_kit_lint_artifacts` (rounds need Verdict + Reviewed-commit) →
`spec(review): [feature] final review (verdict: X)` — specs only, so the round stays fresh. Read-only on source code; writes only the report / round, evidence,
bugs.md entries, approved spec/plan patches, merge-checklist.md on first use.
