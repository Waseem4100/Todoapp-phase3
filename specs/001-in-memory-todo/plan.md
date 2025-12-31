# Implementation Plan: 001-in-memory-todo

**Branch**: `001-in-memory-todo` | **Date**: 2025-12-31 | **Spec**: [specs/001-in-memory-todo/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-in-memory-todo/spec.md`

## Summary

Phase I focuses on delivering a basic, in-memory, single-user Todo application as a Python console program. The implementation will use a simple menu-driven CLI, standard Python list/dictionary structures for task management, and will not include any persistence or external dependencies, ensuring compliance with Phase I scope.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: None (Standard Library only)
**Storage**: In-memory list of dictionaries
**Testing**: pytest (if requested for verification)
**Target Platform**: CLI/Console
**Project Type**: Single project
**Performance Goals**: Instantaneous user interaction (<100ms)
**Constraints**: No persistence, no external libraries, no future-phase abstractions.
**Scale/Scope**: Single-user, transient runtime state.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Article I Compliance**: Does this plan stem from an approved Spec? (Yes)
- [x] **Article III Compliance**: Does this plan strictly adhere to the current Phase scope? (Yes)
- [x] **Article IV Compliance**: Does the proposed stack stick to Python/FastAPI/SQLModel/Neon? (Python used, FastAPI/SQLModel deferred to later phases as per spec)
- [x] **Article V Compliance**: Does the design follow Clean Architecture and SoC? (Yes)

## Project Structure

### Documentation (this feature)

```text
specs/001-in-memory-todo/
├── plan.md              # This file
├── spec.md              # Feature specification
└── tasks.md             # Task list (to be created)
```

### Source Code (repository root)

```text
src/
├── main.py             # Entry point and CLI loop
├── models.py           # Task data structure
└── services.py         # Business logic (CRUD operations)

tests/
├── integration/
│   └── test_cli.py     # End-to-end flow tests
└── unit/
    └── test_services.py # Logic tests
```

## Data Management

### Task Structure (In-Memory)
- `tasks`: A list of dictionaries.
- `next_id`: An integer counter starting at 1.

### Example Task Object
```python
{
    "id": 1,
    "title": "Sample Task",
    "is_completed": False
}
```

## Logic Flow

1. **Initialization**: Clear task list, set `next_id = 1`.
2. **Main Loop**:
   - Display menu: 1. Add, 2. View, 3. Complete, 4. Delete, 5. Exit.
   - Capture choice.
   - Redirect to corresponding service function.
3. **Services**:
   - `add_task(title)`: Validates title, creates task, increments ID.
   - `view_tasks()`: Returns formatted list of all tasks.
   - `complete_task(id)`: Validates existence, toggles `is_completed`.
   - `delete_task(id)`: Validates existence, removes from list.

## Error Handling

- **Non-numeric ID**: Try/Except blocks for `int()` conversion.
- **Missing ID**: Check list for existence before operating.
- **Empty Title**: Guard clause in `add_task`.
- **Invalid Menu Choice**: Default case in loop.

## Implementation Boundaries

- **Explicitly Not Included**: File saving, database connection, web server, REST API.
- **Next Phase Preparation**: None. Code will be self-contained and minimal.

---

📋 Architectural decision detected: Single-file vs Multi-file structure.
Decision: Multi-file (main, models, services) to adhere to Article V (Separation of Concerns and Clean Architecture) from the start.
Document reasoning and tradeoffs? Run `/sp.adr architecture-separation-phase-i`
