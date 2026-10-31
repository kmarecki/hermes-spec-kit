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

## Files — every tier (`sizing.md`: the size changes the workflow, never the evidence)

`specs/[feature]/evidence/`, one file per item, first line = command, second = UTC time.

| File | When |
|------|------|
| `<TASK>-probe-<seam>.txt` — read-only probe before a `[SEAM]` fixture | every `[SEAM]` task |
| `<phase>-red.txt` — the phase's `[TEST]` tasks failing for the right reason | every implement phase (S: the one phase) |
| `<phase>-green.txt` — the phase's tests passing | every implement phase |
| `<TASK>-characterisation.txt` — legacy code pinned before change | when it applies |
| `acceptance-r<N>.txt` (+ `-AC-###.txt` per command/probe AC) | every acceptance round |
| `acceptance-freeze.json` — SHA of the AC tests after RED | every feature with ACs |
| `final-<check>.txt` — diff scan, build, test, lint, format | every final review |

The history entry's `Evidence:` field (history on) or the commit body (history off) names these files. `lint_artifacts` warns about a done `[TEST]`
task without a RED file and a done `[SEAM]` without a probe — every tier.

## Acceptance criteria are always documented

Every feature, S included, ends with an acceptance round in `acceptance.md` that lists every
AC with its outcome. Automated wherever a harness exists (`unit` … `e2e`, `command`, `probe`);
`manual` only where no tool can judge, and then the round (or the final review) quotes the
user's confirmation — an unconfirmed manual AC is 👤 pending, never ✅.

## Status vocabulary (bugs.md)

`open` → `in-progress` → `claimed` (agent believes fixed; **Evidence:** lists files) →
`verified` (only with **Verified-by:** `user` / `ci:<id>` / `review:<other-agent>`) ·
`superseded` (replaced by another entry). Legacy `resolved`/`fixed` read as `claimed`. The
implementing agent never sets `verified`.

## Author / reviewer split

`Implemented-by` = the `<agent>` of the history.md implement entries, or — history off — the
`**Implemented-by**:` line in the tasks.md header. The review reads it: a different agent →
the review is `review:<agent>`; the same agent → **self-review** (fresh-context sub-agent for
L), which opens the merge gate but never verifies a bug.

## Gates

| Gate | Minimum evidence |
|------|------------------|
| Implement phase commit | `output:` RED + GREEN of the phase; probe per seam |
| Acceptance round | `acceptance.md` round with Result + Commit; `output:`; frozen tests unchanged |
| Bug `claimed` | `output:` of the reproducing test green; `probe:` per seam touched |
| Bug `verified` | `Verified-by:` oracle |
| Final review | round with Verdict + Reviewed-commit; `output:` of diff_scan, build, test, lint; `ci:` when a pipeline exists |
| Close | final review READY / READY-WITH-FOLLOWUPS, fresh; every bug verified or superseded; change record filled |

A gate without evidence is **unverified**, never done.
