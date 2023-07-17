#!/usr/bin/python3
"""Module"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


@app.teardown_appcontext
def teardown_db(self):
    """Registers a function to be called when the application context ends."""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """Handles 404 errors"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    else:
        host = "0.0.0.0"
    if getenv("HBNB_API_PORT"):
        port = int(getenv("HBNB_API_PORT"))
    else:
        port = 5000
    app.run(host=host, port=port, threaded=True)
