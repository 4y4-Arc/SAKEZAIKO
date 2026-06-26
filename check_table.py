import sqlite3

conn = sqlite3.connect("stock.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM inventory")

rows = cursor.fetchall()

print(rows)

conn.close()