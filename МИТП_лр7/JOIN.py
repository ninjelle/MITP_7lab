import sqlite3

conn = sqlite3.connect('simple_join.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    group_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

cursor.execute("DELETE FROM students")
cursor.execute("DELETE FROM groups")

cursor.execute("INSERT INTO groups (id, name) VALUES (1, 'Group A')")
cursor.execute("INSERT INTO groups (id, name) VALUES (2, 'Group B')")

cursor.execute("INSERT INTO students (id, name, group_id) VALUES (1, 'John', 1)")
cursor.execute("INSERT INTO students (id, name, group_id) VALUES (2, 'Anna', 1)")
cursor.execute("INSERT INTO students (id, name, group_id) VALUES (3, 'Mike', 2)")
cursor.execute("INSERT INTO students (id, name, group_id) VALUES (4, 'Sara', 2)")
cursor.execute("INSERT INTO students (id, name, group_id) VALUES (5, 'Bob', NULL)") 

conn.commit()

print("All students:")
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(f"  ID: {row[0]}, Name: {row[1]}, Group ID: {row[2]}")

print("\nAll groups:")
cursor.execute("SELECT * FROM groups")
for row in cursor.fetchall():
    print(f"  ID: {row[0]}, Name: {row[1]}")

print("\nJOIN: Students with group names")
cursor.execute("""
SELECT students.name, groups.name 
FROM students 
JOIN groups ON students.group_id = groups.id
""")

for row in cursor.fetchall():
    print(f"  Student: {row[0]}, Group: {row[1]}")

conn.close()
