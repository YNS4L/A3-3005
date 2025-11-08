**README.md**

**PostgreSQL CRUD Application**

* **Database Name:** `students_db`

* **Table Name:** `students`

* **PostgreSQL Version:** 18 (Port 5433)

* **Database Setup:**

  1. Open **pgAdmin 4**.
  2. Create a new database named `students_db`.
  3. Run `db/schema.sql` in the Query Tool to create the `students` table.
  4. Run `db/seed.sql` to insert the initial three records.
  5. Verify the table with:

     ```sql
     SELECT * FROM students;
     ```

* **Application Setup:**

  1. Make sure PostgreSQL 18 is running on port **5433**.
  2. Open the project folder in **VS Code** or a terminal.
  3. Install the required dependencies:

     ```bash
     python -m pip install -r requirements.txt
     ```
  4. Copy the example environment file:

     ```bash
     copy .env.example .env
     ```
  5. Edit `.env` and enter your database credentials.

* **Compiling and Executing:**

  1. Run the program:

     ```bash
     python app.py
     ```
  2. Choose an option from the menu to perform CRUD operations.
  3. Verify the results in **pgAdmin** using:

     ```sql
     SELECT * FROM students;
     ```

* **Functions Implemented:**

  * `get_all_students()` → Displays all student records.
  * `add_student()` → Adds a new student.
  * `update_student_email()` → Updates an existing student's email.
  * `delete_student()` → Deletes a student by ID.

* **Repository Includes:**

  * `app.py`
  * `db/schema.sql`
  * `db/seed.sql`
  * `requirements.txt`
  * `.env.example`

* **Video Demonstration:**

  * Shows database creation and initial data setup in pgAdmin.
  * Demonstrates all CRUD operations in the Python application.
  * Confirms all changes in pgAdmin after each operation.
  * **Video Link:**   https://screenrec.com/share/y5IGv4thuE 
  
