import sqlite3


username = input("\nEnter your username:")
Password = input("\n Enter your password:")

conn = sqlite3.connect("docdata.db")
cursor = conn.cursor()

cursor.execute("""
            CREATE TABLE IF NOT EXISTS docdata(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL UNIQUE,
               password TEXT NOT NULL
               )
               """)
try:
    cursor.execute("INSERT INTO docdata(username,password) VALUES (?, ?)",(username,Password))
    print("doc added")
except sqlite3.IntegrityError:
    print("user already exist.")

conn.commit()
conn.close()