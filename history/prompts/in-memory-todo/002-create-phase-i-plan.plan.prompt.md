---
id: 2
title: "Create Phase I technical plan for in-memory todo"
stage: plan
date: 2025-12-31
surface: "agent"
model: "claude-sonnet-4-5"
feature: "in-memory-todo"
branch: "001-in-memory-todo"
user: "human"
command: "/sp.plan"
labels: ["plan", "architecture", "design"]
links:
  spec: "specs/001-in-memory-todo/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-in-memory-todo/plan.md
tests:
  - "Constitution check validation"
---

## Prompt

/sp.planBelow is the **Phase I Technical Plan** for the **Evolution of Todo** project.
This plan is **derived strictly from the approved Phase I Specification** and **fully compliant with the Global Constitution**.

It describes **HOW** Phase I will be implemented, without introducing any new features, concepts, or future-phase elements.

---

# Evolution of Todo

## Phase I Technical Plan — In-Memory Python Console Application

---

## 1. Plan Scope and Purpose

This plan defines the technical approach for implementing **Phase I**:

* A **single-user**
* **In-memory**
* **Python console application**

The plan covers structure, data handling, CLI flow, and error handling exactly as required by the Phase I specification.

No persistence, networking, external services, or future-phase concepts are included.

---

## 2. High-Level Application Structure

### Structure Overview

* A **single Python program** (single process, single runtime)
* Organized using **functions** and **simple data structures**
* No frameworks or external libraries

### Logical Responsibilities

The program is logically divided into:

1. **Data Management Logic**
2. **CLI / User Interaction Logic**
3. **Application Control Flow**

These divisions are conceptual and may exist within one file.

---

## 3. In-Memory Data Structures

### Task Storage

* Tasks are stored in an **in-memory list**
* Each element in the list represents one task

### Task Representation

Each task is represented using a simple structure (e.g., dictionary or lightweight object) with:

* `id` (int)
* `title` (str)
* `completed` (bool)

### Constraints

* All data exists only in memory
* Data is lost when the program exits
* No serialization or persistence logic exists

---

## 4. Task Identification Strategy

### ID Generation

* Maintain a single integer counter in memory
* Initial value starts at `1`
* Each new task receives the current counter value
* Counter increments after each task creation

### ID Rules

* IDs are unique within the runtime
* IDs are not reused after deletion
* All task operations reference tasks by ID

---

## 5. CLI Control Flow

### Menu Loop

* The application runs inside a **continuous loop**
* The loop displays a numeric menu on each iteration
* The loop exits only when the user selects “Exit”

### Menu Options

Each menu option maps directly to one feature:

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete / Incomplete
6. Exit

### Input Handling

* User input is read as strings
* Menu input is validated before execution
* Task IDs are parsed and validated before use

After each operation, control returns to the main menu.

---

## 6. Separation of Responsibilities

### Data Handling Responsibilities

Functions responsible for:

* Creating tasks
* Retrieving task lists
* Finding tasks by ID
* Updating task fields
* Deleting tasks
* Toggling completion status

These functions operate only on in-memory data structures.

### CLI Responsibilities

Functions responsible for:

* Displaying menus
* Prompting for user input
* Displaying tasks and messages
* Displaying errors and confirmations

### Control Flow Responsibilities

* Route user menu selections to the correct operation
* Ensure invalid input does not crash the application
* Maintain the main application loop

---

## 7. Error Handling Strategy

### Invalid Menu Input

* Non-numeric input is rejected
* Numbers outside valid menu range are rejected
* User is shown an error message and returned to menu

### Empty Task List

* Operations requiring tasks first check if the task list is empty
* If empty, a message is displayed and no ID is requested

### Invalid Task ID

* Task lookup validates existence
* If ID is not found:

  * Display a clear error message
  * Do not modify data
  * Return to main menu

### Invalid Task Title

* Empty titles are rejected
* User is prompted to re-enter or returned to menu

---

## 8. Implementation Boundaries

### Explicitly Not Included

* File I/O
* Databases
* APIs
* Authentication
* Logging systems
* Configuration files
* Future extensibility hooks

The implementation is intentionally minimal and scoped strictly to Phase I.

---

## 9. Plan Completion Criteria

This plan is complete when:

* All Phase I features are mapped to implementation steps
* No new features or abstractions are introduced
* All constraints are respected
* The plan aligns fully with the Phase I specification

---

### Final Statement

This technical plan defines **HOW Phase I will be implemented** and **does not alter WHAT Phase I delivers**.

All implementation tasks must derive directly from this plan.
Any deviation requires a specification update.

## Response snapshot

Established the Phase I technical plan for the in-memory todo application. Defined the application structure using Clean Architecture principles (Separation of Concerns between CLI, services, and models). Mapped all functional requirements to in-memory data structures and controlled CLI flow. Ensured strict adherence to Article III (No future-phase leakage).

## Outcome

- ✅ Impact: High. Provides the technical roadmap for implementation.
- 🧪 Tests: Constitution check passed.
- 📁 Files: specs/001-in-memory-todo/plan.md
- 🔁 Next prompts: Run /sp.tasks to generate the implementation task list.
- 🧠 Reflection: Choosing a multi-file structure even for a simple Phase I app ensures the project starts with the Clean Architecture standards required by Article V.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
