# spec-kit-specify — full procedure

> **Loaded on demand** — the one-screen SKILL.md is the entry point; this file holds only what it leaves out. Read the section you need.

## Parsing the description
Extract actors, actions, data, constraints. Short name = 2–4 word action-noun ("user-auth",
"oauth2-api-integration"). Feature dir `specs/NNN-short-name/` with the next number; MCP
`mcp_spec_kit_init_feature(feature, name)` creates it (and nothing else).

## Writing the spec
- User scenarios P1/P2/P3, each with an *independent test* line and its ACs.
- FR-### testable and technology-agnostic: "System MUST …", "Users MUST be able to …". A simple
  feature is one paragraph + 2–3 FRs — do not force the template.
- Success criteria measurable (time, count, rate), entities domain-only.
- **Security & Privacy table** — answer every row; the honest "None — because [reason]" is
  the expected answer for most UI work; a non-empty row becomes a plan item and a final-review
  §2 verdict.
- `[NEEDS CLARIFICATION: …]` at most 3; more means the scope is too vague — ask first.

## Acceptance criteria (`spec-kit/references/acceptance.md` §1)
One observable outcome per AC, Given/When/Then, `Verify:` = the LOWEST level that proves it;
`e2e` and `manual` need a reason in parentheses; ≤ 2 e2e per feature — prefer an integration
test of the API plus a component test of the UI. Every FR named by ≥ 1 AC (lint warns).

## The size question (always)
```
SCORE spec-kit/references/sizing.md signals → RECOMMENDED = highest tier triggered
ASK "Size for [feature]?"  1. <RECOMMENDED> (Recommended) — <signals>   2./3. the other tiers, one line each
  (Claude Code: AskUserQuestion, recommended option first)
WRITE **Size**: <answer> — <reason>   RECORD the ruling in decisions.md (quote); unattended → assumption
```
Size S after the user confirms the spec: run `spec-kit-plan` (short) and `spec-kit-tasks` (flat),
ONE commit `spec(phase-1-3): [feature] spec, plan, tasks`.

## MCP, then commit
`mcp_spec_kit_update_artifact(spec.md)` · `mcp_spec_kit_advance_phase(from_phase=1)` (returns the
phase card) · `mcp_spec_kit_lint_artifacts` → 0 errors · commit per `spec-kit/references/commits.md`.
