from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
print("👀 Current working dir:", os.getcwd())


app = Flask(__name__)


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def get_db_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'database.db')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    if 'username' in session:   # check inside session dictionary, if there's 'username' data store
        logged_msg = 'You are logged in...'
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

        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('login3'))

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
