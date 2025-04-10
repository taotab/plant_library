from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        logged_msg = 'U R Logged in...'
        return render_template('index.html', logged_msg=logged_msg)
    else:
        return redirect(url_for('login'))

# Route for all pages instead of hardcoding : dynamic routing...

@app.route('/plants/<plant_name>')
def plant_page(plant_name):
    try:
        return render_template(f'{plant_name}.html')
    except:
        return render_template('404.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Pre-added credentials for now,, (later use database)
        username= 'admin'
        password= 'admin'

        if request.form['username'] != username or request.form['password'] != password:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
