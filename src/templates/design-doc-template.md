# [Module name] — design

> **Status:** current · **Owner:** [team / name] · **Last patched:** [DATE] by [feature]
> A living description of how this part of the system works **now** (≤ 3–4 pages). Patched in
> place by every feature close that changes it — never copied to `-v2`. Decisions live in ADRs;
> this page describes the result. (ISO/IEC 27001 A.8.27 — the architecture an auditor reads.)

> `system.md` (the reserved name): replace *Components* with the container table (service / store / external system · technology · owner · trust boundary) and *Data flow* with the context diagram; every module doc links here.

## Purpose and boundary

[What this module is for; what it owns; what it explicitly does not do. Which services /
projects / directories it is.]

## Components

| Component | Path | Responsibility |
|-----------|------|----------------|

## Data flow

[Entry → processing → storage / response, in prose or one diagram. Name the request/event
that starts it and where it ends.]

## Seams and contracts

| Seam | Kind (DB function / HTTP contract / message / file / service) | Contract | Owner |
|------|------|----------|-------|

## Invariants and security

- Authorization / tenant boundary: [how another tenant's data is kept out — the filter, the policy]
- Personal data handled: [what, where, retention] · Never logged: [what]
- [other invariants: idempotency, ordering, money/rounding, time zones]

## Testing

[Harnesses that cover it: unit / integration / contract / e2e; golden files; probes against real data]

## Known debt

- [item — ticket / ADR]

## Decisions

| ADR | Title | Status |
|-----|-------|--------|

## Change log *(one line per feature close that patched this page)*

- [DATE] [feature] — [what changed in the design]
