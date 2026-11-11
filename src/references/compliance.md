# Security Compliance — `compliance: baseline`

Opt-in: `compliance: baseline` in `specs/git-conventions.md`. Absent or `none` → this file does
not apply. `formal` is not implemented (repo `docs/compliance.md` — the ISO 27001 / NIS2 map).

## 1. Security level — per feature, asked at specify beside the size

`**Security**: none | low | medium | high — <reason>`. The highest signal wins; the user may raise
it; lowering it below a signal needs a quoted ruling in `decisions.md`.

| Level | Signals | Adds |
|---|---|---|
| `none` | docs, tests only, styling / copy, a refactor with unchanged behaviour — no change to access, data, dependencies, config or infra | nothing: the Security & Privacy table becomes the one `**Security**:` line; no `[SEC]` tasks |
| `low` | behaviour changes inside an existing authorized surface; no new data class | the 5 base rows |
| `medium` | new endpoint / integration / dependency / setting / secret; personal data read | + the 4 extended rows (§2) |
| `high` | authorization or tenant boundary changed; personal data exported or deleted; cryptography or key handling; new public surface; infra / network / IaC | + threat model (§3) + named human approver (§5) |

## 2. Extended Security & Privacy rows (medium, high)

Secrets & cryptography · Availability & recovery (failure mode, rollback, backup) · Third parties &
dependencies (new package or service, known vulnerabilities, licence, data shared) · Data
lifecycle (retention, deletion, test data, no production data outside production).

## 3. Threat model (high) — plan.md `## Threat Model`

One row per new or changed trust-boundary crossing: STRIDE category → threat → mitigation (task or
`path`) → residual risk. A residual risk left open is accepted only by a `decisions.md` ruling
quoting its owner.

## 4. `[SEC]` tasks

`[SEC]` marks a task that implements or tests a Security & Privacy row or a threat-model
mitigation; the final review verdicts these tasks, and other tasks need no security assessment. Every
authorization / tenant row has a negative `[TEST] [SEC]` (another tenant's id, an unauthorized role).

## 5. Gates

- **Scans**: the merge checklist `security_*` commands run in every final review, whatever the
  level — they are mechanical, not an assessment (`evidence/final-security_<check>.txt`). Exit 126 /
  127 or a missing tool / network = **could not run**: ❌ not run, ASK — never a finding, never a bug.
- **Approval** (high): the final round needs `**Approved-by**: <human> — "<quoted words>"`;
  missing → `AWAITING-OWNER`. An agent's review is evidence, never approval.
- **Bugs**: `**Security**: yes | no`. Yes → no exploit payload or secret in the repo; found in
  production → tell the user to start the project's incident procedure — spec-kit does not report.
- **Change record**: security level + reason, scan results, approver.

## 6. On top of the process level (`rigor.md`) — added at every P1–P3, never below

| Level | Adds |
|---|---|
| `low` | the Security & Privacy row answered in the plan; S1–S2 cited in the final round |
| `medium` | `[SEC]` tasks; every `[TEST] [SEC]` keeps its RED file (test-after too: the negative test fails before the fix); final §4 abuse cases per Security row |
| `high` | + threat model; the final devil's advocate's security pass by a **different agent** even at P1 / P2; `**Approved-by**:` a named human (or the PR's approval `— pr:<id>`); change record required |
