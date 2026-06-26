import sqlite3

conn = sqlite3.connect("stock.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    liquor_name TEXT,
    category TEXT,
    remain_rate INTEGER
)
""")

conn.commit()
conn.close()

print("テーブル作成完了")