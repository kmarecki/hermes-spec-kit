# Evidence of Done

**Rule**: a statement made by the agent that produced a change is never evidence that the change works. Every gate that used to read "tests pass" now needs an **oracle** the agent did not author.

Why: the same model writes the code, the tests, the fixtures and the review. Its fixtures encode its own misunderstanding, and its review shares its blind spots. A fix can pass every artifact gate and still be wrong (hand-built fixture vs real data shape).

## Accepted oracles

| Oracle | Form | Counts as |
|--------|------|-----------|
| `user` | A human ran or inspected it and said so (quote the words) | verification |
| `ci:<run-id>` | A CI pipeline run on the exact commit, with its result | verification |
| `review:<agent>` | A review by a **different** agent than the author (e.g. `review:claude` for Hermes-implemented code) | verification |
| `probe:<path>` | A read-only query/call against the real system or real data, command and result saved under `specs/[feature]/evidence/` | evidence (supports a claim; required for every external seam) |
| `output:<path>` | Saved output of a test/build command, under `specs/[feature]/evidence/` | evidence (supports a claim) |

`probe:` and `output:` strengthen a **claim**. They do not by themselves verify a bug fix; `verified` needs `user`, `ci:` or `review:<other-agent>`.

## Evidence directory

`specs/[feature]/evidence/` — committed with the feature. One file per item, named `<ID>-<label>.<ext>`, e.g. `BF-014-red.txt`, `BF-014-probe-exchange-rates.txt`, `T012-tests.txt`. Each file starts with the command that produced it and the UTC time.

## RED, GREEN and fixtures (the checkable TDD rules)

| Rule | File |
|------|------|
| A `[TEST]` task's failing run is saved before implementation code is written | `evidence/<phase-or-task>-red.txt` |
| A `[SEAM]` task starts with a read-only probe of the real system; the fixture matches its shape | `evidence/<TASK>-probe-<seam>.txt` |
| Legacy code without tests: pin current behaviour first | `evidence/<TASK>-characterisation.txt` |
| The phase's passing run | `evidence/<phase>-green.txt` |
| The full regression | `evidence/regression-<date>.txt` + `ci:<run-id>` |

`lint_artifacts` warns when a `[SEAM]` task is marked done without a probe file, or a `[TEST]` task is done with no RED file in `evidence/`.

## Status vocabulary (bugs.md)

| Status | Set by | Meaning |
|--------|--------|---------|
| `open` | test skill | logged, not planned |
| `in-progress` | implement skill | fix under way |
| `claimed` | implement skill | the agent believes it is fixed; **Evidence:** lists the `output:`/`probe:` files |
| `verified` | test skill, only with **Verified-by:** `user` / `ci:<id>` / `review:<other-agent>` | an oracle confirmed it |
| `superseded` | plan/test skill | replaced by another bug entry (name it) |

Legacy values `resolved` and `fixed` are read as `claimed`. An implementing agent never sets `verified` on its own claim.

## Author / reviewer split

Every implement-phase history entry records `Implemented-by: <agent>` (`hermes`, `claude`, or the user's name). `spec-kit-review` reads it:

- a different agent → the report may be cited as `review:<agent>`;
- the same agent → the report is labelled **self-review** and cannot be cited as verification.

With both agents installed, the default is: whoever implemented does not review.

## What each gate must show

| Gate | Minimum evidence |
|------|------------------|
| Implement phase commit | `output:` of the phase's test run |
| Full regression (implement step 7) | `output:` of the full run **and** `ci:<id>` when a pipeline exists |
| Bug `claimed` | `output:` of the reproducing test now green; `probe:` for every external seam the fix touches |
| Bug `verified` | `Verified-by:` oracle |
| Final review (phase 5.5) | `review-final.md` round with Verdict + Reviewed-commit; `output:` of diff_scan, build, full test, lint; `ci:<id>` when a pipeline exists |
| Close (phase 6) | final review READY / READY-WITH-FOLLOWUPS and not stale; every bug `verified` or `superseded`; every ❌/⚠️ in the gap table names its evidence or its absence |

A gate without evidence is reported as **unverified**, never as done.
