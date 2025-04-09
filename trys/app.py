from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return 'how are u?'


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            # url_for() func generates the URL for index() function
            return redirect(url_for('index'))
            # return redirect('http://127.0.0.1:5000/')  # also works,, as its for default root link path page. ie. link of index() generating page
    return render_template('login.html', error=error)

# for login3 page:


@app.route('/login3', methods=['GET', 'POST'])
def login3():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            # url_for() func generates the URL for index() function
            return redirect(url_for('index'))
            # return redirect('http://127.0.0.1:5000/')  # also works,, as its for default root link path page. ie. link of index() generating page
    return render_template('login3.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
