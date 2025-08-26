import sqlite3
conn = sqlite3.connect("patient.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM appointment")
rows = cursor.fetchall()
print(rows)
