#触らないで

import sqlite3

conn = sqlite3.connect("stock.db")

conn.execute("""
CREATE TABLE inventory(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    stock INTEGER NOT NULL,
    amount INTEGER NOT NULL
)
""")

conn.commit()
conn.close()