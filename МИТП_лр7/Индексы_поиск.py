import sqlite3
import time

conn = sqlite3.connect('speed_test.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS data")
c.execute("CREATE TABLE data (id INT, value TEXT)")

for i in range(1000000):
    c.execute(f"INSERT INTO data VALUES ({i}, 'text{i}')")

conn.commit()

start = time.time()
c.execute("SELECT * FROM data WHERE value = 'text5000'")
print("Without index:", time.time() - start, "seconds")

c.execute("CREATE INDEX idx_value ON data(value)")

start = time.time()
c.execute("SELECT * FROM data WHERE value = 'text5000'")
print("With index:", time.time() - start, "seconds")

conn.close()