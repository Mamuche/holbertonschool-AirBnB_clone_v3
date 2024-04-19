#!/usr/bin/python3
"""This module handles all default RestFul API actions for State"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage


"""Retrieve the list of all states"""


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    result = []
    for state in storage.all(State).values():
        result.append(state.to_dict())

    return jsonify(result)


"""Retrieve a specific State"""


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    if not state_id:
        abort(404)
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


"""Deletes a State"""


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    if not state_id:
        abort(404)

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    state.delete()
    storage.save()

    return jsonify({}), 200


"""Create a new State"""


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    data = request.get_json()
    if data is not dict:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")

    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


"""Update an existing State"""


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if data is not dict:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
