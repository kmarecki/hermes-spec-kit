#!/usr/bin/env python3
"""spec-kit MCP server — derive-and-enforce workflow service.

DESIGN (v3): the server keeps NO state of its own. Every call derives the
feature's phase and artifact status from the files under specs/<feature>/ at
that moment. A persisted state file (v2's specs/.spec-kit/state.json) proved
to be a second source of truth that drifted from the artifacts (30 of 34
features out of sync in one deployment) and collided on every merge. Files on
disk are the single source of truth; this server reads them and enforces.

What the server is for — the things an LLM agent does badly and a script does
perfectly:
  * phase derivation and prerequisite validation (advance_phase, get_feature_state)
  * sequential id allocation (next_id: BUG / T / BF)
  * artifact schema lint (lint_artifacts: bugs.md, tasks.md, history.md, spec.md ACs, acceptance.md, review-final.md)
  * the history-before-commit guard (history_guard)
  * real timestamps (timestamp)
  * a ten-line phase card to re-read after context compaction (get_next_actions)
  * the merge gate: the final review's verdict and freshness (close_feature) and a
    mechanical scan of the branch diff (diff_scan)
  * the size tier (S/M/L) read from spec.md, and ADR number allocation (next_id ADR)
  * acceptance criteria: the AC → test → result matrix from spec.md, tasks.md and JUnit/TRX
    results (acceptance_status), and the freeze of acceptance tests (acceptance_freeze)

Bug tracking stays file-based — bugs.md is the single source of truth and this
server never edits it; it only reads and lints.

Dependency: pip install "mcp<2"  (auto-installed by install.sh venv)
"""

import datetime
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from mcp.server.fastmcp import FastMCP

SPECS_DIR = Path("specs")
LEGACY_STATE_FILE = SPECS_DIR / ".spec-kit" / "state.json"

PHASES = {
    0: {"name": "constitution", "artifacts": ["constitution.md"]},
    1: {"name": "specify",      "artifacts": ["spec.md"]},
    2: {"name": "plan",         "artifacts": ["plan.md"]},
    3: {"name": "tasks",        "artifacts": ["tasks.md"]},
    4: {"name": "implement",    "artifacts": []},
    5: {"name": "test",         "artifacts": ["bugs.md"]},
    6: {"name": "close",        "artifacts": ["close.md"]},
}

# Artifact required ON DISK before a feature may stand in the given phase.
PREREQUISITES = {
    2: ["spec.md"],
    3: ["spec.md", "plan.md"],
    4: ["spec.md", "plan.md", "tasks.md"],
    5: ["tasks.md"],
    6: ["tasks.md"],
}

CLOSE_DOCS = ("close.md", "implementation-summary.md")
FINAL_REVIEW = "review-final.md"
ACCEPTANCE = "acceptance.md"
FREEZE_FILE = "evidence/acceptance-freeze.json"
AC_LEVELS = ("unit", "integration", "component", "e2e", "command", "probe", "manual")
AC_TEST_LEVELS = ("unit", "integration", "component", "e2e")   # proven by a test result file
AC_REASON_LEVELS = ("e2e", "manual")                           # need a written reason in spec.md
TRACKED_ARTIFACTS = [
    "spec.md", "clarify.md", "plan.md", "research.md", "data-model.md",
    "quickstart.md", "tasks.md", "bugs.md", "decisions.md", "history.md",
    ACCEPTANCE, FINAL_REVIEW, "close.md", "implementation-summary.md", "change-record.md",
]
SIZES = ("S", "M", "L")
VERDICTS = ("READY", "READY-WITH-FOLLOWUPS", "AWAITING-OWNER", "NOT READY")
PASSING_VERDICTS = ("READY", "READY-WITH-FOLLOWUPS")
ADR_DIR_CANDIDATES = ("docs/adr", "docs/decisions", "doc/adr", "adr", "docs/architecture/decisions")

BUG_STATUSES = {"open", "in-progress", "claimed", "verified", "superseded"}
LEGACY_BUG_STATUSES = {"resolved": "claimed", "fixed": "claimed"}
VERIFIED_BY_RE = re.compile(r"^(user|ci:\S+|review:\S+)$")

_BUG_HEADER_RE = re.compile(r"^### (BUG-(\d+)):", re.M)
# "- [X] T001 …" (template) and "- T001 [X] …" (id first) are both task lines.
_TASK_RE = re.compile(r"^- (?:\[(?P<pre>[ xX])\] )?(?P<id>(?:T|BF-?)(?P<num>\d+))\b(?: \[(?P<post>[ xX])\])?", re.M)
_HISTORY_ENTRY_RE = re.compile(r"^## \[?([0-9T:\-+.Z]+)\]? *\| *(.*)$", re.M)
_SIZE_RE = re.compile(r"^\*\*Size\*\*:\s*\[?([SML])\b", re.M)
_ROUND_RE = re.compile(r"^## Round (\d+)\b[^\n]*$", re.M)
_VERDICT_RE = re.compile(r"\*\*Verdict\*\*:\s*(READY-WITH-FOLLOWUPS|AWAITING-OWNER|NOT READY|READY)\b")
_REVIEWED_COMMIT_RE = re.compile(r"\*\*Reviewed-commit\*\*:\s*([0-9a-f]{7,40})\b")
# spec.md: "- **AC-003** (FR-002) Given … When … Then … — Verify: integration"
_AC_LINE_RE = re.compile(r"^.*\*\*AC-(\d{3})\*\*.*$", re.M)
_AC_VERIFY_RE = re.compile(r"Verify:\s*`?([a-z0-9]+)`?(?:\s*\(([^)]*)\))?", re.I)
# a test name carries the AC id: "AC-003 …", "AC003_…", "test_ac003_…"
_AC_IN_NAME_RE = re.compile(r"(?<![A-Za-z0-9])AC[-_]?(\d{3})(?!\d)", re.I)
_AC_TAG_RE = re.compile(r"\[AC-(\d{3})\]")
_ACC_RESULT_RE = re.compile(r"\*\*Result\*\*:\s*(PASS|FAIL|STOPPED)\b")
_ACC_COMMIT_RE = re.compile(r"\*\*Commit\*\*:\s*([0-9a-f]{7,40})\b")
_PATH_TOKEN_RE = re.compile(r"[\w@.\-/]+/[\w@.\-]+\.[A-Za-z0-9]{1,6}")


# ── Derivation ─────────────────────────────────────────────────────────────


def _now():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()


def _feature_dir(feature):
    return SPECS_DIR / feature


def _parse_bugs(text):
    """Return list of {id, num, status, raw_status, verified_by} from bugs.md text."""
    bugs = []
    headers = list(_BUG_HEADER_RE.finditer(text))
    for i, m in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        body = text[m.end():end]
        # the Summary table may follow the last bug — cut at the separator
        body = body.split("\n---", 1)[0]
        sm = re.search(r"\*\*Status\*\*:\s*([A-Za-z-]*)", body)
        raw = (sm.group(1).strip().lower() if sm else "")
        status = LEGACY_BUG_STATUSES.get(raw, raw)
        vm = re.search(r"\*\*Verified-by\*\*:\s*([^\n]*)", body)
        verified_by = vm.group(1).strip() if vm else ""
        if verified_by.startswith("[") or verified_by in ("", "—", "-"):
            verified_by = ""
        bugs.append({"id": m.group(1), "num": int(m.group(2)), "status": status,
                     "raw_status": raw, "verified_by": verified_by})
    return bugs


def _task_mark(m):
    """The checkbox of a _TASK_RE match ('x', 'X', ' '), or None when the line has none."""
    return m.group("pre") if m.group("pre") is not None else m.group("post")


def _parse_tasks(text):
    tasks = []
    for m in _TASK_RE.finditer(text):
        mark = _task_mark(m)
        if mark is None:
            continue
        tasks.append({"id": m.group("id"), "done": mark in "xX",
                      "kind": "BF" if m.group("id").startswith("BF") else "T",
                      "num": int(m.group("num"))})
    return tasks


def _git(*args):
    """Run git in the project root; (returncode, stdout). (-1, '') when git is unavailable."""
    try:
        r = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
        return r.returncode, r.stdout
    except OSError:
        return -1, ""


def _conventions():
    """key: value pairs from specs/git-conventions.md (branch_source, adr_dir, …). Empty when absent."""
    f = SPECS_DIR / "git-conventions.md"
    if not f.exists():
        return {}
    pairs = re.findall(r"^\s*([a-z_]+):\s*([^\s#]+)", f.read_text(errors="replace"), re.M)
    found = {}
    for k, v in pairs:  # first occurrence wins — the template's "Examples" block repeats keys
        found.setdefault(k, v)
    return found


def _adr_dir():
    """The project's ADR directory: git-conventions `adr_dir`, else the first existing candidate."""
    configured = _conventions().get("adr_dir")
    if configured:
        return Path(configured)
    for c in ADR_DIR_CANDIDATES:
        if Path(c).is_dir():
            return Path(c)
    return None


def _parse_size(fd):
    """S | M | L from the spec.md header line `**Size**: X`; None when absent (legacy specs = M)."""
    spec = fd / "spec.md"
    if not spec.exists():
        return None
    m = _SIZE_RE.search(spec.read_text(errors="replace"))
    return m.group(1) if m else None


def _code_changed_since(commit):
    """True when a commit after `commit` touches code outside specs/ (or `commit` is unknown);
    None outside a git repository."""
    if _git("rev-parse", "--git-dir")[0] != 0:
        return None
    rc, out = _git("log", "--format=%h", f"{commit}..HEAD", "--", ".", ":(exclude)specs")
    if rc == 0:
        return bool(out.strip())
    return True  # the commit is gone (rebased/amended) — it no longer names this code


def _parse_acs(fd):
    """Acceptance criteria from spec.md: [{id, num, frs, level, reason}] in file order."""
    spec = fd / "spec.md"
    if not spec.exists():
        return []
    acs = []
    for m in _AC_LINE_RE.finditer(spec.read_text(errors="replace")):
        line = m.group(0)
        vm = _AC_VERIFY_RE.search(line)
        acs.append({"id": f"AC-{m.group(1)}", "num": int(m.group(1)),
                    "frs": sorted(set(re.findall(r"FR-\d{3}", line))),
                    "level": vm.group(1).lower() if vm else None,
                    "reason": (vm.group(2) or "").strip() if vm else ""})
    return acs


def _ac_test_tasks(fd):
    """{AC id: [task line, …]} for tasks.md lines carrying [TEST] and [AC-###]."""
    tasks = fd / "tasks.md"
    found = {}
    if not tasks.exists():
        return found
    for line in tasks.read_text(errors="replace").splitlines():
        if "[TEST]" in line:
            for n in _AC_TAG_RE.findall(line):
                found.setdefault(f"AC-{n}", []).append(line)
    return found


def _parse_results(paths):
    """Test cases from JUnit XML and TRX files: [{name, outcome: pass|fail|skip, file}]."""
    cases = []
    for path in paths:
        try:
            root = ET.parse(path).getroot()
        except (ET.ParseError, OSError):
            continue
        for el in root.iter():
            tag = el.tag.rsplit("}", 1)[-1]
            if tag == "testcase":                                 # JUnit (Vitest, Cypress, jest, pytest)
                name = " ".join(filter(None, [el.get("classname"), el.get("name")]))
                kids = {c.tag.rsplit("}", 1)[-1] for c in el}
                outcome = "fail" if kids & {"failure", "error"} else "skip" if "skipped" in kids else "pass"
                cases.append({"name": name, "outcome": outcome, "file": str(path)})
            elif tag == "UnitTestResult":                         # TRX (dotnet test --logger trx)
                o = (el.get("outcome") or "").lower()
                outcome = "pass" if o == "passed" else "fail" if o in ("failed", "error", "timeout", "aborted") else "skip"
                cases.append({"name": el.get("testName") or "", "outcome": outcome, "file": str(path)})
    return cases


def _freeze(fd):
    f = fd / FREEZE_FILE
    if not f.exists():
        return None
    try:
        return json.loads(f.read_text())
    except json.JSONDecodeError:
        return None


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _frozen_changed(fd):
    """Frozen acceptance-test files whose content differs from the freeze (or that vanished)."""
    fr = _freeze(fd)
    if not fr:
        return []
    changed = []
    for path, digest in fr.get("files", {}).items():
        if not Path(path).exists() or _sha(path) != digest:
            changed.append(path)
    return changed


def _acceptance_round(fd):
    """The latest round of acceptance.md: result, commit, staleness."""
    f = fd / ACCEPTANCE
    if not f.exists():
        return {"present": False, "rounds": 0, "result": None, "commit": None, "stale": None}
    text = f.read_text(errors="replace")
    rounds = list(_ROUND_RE.finditer(text))
    last = text[rounds[-1].start():] if rounds else text
    rm, cm = _ACC_RESULT_RE.search(last), _ACC_COMMIT_RE.search(last)
    commit = cm.group(1) if cm else None
    return {"present": True, "rounds": len(rounds), "result": rm.group(1) if rm else None,
            "commit": commit, "stale": _code_changed_since(commit) if commit else None}


def _acceptance_problem(fd):
    """Why acceptance does not open the gate; None when it does or the spec has no ACs."""
    if not _parse_acs(fd):
        return None
    ar = _acceptance_round(fd)
    if not ar["present"]:
        return f"no {ACCEPTANCE} — run the acceptance loop ('accept [feature]') first"
    if ar["result"] != "PASS":
        return f"{ACCEPTANCE}: latest round is {ar['result'] or 'without a **Result**'} — every automated AC must pass"
    if ar["commit"] is None:
        return f"{ACCEPTANCE}: latest round has no '**Commit**:' sha"
    if ar["stale"]:
        return f"{ACCEPTANCE}: code changed after the passing round's commit {ar['commit']} — re-run 'accept [feature]'"
    return None


def _final_review(fd):
    """The latest round of review-final.md: verdict, reviewed commit, and whether code changed since."""
    f = fd / FINAL_REVIEW
    if not f.exists():
        return {"present": False, "rounds": 0, "verdict": None, "reviewed_commit": None, "stale": None}
    text = f.read_text(errors="replace")
    rounds = list(_ROUND_RE.finditer(text))
    last = text[rounds[-1].start():] if rounds else text
    vm = _VERDICT_RE.search(last)
    cm = _REVIEWED_COMMIT_RE.search(last)
    commit = cm.group(1) if cm else None
    stale = _code_changed_since(commit) if commit else None
    return {"present": True, "rounds": len(rounds), "verdict": vm.group(1) if vm else None,
            "reviewed_commit": commit, "stale": stale}


def _final_review_problem(fr):
    """Why the final review does not open the merge gate; None when it does."""
    if not fr["present"]:
        return f"no {FINAL_REVIEW} — run the final review (spec-kit-review, final mode) first"
    if fr["verdict"] is None:
        return f"{FINAL_REVIEW}: latest round has no '**Verdict**:' line"
    if fr["verdict"] == "AWAITING-OWNER":
        return f"{FINAL_REVIEW}: latest verdict is AWAITING-OWNER — get the owner's answers and append a specs-only Round N+1"
    if fr["verdict"] not in PASSING_VERDICTS:
        return f"{FINAL_REVIEW}: latest verdict is {fr['verdict']} — fix the findings (bugfix loop) and re-review"
    if fr["reviewed_commit"] is None:
        return f"{FINAL_REVIEW}: latest round has no '**Reviewed-commit**:' sha"
    if fr["stale"]:
        return f"{FINAL_REVIEW}: code changed after the reviewed commit {fr['reviewed_commit']} — re-run the final review"
    return None


def _derive(feature):
    """Derive the feature's state from its files. None when the directory is absent."""
    fd = _feature_dir(feature)
    if not fd.is_dir():
        return None
    present = {a for a in TRACKED_ARTIFACTS if (fd / a).exists()}
    contracts = sorted(p.name for p in (fd / "contracts").glob("*")) if (fd / "contracts").is_dir() else []

    bugs = _parse_bugs((fd / "bugs.md").read_text(errors="replace")) if "bugs.md" in present else []
    tasks = _parse_tasks((fd / "tasks.md").read_text(errors="replace")) if "tasks.md" in present else []
    open_bugs = [b for b in bugs if b["status"] in ("open", "in-progress")]
    claimed = [b for b in bugs if b["status"] == "claimed"]
    closed_on_disk = any(c in present for c in CLOSE_DOCS)
    size = _parse_size(fd)

    if not {"spec.md"} <= present:
        phase, status = 1, "new"
    elif "plan.md" not in present:
        phase, status = 2, "active"
    elif "tasks.md" not in present:
        phase, status = 3, "active"
    elif closed_on_disk:
        if open_bugs:
            phase, status = 5, "reopened"
        else:
            phase, status = 6, "closed"
    elif tasks and all(t["done"] for t in tasks) or "bugs.md" in present:
        phase, status = 5, "active"
    else:
        phase, status = 4, "active"

    return {
        "feature": feature,
        "current_phase": phase,
        "phase_name": PHASES[phase]["name"],
        "status": status,
        "artifacts": {a: ("present" if a in present else "absent") for a in TRACKED_ARTIFACTS},
        "contracts": contracts,
        "size": size or "M",
        "size_declared": size is not None,
        "final_review": _final_review(fd) if phase >= 5 else None,
        "acceptance": ({"criteria": len(acs), "round": _acceptance_round(fd) if phase >= 5 else None}
                       if (acs := _parse_acs(fd)) else None),
        "tasks": {"total": len(tasks), "done": sum(t["done"] for t in tasks),
                  "bugfix": sum(t["kind"] == "BF" for t in tasks)},
        "bugs": {"total": len(bugs), "open": len(open_bugs), "claimed": len(claimed),
                 "verified": sum(b["status"] == "verified" for b in bugs),
                 "superseded": sum(b["status"] == "superseded" for b in bugs)},
        "derived_at": _now(),
    }


def _phase_card(state):
    """Ten lines to re-read after context compaction."""
    f = state["feature"]
    phase = state["current_phase"]
    allowed = {
        1: "spec.md only — no code",
        2: "plan.md, research.md, data-model.md, contracts/*, quickstart.md — no code",
        3: "tasks.md only — no code",
        4: "source code, tasks.md [X] marks, bugs.md status→claimed with Evidence",
        5: "bugs.md only — log before fix; verified needs an oracle",
        6: "close.md + change-record.md, plan.md Current Design, spec/plan deviation patches, ADRs, AGENTS.md",
    }[phase]
    gate = {
        1: "spec.md written → commit spec(phase-1)",
        2: "plan artifacts written → commit spec(phase-2)",
        3: "tasks.md written, TDD question asked → commit spec(phase-3)",
        4: "phase RED/GREEN evidence saved, probes per [SEAM], tasks [X], history entry with Implemented-by → one commit per phase; then accept",
        5: f"{state['bugs']['open']} open, {state['bugs']['claimed']} claimed-unverified → verify with user/ci/other-agent or run 'bugfix {f}'; then the final review ({FINAL_REVIEW}) must say READY",
        6: "final review READY and fresh, every bug verified/superseded, close.md (Architecture Decisions) + change-record.md → one commit spec(phase-6)",
    }[phase]
    fr = state.get("final_review") or {}
    review_line = (f"final review: {fr.get('verdict') or 'missing verdict'} @ {fr.get('reviewed_commit') or '?'}"
                   f"{' — STALE, re-review' if fr.get('stale') else ''}" if fr.get("present")
                   else "final review: not run" if phase >= 5 else None)
    acc = state.get("acceptance") or {}
    if acc.get("round"):
        r = acc["round"]
        acc_line = (f"acceptance: {acc['criteria']} ACs · round {r['rounds']} {r['result'] or '?'} @ {r['commit'] or '?'}"
                    f"{' — STALE, re-run accept' if r['stale'] else ''}" if r["present"]
                    else f"acceptance: {acc['criteria']} ACs · not run — 'accept {f}' before the final review")
    else:
        acc_line = None
    lines = [
        f"PHASE CARD — {f}",
        f"phase: {phase} ({state['phase_name']})  status: {state['status']}  size: {state['size']}{'' if state['size_declared'] else ' (undeclared — treated as M)'}",
        f"allowed writes: {allowed}",
        f"next gate: {gate}",
        f"tasks: {state['tasks']['done']}/{state['tasks']['total']} done ({state['tasks']['bugfix']} BF)",
        f"bugs: {state['bugs']['open']} open · {state['bugs']['claimed']} claimed · {state['bugs']['verified']} verified",
        "rules: history entry BEFORE commit · additive-only · evidence before claims (evidence.md)",
        acc_line or "ids: call next_id before adding a BUG/T/BF · lint_artifacts before every commit",
        review_line or "ask: an ASK you cannot put to a human is an ASSUMPTION — record it in decisions.md",
        f"derived from files at {state['derived_at']} — the files are the truth, not this card",
    ]
    return "\n".join(lines)


def _json(obj):
    return json.dumps(obj, ensure_ascii=False)


def _not_found(feature):
    available = sorted(d.name for d in SPECS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")) if SPECS_DIR.is_dir() else []
    return _json({"error": f"Feature '{feature}' not found", "available_features": available})


mcp = FastMCP("spec-kit-workflow")


# ── Project-level tools ────────────────────────────────────────────────────


@mcp.tool(name="project_status")
def project_status() -> str:
    """Project-level status derived from files: constitution present?, feature count,
    whether a legacy specs/.spec-kit/state.json still exists (it is ignored — delete it).
    """
    features = sorted(d.name for d in SPECS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")) if SPECS_DIR.is_dir() else []
    return _json({
        "version": 3,
        "constitution": "present" if (SPECS_DIR / "constitution.md").exists() else "absent",
        "git_conventions": "present" if (SPECS_DIR / "git-conventions.md").exists() else "absent",
        "merge_checklist": "present" if (SPECS_DIR / "merge-checklist.md").exists() else "absent",
        "adr_dir": str(_adr_dir()) if _adr_dir() else None,
        "features": len(features),
        "legacy_state_file": LEGACY_STATE_FILE.exists(),
        "note": "state is derived from files on every call; nothing is persisted by this server",
    })


@mcp.tool(name="project_set_constitution")
def project_set_constitution(status: str = "present", principles: str = "") -> str:
    """Confirm the constitution after writing it. Nothing is stored: the call checks that
    specs/constitution.md exists (status 'present') or does not ('absent') and reports.

    Args:
        status: 'present' or 'absent' — must match the file on disk
        principles: Optional JSON object of parsed principles (validated, echoed back)
    """
    exists = (SPECS_DIR / "constitution.md").exists()
    actual = "present" if exists else "absent"
    parsed = {}
    if principles:
        try:
            parsed = json.loads(principles)
        except json.JSONDecodeError:
            return _json({"error": "principles must be valid JSON object", "constitution": actual})
    if status != actual:
        return _json({"error": f"specs/constitution.md is {actual} on disk, not '{status}' — write the file first", "constitution": actual})
    return _json({"success": True, "constitution": actual, "principles": parsed})


# ── Feature tools ──────────────────────────────────────────────────────────


@mcp.tool(name="init_feature")
def init_feature(feature: str, name: str = None, mode: str = "specify") -> str:
    """Create specs/<feature>/ with a history.md header. Fails if the directory exists.

    Args:
        feature: Feature ID (e.g., 003-user-auth)
        name: Human-readable name (defaults to feature ID)
        mode: specify, bugfix, or reopen (recorded in the history header only)
    """
    fd = _feature_dir(feature)
    if fd.exists():
        return _json({"error": f"Feature '{feature}' already exists", "state": _derive(feature)})
    fd.mkdir(parents=True)
    (fd / "history.md").write_text(f"# Process History: {name or feature}\n\n> mode: {mode} · created {_now()}\n")
    return _json({"success": True, "state": _derive(feature)})


@mcp.tool(name="get_feature_state")
def get_feature_state(feature: str) -> str:
    """Derive the feature's phase, status, artifacts, task and bug counts from its files.

    Args:
        feature: Feature ID
    """
    state = _derive(feature)
    if state is None:
        return _not_found(feature)
    return _json({"state": state, "phase_card": _phase_card(state)})


@mcp.tool(name="get_next_actions")
def get_next_actions(feature: str) -> str:
    """Available actions from the derived phase, plus the ten-line PHASE CARD. Call this
    after context compaction and before any write.

    Args:
        feature: Feature ID
    """
    state = _derive(feature)
    if state is None:
        return _not_found(feature)
    phase, status = state["current_phase"], state["status"]
    actions = []
    if status == "closed":
        actions.append({"action": "reopen_feature", "description": "Reopen for bugfixing (log bugs via spec-kit-test first)"})
    elif phase < 6:
        nxt = phase + 1
        ok, reason = _validate_phase(state, nxt)
        a = {"action": f"advance_to_{PHASES[nxt]['name']}", "phase": nxt,
             "description": f"Advance to phase {nxt} ({PHASES[nxt]['name']})"}
        if not ok:
            a.update({"blocked": True, "reason": reason})
        actions.append(a)
    if state["bugs"]["open"]:
        actions.append({"action": "bugfix", "description": f"'bugfix {feature}' — {state['bugs']['open']} open bug(s)"})
    if state["bugs"]["claimed"]:
        actions.append({"action": "verify", "description": f"{state['bugs']['claimed']} claimed bug(s) need an oracle (user / ci / review:<other-agent>)"})
    acc_problem = _acceptance_problem(_feature_dir(feature)) if phase == 5 else None
    if acc_problem:
        actions.append({"action": "accept", "description": f"Run the acceptance loop — {acc_problem}"})
    if phase == 5 and not state["bugs"]["open"] and not acc_problem:
        problem = _final_review_problem(state["final_review"])
        if problem:
            actions.append({"action": "final_review", "description": f"Run the final (merge-readiness) review — {problem}"})
    if phase == 6 and status != "closed":
        actions.append({"action": "close_feature", "description": "Write close.md / implementation-summary.md"})
    return _json({"current_phase": phase, "phase_name": state["phase_name"], "status": status,
                  "available_actions": actions, "phase_card": _phase_card(state)})


def _validate_phase(state, to_phase):
    fd = _feature_dir(state["feature"])
    for art in PREREQUISITES.get(to_phase, []):
        if not (fd / art).exists():
            return False, f"Prerequisite not met: {art} must exist"
    if to_phase == 6:
        bugs_file = fd / "bugs.md"
        if bugs_file.exists():
            bugs = _parse_bugs(bugs_file.read_text(errors="replace"))
            blocking = [b["id"] for b in bugs if b["status"] in ("open", "in-progress")]
            if blocking:
                return False, f"Prerequisite not met: open bugs {blocking} — run bugfix first"
        problem = _acceptance_problem(fd) or _final_review_problem(_final_review(fd))
        if problem:
            return False, f"Prerequisite not met: {problem}"
    return True, None


@mcp.tool(name="advance_phase")
def advance_phase(feature: str, from_phase: int, artifacts_created: list[str] = None) -> str:
    """Validate that the feature may leave `from_phase`: the derived phase must be
    from_phase (or already from_phase + 1, since the artifacts were just written) and
    every artifact named in artifacts_created plus the next phase's prerequisites must
    exist on disk. Nothing is written — the artifacts ARE the state.

    Args:
        feature: Feature ID
        from_phase: The phase the skill believes it is completing
        artifacts_created: Artifact files the skill wrote (verified to exist)
    """
    artifacts_created = artifacts_created or []
    state = _derive(feature)
    if state is None:
        return _not_found(feature)
    if from_phase == 0:
        return _json({"error": "Phase 0 (constitution) is project-level — use project_set_constitution"})
    if state["status"] == "closed":
        return _json({"error": f"Feature '{feature}' is closed — use reopen"})
    # The skill calls this AFTER writing its artifacts, so the files may already
    # place the feature in from_phase + 1. Anything else is a mismatch.
    if state["current_phase"] not in (from_phase, from_phase + 1):
        return _json({"error": f"Phase mismatch: expected {from_phase}, derived phase is {state['current_phase']} ({state['phase_name']}) from the files on disk"})
    fd = _feature_dir(feature)
    missing = [a for a in artifacts_created if not (fd / a).exists()]
    if missing:
        return _json({"error": f"artifacts_created not on disk: {missing} — write the file before syncing"})
    to_phase = from_phase + 1
    ok, reason = _validate_phase(state, to_phase)
    if not ok:
        return _json({"error": reason})
    # Re-derive: the written artifacts may already move the feature forward.
    after = _derive(feature)
    return _json({"success": True, "from_phase": from_phase, "to_phase": to_phase,
                  "phase_name": PHASES[to_phase]["name"], "artifacts_verified": artifacts_created,
                  "state": after, "phase_card": _phase_card(after)})


@mcp.tool(name="list_features")
def list_features() -> str:
    """List every specs/<feature>/ directory with derived phase, status and bug counts."""
    if not SPECS_DIR.is_dir():
        return _json({"error": "specs/ directory not found"})
    result = []
    for d in sorted(SPECS_DIR.iterdir()):
        if d.is_dir() and not d.name.startswith("."):
            s = _derive(d.name)
            result.append({"feature": d.name, "phase": s["current_phase"], "phase_name": s["phase_name"],
                           "status": s["status"], "open_bugs": s["bugs"]["open"], "claimed_bugs": s["bugs"]["claimed"]})
    return _json({"features": result})


@mcp.tool(name="reopen_feature")
def reopen_feature(feature: str) -> str:
    """Check that a feature can be reopened (it must be closed on disk) and return the
    reopen branch pattern. Reopening is materialised by logging an open bug in bugs.md
    via spec-kit-test — this call writes nothing.

    Args:
        feature: Feature ID
    """
    state = _derive(feature)
    if state is None:
        return _not_found(feature)
    if state["status"] not in ("closed", "reopened"):
        return _json({"error": f"Feature '{feature}' is not closed (status: {state['status']})"})
    return _json({"success": True, "feature": feature, "status": state["status"],
                  "next": "Log the bug(s) in bugs.md via spec-kit-test (Status: open), then run 'bugfix [feature]'",
                  "branch_hint": "{original_prefix}/" + feature + "{reopen_suffix}"})


@mcp.tool(name="close_feature")
def close_feature(feature: str) -> str:
    """Validate the close: a close document exists with an `## Architecture Decisions`
    section and change-record.md is present, the latest acceptance round PASSes on the current code (when spec.md has ACs), the final review's latest verdict is READY / READY-WITH-FOLLOWUPS and no code
    changed after its reviewed commit, no bug is open/in-progress, and every verified bug
    carries a Verified-by oracle. Reports claimed-unverified bugs. Writes nothing.

    Args:
        feature: Feature ID
    """
    state = _derive(feature)
    if state is None:
        return _not_found(feature)
    fd = _feature_dir(feature)
    if not any((fd / c).exists() for c in CLOSE_DOCS):
        return _json({"error": f"Feature '{feature}' has no close.md / implementation-summary.md — write it first (phase {state['current_phase']})"})
    problems = []
    unverified = []
    close_text = "".join((fd / c).read_text(errors="replace") for c in CLOSE_DOCS if (fd / c).exists())
    if "## Architecture Decisions" not in close_text:
        problems.append("close document has no '## Architecture Decisions' section (write 'none met the ADR bar' if so)")
    if not (fd / "change-record.md").exists():
        problems.append("change-record.md missing — the auditor's page (change-record-template.md)")
    for problem in (_acceptance_problem(fd), _final_review_problem(_final_review(fd))):
        if problem:
            problems.append(problem)
    if (fd / "bugs.md").exists():
        for b in _parse_bugs((fd / "bugs.md").read_text(errors="replace")):
            if b["status"] in ("open", "in-progress"):
                problems.append(f"{b['id']} is {b['status']}")
            elif b["status"] == "claimed":
                unverified.append(b["id"])
            elif b["status"] == "verified" and not VERIFIED_BY_RE.match(b["verified_by"]):
                problems.append(f"{b['id']} is verified without a Verified-by oracle")
    if problems:
        return _json({"error": "Cannot close: " + "; ".join(problems)})
    return _json({"success": True, "feature": feature, "status": "closed",
                  "claimed_unverified": unverified,
                  "note": "list claimed_unverified bugs in the close document" if unverified else "all bugs verified or superseded"})


@mcp.tool(name="update_artifact")
def update_artifact(feature: str, artifact: str, status: str = "present") -> str:
    """Confirm an artifact's status against disk after writing it. 'present'/'verified'
    require the file to exist; 'absent' requires it not to. Nothing is stored.

    Args:
        feature: Feature ID
        artifact: Artifact filename (e.g., spec.md, plan.md)
        status: present, absent, or verified
    """
    state = _derive(feature)
    if state is None:
        return _not_found(feature)
    exists = (_feature_dir(feature) / artifact).exists()
    if status in ("present", "verified") and not exists:
        return _json({"error": f"{artifact} is not on disk — write it before syncing"})
    if status == "absent" and exists:
        return _json({"error": f"{artifact} exists on disk — it is not absent"})
    return _json({"success": True, "feature": feature, "artifact": artifact, "status": status})


@mcp.tool(name="auto_detect_features")
def auto_detect_features(feature: str = None) -> str:
    """Scan specs/ and report every feature's derived state. Also reports whether a legacy
    specs/.spec-kit/state.json is present (ignored; delete it and gitignore the directory).

    Args:
        feature: Optional feature ID to scan (scans all if omitted)
    """
    if not SPECS_DIR.is_dir():
        return _json({"error": "specs/ directory not found"})
    found = {}
    for d in sorted(SPECS_DIR.iterdir()):
        if d.is_dir() and not d.name.startswith(".") and (feature is None or d.name == feature):
            found[d.name] = _derive(d.name)
    return _json({
        "success": True,
        "features_detected": len(found),
        "features": list(found.keys()),
        "states": found,
        "project": {"constitution": "present" if (SPECS_DIR / "constitution.md").exists() else "absent"},
        "legacy_state_file": LEGACY_STATE_FILE.exists(),
    })


# ── Enforcement tools ──────────────────────────────────────────────────────


@mcp.tool(name="next_id")
def next_id(feature: str, kind: str) -> str:
    """Allocate the next sequential id by scanning the files: kind 'BUG' (bugs.md),
    'T' (tasks.md T###) or 'BF' (tasks.md BF-###). Call before adding an entry.

    Args:
        feature: Feature ID
        kind: BUG | T | BF | AC | ADR (ADR scans the project's ADR directory, not the feature)
    """
    state = _derive(feature)
    if state is None:
        return _not_found(feature)
    fd = _feature_dir(feature)
    kind = kind.upper()
    if kind == "BUG":
        nums = [b["num"] for b in _parse_bugs((fd / "bugs.md").read_text(errors="replace"))] if (fd / "bugs.md").exists() else []
        fmt = "BUG-{:03d}"
    elif kind == "AC":
        nums = [a["num"] for a in _parse_acs(fd)]
        fmt = "AC-{:03d}"
    elif kind == "ADR":
        adr_dir = _adr_dir()
        if adr_dir is None:
            return _json({"error": f"no ADR directory — set adr_dir in specs/git-conventions.md or create one of {list(ADR_DIR_CANDIDATES)}"})
        nums = [int(m.group(1)) for p in adr_dir.glob("*.md") for m in [re.match(r"(\d{3,4})-", p.name)] if m]
        n = (max(nums) + 1) if nums else 1
        return _json({"success": True, "kind": kind, "next_id": f"{n:04d}", "adr_dir": str(adr_dir), "existing": len(nums)})
    elif kind in ("T", "BF"):
        tasks = _parse_tasks((fd / "tasks.md").read_text(errors="replace")) if (fd / "tasks.md").exists() else []
        nums = [t["num"] for t in tasks if t["kind"] == kind]
        fmt = "T{:03d}" if kind == "T" else "BF-{:03d}"
    else:
        return _json({"error": "kind must be BUG, T, BF, AC or ADR"})
    n = (max(nums) + 1) if nums else 1
    return _json({"success": True, "kind": kind, "next_id": fmt.format(n), "existing": len(nums)})


@mcp.tool(name="lint_artifacts")
def lint_artifacts(feature: str) -> str:
    """Lint bugs.md, tasks.md, history.md, spec.md ACs, acceptance.md and review-final.md
    against the spec-kit schema: status vocabulary, Verified-by on verified bugs, Evidence on claimed bugs,
    ascending ids, summary-table counts, probes per [SEAM], RED files per done [TEST],
    round headers, history header present. Returns findings; call before every commit.

    Args:
        feature: Feature ID
    """
    state = _derive(feature)
    if state is None:
        return _not_found(feature)
    fd = _feature_dir(feature)
    findings = []

    if (fd / "bugs.md").exists():
        text = (fd / "bugs.md").read_text(errors="replace")
        bugs = _parse_bugs(text)
        nums = [b["num"] for b in bugs]
        if nums != sorted(nums) or len(set(nums)) != len(nums):
            findings.append({"file": "bugs.md", "severity": "error", "msg": f"BUG ids not strictly ascending: {nums}"})
        for b in bugs:
            if b["raw_status"] not in BUG_STATUSES:
                sev = "warning" if b["raw_status"] in LEGACY_BUG_STATUSES else "error"
                findings.append({"file": "bugs.md", "severity": sev, "msg": f"{b['id']}: status '{b['raw_status'] or '(empty)'}' not in {sorted(BUG_STATUSES)}"})
            if b["status"] == "verified" and not VERIFIED_BY_RE.match(b["verified_by"]):
                findings.append({"file": "bugs.md", "severity": "error", "msg": f"{b['id']}: verified without Verified-by (user | ci:<id> | review:<agent>)"})
            if b["status"] == "claimed":
                blk = text.split(f"### {b['id']}:", 1)[1].split("\n### ", 1)[0]
                if not re.search(r"\*\*Evidence\*\*:\s*(?!\[)(output:|probe:)", blk):
                    findings.append({"file": "bugs.md", "severity": "warning", "msg": f"{b['id']}: claimed without Evidence (output:/probe:)"})
        if "## Summary" in text:
            summary = text.split("## Summary", 1)[1]
            rows = set(re.findall(r"^\| (BUG-\d+) ", summary, re.M))
            missing = [b["id"] for b in bugs if b["id"] not in rows]
            if missing:
                findings.append({"file": "bugs.md", "severity": "error", "msg": f"Summary table missing rows for {missing}"})
            tm = re.search(r"\*\*Total Bugs\*\*:\s*(\d+)", summary)
            if tm and int(tm.group(1)) != len(bugs):
                findings.append({"file": "bugs.md", "severity": "error", "msg": f"Total Bugs says {tm.group(1)}, found {len(bugs)}"})

    if (fd / "tasks.md").exists():
        tasks_text = (fd / "tasks.md").read_text(errors="replace")
        tasks = _parse_tasks(tasks_text)
        evidence = [p.name for p in (fd / "evidence").glob("*")] if (fd / "evidence").is_dir() else []
        for line in tasks_text.splitlines():
            m = _TASK_RE.match(line)
            if not m or (_task_mark(m) or " ") not in "xX":
                continue
            tid = m.group("id")
            if "[SEAM]" in line and not any(e.startswith(f"{tid}-probe") for e in evidence):
                findings.append({"file": "tasks.md", "severity": "warning", "msg": f"{tid} [SEAM] marked done without evidence/{tid}-probe-*.txt"})
            if "[TEST]" in line and not any("-red" in e for e in evidence):
                findings.append({"file": "tasks.md", "severity": "warning", "msg": f"{tid} [TEST] marked done but no *-red* file in evidence/"})
        for kind in ("T", "BF"):
            nums = [t["num"] for t in tasks if t["kind"] == kind]
            if nums != sorted(nums):
                findings.append({"file": "tasks.md", "severity": "error", "msg": f"{kind} ids not ascending: {nums}"})
            dup = {n for n in nums if nums.count(n) > 1}
            if dup:
                findings.append({"file": "tasks.md", "severity": "error", "msg": f"duplicate {kind} ids: {sorted(dup)}"})

    if (fd / "plan.md").exists() and any((fd / c).exists() for c in CLOSE_DOCS):
        if "## Current Design" not in (fd / "plan.md").read_text(errors="replace"):
            findings.append({"file": "plan.md", "severity": "warning", "msg": "closed feature without a '## Current Design' section — regenerate it at close"})

    if (fd / FINAL_REVIEW).exists():
        text = (fd / FINAL_REVIEW).read_text(errors="replace")
        rounds = list(_ROUND_RE.finditer(text))
        if not rounds:
            findings.append({"file": FINAL_REVIEW, "severity": "error", "msg": "no '## Round N — <date>' section"})
        for i, m in enumerate(rounds):
            body = text[m.start():rounds[i + 1].start() if i + 1 < len(rounds) else len(text)]
            if not _VERDICT_RE.search(body):
                findings.append({"file": FINAL_REVIEW, "severity": "error", "msg": f"Round {m.group(1)}: no '**Verdict**: READY | READY-WITH-FOLLOWUPS | AWAITING-OWNER | NOT READY'"})
            if not _REVIEWED_COMMIT_RE.search(body):
                findings.append({"file": FINAL_REVIEW, "severity": "error", "msg": f"Round {m.group(1)}: no '**Reviewed-commit**: <sha>'"})
        nums = [int(m.group(1)) for m in rounds]
        if nums != list(range(1, len(nums) + 1)):
            findings.append({"file": FINAL_REVIEW, "severity": "error", "msg": f"rounds not numbered 1..N: {nums}"})

    acs = _parse_acs(fd)
    if acs:
        nums = [a["num"] for a in acs]
        if nums != sorted(nums) or len(set(nums)) != len(nums):
            findings.append({"file": "spec.md", "severity": "error", "msg": f"AC ids not strictly ascending: {nums}"})
        for a in acs:
            if a["level"] not in AC_LEVELS:
                findings.append({"file": "spec.md", "severity": "error", "msg": f"{a['id']}: 'Verify: <{'|'.join(AC_LEVELS)}>' missing or unknown ({a['level']})"})
            elif a["level"] in AC_REASON_LEVELS and not a["reason"]:
                findings.append({"file": "spec.md", "severity": "error", "msg": f"{a['id']}: Verify: {a['level']} needs a reason — 'Verify: {a['level']} (why no lower level can prove it)'"})
        spec_text = (fd / "spec.md").read_text(errors="replace")
        frs = sorted(set(re.findall(r"\*\*(FR-\d{3})\*\*", spec_text)))
        covered = {fr for a in acs for fr in a["frs"]}
        uncovered = [fr for fr in frs if fr not in covered]
        if uncovered:
            findings.append({"file": "spec.md", "severity": "warning", "msg": f"FRs no acceptance criterion names: {uncovered}"})
        if (fd / "tasks.md").exists():
            tagged = _ac_test_tasks(fd)
            known = {a["id"] for a in acs}
            for ac in sorted(set(tagged) - known):
                findings.append({"file": "tasks.md", "severity": "error", "msg": f"[{ac}] tagged on a task but not defined in spec.md"})
            for a in acs:
                if a["level"] in AC_TEST_LEVELS and a["id"] not in tagged:
                    findings.append({"file": "tasks.md", "severity": "error", "msg": f"{a['id']} (Verify: {a['level']}) has no '[TEST] [{a['id']}]' task"})
        changed = _frozen_changed(fd)
        if changed:
            findings.append({"file": FREEZE_FILE, "severity": "error", "msg": f"frozen acceptance tests changed: {changed} — revert, or re-freeze with the user's approval (acceptance_freeze refreeze=true)"})

    if (fd / ACCEPTANCE).exists():
        text = (fd / ACCEPTANCE).read_text(errors="replace")
        rounds = list(_ROUND_RE.finditer(text))
        for i, m in enumerate(rounds):
            body = text[m.start():rounds[i + 1].start() if i + 1 < len(rounds) else len(text)]
            if not _ACC_RESULT_RE.search(body):
                findings.append({"file": ACCEPTANCE, "severity": "error", "msg": f"Round {m.group(1)}: no '**Result**: PASS | FAIL | STOPPED'"})
            if not _ACC_COMMIT_RE.search(body):
                findings.append({"file": ACCEPTANCE, "severity": "error", "msg": f"Round {m.group(1)}: no '**Commit**: <sha>'"})

    if "spec.md" in state["artifacts"] and state["artifacts"]["spec.md"] == "present" and not state["size_declared"]:
        findings.append({"file": "spec.md", "severity": "warning", "msg": "no '**Size**: S | M | L' header line — treated as M"})

    if any((fd / c).exists() for c in CLOSE_DOCS):
        close_text = "".join((fd / c).read_text(errors="replace") for c in CLOSE_DOCS if (fd / c).exists())
        if "## Architecture Decisions" not in close_text:
            findings.append({"file": "close.md", "severity": "warning", "msg": "close document has no '## Architecture Decisions' section"})
        if not (fd / "change-record.md").exists():
            findings.append({"file": "change-record.md", "severity": "warning", "msg": "closed feature without change-record.md — write it from change-record-template.md"})

    if (fd / "history.md").exists():
        if not (fd / "history.md").read_text(errors="replace").lstrip().startswith("#"):
            findings.append({"file": "history.md", "severity": "warning", "msg": "missing title header"})
    elif state["current_phase"] > 1 or state["status"] != "new":
        findings.append({"file": "history.md", "severity": "error", "msg": "history.md missing — every feature with artifacts must have one"})

    errors = sum(f["severity"] == "error" for f in findings)
    return _json({"success": errors == 0, "errors": errors, "warnings": len(findings) - errors, "findings": findings})


@mcp.tool(name="acceptance_freeze")
def acceptance_freeze(feature: str, refreeze: bool = False, reason: str = "") -> str:
    """Record SHA-256 checksums of the acceptance-test files — the files named on tasks.md
    lines that carry [TEST] and [AC-###] — in specs/<feature>/evidence/acceptance-freeze.json.
    Call after each implement phase's RED run. Additive: files already frozen keep their
    checksum; new ones are added. A frozen file that changed is an error unless
    refreeze=true with the user's reason (record the ruling in decisions.md).

    Args:
        feature: Feature ID
        refreeze: Re-hash changed frozen files (only with the user's approval)
        reason: Why the frozen tests changed (required with refreeze)
    """
    state = _derive(feature)
    if state is None:
        return _not_found(feature)
    fd = _feature_dir(feature)
    tagged = _ac_test_tasks(fd)
    if not tagged:
        return _json({"error": "no tasks.md line carries both [TEST] and [AC-###] — tag the acceptance tests first"})
    paths = sorted({tok for lines in tagged.values() for line in lines
                    for tok in _PATH_TOKEN_RE.findall(line) if Path(tok).is_file()})
    if not paths:
        return _json({"error": "the [AC-###] test tasks name no existing file — write the tests (RED) first",
                      "acs": sorted(tagged)})
    fr = _freeze(fd) or {"files": {}, "history": []}
    changed = [p for p in _frozen_changed(fd)]
    if changed and not refreeze:
        return _json({"error": f"frozen acceptance tests changed: {changed} — revert them, or refreeze with the user's approval",
                      "changed": changed})
    if refreeze and not reason.strip():
        return _json({"error": "refreeze needs the user's reason"})
    added = [p for p in paths if p not in fr["files"]]
    for p in added + (changed if refreeze else []):
        if Path(p).exists():
            fr["files"][p] = _sha(p)
        else:
            fr["files"].pop(p, None)
    _, head = _git("rev-parse", "--short", "HEAD")
    fr["history"].append({"at": _now(), "commit": head.strip() or None, "added": added,
                          "refrozen": changed if refreeze else [], "reason": reason.strip() or None})
    out = fd / FREEZE_FILE
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(fr, indent=2) + "\n")
    return _json({"success": True, "frozen": len(fr["files"]), "added": added,
                  "refrozen": changed if refreeze else [], "file": str(out)})


@mcp.tool(name="acceptance_status")
def acceptance_status(feature: str, results: str = "", round: int = 0) -> str:
    """The acceptance matrix: every AC in spec.md → its verify level, its [TEST] [AC-###] tasks,
    and its outcome from test result files (JUnit XML or TRX; a test belongs to an AC when its
    name carries the id — 'AC-003 …', 'AC003_…', 'test_ac003_…'). command/probe ACs read
    evidence/acceptance-r<round>-AC-###.txt whose first line is 'RESULT: PASS' or 'RESULT: FAIL'.
    Outcomes: pass · fail · missing (automated, no result) · deferred (e2e not run) · manual.
    Also reports frozen tests that changed. Read-only; the accept loop writes acceptance.md.

    Args:
        feature: Feature ID
        results: Comma-separated result files or globs, relative to the project root
        round: Acceptance round number (for the command/probe evidence files)
    """
    state = _derive(feature)
    if state is None:
        return _not_found(feature)
    fd = _feature_dir(feature)
    acs = _parse_acs(fd)
    if not acs:
        return _json({"error": "spec.md defines no '**AC-###**' acceptance criteria"})
    files = []
    for pattern in [r.strip() for r in results.split(",") if r.strip()]:
        matches = sorted(Path(".").glob(pattern)) if any(ch in pattern for ch in "*?[") else [Path(pattern)]
        files.extend(m for m in matches if m.is_file())
    cases = _parse_results(files)
    by_ac = {}
    for c in cases:
        for n in _AC_IN_NAME_RE.findall(c["name"]):
            by_ac.setdefault(f"AC-{n}", []).append(c)
    tagged = _ac_test_tasks(fd)
    matrix = []
    for a in acs:
        tests = by_ac.get(a["id"], [])
        if a["level"] == "manual":
            outcome = "manual"
        elif a["level"] in ("command", "probe"):
            ev = fd / "evidence" / f"acceptance-r{round}-{a['id']}.txt"
            first = ev.read_text(errors="replace").splitlines()[0].strip().upper() if ev.exists() and ev.stat().st_size else ""
            outcome = "pass" if first == "RESULT: PASS" else "fail" if first == "RESULT: FAIL" else "missing"
        elif any(t["outcome"] == "fail" for t in tests):
            outcome = "fail"
        elif any(t["outcome"] == "pass" for t in tests):
            outcome = "pass"
        elif a["level"] == "e2e":
            outcome = "deferred"
        else:
            outcome = "missing"
        matrix.append({"ac": a["id"], "frs": a["frs"], "level": a["level"], "outcome": outcome,
                       "tasks": len(tagged.get(a["id"], [])),
                       "tests": [{"name": t["name"][:160], "outcome": t["outcome"]} for t in tests[:10]]})
    counts = {k: sum(m["outcome"] == k for m in matrix) for k in ("pass", "fail", "missing", "deferred", "manual")}
    changed = _frozen_changed(fd)
    # the acceptance run is also the full regression: a failing test outside any AC fails the round
    regressions = [c["name"][:160] for c in cases if c["outcome"] == "fail" and not _AC_IN_NAME_RE.search(c["name"])]
    blocking = counts["fail"] + counts["missing"] + len(regressions)
    result = "STOPPED" if changed else "PASS" if blocking == 0 else "FAIL"
    _, head = _git("rev-parse", "--short", "HEAD")
    return _json({"success": True, "result": result, "commit": head.strip() or None, "counts": counts,
                  "matrix": matrix, "regressions": regressions[:30], "regression_count": len(regressions),
                  "frozen_changed": changed, "result_files": [str(f) for f in files], "test_cases": len(cases),
                  "note": "PASS = no automated AC failing or missing and no regression; deferred e2e and manual ACs go to the final review"})


# Added lines matching these are reported by diff_scan. Kept to high-signal patterns: every
# hit is something a reviewer must look at, not a style opinion.
_SCAN_LINE_PATTERNS = [
    ("conflict-marker", "error", re.compile(r"^(<{7}|>{7}|={7})( |$)")),
    ("private-key", "error", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("secret-assignment", "warning", re.compile(r"(?i)\b(password|pwd|secret|api[_-]?key|accountkey|client[_-]?secret)\s*[=:]\s*['\"]?[^\s'\";{}<>$]{8,}")),
    ("aws-access-key", "error", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("focused-test", "error", re.compile(r"\b(fdescribe|fit|describe\.only|it\.only|test\.only)\s*\(")),
    ("debugger", "warning", re.compile(r"^\s*debugger;?\s*$")),
    ("todo", "warning", re.compile(r"\b(TODO|FIXME|HACK|XXX)\b")),
]
_SCAN_FORBIDDEN_FILES = re.compile(r"(?i)\.(pfx|p12|pem|key|keystore|jks|bacpac)$|(^|/)\.env(\.[^/]*)?$")
_SCAN_LARGE_BYTES = 1_000_000


@mcp.tool(name="diff_scan")
def diff_scan(feature: str, base: str = None) -> str:
    """Mechanical merge-readiness scan of the branch diff (merge-base(base, HEAD)..HEAD,
    code outside specs/ only): merge conflicts against base, conflict markers, secrets and
    private keys, focused tests, debugger statements, new TODO/FIXME, forbidden files
    (.pfx/.pem/.bacpac/.env…), files over 1 MB, and changed files that tasks.md/plan.md never
    name (unplanned changes). Read-only. The final review saves this output as evidence.

    Args:
        feature: Feature ID
        base: Base branch (default: branch_source from specs/git-conventions.md, else main)
    """
    state = _derive(feature)
    if state is None:
        return _not_found(feature)
    base = base or _conventions().get("branch_source") or "main"
    if "/" not in base and _git("rev-parse", "--verify", "--quiet", f"origin/{base}")[0] == 0:
        base = f"origin/{base}"  # the remote-tracking branch is what the PR merges into; a local one goes stale
    rc, mb = _git("merge-base", base, "HEAD")
    if rc != 0:
        return _json({"error": f"cannot find merge-base of '{base}' and HEAD — fetch the base branch or pass base="})
    mb = mb.strip()
    findings = []

    rc, out = _git("merge-tree", "--write-tree", "--name-only", "--no-messages", base, "HEAD")
    if rc == 1:
        conflicted = [l for l in out.splitlines()[1:] if l.strip()]
        findings.append({"check": "merge-conflict", "severity": "error", "file": None,
                         "msg": f"merging into {base} conflicts in {len(conflicted)} file(s): {conflicted[:10]}"})
    elif rc not in (0, 1):
        findings.append({"check": "merge-conflict", "severity": "warning", "file": None,
                         "msg": "git merge-tree --write-tree unavailable (git < 2.38) — check conflicts by hand"})

    _, names = _git("diff", "--name-status", "--no-renames", f"{mb}..HEAD", "--", ".", ":(exclude)specs")
    changed = []
    for line in names.splitlines():
        parts = line.split("\t")
        if len(parts) == 2:
            changed.append((parts[0], parts[1]))
    for status, path in changed:
        if status == "D":
            continue
        if _SCAN_FORBIDDEN_FILES.search(path):
            findings.append({"check": "forbidden-file", "severity": "error", "file": path, "msg": "certificate/key/backup/env file in the diff"})
        try:
            if Path(path).stat().st_size > _SCAN_LARGE_BYTES:
                findings.append({"check": "large-file", "severity": "warning", "file": path, "msg": f"{Path(path).stat().st_size // 1024} KB"})
        except OSError:
            pass

    _, diff = _git("diff", "-U0", "--no-color", f"{mb}..HEAD", "--", ".", ":(exclude)specs")
    current, lineno = None, 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else None
            continue
        if line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            lineno = int(m.group(1)) if m else 0
            continue
        if line.startswith("+") and current:
            text = line[1:]
            for check, sev, rx in _SCAN_LINE_PATTERNS:
                if rx.search(text):
                    findings.append({"check": check, "severity": sev, "file": f"{current}:{lineno}", "msg": text.strip()[:120]})
            lineno += 1

    fd = _feature_dir(feature)
    planned_text = "".join((fd / a).read_text(errors="replace") for a in ("tasks.md", "plan.md", "spec.md") if (fd / a).exists())
    unplanned = [p for st, p in changed if st != "D" and p not in planned_text and Path(p).name not in planned_text]
    if unplanned:
        findings.append({"check": "unplanned-change", "severity": "info", "file": None,
                         "msg": f"{len(unplanned)} changed file(s) not named in spec/plan/tasks — confirm each is in scope",
                         "files": unplanned[:50]})

    errors = sum(f["severity"] == "error" for f in findings)
    return _json({"success": errors == 0, "base": base, "merge_base": mb[:12], "files_changed": len(changed),
                  "errors": errors, "warnings": sum(f["severity"] == "warning" for f in findings),
                  "findings": findings, "scanned_at": _now()})


@mcp.tool(name="timestamp")
def timestamp() -> str:
    """The real current UTC time (ISO 8601, seconds). Use it for every history entry,
    evidence file header and date field — never type a timestamp from memory.
    """
    return _json({"utc": _now()})



@mcp.tool(name="append_history")
def append_history(feature: str, phase: str, skill: str, agent: str, artifacts: str = "none",
                   tests: str = "none", evidence: str = "none — unverified", commit: str = "n/a",
                   note: str = "-") -> str:
    """Append one fixed-field entry to specs/<feature>/history.md with the REAL UTC time.
    The entry is the record, not the story: note ≤ 25 words, whole entry ≤ 60 words.

    Args:
        feature: Feature ID
        phase: Phase label (e.g. 'Phase 2', 'Phase 4 — Core', 'BF-014', 'Regression', 'Phase 6')
        skill: The skill that completed (e.g. spec-kit-plan)
        agent: hermes | claude | <human name> — read later as Implemented-by
        artifacts: Comma-separated files created or modified
        tests: '<command> → N passed, M failed' or 'none'
        evidence: 'output:…; probe:…; ci:…; review:…' or 'none — unverified'
        commit: The commit message that follows this entry
        note: ≤ 25 words — the one fact a reader needs
    """
    state = _derive(feature)
    if state is None:
        return _not_found(feature)
    if len(note.split()) > 25:
        return _json({"error": f"note has {len(note.split())} words — max 25; narrative belongs in implementation-summary.md"})
    body = (f"- Artifacts: {artifacts or 'none'}\n- Tests: {tests or 'none'}\n- Evidence: {evidence or 'none — unverified'}\n"
            f"- Commit: {commit or 'n/a'}\n- Note: {note or '-'}\n")
    words = len(body.split())
    if words > 60:
        return _json({"error": f"entry body has {words} words — max 60; shorten artifacts/tests/evidence/note"})
    ts = _now()
    hist = _feature_dir(feature) / "history.md"
    if not hist.exists():
        hist.write_text(f"# Process History: {feature}\n")
    with hist.open("a", encoding="utf-8") as fh:
        fh.write(f"\n## {ts} | {phase} | {skill} | {agent}\n{body}")
    return _json({"success": True, "timestamp": ts, "file": str(hist), "words": words})


@mcp.tool(name="history_guard")
def history_guard(feature: str, phase: str) -> str:
    """Pre-commit guard: is there a history.md entry mentioning `phase` that is newer than
    the last commit touching specs/<feature>/? Returns ok=false with the reason otherwise.

    Args:
        feature: Feature ID
        phase: Text that must appear in the entry header (e.g. 'Phase 2', 'BF-014', 'Regression')
    """
    state = _derive(feature)
    if state is None:
        return _not_found(feature)
    hist = _feature_dir(feature) / "history.md"
    if not hist.exists():
        return _json({"ok": False, "reason": "history.md missing"})
    entries = [(m.group(1), m.group(2)) for m in _HISTORY_ENTRY_RE.finditer(hist.read_text(errors="replace"))]
    matching = [(ts, hdr) for ts, hdr in entries if phase.lower() in hdr.lower()]
    if not matching:
        return _json({"ok": False, "reason": f"no history entry mentions '{phase}'", "entries": len(entries)})
    try:
        last_commit = subprocess.run(["git", "log", "-1", "--format=%cI", "--", str(_feature_dir(feature))],
                                     capture_output=True, text=True, check=False).stdout.strip()
    except OSError:
        last_commit = ""
    newest_ts = max(ts for ts, _ in matching)
    if last_commit:
        try:
            lc = datetime.datetime.fromisoformat(last_commit.replace("Z", "+00:00"))
            et = datetime.datetime.fromisoformat(newest_ts.replace("Z", "+00:00"))
            if et.tzinfo is None:
                et = et.replace(tzinfo=datetime.timezone.utc)
            if et < lc:
                return _json({"ok": False, "reason": f"newest '{phase}' entry ({newest_ts}) predates the last commit ({last_commit}) — append a new entry",
                              "matching_entries": len(matching)})
        except ValueError:
            pass
    return _json({"ok": True, "matching_entries": len(matching), "newest": newest_ts, "last_commit": last_commit or None})


# ── Entry point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")
