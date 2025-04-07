"""An example application to demonstrate Variable Rules in Routing"""
from flask import Flask
app = Flask(__name__)


@app.route("/")
def home():
    """View for the Home page of your website."""
    return "This is your homepage :)"


@app.route("/<your_name>")
def greetings(your_name='this is a default value'):
    """View function to greet the user by name."""
    return "Welcome " + your_name + "!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
