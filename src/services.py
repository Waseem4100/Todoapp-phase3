from typing import List
from src.models import TaskDict

# In-memory storage
tasks: List[TaskDict] = []
next_id: int = 1

def validate_title(title: str) -> bool:
    """Validates that a task title is not empty."""
    return bool(title and title.strip())

def validate_id(task_id_str: str) -> int:
    """Validates that a task ID is a valid integer."""
    try:
        return int(task_id_str)
    except ValueError:
        raise ValueError("Task ID must be a numeric value.")

def add_task(title: str) -> TaskDict:
    """Adds a new task to the in-memory storage."""
    global next_id
    if not validate_title(title):
        raise ValueError("Task title cannot be empty.")

    new_task: TaskDict = {
        "id": next_id,
        "title": title.strip(),
        "is_completed": False
    }
    tasks.append(new_task)
    next_id += 1
    return new_task

def get_tasks() -> List[TaskDict]:
    """Returns the list of all tasks."""
    return tasks

def complete_task(task_id: int) -> bool:
    """Marks a task as complete."""
    for task in tasks:
        if task["id"] == task_id:
            task["is_completed"] = True
            return True
    return False

def delete_task(task_id: int) -> bool:
    """Deletes a task from the in-memory storage."""
    global tasks
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return True
    return False
