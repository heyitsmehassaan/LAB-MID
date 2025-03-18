import sqlite3

# Secure database connection
conn = sqlite3.connect("university.db", isolation_level=None)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL, 
    seats_available INTEGER NOT NULL CHECK(seats_available >= 0)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollments (
    student_id INTEGER, 
    course_id INTEGER, 
    PRIMARY KEY(student_id, course_id),
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(course_id) REFERENCES courses(id)
)""")

# Secure function to register a student
def register_student(name):
    if not name.strip():
        print("Invalid name. Please enter a valid name.")
        return

    try:
        cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
        print(f"Student {name} registered successfully!")
    except sqlite3.IntegrityError:
        print("Error: Student registration failed.")

# Secure function to enroll in a course
def enroll_course(student_id, course_id):
    if not student_id.isdigit() or not course_id.isdigit():
        print("Invalid input! Student ID and Course ID must be numbers.")
        return
    
    student_id, course_id = int(student_id), int(course_id)

    cursor.execute("SELECT seats_available FROM courses WHERE id = ?", (course_id,))
    course = cursor.fetchone()

    if not course:
        print("Course not found!")
        return

    seats_available = course[0]
    
    if seats_available <= 0:
        print("No seats available in this course.")
        return

    cursor.execute("SELECT 1 FROM enrollments WHERE student_id = ? AND course_id = ?", (student_id, course_id))
    if cursor.fetchone():
        print("Student is already enrolled in this course!")
        return

    try:
        cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
        cursor.execute("UPDATE courses SET seats_available = seats_available - 1 WHERE id = ?", (course_id,))
        print(f"Student {student_id} successfully enrolled in course {course_id}!")
    except sqlite3.IntegrityError:
        print("Error: Enrollment failed.")

# Secure input handling
print("1. Register Student\n2. Enroll in Course")
choice = input("Enter choice: ")

if choice == "1":
    student_name = input("Enter student name: ")
    register_student(student_name)
elif choice == "2":
    student_id = input("Enter student ID: ")
    course_id = input("Enter course ID: ")
    enroll_course(student_id, course_id)
else:
    print("Invalid choice!")

conn.close()
