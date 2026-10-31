# Epic review: [EPIC NAME]

> One `## Round N` per run, appended. Stage E3.5 (before the first feature is specified) and
> E6 (at close). Verdict gates the next stage.

## Round 1 — [YYYY-MM-DD] — E3.5 pre-build — [review:<agent> | self-review (fresh context: yes/no)]

**Verdict**: GO | GO-WITH-CHANGES | NO-GO

### 1. Coverage and scope
EAC → features: [n/N covered; uncovered: …] · features without an EAC: [scope creep?] ·
non-goals respected: [yes / which row violates] · size realism: [rows likely bigger than their size]

### 2. Fit and rules
Constitution, existing ADRs, module design docs (current state is true?), cross-feature rules
consistent and checkable: [findings with path / § references]

### 3. Sequencing and risk
First feature delivers something testable: [yes/no] · hidden dependency: [...] · the plan's risks
have owners: [...]

### 4. Devil's advocate *(separate sub-agent for 5+ features; different model when available)*

| # | Objection (concrete) | Answer | Outcome |
|---|----------------------|--------|---------|
| O1 | strongest case against doing this epic at all; the simplest alternative that delivers ~80 % | | accepted → change / rebutted (evidence) / deferred |
| O2 | pre-mortem: six months later the epic failed or was abandoned — why? | | |
| O3 | abuse case at system level (new trust boundary, tenant path, data export) | | |
| O4 | riskiest assumption in epic.md / ED-… — what if it is wrong? | | |
| O5 | | | |

### 5. Findings
| ID | Severity | Where | Finding | Fix |
|----|----------|-------|---------|-----|

### 6. Outcome
Changes applied to epic.md / plan.md / features.md: [list] · open rulings for the owner: [list]

## Round N — [YYYY-MM-DD] — E6 close review

**Verdict**: CLOSED | NOT-DONE
EAC verified: [each with evidence — feature ACs, probe, user's quoted words] · dropped scope: [rows + why] ·
design docs patched: [list] · ADRs: [list] · devil's advocate at close: "what does the goal look like unmet?" — [answer]
