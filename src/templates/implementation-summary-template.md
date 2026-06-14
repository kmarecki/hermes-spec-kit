[Implementation Summary: FEATURE NAME]

**Feature**: specs/[###-feature-name]/
**Created**: [DATE]
**Status**: [Complete / In Progress]
**Spec Health**: N%
**TDD Mode**: Active / Bypassed by user

## Spec Health Scoring

| Category | Count |
|----------|-------|
| ✅ Resolved (implemented or intentionally deviated with rationale) | N |
| ⚠️ Acknowledged (deferred with documented reason) | N |
| ❌ Not Done (missing without documented reason) | N |
| **Spec Health** | **N%** |

> Formula: `(resolved + acknowledged) / (resolved + acknowledged + not_done) * 100`
> - **100%**: Artifacts fully aligned with code — no action needed
> - **80-99%**: Minor gaps tracked but not blocking — acceptable
> - **50-79%**: Significant drift — recommend running `spec-kit-refresh` before refactoring
> - **<50%**: Artifacts are misleading — run `spec-kit-refresh` before proceeding

## Overview

[Brief summary of what was implemented — 2-3 sentences]

## What Was Implemented

### Core Features
| User Story / Requirement | Status | Notes |
|--------------------------|--------|-------|
| [US1: description] | [Implemented / Partial / Not Started] | [key files changed, decisions made] |
| [FR-001: description] | [Implemented / Partial / Not Started] | [key files changed, decisions made] |
| ... | | |

### Architecture & Design
- **Architecture type**: [single project / web app / etc.]
- **Language / Runtime**: [e.g., Python 3.11, Node 20]
- **Key Dependencies**: [list added dependencies]
- **Data Model**: [entities created / modified]
- **Contracts**: [APIs, schemas defined]

## Files Changed

| File | Change Type | Description |
|------|------------|-------------|
| `path/to/file.ext` | created / modified / deleted | Brief purpose |
| ... | | |

## Test Coverage

| Type | Passing | Notes |
|------|---------|-------|
| Unit tests | N | [frameworks used] |
| Integration tests | N | [what's covered] |
| E2E tests | N | [scope] |
| Contract tests | N | [if applicable] |

## Known Issues & Bugs

| Bug ID | Severity | Status | Summary |
|--------|----------|--------|---------|
| BUG-001 | minor | resolved | [short description] |
| BUG-002 | critical | verified | [short description] |

## Gap Analysis — Plan vs Implementation

This section compares what was specified/planned with what was actually implemented. Each gap is either **resolved** (intentional, with rationale) or **acknowledged** (deferred, tracked for future).

| Category | Planned | Actual | Verdict | Notes / Rationale |
|----------|---------|--------|---------|-------------------|
| [FR-001] | [description] | [what was built] | ✅ Resolved | [rationale if different] |
| [US2 user story] | [acceptance criteria] | [actual behavior] | ✅ Resolved | [test outcome] |
| [Data model entity] | [planned entity/field] | [actual entity/field] | ⚠️ Acknowledged | [deferred — not critical, tracked for later] |
| [API contract] | [planned endpoint] | [actual endpoint] | ❌ Not Done | [not implemented, should be in bugs.md] |
| ... | | | ✅ Resolved / ⚠️ Acknowledged / ❌ Not Done | |

### Resolved Deviations
- **[Aspect]**: Planned X, built Y because [reason]. Spec should be updated to reflect Y.
- ...

### Acknowledged Gaps (Deferred)
- **[Aspect]**: Planned X, not built. Reason: [scope cut, ran out of time, not needed]. Track as future work.
- ...

## Spec Artifact Refresh

The following spec artifacts were **automatically updated** to reflect intentional deviations found during gap analysis:

| Artifact | Change | Rationale |
|----------|--------|-----------|
| `spec.md` | [FR-XXX: updated requirement wording to match actual behavior] | Code intentionally deviated from spec — spec brought in line |
| `plan.md` | [architecture section updated] | Implementation used a different data structure than planned |
| *(none)* | *All artifacts already aligned* | *No changes needed* |

> If artifacts show `⚠️ needs review` or `❌ outdated`, they were NOT auto-updated because the drift requires user judgment. Run `spec-kit-refresh` to reconcile them manually.

## Decisions Made

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| [choice made] | [why] | [what else was considered] |

## Open Questions / Future Work

- [anything deferred, known limitations, future improvements]

## Spec State

| Artifact | Status | Action Needed |
|----------|--------|---------------|
| `spec.md` | ✅ up-to-date / ⚠️ needs review / ❌ outdated | [update to match actual implementation] |
| `plan.md` | ✅ up-to-date / ⚠️ needs review / ❌ outdated | [update architecture to match what was built] |
| `tasks.md` | ✅ all complete / ⚠️ N remaining | [mark incomplete or close] |
| `bugs.md` | ✅ all verified / ⚠️ N open | [resolve or defer remaining] |
| `data-model.md` | ✅ up-to-date / ⚠️ needs review | [sync with actual schema] |
| `contracts/` | ✅ up-to-date / ⚠️ needs review | [sync with actual API contracts] |
