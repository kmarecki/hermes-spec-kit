---
name: spec-kit-constitution
description: Load when the user says 'spec-kit constitution', 'speckit constitution', 'spec-kit principles', 'speckit principles', "create constitution", "create project principles", or "set up project principles" — Phase 0 project setup. Handles both brownfield (existing codebase) and greenfield (new project) modes.
version: 2.0.0
author: Hermes Agent
license: MIT
category: software-development
metadata:
  hermes:
    tags: [spec, constitution, principles, project-setup, brownfield, greenfield]
    related_skills: [spec-kit-specify, spec-kit-workflow]
---

# spec-kit-constitution

**Task Persona**: Adopt the mindset of a project founder setting ground rules.
Constitutions should be principled but practical — they guide decisions without
being bureaucratic. Every rule must have a clear purpose. Always offer choice
with tradeoffs explained.

**Phase**: 0 (Project Foundation)

**Purpose**: Create or update the project constitution at `specs/constitution.md`.
Auto-detects project stack in brownfield mode, or guides the user through
principled choices in greenfield mode. Always presents 3 options per principle
with pros and cons.

**When NOT to use**: This is a one-time setup per project. Do NOT re-run for
every feature — principles are project-wide.

**Prerequisites**: None. This is the first skill — run first for a new project.

**Artifacts**: `specs/constitution.md`

**Routing**: Load this skill when the user says "create constitution" or
"create project principles". If loaded directly (not via spec-kit-workflow),
consider loading the workflow first for prerequisite checks.

## Pre-flight
Load and follow `spec-kit/references/preflight.md` before any action in this skill.

## Execution

### Step 0: Check for existing constitution

```
IF specs/constitution.md EXISTS:
  LOAD existing constitution
  NOTE: "Constitution exists at v[VERSION]. Run 'amend constitution' to update."
  HALT — constitution is one-time setup, do not overwrite without user intent
```

### Step 1: Detect mode — brownfield vs greenfield

```
SCAN project root for these files:

  # Language & framework
  package.json → JavaScript/TypeScript + framework (React, Vue, Express, etc.)
  pyproject.toml → Python + framework (Django, FastAPI, Flask, etc.)
  go.mod → Go + module name
  Cargo.toml → Rust
  Gemfile → Ruby + framework (Rails, Sinatra)
  build.gradle / build.gradle.kts → Java/Kotlin + framework (Spring, Micronaut)
  Project.swift → Swift (Tuist)
  
  # Test framework
  search for test files matching patterns like test_*.py, *_test.go, *.spec.ts, *_test.rb
  LOOK for pytest, vitest/jest, gotest, rspec, junit configs
  
  # Linting & formatting
  .eslintrc* / eslint.config.*, .prettierrc*, gofmt/golangci-lint, ruff/pylint config in pyproject.toml
  
  # CI/CD
  .github/workflows/*, .gitlab-ci.yml, Jenkinsfile, .circleci/config.yml
  
  # Existing docs
  README.md, CONTRIBUTING.md, docs/

  IF any project files detected:
    MODE = brownfield
    NOTE: "Detected [language] project with [framework], [test_framework], [ci]."
    TAG each detected field with ⭐ in the option tables below
  
  ELSE:
    MODE = greenfield
    NOTE: "No existing project detected — greenfield mode. I'll guide you through
           choosing principles for your new project."
```

### Step 2: Load the principles reference

```
LOAD spec-kit/references/constitution-principles.md

This reference defines 12 principles, each with 3 options (A/B/C).
Each option has a rule, pros, and cons.

FOR each principle:
  READ the 3 options
  IF MODE == brownfield:
    SELECT the option that best matches detected project artifacts
    TAG it with ⭐ "detected"
  IF MODE == greenfield:
    ASK the user about their intent or preference
```

### Step 3: Present each principle with choice

**For each principle, present the 3 options as a formatted table.**
Always show pros and cons. Never skip the choice — even if a detected default
exists, the user may disagree.

```
PRESENT for each principle:

  ## Principle N: [Name]

  | Option | Rule | Pros | Cons |
  |--------|------|------|------|
  | ⭐ A — [Name] *(detected)* | ... | ... | ... |
  | B — [Name] | ... | ... | ... |
  | C — [Name] | ... | ... | ... |

  The ⭐ marker means this was auto-detected from your project files.
  Pick A, B, or C (or type 'skip' to use detected default).

  USER picks: [A | B | C | skip]
  RECORD the chosen option
  ASK: "Any notes or rationale for this choice?" → RECORD as rationale
```

In greenfield mode, after showing the 3 options, include a short guiding question:

```
  GUIDING QUESTION (greenfield only):
  "For a [project type], most teams pick [option]. This means [summary of tradeoff].
   Does that match your priorities?"
```

### Step 4: Handle principle exceptions

```
IF project has no database (no DB config, no ORM, no schema files):
  SKIP Principle 10 (Database & Schema)
  NOTE: "Skipping Database principle — no database detected."
```

### Step 5: Write the constitution

```
COPY spec-kit/templates/constitution-template.md → specs/constitution.md

FILL each section with:
  - Chosen option letter and name
  - Full rule text from the reference
  - Recorded rationale
  - Rejected alternatives table with reasons

INCLUDE in the Tech Stack section:
  - Detected language/framework (brownfield) or "New project — TBD" (greenfield)
  - Test framework, CI, package manager
```

### Step 6: Version management
- **MAJOR** (1.x.x → 2.0.0): Backward-incompatible governance changes
- **MINOR** (x.1.x → x.2.0): New principles
- **PATCH** (x.x.1 → x.x.2): Clarifications

### Append to history.md and Commit

**Order is critical: history.md FIRST, then commit.**

1. **Append to history.md**:
   Append entry to `specs/history.md` (create if missing):
   - Phase: Phase 0 — Complete
   - Artifact: `specs/constitution.md`

2. **PRE-COMMIT GUARD**:
   READ `specs/history.md` — confirm the constitution entry is recorded.
   If missing: BLOCK — must append before commit.

3. **Commit**:
   Follow `spec-kit/references/auto-commit.md`:
   - Scope: `specs/constitution.md`
   - Message: `"spec(phase-0): constitution for [PROJECT]"`

## Completion
- Report: "Constitution ratified with [N] principles."
- Report mode: brownfield or greenfield
- List all chosen options (A/B/C per principle)
- List any principles skipped with reason
- Propose: Run `spec-kit-specify` to create the first feature specification.

## Brownfield Detection Examples

| Project file(s) | Detected language | Likely test framework | Recommended options |
|-----------------|-------------------|----------------------|---------------------|
| `package.json` + `next.config.js` | TypeScript/Next.js | Vitest/Jest | B (Pragmatic TDD), B (Pragmatic Linting), C (YAGNI) |
| `pyproject.toml` + `manage.py` | Python/Django | pytest | A (Strict TDD), B (Pragmatic Linting), B (Modular Monolith) |
| `go.mod` + `main.go` | Go | go test (std lib) | A (Strict TDD), B (Pragmatic Linting), A (Clean Arch) |
| `Cargo.toml` | Rust | cargo test | A (Strict TDD), A (Strict Linting), A (Clean Arch) |
| `package.json` + `vite.config.ts` | TypeScript/Vite | Vitest | B (Pragmatic TDD), B (Pragmatic Linting), C (YAGNI) |
| `Gemfile` + `config/routes.rb` | Ruby/Rails | RSpec | B (Pragmatic TDD), B (Pragmatic Linting), B (Modular Monolith) |
| `build.gradle.kts` | Kotlin | JUnit 5 | B (Pragmatic TDD), A (Strict Linting), B (Modular Monolith) |

## Common Pitfalls
1. **Skipping the choice dialog**: Always present ALL 3 options with pros/cons.
   The user needs to understand tradeoffs to make an informed decision.
2. **Burying detected defaults**: In brownfield mode, show ⭐ clearly but let the
   user override. Detection is guidance, not dictation.
3. **Assuming all 12 principles apply**: Skip Database principle for stateless
   projects. Skip Code Review for solo projects (but mentioning it is still useful).
4. **Overwriting an existing constitution**: Always check first. Constitution is
   one-time setup. If the user wants to amend, offer to add principles with
   version bump.

## Prerequisite Enforcement
**No prerequisites** — this is Phase 0.
