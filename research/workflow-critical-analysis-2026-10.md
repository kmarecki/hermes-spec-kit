# Spec-kit workflow — critical analysis

> **Status:** analysis, 2026-10-22. No workflow changes proposed here have been applied.
> Evidence comes from the 12 installed skills (v1.1–2.1), the shared references, the MCP server, and one real deployment: the `oesgpoint` repository (37 spec-kit features, 1 323 history entries, 405 logged bugs) plus the merge review of `370-v2-reader-cross-domain-ops` done the same day.

## 1. Scope and method

Three questions:

1. Where does the workflow deliver, and where does it produce ceremony without control?
2. Which rules assume capabilities that today's LLM agents (Claude, Hermes-hosted models) do not reliably have?
3. What should change, and in which order?

Method: read every skill and reference; measure the artifacts the workflow produced in a real repository; cross-check with one end-to-end case where the workflow's own gates passed but the code was wrong.

## 2. What the real deployment shows

| Measure (oesgpoint, 37 features) | Value | Reading |
|---|---|---|
| `history.md` total | 293 790 words; largest file 215 KB | The "process log" became a narrative archive. Median entry 200 words, p90 404, max 1 651. |
| Spec commits vs code commits on feature 370 | 19 vs 8 | More than two document commits per code commit. |
| MCP `state.json` vs artifacts on disk | 30 of 34 features disagree (e.g. `status: active` while `close.md` exists) | The "deterministic state" is a second source of truth that drifted almost immediately. |
| Commits touching the shared `state.json` | 36, including 4 merge commits that had to resolve it | One JSON file for all features is a merge-conflict generator. It blocked PR 142. |
| Bug statuses | 295 `resolved`, 44 `verified`, 23 `fixed` (not a defined value), 10 empty | The rule "only the user marks verified" is not practised; the schema drifts. |
| Spec health scores | 46 of 68 are 100 %, none below 82 % | Self-graded metric; no discriminating power. |
| Procedural text loaded per phase | 6–10 k tokens (implement ≈ 9 k, review ≈ 10 k) plus 4 k words of templates | Instructions compete with the code context the work actually needs. |
| Features with `clarify.md` / review reports | 23 / 26 of 37 | Optional phases are used; the pipeline is real, not abandoned. |

The last row matters: the team does follow the workflow. The problems below are therefore design problems, not adoption problems.

### 2.1 The case that passed every gate and was still wrong

Feature 370, bug BUG-005: revenue intensity never resolved in production. The bugfix round followed the full chain (bugs.md → plan section → BF-014 task → RED test → GREEN → history entry → commit). Three unit tests passed. The fix did not work against the real exchange-rate function, because the tests used a hand-built single-row fixture while the real TVF returns four rows per stored rate. The defect was found only by a read-only query against DEV data.

Everything the workflow can check (artifacts exist, tests exist, tests pass, history recorded) was green. The one thing that mattered, contact with reality, is not a gate anywhere in the twelve skills.

In the same round, tasks.md marked "the parse-message token" done although no code changed, and plan.md's BF-018 section describes a design the implementation deliberately abandoned. Both are self-attestation failures the workflow has no mechanism to catch.

## 3. What works and should stay

- **Phase separation with artifacts.** spec → plan → tasks → implement gives an auditable trail and lets two agents hand over work. The Claude/Hermes interchangeability built today exists only because the artifacts are the interface.
- **Log before fix.** Forcing bugs through `bugs.md` before code stops the "fix the symptom I was just told about" reflex. Keep it.
- **Additive-only documents.** Prevents the model from rewriting a spec to match whatever it built. Keep the rule, fix the consequences (see §4.5).
- **Constitution as context, not gate.** The v2 change to inject principles rather than block on them was right.
- **Nitpick filter in review.** The explicit "five harms" bar is one of the few places the workflow fights a known LLM failure mode (volume over substance).

## 4. Critical findings

Ranked by impact. Each gives the evidence, the LLM-capability reason it fails, and a direction.

### 4.1 No external oracle anywhere in the pipeline

**Evidence.** §2.1. Also: 295 bugs are `resolved` on the agent's word; 46 health scores of 100 % are the agent grading itself.

**Why LLMs cannot carry this.** A model cannot reliably verify its own claims. "Tests pass" is a statement the same model produced that wrote the tests and the code; its fixtures encode its own misunderstanding. Model-written review of model-written code shares the blind spot (BF-014 survived its own review round).

**Direction.** Every "Done When" that currently says "tests pass" should require evidence the agent did not author: a CI run id and result, a captured command output file, a query against real data for every external dependency touched, or a review by a *different* agent. Make the dual-agent setup the review policy: whichever agent implemented, the other reviews. Rename the agent-set status to `claimed`; reserve `verified` for user or CI evidence and record the source (`verified-by: ci:816`).

### 4.2 The MCP state file is a second source of truth that lost

**Evidence.** 30 of 34 features out of sync; one shared JSON for all features; merge conflicts in 366, 369, 370.

**Why it fails.** Skills call `advance_phase` optionally ("if MCP is configured, skip otherwise") and from inside long sessions where the call is forgotten after compaction. A persisted state that is updated by voluntary calls from a forgetful actor will drift. Deterministic *derivation* is fine; deterministic *persistence* is not.

**Direction.** Keep the MCP server, change its job: compute state from the artifacts on every call (`auto_detect_features` already does this), never persist, or persist per feature under `specs/<feature>/.state.json` and gitignore it. The server is far more valuable as an **enforcement and allocation** service: next BUG/T/BF id, bugs.md schema lint, pre-commit history guard, branch check, timestamping. Those are the things the model does badly (§5) and a script does perfectly.

### 4.3 Instruction volume exceeds what a model follows

**Evidence.** 6–10 k tokens of IF/BLOCK/HALT pseudo-code per phase, preflight re-read by all eleven skills, the workflow skill (2 400 words) loaded alongside every phase skill. Observed: the `--no-verify` rule, the "ASK the user" rule, the "date -u" rule for timestamps and the "only user verifies" rule are all routinely not followed.

**Why it fails.** Instruction-following degrades with instruction count, and after context compaction the loaded skill text is gone while the phase continues. The implement phase can run for hours; the 9 k-token procedure is read once at the start.

**Direction.** Cut each skill to a one-screen checklist (≈800 tokens) with progressive disclosure to references only when needed. Move every mechanical rule into a script or hook (§4.2). Add a ten-line "phase card" (feature, phase, allowed writes, next gate) that the MCP server returns from `get_next_actions`, designed to be re-read after compaction.

### 4.4 history.md is written for nobody

**Evidence.** 294 k words; entries of 1 600 words; timestamps that are round hours and do not match the commit times they describe (`2026-10-22T20:00:00Z` on a round committed at 15:46Z).

**Why it fails.** The template says "notes: key decisions", but a model asked to "record what was done" produces prose proportional to effort, not to information. Models also cannot know the current time; without a forced `date -u` call they invent plausible stamps.

**Direction.** Make the entry a fixed-field record (phase, artifacts, tests: command + count, commit) capped at about 60 words, appended by a script that stamps the real time. Narrative belongs in `implementation-summary.md` once, at close.

### 4.5 Append-only plans become unreadable and contradictory

**Evidence.** plan.md for 370 modified four times after implementation began; its BF-018 section describes the rejected design while history.md describes the shipped one. bugs.md grows round by round; the reader must know the rounds to know the current truth.

**Why it fails.** "Never overwrite" protects provenance but gives the model no place to state the current design, so each round appends a new partial truth. Models summarise poorly across long contradictory documents.

**Direction.** Keep append-only history but add a regenerated "Current design" section at the top of plan.md, rewritten at each close (the one phase allowed to patch plan.md). Treat bugfix-round sections as ADRs: dated, superseding earlier sections explicitly.

### 4.6 TDD dogma the model cannot honour, so it performs it

**Evidence.** "If you wrote code before the test, delete it" (Iron Law). In practice the model writes test and code in one pass and reports RED → GREEN. Feature 370 has 17 `[TEST]` tasks for 54 tasks; the RED runs are asserted, not captured.

**Why it fails.** The value of RED is proof that the test can fail. A model asserting "confirmed RED" is the same self-attestation as §4.1. The rule also produces fixtures shaped by the model's belief rather than by data (the four-row TVF).

**Direction.** Replace the Iron Law with two enforceable requirements: (a) the RED run's output is saved as a file referenced from tasks.md; (b) any test touching an external seam (database function, HTTP contract, file format) uses a fixture captured from a real probe, with the probe command recorded. Keep test-first for pure logic, allow characterisation tests for legacy code.

### 4.7 "Ask the user" in an autonomous pipeline

**Evidence.** Skills contain ASK/WAIT at ~25 points. Documents cite "the owner's ruling" for decisions whose provenance is not recorded. Autonomous runs (Hermes cron, Claude background) either stall at a WAIT or the model answers its own question and calls it a ruling.

**Why it fails.** A model has no way to distinguish a real user answer from its own continuation once the conversation is compacted or the run is unattended.

**Direction.** Add a `decisions.md` (or a section in plan.md) where every ASK that was not actually answered by a human is recorded as an **assumption** with the alternative not taken. Real rulings quote the user's words. Reviews check that file first.

### 4.8 Commit policy fights the project's own guardrails

**Evidence.** Every spec commit uses `--no-verify`; 19 document commits to 8 code commits on one feature; spec changes are required to precede code even for one-line status flips.

**Why it fails.** Bypassing hooks to make the workflow pass is a design smell, and the document-commit ratio makes `git log` useless for reading what the code did.

**Direction.** Drop `--no-verify`; fix the hooks instead. Allow one commit per phase that includes its document updates, and keep the spec-before-code rule only for changes to requirements or design intent (the reference already distinguishes these; the skills do not).

## 5. What current LLM agents cannot be trusted with, and what to do instead

| Capability the workflow assumes | Reality in 2026 models | Mechanical substitute |
|---|---|---|
| Self-verification ("tests pass", "RED confirmed", "100 % health") | Unreliable; shares blind spots with the code | CI result, captured output, cross-agent review, real-data probe |
| Knowing the time | Not available; stamps are invented | `date -u` via script, or server-side stamping |
| Following 10 k tokens of procedure across a long phase | Degrades; lost at compaction | Short checklist, phase card re-injected, hooks |
| Sequential id allocation across large files (BUG-NNN, T###) | Error-prone counting | Allocate ids in the MCP server |
| Keeping a persisted state in sync by voluntary calls | Forgotten after compaction | Derive state from files; never persist |
| Distinguishing a user answer from its own continuation | Impossible after compaction or unattended | Record assumptions explicitly; quote real rulings |
| Summarising contradictory append-only documents | Poor | Regenerated "current design" section |
| Proportionate writing | Prose scales with effort, not information | Fixed-field records with word caps |
| Reviewing its own output | Blind-spot preserving | Author/reviewer split across agents (now possible) |

## 6. Recommended order of change

1. **External oracle in Done When** (§4.1) and the `claimed`/`verified-by` status split. Highest value, smallest change: edit the Done When lists and the bugs template.
2. **MCP server becomes a derive-and-enforce service** (§4.2): no persisted state, id allocation, schema lint, history guard, timestamps. Removes the merge conflicts and the drift.
3. **Skill diet** (§4.3): one-screen checklists, phase card, references on demand. Cuts per-phase overhead by roughly 80 %.
4. **history.md as a record, not a story** (§4.4), appended by script.
5. **Current-design section and ADR-style rounds** (§4.5).
6. **TDD rules that can be checked** (§4.6): saved RED output, real-shape fixtures.
7. **Assumptions log** (§4.7) and **commit policy** (§4.8).

Items 1 and 2 address the two failures that actually cost time this month (a wrong fix that passed its gates, and a PR blocked by `state.json`). Items 3 and 4 are where most of the token and reading cost sits. The rest are hygiene.

## 7. Appendix — how the numbers were produced

```bash
# process-log volume and entry sizes
cat specs/*/history.md | wc -w
python3 - <<'EOF'
import glob,re
lens=sorted(len(e.split()) for f in glob.glob('specs/*/history.md')
            for e in re.split(r'\n(?=## )', open(f).read()))
print(len(lens), lens[len(lens)//2], lens[int(len(lens)*.9)], lens[-1])
EOF
# state.json vs artifacts
python3 -c "import json,os;d=json.load(open('specs/.spec-kit/state.json'))['features'];print(sum(((os.path.exists(f'specs/{k}/close.md') or os.path.exists(f'specs/{k}/implementation-summary.md'))!=(v.get('status')=='closed')) for k,v in d.items()),'of',len(d))"
# bug statuses and health scores
grep -h -o 'Status\*\*: [a-z-]*' specs/*/bugs.md | sort | uniq -c
grep -h -o 'health[^|]*: *[0-9]*%' specs/*/implementation-summary.md specs/*/close.md | grep -o '[0-9]*%' | sort | uniq -c
# per-phase instruction volume
wc -w ~/.hermes/skills/spec-kit-*/SKILL.md ~/.hermes/skills/spec-kit/references/{preflight,auto-commit}.md
```
