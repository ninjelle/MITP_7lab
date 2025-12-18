import sqlite3

conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT
)
""")

cursor.execute("INSERT INTO users (username, email) VALUES ('alex', 'alex@mail.com')")
cursor.execute("INSERT INTO users (username, email) VALUES ('maria', 'maria@example.com')")

conn.commit()

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

conn.close()
