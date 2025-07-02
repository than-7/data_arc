# create_db.py
import sqlite3
conn = sqlite3.connect('blog.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
)
''')
conn.close()
print("Database created.")
