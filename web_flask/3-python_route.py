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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
