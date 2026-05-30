# System Design: Hermes Spec Kit

## Architecture Overview

The Hermes Spec Kit is built on three layers:

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  Natural language prompts → "Create a spec for..."          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     Workflow Orchestration Layer             │
│  spec-kit-workflow skill routes to phase-specific skills    │
│  Constitution → Specify → Clarify → Plan → Tasks → Implement│
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     Artifact Generation Layer                 │
│  Skills create/update markdown artifacts in specs/ dirs      │
│  Validation checklists ensure quality before phase advance   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     Automation & Memory Layer                 │
│  Cron jobs for maintenance                                   │
│  Persistent memory for project conventions                   │
│  Multi-agent delegation for parallel work                    │
└─────────────────────────────────────────────────────────────┘
```

## Component Design

### 1. Skill System

Each workflow phase is implemented as a Hermes Agent skill:

**Master Orchestrator: `spec-kit-workflow`**
- Entry point for all spec kit operations
- Routes to phase-specific skills based on user intent
- Maintains workflow state across sessions
- Validates phase completion before allowing progression

**Phase Skills:**
- `spec-kit-constitution`: Phase 0 — Project principles and constraints
- `spec-kit-specify`: Phase 1 — Feature specification creation
- `spec-kit-clarify`: Phase 2 — Ambiguity resolution (optional)
- `spec-kit-plan`: Phase 3 — Implementation planning
- `spec-kit-tasks`: Phase 4 — Task breakdown generation
- `spec-kit-implement`: Phase 5 — Task execution with TDD

### 2. Artifact Structure

Each feature gets a numbered directory under `specs/`:

```
specs/
  001-feature-name/
    constitution.md      # Phase 0: Project principles (shared)
    spec.md              # Phase 1: Feature specification
    clarify.md           # Phase 2: Clarification questions (optional)
    plan.md              # Phase 3: Implementation plan
    research.md          # Phase 3: Technical research
    data-model.md        # Phase 3: Data models
    quickstart.md        # Phase 3: Integration guide
    contracts/           # Phase 3: API contracts
      api-schema.md
      data-schema.md
    checklists/          # Quality validation
      requirements.md    # Spec quality
      implementation.md  # Implementation readiness
    tasks.md             # Phase 4: Task breakdown
```

### 3. Validation System

Quality checklists are optional guides, not blocking gates:

**Requirements Checklist (spec.md)**
- No implementation details leaked
- All requirements testable
- Success criteria measurable
- Edge cases identified
- Dependencies documented

**Implementation Checklist (tasks.md)**
- All prerequisites met
- Test tasks precede implementation
- Parallel tasks marked [P]
- File paths specified

### 4. Memory Integration

Hermes Agent's persistent memory stores:
- Project conventions and standards
- Technology stack decisions
- Architecture patterns used
- User preferences for workflow

This survives across sessions, unlike context-window-only approaches.

### 5. Delegation Model

Complex phases can spawn parallel subagents:

**Research Phase:**
```
Main agent coordinates:
  Subagent 1: Research technology A
  Subagent 2: Research technology B  
  Subagent 3: Analyze existing codebase
Main agent consolidates findings into research.md
```

**Implementation Phase:**
```
Main agent validates:
  Subagent 1: Implement User Story 1 (parallel)
  Subagent 2: Implement User Story 2 (parallel)
  Subagent 3: Write integration tests
Main agent verifies and merges
```

## Data Flow

### Phase 0: Constitution
```
 constitution.md → spec-kit-constitution skill → project principles
```

### Phase 1: Specify
```
User Input → spec-kit-specify skill → spec.md
```

### Phase 2: Clarify (Optional)
```
spec.md ambiguities → spec-kit-clarify skill → clarify.md
```

### Phase 3: Plan
```
spec.md + constitution.md → spec-kit-plan skill →
  ├─ research.md
  ├─ data-model.md
  ├─ contracts/
  └─ plan.md
```

### Phase 4: Tasks
```
plan.md + spec.md → spec-kit-tasks skill → tasks.md
```

### Phase 5: Implement
```
tasks.md → spec-kit-implement skill → code changes + test results
```

## Security Considerations

### Secret Management
- Never store API keys or secrets in spec artifacts
- Use environment variables for sensitive configuration
- Validate that generated code doesn't hardcode credentials

### Input Validation
- User descriptions are treated as untrusted input
- Sanitize file paths to prevent directory traversal
- Validate markdown structure before writing

### Access Control
- Spec artifacts are project-level, not user-specific
- Constitution defines project-wide standards
- Skills can be pinned to prevent accidental modification

## Performance Considerations

### Token Efficiency
- Skills are loaded on-demand based on triggers
- Only relevant phase skills are active
- Memory is compact and focused on durable facts

### Parallel Processing
- Research tasks run in parallel via delegation
- Independent user stories implemented concurrently
- Test suites can run in parallel

### Session Management
- Phase state persists in markdown artifacts
- No reliance on context window for workflow state
- Sessions can be resumed from any phase

## Error Handling

### Missing Artifacts
- Skills check for required files before proceeding
- Clear error messages indicate what's missing
- Suggested commands to generate missing artifacts

### Inconsistent State
- Constitution check validates against project standards
- Data model consistency verified
- Contract compatibility checked

## Extensibility

### Custom Phases
New phases can be added by creating skills with the pattern:
```
spec-kit-[phase-name]
```

### Custom Checklists
Projects can define additional validation criteria in their constitution.

### Integration Hooks
- Pre-phase scripts for setup
- Post-phase scripts for cleanup
- Webhook notifications for phase completion

## Integration with Existing Tools

### Git Integration
- Each phase can create commits
- Branch naming convention: `spec/[NNN-feature-name]`
- Commit messages follow conventional format

### CI/CD Integration
- Checklists can be validated in CI
- Spec completeness as merge requirement
- Automated spec generation from PR descriptions

### Project Management
- Tasks can sync with Linear/Jira
- Progress tracking via checklist completion
- Status reports from spec directory analysis
