# Feature Specification: Basic In-Memory Todo (Console)

**Feature Branch**: `001-in-memory-todo`
**Created**: 2025-12-31
**Status**: Draft
**Input**: Phase I Specification for the "Evolution of Todo" project.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Task Creation (Priority: P1)

As a user, I want to create new tasks so I can track what I need to do.

**Why this priority**: Essential for a todo application; without creation, the app provides no value.

**Independent Test**: Can be tested by adding a task and then selecting the "View Tasks" option to see if it appears.

**Acceptance Scenarios**:

1. **Given** the application is running, **When** I choose "Add Task" and enter "Buy milk", **Then** the task is added to my in-memory list.
2. **Given** the application is running, **When** I choose "Add Task" and enter an empty title, **Then** the system displays an error and rejects the input.

---

### User Story 2 - Task Listing (Priority: P1)

As a user, I want to view all my tasks so I can see my progress.

**Why this priority**: Core functionality; required to verify all other operations (add, update, delete).

**Independent Test**: Can be tested by adding multiple tasks and selecting "View Tasks" to see them displayed with their IDs.

**Acceptance Scenarios**:

1. **Given** I have added two tasks, **When** I select "View Tasks", **Then** I see both tasks with numerical IDs and status indicators.
2. **Given** I have no tasks, **When** I select "View Tasks", **Then** the system displays "No tasks found".

---

### User Story 3 - Task Status Completion (Priority: P2)

As a user, I want to mark tasks as complete so I can track my finished work.

**Why this priority**: Primary workflow after task creation.

**Independent Test**: Can be tested by adding a task, marking it complete by ID, and then viewing the list to check the status indicator.

**Acceptance Scenarios**:

1. **Given** I have a task with ID 1 marked as "Pending", **When** I choose "Complete Task" and enter "1", **Then** the status of task 1 changes to "Complete".
2. **Given** the task list is empty, **When** I choose "Complete Task", **Then** the system informs me no tasks exist and returns to the menu.

---

### User Story 4 - Task Deletion (Priority: P3)

As a user, I want to delete tasks so I can remove items I no longer need to track.

**Why this priority**: Basic CRUD operation for list maintenance.

**Independent Test**: Can be tested by adding a task, deleting it by ID, and verifying it no longer appears in the list.

**Acceptance Scenarios**:

1. **Given** I have a task with ID 1, **When** I choose "Delete Task" and enter "1", **Then** the task is permanently removed from the list.
2. **Given** I enter a non-existent task ID for deletion, **When** I submit the ID, **Then** the system displays a clear error message and returns to the menu.

---

### Edge Cases

- **Invalid Task ID**: Non-numeric IDs or IDs that do not exist in the current list are handled gracefully with an error message and no system crash.
- **Empty Task List**: Operations requiring an ID (complete/delete) are blocked when the list is empty, informing the user instead.
- **Invalid Menu Input**: Entering a string or a number outside the menu options returns the user to the menu with an error message.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a menu-driven interface for: Add Task, View Tasks, Complete Task, Delete Task, and Exit.
- **FR-002**: System MUST store tasks in-memory only (duration of runtime).
- **FR-003**: System MUST assign a unique numerical ID to each task created.
- **FR-004**: System MUST validate that task titles are not empty.
- **FR-005**: System MUST display task status (e.g., [ ] for Pending, [X] for Complete).
- **FR-006**: System MUST reject non-numeric task ID inputs for completion and deletion.

### Key Entities

- **Task**: Represents a single item of work.
  - `id`: (Integer) Unique identifier.
  - `title`: (String) Small description of the task.
  - `is_completed`: (Boolean) Status of the task.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of CRUD operations (Add, View, Complete, Delete) function as specified without persistence.
- **SC-002**: System response to menu selection and data entry is instantaneous (<100ms).
- **SC-003**: System handles invalid inputs (empty titles, bad IDs) without crashing 100% of the time.
- **SC-004**: Users can complete a task addition journey (Menu -> Add -> Input -> Menu) in under 10 seconds.
