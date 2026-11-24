import psycopg2

from Todos import get_connection

from Todos import get_connection

# 1. Database connection settings
DB_CONFIG = {
    "dbname": "todo_db",
    "user": "postgres",
    "password": "",  # <-- Change this!
    "host": "localhost",
    "port": "5432",
}


def create_connection():
    return psycopg2.connect(**DB_CONFIG)


def setup_database():
    """Creates the tasks table if it doesn't already exist."""
    query = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        is_completed BOOLEAN DEFAULT FALSE
    );
    """
    with create_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()


# --- CRUD OPERATIONS ---


def add_task(title):
    """CREATE: Adds a new task."""
    query = "INSERT INTO tasks (title) VALUES (%s);"
    with create_connection() as conn:
        with conn.cursor() as cur:
            # Using (%s,) prevents SQL injection
            cur.execute(query, (title,))
        conn.commit()
    print(f"Added: '{title}'")


def view_tasks():
    """READ: Displays all tasks ordered by ID."""
    query = "SELECT id, title, is_completed FROM tasks ORDER BY id;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            tasks = cur.fetchall()

    print("\n--- YOUR TO-DO LIST ---")
    if not tasks:
        print("No tasks found.")
    else:
        for task_id, title, is_completed in tasks:
            status = "✓" if is_completed else " "
            print(f"{task_id}. [{status}] {title}")
    print("-----------------------\n")


def complete_task(task_id):
    """UPDATE: Marks a task as completed."""
    query = "UPDATE tasks SET is_completed = TRUE WHERE id = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (task_id,))
            if cur.rowcount == 0:
                print("Task ID not found.")
            else:
                print(f"Task {task_id} marked as complete!")
        conn.commit()


def delete_task(task_id):
    """DELETE: Removes a task from the database."""
    query = "DELETE FROM tasks WHERE id = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (task_id,))
            if cur.rowcount == 0:
                print("Task ID not found.")
            else:
                print(f"Task {task_id} deleted.")
        conn.commit()


# --- MAIN APPLICATION LOOP ---


def main():
    setup_database()

    while True:
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("\nChoose an option (1-5): ").strip()

        if choice == "1":
            view_tasks()
        elif choice == "2":
            title = input("Enter task description: ").strip()
            if title:
                add_task(title)
        elif choice == "3":
            view_tasks()
            task_id = input("Enter the ID of the task to complete: ").strip()
            if task_id.isdigit():
                complete_task(int(task_id))
        elif choice == "4":
            view_tasks()
            task_id = input("Enter the ID of the task to delete: ").strip()
            if task_id.isdigit():
                delete_task(int(task_id))
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()
