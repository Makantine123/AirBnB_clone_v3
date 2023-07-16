#!/usr/bin/python3
"""
States module app
"""

from flask import jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states():
    """Retrieves the list of all state objects"""
    objs = storage.all(State)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def single_state(state_id):
    """Retrieves a State object by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    """Returns the new State with the status code 201"""
    nobj = request.get_json()
    if not nobj:
        abort(400, "Not a json")
    if "name" not in nobj:
        abort(400, "Missing name")
    obj = State(**nobj)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def put_state(state_id):
    """Updates a state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    ignore = ["id", "created_at", "updated_at"]
    for key, value in request.json.items():
        if key not in ignore:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
