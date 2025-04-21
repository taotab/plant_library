from flask import Flask, render_template
import os

print("👀 Current working dir:", os.getcwd())


app = Flask(__name__)


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/3')
def index2():

    return render_template('index2.html')


@app.route('/login')
def login():

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
