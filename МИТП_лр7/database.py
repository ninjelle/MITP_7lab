import sqlite3

def create_database():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT UNIQUE
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
    
    conn.commit()
    conn.close()

def add_user(name, age, email):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
            (name, age, email)
        )
        user_id = cursor.lastrowid
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        raise ValueError("Email already exists")
    finally:
        conn.close()

def get_user(user_id):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    return user

def get_all_users():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    
    return users

def update_user_age(user_id, new_age):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE users SET age = ? WHERE id = ?",
        (new_age, user_id)
    )
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return updated

def delete_user(user_id):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return deleted

def add_order(user_id, product, price):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO orders (user_id, product, price) VALUES (?, ?, ?)",
        (user_id, product, price)
    )
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return order_id

def get_user_orders(user_id):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,))
    orders = cursor.fetchall()
    conn.close()
    
    return orders

def join_users_orders():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT users.name, orders.product, orders.price
    FROM users
    JOIN orders ON users.id = orders.user_id
    """)
    
    results = cursor.fetchall()
    conn.close()
    
    return results