import sqlite3

conn = sqlite3.connect('users_products.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    city TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product TEXT,
    price REAL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

users_data = [
    ('Anna', 25, 'Moscow'),
    ('Ivan', 30, 'Saint Petersburg'),
    ('Maria', 28, 'Kazan'),
    ('Alexey', 35, 'Moscow'),
]

cursor.executemany("INSERT INTO users (name, age, city) VALUES (?, ?, ?)", users_data)

orders_data = [
    (1, 'Laptop', 50000),
    (1, 'Mouse', 1500),
    (2, 'Phone', 30000),
    (3, 'Tablet', 25000),
    (4, 'Monitor', 15000),
]

cursor.executemany("INSERT INTO orders (user_id, product, price) VALUES (?, ?, ?)", orders_data)
conn.commit()

print("Data added successfully\n")

city_to_find = 'Moscow'
cursor.execute("SELECT name, age FROM users WHERE city = ?", (city_to_find,))
print(f"Users from {city_to_find}:")
for user in cursor.fetchall():
    print(f"  - {user[0]}, {user[1]} years old")

min_age = 25
max_age = 32
cursor.execute("SELECT name, age, city FROM users WHERE age BETWEEN ? AND ?", (min_age, max_age))
print(f"\nUsers aged {min_age} to {max_age}:")
for user in cursor.fetchall():
    print(f"  - {user[0]}, {user[1]} years, {user[2]}")

user_name = 'Ivan'
age_increase = 1
cursor.execute("UPDATE users SET age = age + ? WHERE name = ?", (age_increase, user_name))
conn.commit()
print(f"\nUser {user_name}'s age increased by {age_increase} year")

min_price = 20000
cursor.execute("DELETE FROM orders WHERE price < ?", (min_price,))
conn.commit()
print(f"Orders cheaper than {min_price} rubles deleted")

cursor.execute("SELECT * FROM orders")
print("\nRemaining orders:")
for order in cursor.fetchall():
    print(f"  Order {order[0]}: {order[2]} - {order[3]} rub.")

conn.close()
print("\nConnection closed")