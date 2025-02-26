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


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """Gets all amenity objects in storage"""
    amenities = storage.all(Amenity).values()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return make_response(jsonify(amenities_list))


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Returns amenity object using id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return make_response(jsonify(amenity.to_dict()))


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object based on id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Creates a Aemity object based on state id"""
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    if "name" not in req:
        abort(400, "Missing name")
    amenity = Amenity(**req)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates Amenity object using id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "created_at", "updated_at"]
    for key, value in req.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
