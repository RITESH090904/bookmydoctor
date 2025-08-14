import sqlite3

illness = input("enter the illness by which you want to search patient names:")

conn=sqlite3.connect("patient.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM appointment WHERE illness = ?",(illness,))
rows= cursor.fetchall()

if rows:
    print("todays patient's are:")
    for row in rows:
        print(f"ID:{row[0]}, Name:{row[1]}, \nIllness:{row[2]}, \nPhone_number:{row[3]}, \nEmail:{row[4]}, \nAddress:{row[5]}, \nDate:{row[6]}, \nTime:{row[7]}\n\n")
else:
    print("No patient for today Doc.")

conn.commit()
conn.close()