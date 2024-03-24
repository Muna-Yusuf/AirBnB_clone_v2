#!/usr/bin/python3
"""Stating flask app. """
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """Script that starts a Flask web application."""
    return 'Hello HBNB!'


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Script that displays HBNB."""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def C_text(text):
    """Script that displays "C" followed by the value of the text variable."""
    return 'C ' + text.replace('_', ' ')


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_text(text):
    """Script displays"Python"followed by the value of the text variable."""
    return 'Python ' + text.replace('_', ' ')


@app.route("/number/<n>", strict_slashes=False)
def number(n):
    """Script displays n is a number only if n is an integer."""
    return str(n) + ' is a number'


@app.route("/number_template/<n>", strict_slashes=False)
def number_template(n):
    """Script displays a HTML page only if n is an integer."""
    path = '5-number.html'
    return render_template(path, n=n)


@app.route("/number_odd_or_even/<n>", strict_slashes=False)
def number_odd_even(n):
    """Script displays a HTML page only if n is an integer.."""
    path = '6-number_odd_or_even.html'
    return render_template(path, n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
