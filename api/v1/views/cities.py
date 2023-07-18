#!/usr/bin/python3
"""
City module app
"""

from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return make_response(jsonify(cities))


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """retrieves a City object based on id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return make_response(jsonify(city.to_dict()))


@app_views.route("/cities/<city_id>", methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object based on id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City object based on state id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    if "name" not in req:
        abort(400, "Missing name")
    req["state_id"] = state_id
    city = City(**req)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates city object using id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "state_id", "created_at", "updated_at"]
    for key, value in req.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
