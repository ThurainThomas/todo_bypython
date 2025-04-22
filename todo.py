tasks = []  # Task list


def show_tasks():
    """Display all tasks."""
    if not tasks:
        print("\n📌 No tasks available!")
    else:
        print("\n📋 Your Tasks:")
        for index, task in enumerate(tasks, start=1):
            print(f"{index}. {task}")


def add_task():
    """Add a new task."""
    task = input("Enter a new task: ")
    tasks.append(task)
    print(f"✅ '{task}' added to the list!")


def delete_task():
    """Delete a task by index."""
    show_tasks()
    try:
        task_no = int(input("Enter task number to delete: ")) - 1
        if 0 <= task_no < len(tasks):
            removed_task = tasks.pop(task_no)
            print(f"❌ '{removed_task}' removed from the list!")
        else:
            print("⚠ Invalid task number!")
    except ValueError:
        print("⚠ Please enter a valid number!")


def edit_task():
    """Edit an existing task."""
    show_tasks()
    try:
        task_no = int(input("Enter task number to edit: ")) - 1
        if 0 <= task_no < len(tasks):
            new_task = input("Enter the new task: ")
            old_task = tasks[task_no]
            tasks[task_no] = new_task
            print(f"✏️ '{old_task}' updated to '{new_task}'")
        else:
            print("⚠ Invalid task number!")
    except ValueError:
        print("⚠ Please enter a valid number!")


while True:
    print("\n📌 To-Do List Menu:")
    print("1️⃣ View Tasks")
    print("2️⃣ Add Task")
    print("3️⃣ Delete Task")
    print("4️⃣ Edit Task")
    print("5️⃣ Exit")

    choice = input("Choose an option (1-5): ")

    if choice == "1":
        show_tasks()
    elif choice == "2":
        add_task()
    elif choice == "3":
        delete_task()
    elif choice == "4":
        edit_task()
    elif choice == "5":
        print("👋 Exiting To-Do List... Have a productive day!")
        break
    else:
        print("⚠ Invalid choice! Please select a valid option.")
