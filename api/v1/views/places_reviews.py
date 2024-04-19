#!/usr/bin/python3
"""This module handles all default RestFul API actions for reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all place objects of a review"""
    if place_id is None:
        abort(404)

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place_review = []
    for review in place.reviews:
        place_review.append(place.to_dict())

    return jsonify(place_review)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object"""
    if review_id is None:
        abort(404)

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object"""
    if review_id is None:
        abort(404)

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a review"""
    if place_id is None:
        abort(404)

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    review = request.get_json()
    if review is None:
        abort(400, 'Not a JSON')

    if review.get('name') is None:
        abort(400, 'Missing name')
    if review.get('user_id') is None:
        abort(400, 'Missing user_id')
    if review.get('text') is None:
        abort(400, 'Missing text')

    if storage.get(User, place.get('user_id')) is None:
        abort(404)

    new_review = Review(**review)
    new_review.place_id = place_id

    storage.new(new_review)
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_place_review(review_id):
    """Updates a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review_json = request.get_json()
    if review_json is None:
        abort(400, 'Not a JSON')

    for key, value in review_json.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
        storage.save()

    return jsonify(review.to_dict()), 200
