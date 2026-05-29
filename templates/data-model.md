# Data Model: [Feature Name]

**Feature**: [Link to spec.md]
**Date**: [DATE]

## Overview

[Brief description of the data model and its purpose]

## Entities

### [Entity Name]

**Purpose**: [What this entity represents in the domain]

**Fields**:
| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `id` | string | Yes | Unique identifier | UUID v4 |
| `name` | string | Yes | Human-readable name | Max 255 chars |
| `created_at` | timestamp | Yes | Creation timestamp | Auto-generated |
| `updated_at` | timestamp | Yes | Last update timestamp | Auto-updated |

**Relationships**:
- **[Entity]** → **[Entity]**: [one-to-many / many-to-one / many-to-many]
- **[Entity]** → **[Entity]**: [relationship type]

**Validation Rules**:
- [Rule]: [Description of validation]
- [Rule]: [Description of validation]

**State Transitions** (if applicable):
- [State] → [State]: [Trigger/Condition]
- [State] → [State]: [Trigger/Condition]

**Indexes**:
- `field_name`: [unique / composite / standard]

---

### [Entity Name]

**Purpose**: [What this entity represents]

**Fields**:
| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `id` | string | Yes | Unique identifier | UUID v4 |
| ... | ... | ... | ... | ... |

**Relationships**:
- [...]

**Validation Rules**:
- [...]

**State Transitions**:
- [...]

---

## Entity Relationship Diagram

```
[Entity A] 1───────* [Entity B]
   │
   │ *
   └────────────── [Entity C]
```

## Data Flow

[Description of how data moves through the system]

### Ingestion
- [How data enters the system]

### Processing
- [How data is transformed]

### Storage
- [How data is persisted]

### Retrieval
- [How data is queried and returned]

## Migration Considerations

- [Backward compatibility notes]
- [Data migration strategy]
- [Rollback plan for schema changes]

## Performance Considerations

- [Query optimization strategies]
- [Caching strategy]
- [Partitioning/sharding if applicable]
