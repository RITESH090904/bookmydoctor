import sqlite3

conn = sqlite3.connect("patient.db")
cursor = conn.cursor()

Doctor_name = input("Enter Doctor name:")

cursor.execute("Select * from ")