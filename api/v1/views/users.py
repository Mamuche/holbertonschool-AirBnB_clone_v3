#!/usr/bin/python3
"""This module handles all default RestFul API actions for user"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all user objects"""
    result = []
    for user in storage.all(User).values():
        result.append(user.to_dict())

    return jsonify(result)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a user object"""
    if not user_id:
        abort(404)
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user object"""
    if not user_id:
        abort(404)

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new user"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    if data.get('name') is None:
        abort(400, "Missing name")
    if data.get('email') is None:
        abort(400, "Missing email")
    if data.get('password') is None:
        abort(400, "Missing password")

    new_user = User(**data)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """Updates a user object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
