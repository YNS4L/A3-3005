-- db/schema.sql
-- Creates the 'students' table according to the assignment schema.
-- Run this in pgAdmin Query Tool (or psql) against your target database.

CREATE TABLE IF NOT EXISTS students (
    student_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    enrollment_date DATE
);
