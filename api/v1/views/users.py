#!/usr/bin/python3
"""
Users module app
"""

from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """Gets all user objects in storage"""
    users = storage.all(User).values()
    user_list = [user.to_dict() for user in users]
    return make_response(jsonify(user_list))


@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Returns user object using id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return make_response(jsonify(user.to_dict()))


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object based on id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Creates a User object based on state id"""
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    if "email" not in req:
        abort(400, "Missing eamil")
    if "password" not in req:
        abort(400, "Missing password")
    user = User(**req)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates User object using id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in req.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
