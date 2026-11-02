# [PROJECT_NAME] Constitution

> Ratified: [DATE] | Version: [VERSION] | Rigor: [lean | standard | strict] (`spec-kit/references/rigor.md`)
> Auto-detected from: [brownfield detected sources] *(remove if greenfield)*
> *[If monorepo: Multi-project constitution — see Projects section]*

## Projects *(omit if single-project)*

| Project | Purpose | Language/Framework | Architecture | 
|---------|---------|-------------------|--------------|
| [e.g., frontend] | [purpose] | [tech] | [arch option] |
| [e.g., mobile] | C — Native / Desktop Client | [Flutter] | C2 — Cross-Platform |
| [e.g., backend] | A — User-Facing App | [Go] | A2 — Modular Monolith |

## Tech Stack

*(For single-project constitutions. Multi-project: see Projects table above.)*

- **Language**: [LANGUAGE_VERSION]
- **Framework**: [FRAMEWORK]
- **Test Framework**: [TEST_FRAMEWORK]
- **Package Manager**: [PACKAGE_MANAGER]
- **CI/CD**: [CI_PLATFORM]
- **Database**: [DATABASE]
- **Deployment**: [DEPLOYMENT_TARGET]
- **Traits**: runs [multi-tenant SaaS | single-tenant | on-prem | local-first | edge] · regulated [none | personal data | finance | health | safety-critical | AI Act high-risk] · lifecycle [prototype | product | modernization]

## Core Principles

*(Shared principles apply to all projects in a monorepo. Project-specific variations noted per principle.)*

### 1. Testing Philosophy
**Chosen: [A | B | C] — [Rule Name]**

[User-picked option's full text as the constitutional rule]

**Rationale:** [Why this option was chosen]

### 2. Code Quality & Linting
**Chosen: [A | B | C] — [Rule Name]**

[User-picked option's full text]

**Rationale:** [Why this option was chosen]

### 3. Architecture
**Chosen: [A1–A6 | B1–B3 | C1–C3 | D1–D4 | E1–E5 | F1–F4 | G1–G4 | H1–H5 | I1–I4 | J1–J3 | K1–K3 | Other] — [Rule Name]**

[User-picked option's full text]

**Rationale:** [Why this option was chosen]

### 4. Dependencies & Third-Party
**Chosen: [A | B | C] — [Rule Name]**

[User-picked option's full text]

**Rationale:** [Why this option was chosen]

### 5. Git Workflow
**Chosen: [A | B | C] — [Rule Name]**

[User-picked option's full text]

**Rationale:** [Why this option was chosen]

### 6. Documentation
**Chosen: [A | B | C] — [Rule Name]**

[User-picked option's full text]

**Rationale:** [Why this option was chosen]

### 7. Error Handling
**Chosen: [A | B | C] — [Rule Name]**

[User-picked option's full text]

**Rationale:** [Why this option was chosen]

### 8. Performance
**Chosen: [A | B | C] — [Rule Name]**

[User-picked option's full text]

**Rationale:** [Why this option was chosen]

### 9. Code Review
**Chosen: [A | B | C] — [Rule Name]**

[User-picked option's full text]

**Rationale:** [Why this option was chosen]

### 10. Database & Schema
**Chosen: [A | B | C] — [Rule Name]**
*(omit if project has no database)*

[User-picked option's full text]

**Rationale:** [Why this option was chosen]

### 11. Configuration & Secrets
**Chosen: [A | B | C] — [Rule Name]**

[User-picked option's full text]

**Rationale:** [Why this option was chosen]

### 12. Dev Toolchain
**Chosen: [A | B | C] — [Rule Name]**

[User-picked option's full text]

**Rationale:** [Why this option was chosen]

## Engineering Guidelines

*(lean: one line. standard / strict: layout and module boundaries, lint / format config, testing shape, coverage target; every MUST also appears as a P-item in `specs/merge-checklist.md`.)*

- [e.g., "Modules own their tables; no cross-module SQL" — MUST — P3]

## Rejected Alternatives

For transparency, record the options that were considered and rejected:

| Principle | Rejected Options | Reason |
|-----------|-----------------|--------|
| Testing | [e.g., Option C — Test-After] | [e.g., existing test suite uses pytest, must maintain coverage] |
| ... | ... | ... |

## Amendments

| Date | Version | Change |
|------|---------|--------|
| [DATE] | [VERSION] | Initial ratification |
