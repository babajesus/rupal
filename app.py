from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector as p
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "miniportal123"

# --- DB Configuration ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'India@12345',
    'database': 'mini_project'
}

# --- DB Connection ---
def get_db_connection():
    try:
        connection = p.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySql: {e}")
        return None

# --- Signup ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                        (username, email, password))
            conn.commit()
            return render_template("success.html")
        except:
            return render_template("signup.html", error="Username already exists")
        finally:
            cur.close()
            conn.close()
    return render_template("signup.html")

# --- Login ---
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template("index.html", error="Invalid username or password")
    return render_template("index.html")

# --- Dashboard ---
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("dashboard.html", user=session['user'])

# --- About ---
@app.route('/about')
def about():
    return render_template("about.html")

# --- Contact ---
@app.route('/contact')
def contact():
    return render_template("contact.html")

# --- Employee List ---
@app.route('/employees')
def employees():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("employees.html", employees=employees)

# --- Create Employee ---
@app.route('/create_employee', methods=['GET','POST'])
def create_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        email = request.form['email']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO employees (name, position, email) VALUES (%s, %s, %s)",
                    (name, position, email))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('employees'))
    return render_template("create_employee.html")

# --- Logout ---
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


 

if __name__ == '__main__':
  
    app.run(debug=True)
