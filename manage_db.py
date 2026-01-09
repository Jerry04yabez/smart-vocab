import sqlite3
import sys
import os

DB_PATH = 'users.db'

def get_connection():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file '{DB_PATH}' not found.")
        sys.exit(1)
    return sqlite3.connect(DB_PATH)

def run_query(query, args=()):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, args)
            conn.commit()
            
            # If it's a select query (basic check), print results
            if query.strip().lstrip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                if rows:
                    # Get column names
                    col_names = [description[0] for description in cursor.description]
                    print(f"{' | '.join(col_names)}")
                    print("-" * 40)
                    for row in rows:
                        print(row)
                    print(f"\nTotal rows: {len(rows)}")
                else:
                    print("No results found.")
            else:
                print(f"Operation successful. Rows affected: {cursor.rowcount}")
    except Exception as e:
        print(f"Error executing query: {e}")

def delete_user(email):
    print(f"Attempting to delete user with email: {email}")
    # Check if user exists first
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if not row:
            print(f"User with email '{email}' not found.")
            return
        user_id = row[0]
        
    print(f"Found user_id: {user_id}. Deleting data...")
    run_query("DELETE FROM user_words WHERE user_id = ?", (user_id,))
    run_query("DELETE FROM user_stats WHERE user_id = ?", (user_id,))
    run_query("DELETE FROM users WHERE id = ?", (user_id,))
    print("User deletion complete.")

def clear_table(table_name):
    allowed_tables = ['users', 'user_words', 'user_stats']
    if table_name not in allowed_tables:
        print(f"Error: Table '{table_name}' is not in the allowed list: {allowed_tables}")
        return

    confirm = input(f"WARNING: Are you sure you want to delete ALL data from table '{table_name}'? (y/n): ")
    if confirm.lower() == 'y':
        run_query(f"DELETE FROM {table_name}")
    else:
        print("Operation cancelled.")

def print_usage():
    print("""
Usage:
  python manage_db.py query "SQL_QUERY"
  python manage_db.py delete_user email@example.com
  python manage_db.py clear_table table_name
  python manage_db.py help

Examples:
  python manage_db.py query "SELECT * FROM users"
  python manage_db.py delete_user test@example.com
  python manage_db.py clear_table user_words
    """)

def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()

    if command == "query":
        if len(sys.argv) < 3:
            print("Error: Missing SQL query.")
            print('Usage: python manage_db.py query "SELECT * FROM users"')
        else:
            run_query(sys.argv[2])
    elif command == "delete_user":
        if len(sys.argv) < 3:
            print("Error: Missing email address.")
            print('Usage: python manage_db.py delete_user email@example.com')
        else:
            delete_user(sys.argv[2])
    elif command == "clear_table":
        if len(sys.argv) < 3:
            print("Error: Missing table name.")
            print('Usage: python manage_db.py clear_table table_name')
        else:
            clear_table(sys.argv[2])
    elif command == "help":
        print_usage()
    else:
        print(f"Unknown command: {command}")
        print_usage()

if __name__ == "__main__":
    main()
