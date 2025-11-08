#!/usr/bin/env python3
"""
PostgreSQL CRUD demo app for the 'students' table, with extra connection diagnostics.

Functions:
- get_all_students(conn)
- add_student(conn, first_name, last_name, email, enrollment_date)
- update_student_email(conn, student_id, new_email)
- delete_student(conn, student_id)

Run:
  python app.py
"""

import os
import sys

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

# Load environment variables from .env
load_dotenv()

def _dsn_from_env():
    host = os.getenv("PGHOST")
    port = os.getenv("PGPORT")
    db   = os.getenv("PGDATABASE")
    user = os.getenv("PGUSER")
    pwd  = os.getenv("PGPASSWORD")
    return host, port, db, user, pwd

def connect():
    """Connect using values from .env and print helpful diagnostics."""
    host, port, db, user, pwd = _dsn_from_env()
    try:
        print("Attempting connection with:")
        print(f"  Host={host}  Port={port}  DB={db}  User={user}")
        conn = psycopg2.connect(
            host=host, port=int(port), dbname=db, user=user, password=pwd
        )
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("SHOW server_version;")
            ver = cur.fetchone()[0]
            print(f"Connected! PostgreSQL server_version = {ver}")
        return conn
    except Exception as e:
        print("\nDatabase connection failed.")
        print(f"Tried: Host={host}  Port={port}  DB={db}  User={user}")
        print("Common fixes on Windows:")
        print("  • Ensure 'PostgreSQL 18' service is running (services.msc).")
        print("  • Verify the actual port in pgAdmin: Server > Properties > Connection.")
        print("  • If your server uses 5433 (common), set PGPORT=5433 in .env.")
        print("  • Reset password in pgAdmin Query Tool if needed:")
        print("      ALTER USER postgres WITH PASSWORD 'your_password';")
        print(f"Raw error: {e!r}")
        sys.exit(1)

def get_all_students(conn):
    """Retrieve and print all students."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT student_id, first_name, last_name, email, enrollment_date
            FROM students
            ORDER BY student_id;
        """)
        rows = cur.fetchall()
        if not rows:
            print("No students found.")
            return rows
        print("\nAll students:")
        print("-" * 72)
        for r in rows:
            print(f"#{r['student_id']:>3} | {r['first_name']} {r['last_name']} | {r['email']} | {r['enrollment_date']}")
        print("-" * 72 + "\n")
        return rows

def add_student(conn, first_name, last_name, email, enrollment_date):
    """Insert a new student and print the new id."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
            RETURNING student_id;
            """,
            (first_name, last_name, email, enrollment_date)
        )
        new_id = cur.fetchone()[0]
        print(f"Inserted student_id={new_id} ({first_name} {last_name}).")
        return new_id

def update_student_email(conn, student_id, new_email):
    """Update email by student_id."""
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE students
               SET email = %s
             WHERE student_id = %s;
            """,
            (new_email, student_id)
        )
        if cur.rowcount == 0:
            print(f"No student found with id={student_id}.")
        else:
            print(f"Updated email for student_id={student_id} -> {new_email}.")

def delete_student(conn, student_id):
    """Delete a student by id."""
    with conn.cursor() as cur:
        cur.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
        if cur.rowcount == 0:
            print(f"No student found with id={student_id}.")
        else:
            print(f"Deleted student_id={student_id}.")

def demo(conn):
    """Scripted demo of CRUD."""
    print("Starting demo...\n")
    get_all_students(conn)
    sid = add_student(conn, "Alice", "Nguyen", "alice.nguyen@example.com", "2023-09-03")
    get_all_students(conn)
    update_student_email(conn, sid, "alice.n@example.com")
    get_all_students(conn)
    delete_student(conn, sid)
    get_all_students(conn)

def main():
    conn = connect()
    MENU = """
Choose an option:
  1) Get all students
  2) Add a student
  3) Update a student's email
  4) Delete a student
  5) Run full demo
  0) Exit
> """
    while True:
        choice = input(MENU).strip()
        try:
            if choice == "1":
                get_all_students(conn)
            elif choice == "2":
                fn = input("First name: ").strip()
                ln = input("Last name: ").strip()
                em = input("Email: ").strip()
                dt = input("Enrollment date (YYYY-MM-DD or leave blank): ").strip() or None
                add_student(conn, fn, ln, em, dt)
            elif choice == "3":
                sid = int(input("Student ID to update: ").strip())
                em = input("New email: ").strip()
                update_student_email(conn, sid, em)
            elif choice == "4":
                sid = int(input("Student ID to delete: ").strip())
                delete_student(conn, sid)
            elif choice == "5":
                demo(conn)
            elif choice == "0":
                print("Bye!")
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
