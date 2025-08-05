from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ---------- ROUTES ----------

@app.route('/')
def home_page():
    return render_template("Home_page.html")

# ---------- PATIENT LOGIN PAGE ----------
@app.route('/login-patient')
def login_page():
    return render_template("login.html", error=None)

# ---------- DOCTOR LOGIN PAGE ----------
@app.route('/login-doctor')
def doctor_login():
    return render_template("doc_login.html", error=None)

# ---------- PATIENT AUTHENTICATION ----------
def check_user(username, password):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route("/create", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return render_template("login.html", error="Please enter both username and password")

    if check_user(username, password):
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html", error="Invalid username or password")

# ---------- DOCTOR AUTHENTICATION ----------
def check_doctor(username, password):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctor WHERE username = ? AND password = ?", (username, password))
    doctor = cursor.fetchone()
    conn.close()
    return doctor

@app.route("/doc-auth", methods=["POST"])
def doctor_auth():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return render_template("doc_login.html", error="Please enter both username and password")

    if check_doctor(username, password):
        return redirect(url_for("search_patients"))
    else:
        return render_template("doc_login.html", error="Invalid doctor credentials")

# ---------- PATIENT DASHBOARD / APPOINTMENT PAGE ----------
@app.route("/dashboard")
def dashboard():
    return render_template("appointment_booking.html")

# ---------- SUBMIT APPOINTMENT ----------
@app.route("/submit-appointment", methods=["POST"])
def submit_appointment():
    name = request.form['name']
    illness = request.form['illness']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']
    date = request.form['date']
    time = request.form['time']

    conn = sqlite3.connect("patient.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            illness TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT,
            appointment_date TEXT,
            appointment_time TEXT
        )
    ''')

    cursor.execute('''
        INSERT INTO appointment (name, illness, phone, email, address, appointment_date, appointment_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, illness, phone, email, address, date, time))

    conn.commit()
    conn.close()

    return f"✅ Appointment booked successfully! At: {date} time: {time}"

# ---------- DOCTOR SEARCH PATIENTS ----------
@app.route('/doctor-search', methods=["GET", "POST"])
def search_patients():
    patients = None
    if request.method == "POST":
        illness = request.form.get("illness")
        if illness:
            illness = illness.lower().strip()
            conn = sqlite3.connect("patient.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM appointment WHERE LOWER(illness) = ?", (illness,))
            patients = cursor.fetchall()
            conn.close()
    return render_template("doc_patient_search.html", patients=patients)

# ---------- DATABASE INITIALIZATION ----------
def init_user_db():
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ---------- START THE FLASK APP ----------
if __name__ == "__main__":
    init_user_db()
    app.run(debug=True, port=5500)
