# Automation Patterns

This document covers automation patterns for the Hermes Spec Kit workflow, including cron jobs, delegation strategies, and maintenance automation.

## Cron Job Patterns

All cron jobs are created using the `cronjob` tool (action='create'). These examples show the `prompt` and `schedule` fields as used with that tool.

### Spec Completeness Monitor

Checks all spec directories for completeness and reports missing artifacts.

```
cronjob(action='create', name='spec-completeness-check', schedule='every 24h', prompt='...')
```

**Prompt content:**
```
Analyze the specs/ directory structure in the current project.
For each spec directory, check for required files:
- spec.md
- plan.md
- research.md
- data-model.md
- tasks.md

Report:
1. Specs with all artifacts present
2. Specs with missing artifacts (list what's missing)
3. Specs that appear incomplete or abandoned
4. Recommendations for next steps
```

### AGENTS.md Reference

AGENTS.md is a project-level context file for Hermes Agent. It is read automatically on every message. Spec-kit does NOT auto-update AGENTS.md — manual updates only.

When creating a project, copy `src/templates/AGENTS-template.md` to the project root as a starting point. Maintain the SPECKIT section manually as specs progress.

```
cp ~/.hermes/skills/spec-kit/templates/AGENTS-template.md /path/to/project/AGENTS.md
```

### Task Progress Tracker

Reports on implementation progress across all specs.

```
cronjob(action='create', name='task-progress-report', schedule='every 12h', prompt='...')
```

**Prompt content:**
```
Check all tasks.md files in specs/ directories.
For each spec with tasks.md:
- Count total tasks
- Count completed tasks (marked with [X])
- Count pending tasks (marked with [ ])
- Calculate completion percentage

Report summary table and highlight stalled specs.
```

## Delegation Patterns

### Parallel Research Delegation

When creating a plan, research multiple topics simultaneously:

```python
delegate_task(tasks=[
  {
    "goal": "Research technology A for [feature]",
    "context": "Read spec.md section on [topic]. Research best practices, alternatives, and trade-offs. Return findings for research.md.",
    "toolsets": ["web", "file"]
  },
  {
    "goal": "Research technology B for [feature]",
    "context": "Read spec.md section on [topic]. Research best practices, alternatives, and trade-offs. Return findings for research.md.",
    "toolsets": ["web", "file"]
  },
  {
    "goal": "Analyze existing codebase for [feature]",
    "context": "Scan project structure. Identify existing code that relates to [feature]. Note patterns, conventions, and integration points.",
    "toolsets": ["file", "terminal"]
  }
])
```

### Parallel Implementation Delegation

When implementing independent user stories:

```python
delegate_task(tasks=[
  {
    "goal": "Implement User Story 1 for [feature]",
    "context": "Read tasks.md, find US1 tasks. Follow TDD: write tests first, then implement. Update tasks.md with completion status.",
    "toolsets": ["file", "terminal"]
  },
  {
    "goal": "Implement User Story 2 for [feature]",
    "context": "Read tasks.md, find US2 tasks. Follow TDD: write tests first, then implement. Update tasks.md with completion status.",
    "toolsets": ["file", "terminal"]
  }
])
```

### Spec Quality Review Delegation

Optional review of spec quality:

```python
delegate_task(
  goal="Review spec quality for [feature]",
  context="Read spec.md. Validate against quality criteria. Report issues found.",
  toolsets=["file"]
)
```

## Automation Workflow

All phase progression is manual. The agent responds to user prompts; there are no automatic phase gates.

### New Feature Setup

When the user requests a new feature:

```
User: "Create a spec for [feature]"

Agent:
1. Load spec-kit-workflow skill
2. Determine next spec number (NNN)
3. Create specs/NNN-feature-name/ directory
4. Load spec-kit-specify skill
5. Generate spec.md from user description
6. Report: "Spec created at specs/NNN-feature-name/"
```

When the user wants to advance to the next phase:

```
User: "Plan [feature]"

Agent:
1. Load spec-kit-plan skill
2. Read spec.md to understand the feature
3. Generate research.md (optional — user may skip)
4. Generate data-model.md (optional)
5. Generate plan.md
6. Report: "Plan complete"
```

### Implementation

When starting implementation:

```
User: "Implement [feature]"

Agent:
1. Load spec-kit-implement skill
2. Read tasks.md
3. Find next incomplete task
4. If test task: write failing test
5. If implementation task: implement feature
6. Run tests
7. Update tasks.md
8. Repeat until user stops or all tasks done
9. Report progress
```

## Maintenance Automation

### Weekly Spec Health Report

```
cronjob(action='create', name='weekly-spec-health', schedule='0 9 * * 1', prompt='...')
```

**Prompt content:**
```
Generate a weekly spec health report:

1. Active Specs (work in progress)
2. Completed Specs (all tasks done)
3. Stalled Specs (no progress in 7+ days)
4. Draft Specs (only spec.md, no plan)
5. Recommendations for next week
```

## Integration Patterns

### Git Integration

Each phase can create commits. After creating artifacts:

```
git add specs/NNN-feature-name/
git commit -m "spec: [phase] - [feature name]"
```

### CI/CD Integration

Validate spec completeness in CI:

```yaml
# .github/workflows/spec-check.yml
name: Spec Completeness Check
on: [pull_request]
jobs:
  spec-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check spec completeness
        run: |
          for spec_dir in specs/*/; do
            if [ ! -f "$spec_dir/spec.md" ]; then
              echo "Missing spec.md in $spec_dir"
              exit 1
            fi
          done
```

## Error Handling

### Failed Cron Jobs

On cron job failure:
1. Log error
2. Notify user with error summary
3. Suggest fix or manual intervention

### Delegation Failures

When a subagent fails:
1. Log error
2. Retry with adjusted parameters
3. Escalate to user if repeated failures

## Performance Optimization

### Token Efficiency

- Load only relevant skills based on triggers
- Use compact memory entries
- Summarize long spec files when injecting context

### Parallel Execution

- Research tasks run in parallel
- Independent user stories implemented concurrently
- Test suites executed in parallel

## Monitoring

### Metrics to Track

- Average time per phase
- Spec completion rate
- Task completion velocity
- Delegation success rate

### Alerts

- Spec stalled for > 7 days
- Constitution violations detected
- Task completion rate dropping