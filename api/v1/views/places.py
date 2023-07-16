#!/usr/bin/python3
"""
Amenities module app
"""

from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """
    Returns places by city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return make_response(jsonify(places))


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_places(place_id):
    """
    Return place by id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return make_response(jsonify(place.to_dict()))


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Delete place by id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Create Place object
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    if "user_id" not in req:
        abort(400, "Missing user_id")
    user = storage.get(User, req["user_id"])
    if not user:
        abort(404)
    if "name" not in req:
        abort(400, "Missing name")
    place = Place(**req)
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Update Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in req.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
