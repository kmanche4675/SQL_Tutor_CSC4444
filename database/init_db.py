import sqlite3

conn = sqlite3.connect('database/tutor.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER,
    manager_id INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    name TEXT,
    budget INTEGER
)
''')

cursor.executemany('INSERT OR IGNORE INTO employees VALUES (?,?,?,?,?)', [
    (1, 'Alice', 'Sales', 60000, None),
    (2, 'Bob', 'Sales', 50000, 1),
    (3, 'Charlie', 'Engineering', 90000, None),
    (4, 'Diana', 'Engineering', 80000, 3),
    (5, 'Eve', 'Sales', 55000, 1),
])

cursor.executemany('INSERT OR IGNORE INTO departments VALUES (?,?,?)', [
    (1, 'Sales', 200000),
    (2, 'Engineering', 300000),
])

conn.commit()
conn.close()
print("Database created with sample data.")
