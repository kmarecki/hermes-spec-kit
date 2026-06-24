#!/usr/bin/env python3
"""Validate all spec-kit skill files for consistency and correctness.

Tests:
  1. Every skill has valid YAML frontmatter with required fields
  2. All 7 phases (0-6) have corresponding skills
  3. Every `spec-kit/references/*` reference in skill content points to an existing file
  4. Every template reference points to an existing template
  5. All cross-skill references point to existing skills
  6. Skills follow correct naming convention
  7. Each skill lists correct trigger phrases
  8. Every phase skill (except workflow) references preflight.md
  9. Phase numbers in skills match expected phases
 10. No orphan references and no missing phases
"""

import re, sys, yaml, json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "src" / "skills"
REFERENCES_DIR = REPO / "src" / "references"
TEMPLATES_DIR = REPO / "src" / "templates"

failures = 0

def check(label, ok, detail=""):
    global failures
    if ok:
        print(f"  ✓ {label}")
    else:
        print(f"  ✗ {label}  {detail}")
        failures += 1

# ── Expected skill inventory ──────────────────────────────────────────────

# Phase -> skill name, expected phase number
PHASE_SKILLS = {
    0:   "spec-kit-constitution",
    1:   "spec-kit-specify",
    1.5: "spec-kit-clarify",
    2:   "spec-kit-plan",
    3:   "spec-kit-tasks",
    3.5: "spec-kit-review",
    4:   "spec-kit-implement",
    5:   "spec-kit-test",
    6:   "spec-kit-summarize",
}

NON_PHASE_SKILLS = {"spec-kit-refresh", "spec-kit-workflow"}
UMBRELLA_DIR = "spec-kit"  # umbrella SKILL.md inside spec-kit/ directory
ALL_SKILLS = set(PHASE_SKILLS.values()) | NON_PHASE_SKILLS | {UMBRELLA_DIR}

EXPECTED_TEMPLATES = {
    "AGENTS-template.md",
    "bugs-template.md",
    "close-template.md",
    "constitution-template.md",
    "data-model-template.md",
    "git-conventions-template.md",
    "gitignore-template.md",
    "history-template.md",
    "implementation-summary-template.md",
    "plan-template.md",
    "research-template.md",
    "spec-template.md",
    "tasks-template.md",
}

EXPECTED_REFERENCES = {
    "auto-commit.md",
    "constitution-principles.md",
    "constitution-tables.md",
    "history-tracking.md",
    "preflight.md",
}

# ── Helpers ────────────────────────────────────────────────────────────────

def parse_frontmatter(path):
    """Parse YAML frontmatter from a markdown file."""
    content = path.read_text()
    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return None, content
    try:
        return yaml.safe_load(m.group(1)), content
    except yaml.YAMLError:
        return None, content


def collect_skill_names():
    """Return set of all skill names (both flat .md files and umbrella dirs)."""
    names = set()
    for p in SKILLS_DIR.rglob("SKILL.md"):
        # umbrella: spec-kit/SKILL.md -> spec-kit
        names.add(p.parent.name)
    for p in SKILLS_DIR.glob("spec-kit-*.md"):
        names.add(p.stem)
    return names


def collect_refs_in_text(text):
    """Find all `spec-kit/references/*` references in text."""
    return set(re.findall(r'`(?:spec-kit/)?references/([^`]+)`', text))


def collect_templates_in_text(text):
    """Find all `spec-kit/templates/*` references in text."""
    # Exclude placeholder patterns like <name>.md
    refs = set()
    for m in re.finditer(r'`(?:spec-kit/)?templates/([^`]+)`', text):
        name = m.group(1)
        if '<' not in name and '>' not in name:  # skip placeholders like <name>.md
            refs.add(name)
    return refs


def collect_skill_refs_in_text(text):
    """Find all `spec-kit-*` skill references in text."""
    refs = set()
    for m in re.finditer(r'`(spec-kit-[a-z-]+)`', text):
        refs.add(m.group(1))
    return refs


# ── Tests ──────────────────────────────────────────────────────────────────


def test_all_skills_present():
    """Every expected skill has a file."""
    print("\n═══ Skill inventory ═══")
    existing = collect_skill_names()

    for name in sorted(ALL_SKILLS):
        if name == UMBRELLA_DIR:
            path = SKILLS_DIR / name / "SKILL.md"
        else:
            path = SKILLS_DIR / f"{name}.md"
        check(f"skill exists: {name}", path.exists(), f"missing: {path}")

    # No unexpected skills
    expected_files = set()
    for name in ALL_SKILLS:
        if name == UMBRELLA_DIR:
            expected_files.add(name)
        else:
            expected_files.add(f"{name}.md")
    unexpected = set()
    for p in SKILLS_DIR.glob("spec-kit-*.md"):
        if p.stem not in ALL_SKILLS:
            unexpected.add(p.stem)
    # Also check for unexpected umbrella dirs
    for d in SKILLS_DIR.iterdir():
        if d.is_dir() and (d / "SKILL.md").exists() and d.name not in ALL_SKILLS:
            unexpected.add(d.name)
    check("no unexpected skills", len(unexpected) == 0, f"unexpected: {unexpected}")


def test_frontmatter():
    """Every skill file has valid YAML frontmatter with required fields."""
    print("\n═══ Frontmatter validation ═══")
    required = {"name", "description"}
    for name in sorted(ALL_SKILLS):
        if name == UMBRELLA_DIR:
            path = SKILLS_DIR / name / "SKILL.md"
        else:
            path = SKILLS_DIR / f"{name}.md"
        if not path.exists():
            continue

        fm, _ = parse_frontmatter(path)
        check(f"{name}: frontmatter parses", fm is not None)
        if fm:
            for field in required:
                check(f"{name}: has field '{field}'", field in fm, f"missing: {field}")
            check(f"{name}: has description", bool(fm.get("description", "").strip()))


def test_phase_coverage():
    """All 7 phases have a skill, and phase numbers match."""
    print("\n═══ Phase coverage ═══")
    for phase, name in sorted(PHASE_SKILLS.items()):
        path = SKILLS_DIR / f"{name}.md"
        if not path.exists():
            check(f"phase {phase} ({name}): file missing", False)
            continue
        fm, content = parse_frontmatter(path)
        if not fm:
            continue

        # Check phase mention in content
        phase_refs = re.findall(r'\*\*Phase\*\*:?\s*([0-9.]+)', content)
        phase_match = False
        for pr in phase_refs:
            expected = str(phase).rstrip('0').rstrip('.')
            actual = str(pr).rstrip('0').rstrip('.')
            if actual == expected:
                phase_match = True
        check(f"phase {phase} ({name}): mentions correct phase", phase_match,
              f"expected Phase {phase}, found: {phase_refs}")


def test_reference_files_exist():
    """Every reference mentioned in skill content exists in references/."""
    print("\n═══ Reference files ═══")
    existing_refs = {p.name for p in REFERENCES_DIR.glob("*.md")}

    for name in sorted(ALL_SKILLS):
        if name == UMBRELLA_DIR:
            path = SKILLS_DIR / name / "SKILL.md"
        else:
            path = SKILLS_DIR / f"{name}.md"
        if not path.exists():
            continue
        _, content = parse_frontmatter(path)
        if content is None:
            continue
        refs = collect_refs_in_text(content)
        for ref in refs:
            check(f"{name}: reference '{ref}' exists", ref in existing_refs,
                  f"not found in references/ ({ref})")


def test_templates_exist():
    """Every template mentioned in skill content exists in templates/."""
    print("\n═══ Template files ═══")
    existing_templates = {p.name for p in TEMPLATES_DIR.glob("*.md")}
    check("all expected templates present",
          existing_templates == EXPECTED_TEMPLATES,
          f"missing: {EXPECTED_TEMPLATES - existing_templates}, "
          f"extra: {existing_templates - EXPECTED_TEMPLATES}")

    for name in sorted(ALL_SKILLS):
        if name == UMBRELLA_DIR:
            path = SKILLS_DIR / name / "SKILL.md"
        else:
            path = SKILLS_DIR / f"{name}.md"
        if not path.exists():
            continue
        _, content = parse_frontmatter(path)
        if content is None:
            continue
        refs = collect_templates_in_text(content)
        for ref in refs:
            check(f"{name}: template '{ref}' exists", ref in existing_templates,
                  f"not found in templates/ ({ref})")


def test_cross_skill_references_exist():
    """Every cross-skill reference points to an existing skill."""
    print("\n═══ Cross-skill references ═══")
    existing = collect_skill_names()

    for name in sorted(ALL_SKILLS):
        if name == UMBRELLA_DIR:
            path = SKILLS_DIR / name / "SKILL.md"
        else:
            path = SKILLS_DIR / f"{name}.md"
        if not path.exists():
            continue
        _, content = parse_frontmatter(path)
        if content is None:
            continue
        refs = collect_skill_refs_in_text(content)
        for ref in refs:
            check(f"{name}: references '{ref}'", ref in existing,
                  f"not an existing skill")


def test_preflight_reference():
    """Every phase skill references preflight.md for its pre-action checks."""
    print("\n═══ Pre-flight reference ═══")
    skip = {"spec-kit-workflow", "spec-kit-refresh", "spec-kit-review", UMBRELLA_DIR}
    for name in sorted(ALL_SKILLS):
        if name in skip:
            continue
        if name == UMBRELLA_DIR:
            path = SKILLS_DIR / name / "SKILL.md"
        else:
            path = SKILLS_DIR / f"{name}.md"
        if not path.exists():
            continue
        _, content = parse_frontmatter(path)
        if content is None:
            continue
        has_preflight = "spec-kit/references/preflight.md" in content or "references/preflight.md" in content
        check(f"{name}: references preflight.md", has_preflight)


def test_trigger_descriptions():
    """Skill description mentions correct trigger phrases."""
    print("\n═══ Trigger descriptions ═══")
    for name in sorted(ALL_SKILLS):
        if name == UMBRELLA_DIR:
            path = SKILLS_DIR / name / "SKILL.md"
        else:
            path = SKILLS_DIR / f"{name}.md"
        if not path.exists():
            continue
        fm, _ = parse_frontmatter(path)
        if not fm:
            continue
        desc = fm.get("description", "")
        # Each skill should mention its own name in the trigger description
        if name.startswith("spec-kit-"):
            short_name = name.replace("spec-kit-", "")
            # Workflow is a router, not a direct-trigger skill
            if short_name == "workflow":
                continue
            check(f"{name}: mentions 'speckit {short_name}' in triggers",
                  f"speckit {short_name}" in desc.lower())


def test_umbrella_coverage():
    """Umbrella SKILL.md mentions all phase skills."""
    print("\n═══ Umbrella coverage ═══")
    path = SKILLS_DIR / UMBRELLA_DIR / "SKILL.md"
    if not path.exists():
        check("umbrella SKILL.md exists", False)
        return
    content = path.read_text()
    for phase, name in sorted(PHASE_SKILLS.items()):
        check(f"umbrella references phase {phase} ({name})", name in content,
              f"missing reference to {name}")
    for name in NON_PHASE_SKILLS:
        check(f"umbrella references {name}", name in content,
              f"missing reference to {name}")


def test_no_loose_reference_files():
    """No extra/missing files in references/ directory."""
    print("\n═══ Reference inventory ═══")
    existing = {p.name for p in REFERENCES_DIR.glob("*.md")}
    check("no unexpected reference files", existing == EXPECTED_REFERENCES,
          f"extra: {existing - EXPECTED_REFERENCES}, "
          f"missing: {EXPECTED_REFERENCES - existing}")


def test_workflow_diagram_phases():
    """Workflow skill mentions all phase numbers in its diagram."""
    print("\n═══ Workflow diagram phases ═══")
    path = SKILLS_DIR / "spec-kit-workflow.md"
    if not path.exists():
        return
    content = path.read_text()
    for phase, name in sorted(PHASE_SKILLS.items()):
        check(f"workflow mentions phase {phase} ({name})", name.replace("spec-kit-", "") in content,
              f"missing phase {name} in workflow")


def test_skills_yaml_parse():
    """All frontmatter YAML parses correctly (no syntax errors)."""
    print("\n═══ YAML parse check ═══")
    for name in sorted(ALL_SKILLS):
        if name == UMBRELLA_DIR:
            path = SKILLS_DIR / name / "SKILL.md"
        else:
            path = SKILLS_DIR / f"{name}.md"
        if not path.exists():
            continue
        content = path.read_text()
        # Extract all frontmatter blocks
        blocks = re.findall(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        for i, block in enumerate(blocks):
            try:
                parsed = yaml.safe_load(block)
                check(f"{name}: YAML block {i} parses", parsed is not None or block.strip() == "")
            except yaml.YAMLError as e:
                check(f"{name}: YAML block {i} valid", False, str(e))


# ── Main ───────────────────────────────────────────────────────────────────


def main():
    print("═" * 55)
    print("  spec-kit Skills — Validation Tests")
    print("═" * 55)

    tests = [
        test_all_skills_present,
        test_frontmatter,
        test_skills_yaml_parse,
        test_phase_coverage,
        test_trigger_descriptions,
        test_reference_files_exist,
        test_templates_exist,
        test_cross_skill_references_exist,
        test_preflight_reference,
        test_umbrella_coverage,
        test_no_loose_reference_files,
        test_workflow_diagram_phases,
    ]

    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"  ✗ {t.__name__} crashed: {e}")
            import traceback
            traceback.print_exc()
            global failures
            failures += 1

    print(f"\n{'═' * 55}")
    if failures:
        print(f"  FAILURES: {failures} check(s) failed")
    else:
        print(f"  All checks passed!")
    print(f"{'═' * 55}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
