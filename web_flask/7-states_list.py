#!/usr/bin/python3
"""Starting Flask app."""

from flask import Flask
from models import *
from models import storage
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Display a HTML page with the list of all State in DBStorage."""
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes storage."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
