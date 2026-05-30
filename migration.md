# Migration Guide: OpenCode/Cline to Hermes Agent

This guide covers migrating from the OpenCode/Cline spec kit workflow to Hermes Agent's skill-based system.

## What Changed

### OpenCode/Cline Architecture

```
OpenCode/Cline Project
├── .clinerules/
│   └── workflows/
│       ├── constitution.md
│       ├── specify.md
│       ├── clarify.md
│       ├── plan.md
│       ├── tasks.md
│       └── implement.md
├── .specify/
│   ├── scripts/
│   │   └── bash/
│   │       ├── create-new-feature.sh
│   │       ├── setup-plan.sh
│   │       ├── check-prerequisites.sh
│   │       └── update-agent-context.sh
│   ├── templates/
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   └── checklist-template.md
│   └── memory/
│       └── constitution.md
└── specs/
    └── NNN-feature-name/
```

### Hermes Agent Architecture

```
Hermes Agent Setup
├── ~/.hermes/
│   ├── skills/
│   │   ├── spec-kit-workflow.md
│   │   ├── spec-kit-constitution.md
│   │   ├── spec-kit-specify.md
│   │   ├── spec-kit-clarify.md
│   │   ├── spec-kit-plan.md
│   │   ├── spec-kit-tasks.md
│   │   └── spec-kit-implement.md
│   ├── memory/
│   │   └── [persistent project knowledge]
│   └── cron/
│       └── [automation jobs]
└── Project/
    ├── AGENTS.md
    └── specs/
        └── NNN-feature-name/
```

## Key Differences

### 1. Workflow Definition

| Aspect | OpenCode/Cline | Hermes Agent |
|--------|----------------|--------------|
| Location | `.clinerules/workflows/` | `~/.hermes/skills/` |
| Format | Markdown with YAML frontmatter | Markdown with YAML frontmatter |
| Invocation | `/speckit.specify` command | Natural language prompt |
| Scope | Project-specific | Global (shared across projects) |
| Persistence | Project files | Skill files + memory |

### 2. Script Execution

| Aspect | OpenCode/Cline | Hermes Agent |
|--------|----------------|--------------|
| Setup scripts | `.specify/scripts/bash/*.sh` | Skill instructions |
| Feature creation | `create-new-feature.sh --json` | Skill generates directory |
| Context update | `update-agent-context.sh` | AGENTS.md auto-update |
| Prerequisites | `check-prerequisites.sh` | Skill validation logic |

### 3. Template System

| Aspect | OpenCode/Cline | Hermes Agent |
|--------|----------------|--------------|
| Templates | `.specify/templates/` | Embedded in skills |
| Customization | Edit template files | Customize skill content |
| Versioning | Git-tracked | Skill versioning |

### 4. Memory & State

| Aspect | OpenCode/Cline | Hermes Agent |
|--------|----------------|--------------|
| Constitution | `.specify/memory/constitution.md` | `specs/constitution.md` + memory |
| Project context | CLAUDE.md | AGENTS.md |
| Cross-session | Context window only | Persistent memory |
| Workflow state | File artifacts | File artifacts + memory |

### 5. Multi-Agent Capabilities

| Aspect | OpenCode/Cline | Hermes Agent |
|--------|----------------|--------------|
| Parallel work | Single agent | `delegate_task()` |
| Research | Sequential | Parallel subagents |
| Implementation | Linear | Parallel user stories |
| Orchestration | Manual | Automated delegation |

## Migration Steps

### Step 1: Analyze Current Setup

```bash
# Check current spec kit structure
find . -path "*/.clinerules/*" -o -path "*/.specify/*" | head -20

# List existing specs
ls -la specs/

# Check AGENTS.md for spec references
grep -A 20 "SPECKIT" AGENTS.md
```

### Step 2: Create Hermes Agent Skills

Create the skill files as defined in `skills.md`. Each skill replaces a workflow file:

```bash
# Create skills directory if needed
mkdir -p ~/.hermes/skills/

# Skills map 1:1 with workflow files
.clinerules/workflows/specify.md    → ~/.hermes/skills/spec-kit-specify.md
.clinerules/workflows/plan.md       → ~/.hermes/skills/spec-kit-plan.md
.clinerules/workflows/implement.md  → ~/.hermes/skills/spec-kit-implement.md
# etc.
```

### Step 3: Migrate Templates

OpenCode uses templates in `.specify/templates/`. In Hermes Agent, templates are embedded in skills. Extract key templates:

```bash
# View existing templates
cat .specify/templates/spec-template.md
cat .specify/templates/plan-template.md
cat .specify/templates/checklist-template.md
```

Copy template structures into the corresponding skill definitions.

### Step 4: Migrate Scripts

OpenCode uses bash scripts for automation. In Hermes Agent, this logic is handled by skills:

| Script | Hermes Agent Equivalent |
|--------|------------------------|
| `create-new-feature.sh` | spec-kit-specify skill creates directory |
| `setup-plan.sh` | spec-kit-plan skill loads context |
| `check-prerequisites.sh` | spec-kit-implement skill validates |
| `update-agent-context.sh` | Skills update AGENTS.md |

### Step 5: Update AGENTS.md

Replace Cline-specific references with Hermes Agent instructions:

**Before (Cline)**:
```markdown
# Agent Instructions

Use the spec kit workflow for all features:
1. /speckit.specify [description]
2. /speckit.plan
3. /speckit.tasks
4. /speckit.implement
```

**After (Hermes Agent)**:
```markdown
# Spec Kit Workflow

This project uses spec-driven development via Hermes Agent skills.

## Workflow Phases

1. "Create a spec for [feature description]"
2. "Plan the implementation for [feature]"
3. "Generate tasks for [feature]"
4. "Implement [feature]"

## Current Specs

<!-- SPECKIT START -->
- specs/006-multi-layered-visualizer/plan.md
- specs/006-multi-layered-visualizer/spec.md
<!-- SPECKIT END -->
```

### Step 6: Preserve Existing Specs

Your existing specs/ directory structure is compatible. No changes needed:

```
specs/
  002-llm-world-generation/     ← Keep as-is
  003-procedural-world-generation/ ← Keep as-is
  004-scenario-location-quality/  ← Keep as-is
  005-scene-cluster-backbone/   ← Keep as-is
  006-multi-layered-visualizer/ ← Keep as-is
```

The Hermes Agent skills will work with your existing spec artifacts.

### Step 7: Test the Migration

```bash
# Start a new Hermes Agent session
hermes

# Test workflow
> "What phase is 006-multi-layered-visualizer in?"
> "Create a spec for [test feature]"
> "Plan the implementation for [test feature]"
```

### Step 8: Set Up Automation (Optional)

Replace OpenCode's script-based automation with Hermes Agent cron jobs:

```python
# Spec completeness check
cronjob(action='create', name='spec-check', schedule='every 24h',
  prompt='Check all spec directories for completeness. Report missing files.')

# AGENTS.md update
cronjob(action='create', name='agents-update', schedule='every 12h',
  prompt='Update AGENTS.md SPECKIT section with current spec references.')
```

## Feature Comparison

### What You Gain

1. **Persistent Memory**: Project conventions survive across sessions
2. **Multi-Agent Delegation**: Parallel research and implementation
3. **Global Skills**: Share workflow across projects
4. **Natural Language**: No special commands needed
5. **Automation**: Cron jobs for maintenance tasks
6. **Flexibility**: Customize skills per project

### What You Lose

1. **Script Precision**: Bash scripts are explicit; skills are LLM-driven
2. **Template Separation**: Templates embedded in skills, not separate files
3. **Command Syntax**: `/speckit.specify` → natural language

### Workarounds

**For script precision**: Use `terminal()` tool in skills for exact commands.

**For template separation**: Store templates in `templates/` directory, reference from skills.

**For command syntax**: Create skill triggers that respond to command-like phrases.

## Project-Specific Migration

### For AI MUD Visualizer Project

Your project already has a well-structured spec kit setup. Migration is straightforward:

1. **No spec changes needed** - Your specs/ directory is compatible
2. **Update AGENTS.md** - Add Hermes Agent workflow instructions
3. **Create skills** - Install the spec-kit-* skills
4. **Test workflow** - Verify skills work with existing specs

### Existing Spec Analysis

```
specs/002-llm-world-generation/
  - spec.md ✓
  - research.md ✓
  - data-model.md ✓
  - quickstart.md ✓
  - checklists/spec-quality.md ✓

specs/003-procedural-world-generation/
  - spec.md ✓
  - plan.md ✓
  - research.md ✓
  - data-model.md ✓
  - tasks.md ✓
  - quickstart.md ✓
  - checklists/ ✓
  - contracts/ ✓

specs/004-scenario-location-quality/
  - spec.md ✓
  - plan.md ✓
  - research.md ✓
  - data-model.md ✓
  - tasks.md ✓
  - quickstart.md ✓
  - checklists/ ✓
  - contracts/ ✓

specs/005-scene-cluster-backbone/
  - plan.md ✓
  - research.md ✓
  - data-model.md ✓

specs/006-multi-layered-visualizer/
  - spec.md ✓
  - plan.md ✓
  - research.md ✓
  - data-model.md ✓
  - tasks.md ✓
  - quickstart.md ✓
  - checklists/ ✓
```

All existing specs are compatible with Hermes Agent skills.

## Rollback Plan

If migration doesn't work:

1. **Keep .clinerules/ and .specify/** - Don't delete originals
2. **Test incrementally** - Migrate one feature at a time
3. **Fallback to OpenCode** - Original workflow still works
4. **Hybrid approach** - Use both systems during transition

## Support

- **Hermes Agent Docs**: https://hermes-agent.nousresearch.com/docs
- **Skill Authoring**: Use `skill_view(name='hermes-agent-skill-authoring')`
- **Original Spec Kit**: https://github.com/JRedeker/cline-spec-kit-workflows
