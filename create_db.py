#触らないで

import sqlite3

conn = sqlite3.connect("stock.db")

conn.execute("""
CREATE TABLE inventory(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    stock INTEGER
)
""")

conn.commit()
conn.close()