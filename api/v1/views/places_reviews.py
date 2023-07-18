#!/usr/bin/python3
"""
Place_reviews module
"""

from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/place/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """
    Reviews by place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return make_response(jsonify(reviews))


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Return place by id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return make_response(jsonify(review.to_dict()))


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Delete place by id
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Create Review object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    if "user_id" not in req:
        abort(400, "Missing user_id")
    user = storage.get(User, req["user_id"])
    if user is None:
        abort(404)
    if "text" not in req:
        abort(400, "Missing text")
    review = Review(**req)
    review.place_id = place_id
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Update Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    ignored_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in req.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
