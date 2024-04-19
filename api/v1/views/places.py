#!/usr/bin/python3
"""This module handles all default RestFul API actions for Places"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all place objects of a city"""
    if city_id is None:
        abort(404)

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    cities = []
    for place in city.cities:
        cities.append(place.to_dict())

    return jsonify(cities)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a place object"""
    if place_id is None:
        abort(404)

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/cities/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place object"""
    if place_id is None:
        abort(404)

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a place"""
    if city_id is None:
        abort(404)

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    place = request.get_json()
    if place is None:
        abort(400, 'Not a JSON')

    if place.get('name') is None:
        abort(400, 'Missing name')
    if place.get('user_id') is None:
        abort(400, 'Missing user_id')

    if storage.get(User, place.get('user_id')) is None:
        abort(404)

    new_place = place(**place)
    new_place.city_id = city_id

    storage.new(new_place)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place_json = request.get_json()
    if place_json is None:
        abort(400, 'Not a JSON')

    for key, value in place_json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
        storage.save()

    return jsonify(place.to_dict()), 200
