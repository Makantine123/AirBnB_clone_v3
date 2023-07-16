#!/usr/bin/python3
"""
Index module app
"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def get_status():
    """Returns status"""
    return jsonify({"status": "OK"})
