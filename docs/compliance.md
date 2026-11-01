# Security compliance in spec-kit — ISO/IEC 27001:2022 and NIS2

> **Status:** current — `baseline` implemented · `formal` documented only (a possible future upgrade, not built)

spec-kit covers the **secure development and change management** slice of an information
security management system (ISMS). It produces, per change, the records an auditor samples:
requirement → design → test evidence → review → approval → rollback. It does **not** run the
ISMS itself — scope, risk assessment, Statement of Applicability (SoA), policies, internal audit,
management review, HR and physical security (ISO 27001 clauses 4–10), management-body
accountability (NIS2 Art. 20) and incident reporting (NIS2 Art. 23) stay with the organisation.
spec-kit's artifacts are evidence for them.

Whether NIS2 applies to a project's operator directly (sector, size threshold, national
transposition) is a legal question. A supplier to in-scope entities is reached anyway through
their supply-chain obligations (Art. 21(2)(d), 21(3)) — `baseline` is sized for that case.

## Profiles

| Profile | Setting (`specs/git-conventions.md`) | State |
|---|---|---|
| none | `compliance: none` or absent | default; the workflow as before |
| **baseline** | `compliance: baseline` | **implemented** — agent rules in `src/references/compliance.md` |
| formal | — | **not implemented** — see [Formal profile (future)](#formal-profile-future) |

## Baseline — what it adds

Security is assessed **per feature**, and inside a feature **per task**. A feature that cannot
affect security says so in one line and carries no further security work.

| Phase | Added | Artifact |
|---|---|---|
| Specify | `**Security**: none \| low \| medium \| high — reason`, asked beside the size from signals (access, data, dependencies, config, infra). `none` replaces the Security & Privacy table; `medium`/`high` add four rows (secrets & crypto, availability & recovery, third parties & dependencies, data lifecycle) | `spec.md` |
| Plan | `high` → `## Threat Model`: STRIDE per new trust-boundary crossing → mitigation → residual risk; an open residual risk is accepted only by its owner's quoted ruling | `plan.md`, `decisions.md` |
| Tasks | `[SEC]` on the tasks that implement or test a security row or mitigation; a negative `[TEST] [SEC]` per authorization / tenant row. Untagged tasks need no security assessment | `tasks.md` |
| Final review | §2 verdicts every `[SEC]` task, threat-model row and S-item with `path:line`; `high` needs `**Approved-by**:` a named human with quoted words, else `AWAITING-OWNER`; the MCP gate blocks the close without it | `review-final.md` |
| Merge checklist | `security_deps` · `security_secrets` · `security_sast` · `security_iac` commands, gate items S1–S5, evidence files `final-security_*.txt` — run at every level (mechanical, not an assessment) | `specs/merge-checklist.md` |
| Bugs | `**Security**: yes \| no`; no exploit payloads or secrets in the repo; production finding → the organisation's incident procedure | `bugs.md` |
| Close | change record row: security level + reason, scan results, approver | `change-record.md` |

Lint (`lint_artifacts`) warns on: a missing `**Security**:` line, `high` without `## Threat
Model`, a non-`none` level without any `[SEC]` task. `close_feature` / `advance_phase(5)` refuse
a `high` feature whose latest final-review round has no named approver.

## Control mapping (for the SoA and the auditor)

ISO/IEC 27001:2022 Annex A · NIS2 Directive (EU) 2022/2555 Art. 21(2) · NIST SP 800-218 SSDF.
**B** = provided by baseline (or by every profile, marked *all*), **F** = would come with formal.

| Control | spec-kit evidence | Profile |
|---|---|---|
| A.5.8 Information security in project management | Security & Privacy table in every spec; security level per feature | all / B |
| A.5.3 Segregation of duties | author / reviewer split (`Implemented-by` vs `review:<other-agent>`); human approver for `high` | all / B |
| A.5.12 Classification of information | security level signals (personal data, tenant data) | B (partial) · F: data class per entity |
| A.5.19–A.5.22 Supplier & ICT supply chain · NIS2 (d) | third-party row; `security_deps`; G11 licence check | B · F: SBOM |
| A.5.24–A.5.26 Incident management · NIS2 (b), Art. 23 | security bug flag → incident procedure hand-off | B (hand-off only) |
| A.5.33 Protection of records | additive-only artifacts; `change-record.md` survives the squash | all |
| A.5.37 Documented operating procedures | runbooks patched at close | all |
| A.8.4 Access to source code | G5 / `security_secrets` — no secrets in the diff | all / B |
| A.8.8 Technical vulnerabilities · NIS2 (e) | `security_deps`, `security_sast` blocking | B |
| A.8.9 Configuration management | G12 config documented; `security_iac` | all / B |
| A.8.24 Use of cryptography · NIS2 (h) | secrets & cryptography row (medium+) | B |
| A.8.25 Secure development life cycle · NIS2 (e) · SSDF PO | the phase workflow itself; constitution | all |
| A.8.26 Application security requirements · SSDF PW.1 | Security & Privacy table (+ extended rows) | all / B |
| A.8.27 Secure architecture & engineering · SSDF PW.1 | plan answers each row; threat model (`high`); design-doc security invariants | all / B |
| A.8.28 Secure coding · SSDF PW.5 | final review §3 security findings; SAST | all / B |
| A.8.29 Security testing in development & acceptance · SSDF PW.7–8 | RED/GREEN evidence; `[TEST] [SEC]` negative tests; acceptance rounds | all / B |
| A.8.31 Separation of environments · A.8.33 Test information | data-lifecycle row (no production data outside production) | B |
| A.8.32 Change management | `change-record.md` (what, why, who, verification, approval, rollback) | all |
| Clause 9.1 Monitoring & measurement · NIS2 (f) | per-feature health score | all · F: project report |
| NIS2 (a) Risk analysis | security level + threat model + accepted residual risks | B |
| NIS2 (c) Business continuity | availability & recovery row; rollback in the change record | B |
| SSDF RV.1–RV.3 Respond to vulnerabilities | security bugs, bugfix loop with evidence | B |

## Formal profile (future)

Not implemented. Recorded here so the upgrade path is known; each item is a separate change to
spec-kit, to be built only when certification or a contract asks for it.

1. **`compliance: formal`** setting and `compliance_dir` (e.g. `docs/compliance`) holding the
   project's SDLC SoA extract and a link to the ISMS risk register.
2. **Security requirements `SR-###`** — every non-`none` Security & Privacy row becomes an
   identified requirement with its own AC; optional OWASP ASVS 5.0 requirement id per SR; SR ACs
   frozen like ACs.
3. **Threat model for `medium` and above**, not only `high`; risk acceptances get an id
   (`RA-###`), an owner, an expiry date and a link to the risk register.
4. **Control tags** — the plan and the change record name the Annex A controls a feature
   touches; the close checks the SoA extract lists them.
5. **Approval policy** — `human_approval: high | medium+ | all`; for covered levels the change
   record may not close with `pending` in *Reviewed by* or *Deployment approval*; the production
   deployment approval references the pipeline's approval record; an *emergency change* flag with
   retrospective approval.
6. **Supply chain** — SBOM (CycloneDX / SPDX) generated per release and stored as evidence;
   build provenance (SLSA level target) recorded in the change record.
7. **Project compliance report** — an MCP tool / script aggregating all specs: changes per
   security level, % with a human approver, scan pass rate, open security bugs and their age,
   accepted risks near expiry. Evidence for ISO 27001 clause 9.1 / management review and NIS2
   Art. 21(2)(f).
8. **AI-assisted development governance** — record the model and version in `Implemented-by`;
   a constitution principle on what may be sent to model providers (ISO A.5.14, A.5.23) and on
   treating agents as development suppliers (A.8.30); optionally map to ISO/IEC 42001.
9. **Constitution principle 13 "Security & Compliance"** — options A none / B baseline / C formal,
   whose choice sets `compliance:`.
10. **Vulnerability disclosure** — a `SECURITY.md` template and a private channel reference for
    security bugs (NIS2 Art. 12 coordinated disclosure).
