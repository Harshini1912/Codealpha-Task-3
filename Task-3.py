from flask import Flask, request, render_template_string, session, redirect, url_for
import sqlite3
import bcrypt
import os

app = Flask(__name__)

# Secret key to sign sessions
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

# Initialize database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    # Add default admin user (if not exists)
    password = 'secure123'
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", hashed_pw))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

# Home page with links
@app.route('/')
def home():
    if 'username' in session:
        return f"Hello, {session['username']}! <a href='/logout'>Logout</a>"
    return render_template_string("""
    <h2>Welcome</h2>
    <a href="/register">Register</a> | <a href="/login">Login</a>
    """)

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            return "Username and password cannot be empty.", 400

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            conn.close()
            return "User already exists. Please choose a different username."

        # Hash password before storing
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        conn.close()
        return f"User '{username}' registered successfully! You can now <a href='/login'>login</a>."
    else:
        return render_template_string("""
        <h2>Register</h2>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input type="password" name="password"><br>
            <button type="submit">Register</button>
        </form>
        """)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            return "Invalid input — username and password required.", 400

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        record = cursor.fetchone()
        conn.close()

        if record and bcrypt.checkpw(password.encode('utf-8'), record[0]):
            session['username'] = username  # Store username in session
            return f"Welcome, {username}! <a href='/logout'>Logout</a>"
        else:
            return "Invalid credentials.", 401
    else:
        return render_template_string("""
        <h2>Login</h2>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input type="password" name="password"><br>
            <button type="submit">Login</button>
        </form>
        """)

# Logout page
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('home'))  # Redirect to home page

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
