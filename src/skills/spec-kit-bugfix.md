---
name: spec-kit-bugfix
description: Alias for bugfix routing. Routes to spec-kit-workflow. Do NOT use this skill directly — load spec-kit-workflow instead.
version: 1.0.0
category: software-development
metadata:
  hermes:
    tags: [spec, workflow, routing, bugfix]
    related_skills: [spec-kit-workflow]
---

# spec-kit-bugfix

This is an alias skill. Bugfix routing is handled by `spec-kit-workflow`.

**Do NOT execute anything from this skill.** Load `spec-kit-workflow` instead:

```
skill_view(name='spec-kit-workflow')
```

Then follow the Bugfix Routing section in that skill.

## Why this exists

Hermes may resolve the user's natural language "bugfix" or "bugfixing" to a skill
named `spec-kit-bugfix`. This alias catches that dispatch and redirects to the
actual workflow orchestrator where all bugfix routing logic lives.
