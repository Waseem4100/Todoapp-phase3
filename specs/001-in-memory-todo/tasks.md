# Tasks: Basic In-Memory Todo (Console)

**Input**: Design documents from `/specs/001-in-memory-todo/`
**Prerequisites**: plan.md (required), spec.md (required)

## Phase 1: Setup & Initialization

**Purpose**: Project structure and tool configuration

- [x] T001 Create project structure: `src/main.py`, `src/models.py`, `src/services.py`, `tests/` per implementation plan
- [x] T002 Initialize Python project and configure basic linting/formatting (Standard Library only)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data structures and logic that underpin all operations

- [x] T003 Implement Task data model in `src/models.py` (dictionary definition or simple class)
- [x] T004 Setup in-memory task list and `next_id` counter in `src/services.py`
- [x] T005 Implement basic input validation utility in `src/services.py` (empty check, type conversion)

---

## Phase 3: User Story 1 & 2 - Task Creation & Listing (Priority: P1) 🎯 MVP

**Goal**: Enable core Add and View functionality

### Implementation for User Story 1 & 2

- [x] T006 Implement `add_task(title)` in `src/services.py` with unique ID generation
- [x] T007 Implement `view_tasks()` in `src/services.py` returning list of tasks
- [x] T008 Implement CLI menu loop in `src/main.py` with options for Add and View
- [x] T009 Connect CLI Add/View options to service functions in `src/main.py`

**Checkpoint**: User can run `main.py`, add tasks, and view them in the console.

---

## Phase 4: User Story 3 - Status Completion (Priority: P2)

**Goal**: Enable marking tasks as complete

### Implementation for User Story 3

- [x] T010 Implement `complete_task(task_id)` service in `src/services.py`
- [x] T011 Add "Complete Task" option to CLI menu in `src/main.py`
- [x] T012 Implement ID prompt and service call for completion in `src/main.py`

**Checkpoint**: User can mark existing tasks as complete by ID.

---

## Phase 5: User Story 4 - Task Deletion (Priority: P3)

**Goal**: Enable removing tasks

### Implementation for User Story 4

- [x] T013 Implement `delete_task(task_id)` service in `src/services.py`
- [x] T014 Add "Delete Task" option to CLI menu in `src/main.py`
- [x] T015 Implement ID prompt and service call for deletion in `src/main.py`

**Checkpoint**: User can delete tasks from the in-memory list by ID.

---

## Phase 6: Polish & Error Handling

**Purpose**: Ensure robustness and user-friendly experience

- [x] T016 Implement comprehensive error messages for invalid task IDs (not found, non-numeric)
- [x] T017 Implement guard for empty task list (View/Complete/Delete should handle gracefully)
- [x] T018 Implement guard for empty task titles during creation
- [x] T019 Implement "Exit" functionality for clean termination

---

## Phase 7: Verification (Optional Testing)

**Purpose**: Validate implementation against specification

- [ ] T020 (Optional) Implement unit tests in `tests/unit/test_services.py` for CRUD logic
- [ ] T021 (Optional) Implement integration tests in `tests/integration/test_cli.py` for flow validation

---

## Dependencies & Execution Order

- **Phase 1 & 2**: MUST be completed first.
- **Phase 3 (MVP)**: Must be completed before Phase 4 or 5.
- **Phase 4 & 5**: Can proceed after Phase 3, ideally in priority order (P2 then P3).
- **Phase 6**: Can be integrated during user story completion or as a final polish pass.
- **Phase 7**: Runs after implementation to verify correctness.
