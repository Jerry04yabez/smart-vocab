import sqlite3
import os
from werkzeug.security import generate_password_hash
from contextlib import closing

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def create_manual_user():
    print("--- Manual User Registration ---")
    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip().lower()
    password = input("Enter password: ").strip()

    if not name or not email or not password:
        print("Error: All fields are required.")
        return

    password_hash = generate_password_hash(password)

    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, password_hash),
            )
            conn.commit()
            print(f"Success! User '{name}' ({email}) registered with ID {cursor.lastrowid}.")
    except sqlite3.IntegrityError:
        print("Error: Email already registered.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        print("Please run app.py at least once to initialize the database.")
    else:
        create_manual_user()
