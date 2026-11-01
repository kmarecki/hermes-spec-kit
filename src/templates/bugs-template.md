# Bug Report: [FEATURE NAME]

**Feature**: specs/[###-feature-name]/
**Created**: [DATE]
**Status**: Open

> **Section ordering**: New bugs are INSERTED at the end of ## Bug Log (before the `---` separator). The ## Summary section stays at the bottom and MUST be updated after every insert. Never put new bugs after the `---` separator.

## Bug Log

### BUG-001: [Short descriptive title]

- **Severity**: [critical/major/minor/trivial]
- **Security**: [no / yes — `compliance: baseline`: no exploit payload or secret here]
- **Area**: [spec section or component affected]
- **Description**: [What the bug is — observed vs expected behavior]
- **Steps to Reproduce**:
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
- **Actual Result**: [What currently happens]
- **Expected Result**: [What should happen]
- **Requires Clarification**: [ ] no / [ ] yes (if yes, run spec-kit-clarify before plan)
- **Plan Ref**: [Populated by plan phase — reference to plan.md fix section]
- **Status**: [open/in-progress/claimed/verified/superseded]
- **Evidence**: [set with `claimed` — `output:<path>`, `probe:<path>` under specs/[feature]/evidence/]
- **Verified-by**: [set with `verified` — `user` / `ci:<run-id>` / `review:<other-agent>`; never the implementing agent's own word]

### BUG-002: [Short descriptive title]

- **Severity**: [critical/major/minor/trivial]
- **Area**: [spec section or component affected]
- **Description**: [What the bug is — observed vs expected behavior]
- **Steps to Reproduce**:
  1. [Step 1]
  2. [Step 2]
- **Actual Result**: [What currently happens]
- **Expected Result**: [What should happen]
- **Requires Clarification**: [ ] no / [ ] yes
- **Plan Ref**: [Populated by plan phase]
- **Status**: [open/in-progress/claimed/verified/superseded]
- **Evidence**: [output:/probe: files]
- **Verified-by**: [user / ci:<run-id> / review:<other-agent>]

*New bugs are inserted here — before the `---` separator below.*

---

## Summary

| Bug ID | Severity | Area | Status | Needs Clarification |
|--------|----------|------|--------|---------------------|
| BUG-001 | [severity] | [area] | open | [ ] no / [ ] yes |
| BUG-002 | [severity] | [area] | open | [ ] no / [ ] yes |

**Total Bugs**: N
**Open**: N
**In Progress**: N
**Claimed** (agent says fixed, awaiting an oracle): N
**Verified** (user / CI / other-agent review): N

> Status rules: `spec-kit/references/evidence.md`. Legacy `resolved`/`fixed` read as `claimed`.
