import sqlite3

conn = sqlite3.connect('students.db')

conn.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        department TEXT
    )
''')

conn.close()
print("Database and table created successfully.")
