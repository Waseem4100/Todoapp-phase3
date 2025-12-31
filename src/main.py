import sys
from src.services import add_task, get_tasks, complete_task, delete_task, validate_id

def display_menu():
    print("\n--- Evolution of Todo (Phase I) ---")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")

def run_add_task():
    title = input("Enter task title: ")
    try:
        task = add_task(title)
        print(f"Task added successfully! (ID: {task['id']})")
    except ValueError as e:
        print(f"Error: {e}")

def run_view_tasks():
    tasks = get_tasks()
    if not tasks:
        print("No tasks found.")
        return

    print("\nYour Tasks:")
    for task in tasks:
        status = "[X]" if task["is_completed"] else "[ ]"
        print(f"{task['id']}. {status} {task['title']}")

def run_complete_task():
    tasks = get_tasks()
    if not tasks:
        print("No tasks found. Add a task first.")
        return

    task_id_str = input("Enter task ID to mark as complete: ")
    try:
        task_id = validate_id(task_id_str)
        if complete_task(task_id):
            print(f"Task {task_id} marked as complete!")
        else:
            print(f"Error: Task ID {task_id} not found.")
    except ValueError as e:
        print(f"Error: {e}")

def run_delete_task():
    tasks = get_tasks()
    if not tasks:
        print("No tasks found. Add a task first.")
        return

    task_id_str = input("Enter task ID to delete: ")
    try:
        task_id = validate_id(task_id_str)
        if delete_task(task_id):
            print(f"Task {task_id} deleted successfully!")
        else:
            print(f"Error: Task ID {task_id} not found.")
    except ValueError as e:
        print(f"Error: {e}")

def main():
    while True:
        display_menu()
        choice = input("Select an option: ")

        if choice == "1":
            run_add_task()
        elif choice == "2":
            run_view_tasks()
        elif choice == "3":
            run_complete_task()
        elif choice == "4":
            run_delete_task()
        elif choice == "5":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
