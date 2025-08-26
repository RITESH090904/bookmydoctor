import sqlite3


username = input("\nEnter username:")
password = input("\nEnter password:")
conn = sqlite3.connect("user.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")

try:
    cursor.execute("INSERT INTO user(username, password) VALUES (?, ?)", (username,password))
    print("User added.")
except sqlite3.IntegrityError:
    print("User already exists.")

conn.commit()
conn.close()