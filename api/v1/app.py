#!/usr/bin/python3
"""Module"""
from flask import Flask, jsonify
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(self):
    """Registers a function to be called when the application context ends."""
    storage.close()


if __name__ == '__main__':
    if os.getenv('HBNB_API_HOST'):
        bnb_host = os.getenv('HBNB_API_HOST')
    else:
        bnb_host = '0.0.0.0'
    if os.getenv('HBNB_API_PORT'):
        bnb_port = int(os.getenv('HBNB_API_PORT'))
    else:
        bnb_port = 5000
    app.run(host=bnb_host, port=bnb_port, threaded=True)
