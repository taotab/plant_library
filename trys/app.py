from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import re
print("👀 Current working dir:", os.getcwd())


app = Flask(__name__)


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Connect to the SQLite database
def get_db_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'database.db')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# If all are true, return true, else return false (readablitly improves)
def is_strong_password(password):

    if (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    ):
        return True
    else:
        return False


@app.route('/')
def index():
    if 'username' in session:   # check inside session dictionary, if there's 'username' data store
        logged_msg = f'You are logged in... {session["username"]}.'

        return render_template('index.html', logged_msg=logged_msg)
    else:
        # redirect to login page if not logged in
        return redirect(url_for('login3'))


# for login3 page:

@app.route('/login3', methods=['GET', 'POST'])
def login3():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login3.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the passwords match
        if password != confirm_password:
            error = 'Passwords do not match.'
            return render_template('register.html', error=error)

        # Check if the password is strong
        if not is_strong_password(password):
            error = 'Password must be at least 8 characters long and contain uppercase, lowercase, digits, and special characters.'
            return render_template('register.html', error=error)

        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('login3'))
        # Handle the case where the username already exists
        # username TEXT UNIQUE.. see this code in schema.sql, That UNIQUE makes sure no two rows can have the same username.
        except sqlite3.IntegrityError:
            error = 'Username already exists.'

    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
