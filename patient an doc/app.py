from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def check_user(username, password):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_db_connection(db_name="patient.db"):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def get_patients_by_illness(illness):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointment WHERE illness = ?", (illness,))
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    username = session.get("username")  # Retrieve username from session
    return render_template('home.html', username=username)

@app.route('/doctor-login', methods=['GET', 'POST'])
def doctor_login():
    return render_template('doctor_login.html')

@app.route("/create", methods=["POST"])
def login1():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return render_template("login.html", error="Please enter both username and password")

    if check_user(username, password):
        session["username"] = username  # Store username in session
        return redirect(url_for("home"))  # Redirect to home
    else:
        return render_template("login.html", error="Invalid username or password")

@app.route('/dashboard')
def dashboard():
    username = session.get("username", "")
    doctor_name = request.args.get("doctor_name", "")  # get from search bar
    location = request.args.get("location","")
    return render_template("appointment_booking.html",
                           username=username,
                           doctor_name=doctor_name,
                           location=location)

@app.route('/submit-appointment', methods=['POST'])
def submit_appointment():
    name = request.form.get('name')
    illness = request.form.get('illness')
    phone = request.form.get('phone')
    email = request.form.get('email')
    doctor_name = request.form.get('doctor_name')
    location = request.form.get('location')
    date = request.form.get('date')
    time = request.form.get('time')

    if not location:
        flash("Please select a location before booking.")
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Ensure table name matches INSERT
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            illness TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            doctor_name TEXT,
            location TEXT,
            appointment_date TEXT,
            appointment_time TEXT
        )
    ''')

    cursor.execute('''
        INSERT INTO appointment 
        (name, illness, phone, email, doctor_name, location, appointment_date, appointment_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, illness, phone, email, doctor_name, location, date, time))

    conn.commit()
    conn.close()

    flash(f"Appointment booked successfully for {date} at {time}")
    return redirect(url_for('dashboard'))



@app.route('/search')
def search_form():
    return render_template('search_form.html')

@app.route('/results')
def show_results():
    illness = request.args.get('illness')
    patients = get_patients_by_illness(illness) if illness else []
    return render_template('search_results.html', illness=illness, patients=patients)

@app.route('/doctor-search', methods=['GET', 'POST'])
def doctor_search():
    patients = []
    illness = None

    if request.method == 'POST':
        illness = request.form.get('illness')
        if illness:
            patients = get_patients_by_illness(illness)

    return render_template('doctor_search.html', patients=patients, illness=illness)

@app.route('/logout')
def logout():
    session.pop("username", None)  # Remove username from session
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5500)
