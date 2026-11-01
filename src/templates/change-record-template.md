# Change Record: [FEATURE NAME]

> One page, written at close, kept with the feature. The auditor reads this file first: what
> changed, why, who decided, how it was verified, who approved, how to roll it back
> (ISO/IEC 27001 A.8.25/A.8.26/A.8.29/A.8.32). Pending fields are written as `pending`, never left blank.

| Field | Value |
|-------|-------|
| **Feature / ticket** | specs/[###-feature-name]/ · [ADO/Jira id] |
| **Branch → base** | [feat/NNN-name] → [dev] · PR [link / pending] |
| **Size / risk tier** | S | M | L — [reason from spec.md] |
| **What changed** | [2–3 sentences; layers touched; the seams] |
| **Why** | [the requirement, in one line] |
| **Security & Privacy impact** | [from spec.md § Security & Privacy — authorization, personal data, new surface, secrets; "none — because …"] |
| **Security level / scans** | [`compliance: baseline`: none/low/medium/high — reason · `final-security_*` results · approver (high) — else delete the row] |
| **Data / schema / config changes** | [migrations, settings, infra; reversible?] |
| **Implemented by** | [agents / humans — history.md entries, or the tasks.md `**Implemented-by**:` line] |
| **Reviewed by** | review:<agent> / self-review (fresh context) · human PR reviewer: [name / pending] |
| **Verification** | acceptance round N PASS @ <sha> · `ci:<id>` · probes: [n] · manual checks: [who, what, quoted] |
| **Decisions** | rulings D-… (by [user]) · assumptions still unconfirmed: [ids / none] · ADRs: [NNNN / none] |
| **Deployment approval** | [who / pipeline run / pending] |
| **Rollback** | [revert PR / redeploy previous artefact / data rollback steps; "forward-only because …"] |
| **Known follow-ups** | [MEDIUM findings, deferred ACs, open bugs by id / none] |

## Timeline

History on: one row per `history.md` entry. History off: `spec-kit/scripts/spec-kit-history.sh [feature]` on the branch before the squash (date · author · subject) — this page is what survives:

| Date | Phase | By | Commit | Evidence |
|------|-------|----|--------|----------|
| | | | | |
