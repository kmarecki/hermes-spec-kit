# Evidence of Done

**Rule**: a statement by the agent that produced a change is never evidence that it works.
The same model writes the code, the tests, the fixtures and the review; its fixtures encode
its own misunderstanding. Every gate needs an **oracle** the agent did not author.

## Oracles

| Oracle | Form | Counts as |
|--------|------|-----------|
| `user` | A human ran or inspected it and said so (quote the words) | verification |
| `ci:<run-id>` | A CI run on the exact commit, with its result | verification |
| `review:<agent>` | A review by a **different** agent than `Implemented-by` | verification |
| `probe:<path>` | Read-only query/call against the real system, saved under `evidence/` | evidence — required for every `[SEAM]` |
| `output:<path>` | Saved output of a test/build command under `evidence/` | evidence |

`probe:` and `output:` support a **claim**; `verified` needs `user`, `ci:` or `review:<other-agent>`.

## Files — by size (`sizing.md`)

`specs/[feature]/evidence/`, one file per item, first line = command, second = UTC time.

| File | S | M | L |
|------|---|---|---|
| `<TASK>-probe-<seam>.txt` — read-only probe before a `[SEAM]` fixture | ✓ | ✓ | ✓ |
| `<phase>-red.txt` — the phase's `[TEST]` tasks failing for the right reason | — | ✓ | ✓ |
| `<phase>-green.txt` — the phase's tests passing | — | — | ✓ |
| `<TASK>-characterisation.txt` — legacy code pinned before change | when it applies | ✓ | ✓ |
| `acceptance-r<N>.txt` (+ `-AC-###.txt` per command/probe AC) | ✓ | ✓ | ✓ |
| `acceptance-freeze.json` — SHA of the AC tests after RED | ✓ | ✓ | ✓ |
| `final-<check>.txt` — diff scan, build, test, lint, format | ✓ | ✓ | ✓ |

Where a RED/GREEN file is not required, the commit's `Evidence:` trailer names the test
command and counts instead. `lint_artifacts` warns about a done `[TEST]` task without a RED
file only for M and L; a done `[SEAM]` without a probe always.

## Status vocabulary (bugs.md)

`open` → `in-progress` → `claimed` (agent believes fixed; **Evidence:** lists files) →
`verified` (only with **Verified-by:** `user` / `ci:<id>` / `review:<other-agent>`) ·
`superseded` (replaced by another entry). Legacy `resolved`/`fixed` read as `claimed`. The
implementing agent never sets `verified`.

## Author / reviewer split

`Implemented-by:` is a commit trailer (`commits.md`). The review reads it: a different agent →
the review is `review:<agent>`; the same agent → **self-review** (fresh-context sub-agent for
L), which opens the merge gate but never verifies a bug.

## Gates

| Gate | Minimum evidence |
|------|------------------|
| Implement phase commit | `Evidence:` trailer (S) / `output:` RED (M) / RED + GREEN (L); probe per seam |
| Acceptance round | `acceptance.md` round with Result + Commit; `output:`; frozen tests unchanged |
| Bug `claimed` | `output:` of the reproducing test green; `probe:` per seam touched |
| Bug `verified` | `Verified-by:` oracle |
| Final review | round with Verdict + Reviewed-commit; `output:` of diff_scan, build, test, lint; `ci:` when a pipeline exists |
| Close | final review READY / READY-WITH-FOLLOWUPS, fresh; every bug verified or superseded; change record filled |

A gate without evidence is **unverified**, never done.
