import os
import psycopg2
import sys
from dotenv import load_dotenv

load_dotenv() 
def create_connection():
    try:
        db_url = os.getenv("DB_URL")
        if not db_url:
            raise ValueError("DB_URL not found in .env file.")
            
        connection = psycopg2.connect(db_url)
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


def execute_query(query, params=None, fetch=False):
    """Safely handles connection, execution, commits, and closing."""
    conn = create_connection()
    if conn is None:
        print("Database operation skipped due to connection failure.\n")
        return None

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if fetch:
                    return cur.fetchall()
                return cur.rowcount
    finally:
        conn.close()


def setup_database():
    """Creates the tasks table if it doesn't already exist."""
    query = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        is_completed BOOLEAN DEFAULT FALSE
    );
    """
    result = execute_query(query)
    if result is None:
        print("Could not initialize database. Exiting...")
        sys.exit(1)


# --- CRUD OPERATIONS ---


def add_task(title):
    """CREATE: Adds a new task."""
    query = "INSERT INTO tasks (title) VALUES (%s);"
    if execute_query(query, (title,)) is not None:
        print(f"Added: '{title}'\n")


def view_tasks():
    """READ: Displays all tasks ordered by ID."""
    query = "SELECT id, title, is_completed FROM tasks ORDER BY id;"
    tasks = execute_query(query, fetch=True)
    
    if tasks is None:
        return

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
    rows_affected = execute_query(query, (task_id,))
    if rows_affected is not None:
        if rows_affected == 0:
            print("Task ID not found.\n")
        else:
            print(f"Task {task_id} marked as complete!\n")


def delete_task(task_id):
    """DELETE: Removes a task from the database."""
    query = "DELETE FROM tasks WHERE id = %s;"
    rows_affected = execute_query(query, (task_id,))
    if rows_affected is not None:
        if rows_affected == 0:
            print("Task ID not found.\n")
        else:
            print(f"Task {task_id} deleted.\n")


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
