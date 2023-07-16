#!/usr/bin/python3
"""
Amenities module app
"""

from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity



