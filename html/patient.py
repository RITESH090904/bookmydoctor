import sqlite3

# Sample input (replace with input() for real usage)
patient_name = input("Patient name: ")
illness = input("Illness: ")
phone_number = input("Phone number: ")
Email = input("Email: ")
Address = input("Address: ")
Appointment_date = input("Appointment date (YYYY-MM-DD): ")
Appointment_time = input("Appointment time (e.g. 14:00): ")

conn = sqlite3.connect("patient.db")
cursor = conn.cursor()

# Drop and recreate the table
cursor.execute("DROP TABLE IF EXISTS patient")
cursor.execute("""
    CREATE TABLE patient (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        illness TEXT NOT NULL,
        phone_number TEXT,
        Email TEXT,
        Address TEXT,
        Appointment_date TEXT,
        Appointment_time TEXT
    )
""")

# Insert new record
cursor.execute("""
    INSERT INTO patient(patient_name, illness, phone_number, Email, Address, Appointment_date, Appointment_time)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (patient_name, illness, phone_number, Email, Address, Appointment_date, Appointment_time))

print("Patient added successfully.")

conn.commit()
conn.close()
