# Automation Patterns

This document covers automation patterns for the Hermes Spec Kit workflow, including cron jobs, delegation strategies, and maintenance automation.

## Cron Job Patterns

### Spec Completeness Monitor

Checks all spec directories for completeness and reports missing artifacts.

```yaml
# hermes cron create
# Name: spec-completeness-check
# Schedule: every 24h
# Prompt: |
#   Analyze the specs/ directory structure in the current project.
#   For each spec directory, check for required files:
#   - spec.md (Phase 1)
#   - plan.md (Phase 3)
#   - research.md (Phase 3)
#   - data-model.md (Phase 3)
#   - tasks.md (Phase 4)
#   - checklists/ directory
#   
#   Report:
#   1. Specs with all artifacts present
#   2. Specs with missing artifacts (list what's missing)
#   3. Specs that appear incomplete or abandoned
#   4. Recommendations for next steps
```

### AGENTS.md Maintenance

Automatically updates the SPECKIT section in AGENTS.md.

```yaml
# hermes cron create
# Name: agents-md-update
# Schedule: every 12h
# Prompt: |
#   Read AGENTS.md and check the SPECKIT section.
#   Compare with actual files in specs/ directory.
#   Update the SPECKIT section to include:
#   - All current spec plan.md files
#   - All current spec research.md files
#   - All current spec data-model.md files
#   - All current spec contract files
#   Preserve manual content outside SPECKIT markers.
```

### Task Progress Tracker

Reports on implementation progress across all specs.

```yaml
# hermes cron create
# Name: task-progress-report
# Schedule: every 12h
# Prompt: |
#   Check all tasks.md files in specs/ directories.
#   For each spec with tasks.md:
#   - Count total tasks
#   - Count completed tasks (marked with [X])
#   - Count pending tasks (marked with [ ])
#   - Calculate completion percentage
#   - Identify current phase
#   
#   Report summary table and highlight specs blocked or stalled.
```

### Constitution Compliance Check

Validates new specs against project constitution.

```yaml
# hermes cron create
# Name: constitution-check
# Schedule: every 24h
# Prompt: |
#   Read specs/constitution.md (if exists).
#   For each recent spec (created in last 7 days):
#   - Check plan.md constitution check section
#   - Verify all principles addressed
#   - Flag any violations without justification
#   
#   Report compliance status and any issues found.
```

## Delegation Patterns

### Parallel Research Delegation

When creating a plan, research multiple topics simultaneously:

```python
delegate_task(
  tasks=[
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
  ]
)
```

### Parallel Implementation Delegation

When implementing independent user stories:

```python
delegate_task(
  tasks=[
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
  ]
)
```

### Spec Quality Review Delegation

Automated review of spec quality:

```python
delegate_task(
  goal="Review spec quality for [feature]",
  context="Read spec.md and checklists/requirements.md. Validate against quality criteria. Report issues found.",
  toolsets=["file"]
)
```

## Automation Workflow

### New Feature Automation

When a user requests a new feature, automate the initial setup:

```
User: "Create a spec for [feature]"

Agent Workflow:
1. Load spec-kit-workflow skill
2. Determine next spec number (NNN)
3. Create specs/NNN-feature-name/ directory
4. Load spec-kit-specify skill
5. Generate spec.md from user description
6. Create checklists/requirements.md
7. Validate spec quality
8. Update AGENTS.md SPECKIT section
9. Report: "Spec created at specs/NNN-feature-name/"
```

### Phase Advancement Automation

When advancing to the next phase:

```
User: "Plan [feature]"

Agent Workflow:
1. Verify spec.md exists and is complete
2. Load spec-kit-plan skill
3. Spawn parallel research subagents
4. Consolidate research into research.md
5. Generate data-model.md
6. Generate contracts/
7. Generate plan.md
8. Update AGENTS.md
9. Report: "Plan complete with all artifacts"
```

### Implementation Automation

When starting implementation:

```
User: "Implement [feature]"

Agent Workflow:
1. Verify tasks.md exists
2. Check checklists status
3. Load spec-kit-implement skill
4. Find next incomplete task
5. If test task: write failing test
6. If implementation task: implement feature
7. Run tests
8. Update tasks.md
9. Repeat until phase complete
10. Report progress
```

## Maintenance Automation

### Weekly Spec Health Report

```yaml
# hermes cron create
# Name: weekly-spec-health
# Schedule: 0 9 * * 1  # Monday 9am
# Prompt: |
#   Generate a weekly spec health report:
#   
#   1. Active Specs (work in progress)
#   2. Completed Specs (all tasks done)
#   3. Stalled Specs (no progress in 7+ days)
#   4. Draft Specs (only spec.md, no plan)
#   5. Constitution compliance status
#   6. Recommendations for next week
```

### Spec Archive Automation

Archive completed specs to reduce context noise:

```yaml
# hermes cron create
# Name: spec-archive-check
# Schedule: 0 9 * * 0  # Sunday 9am
# Prompt: |
#   Check for specs with all tasks completed.
#   For completed specs older than 30 days:
#   - Suggest moving to specs/archive/
#   - Update AGENTS.md to remove references
#   - Preserve spec for historical reference
```

## Integration Patterns

### Git Integration

Automate git operations with spec workflow:

```yaml
# Commit after each phase
# In skill instructions:
# After creating artifacts:
#   git add specs/NNN-feature-name/
#   git commit -m "spec: [phase] - [feature name]"
```

### CI/CD Integration

Validate specs in CI pipeline:

```yaml
# .github/workflows/spec-check.yml
# name: Spec Completeness Check
# on: [pull_request]
# jobs:
#   spec-check:
#     runs-on: ubuntu-latest
#     steps:
#       - uses: actions/checkout@v4
#       - name: Check spec completeness
#         run: |
#           for spec_dir in specs/*/; do
#             if [ ! -f "$spec_dir/spec.md" ]; then
#               echo "Missing spec.md in $spec_dir"
#               exit 1
#             fi
#           done
```

### Project Management Integration

Sync tasks with external tools:

```yaml
# Linear integration example
# hermes cron create
# Name: sync-tasks-to-linear
# Schedule: every 6h
# Prompt: |
#   Read all tasks.md files in specs/.
#   For each incomplete task:
#   - Check if corresponding Linear issue exists
#   - Create issue if missing
#   - Update status if changed
#   Use Linear skill for API calls.
```

## Error Handling

### Failed Cron Jobs

```yaml
# On cron job failure:
# 1. Log error to ~/.hermes/cron-errors.log
# 2. Notify user with error summary
# 3. Suggest fix or manual intervention
```

### Delegation Failures

```python
# When subagent fails:
try:
  result = delegate_task(...)
except Exception as e:
  # Log error
  # Retry with adjusted parameters
  # Escalate to user if repeated failures
```

### Validation Failures

```yaml
# When checklist validation fails:
# 1. Document specific failures
# 2. Quote relevant spec sections
# 3. Suggest fixes
# 4. Block phase advancement
# 5. Ask user: "Fix issues or proceed anyway?"
```

## Performance Optimization

### Token Efficiency

- Load only relevant skills based on triggers
- Use compact memory entries
- Summarize long spec files when injecting context

### Parallel Execution

- Research tasks run in parallel
- Independent user stories implemented concurrently
- Test suites executed in parallel

### Caching

- Cache spec analysis results
- Reuse research findings across related specs
- Maintain constitution check cache

## Monitoring

### Metrics to Track

- Average time per phase
- Spec completion rate
- Checklist pass rate
- Task completion velocity
- Delegation success rate

### Alerts

- Spec stalled for > 7 days
- Checklist failures increasing
- Constitution violations detected
- Task completion rate dropping
