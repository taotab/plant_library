from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:   # check inside session dictionary, if there's 'username' data store
        logged_msg = 'You are logged in...'
        return  render_template('index.html', logged_msg=logged_msg)
    else:
        return redirect(url_for('login3')) # redirect to login page if not logged in


# for login3 page:

@app.route('/login3', methods=['GET', 'POST'])
def login3():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username'] = 'admin'    # store username in session (for later use)
            return redirect(url_for('index'))
            # return redirect('http://127.0.0.1:5000/')  # also works,, as its for default root link path page. ie. link of index() generating page
    return render_template('login3.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        else:
            session['username'] = 'admin'    # store username in session (for later use)
            return redirect(url_for('index'))
            # return redirect('http://127.0.0.1:5000/')  # also works,, as its for default root link path page. ie. link of index() generating page
    return render_template('register.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
