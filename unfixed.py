import sqlite3

conn = sqlite3.connect("university.db")
cursor = conn.cursor()

# Create tables if not exist
cursor.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, name TEXT, seats_available INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS enrollments (student_id INTEGER, course_id INTEGER)")
conn.commit()

# Function to register a student
def register_student(name):
    query = f"INSERT INTO students (name) VALUES ('{name}')"
    cursor.execute(query)
    conn.commit()
    print(f"Student {name} registered successfully!")

# Function to enroll in a course 
def enroll_course(student_id, course_id):
    cursor.execute(f"SELECT seats_available FROM courses WHERE id = {course_id}")
    course = cursor.fetchone()

    if course:
        cursor.execute(f"INSERT INTO enrollments (student_id, course_id) VALUES ({student_id}, {course_id})")
        cursor.execute(f"UPDATE courses SET seats_available = seats_available - 1 WHERE id = {course_id}")
        conn.commit()
        print(f"Student {student_id} enrolled in course {course_id} successfully!")
    else:
        print("Course not found!")

# Main logic
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
