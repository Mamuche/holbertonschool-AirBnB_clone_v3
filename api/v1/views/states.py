#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models.state import State
from models import storage


"""Retrieve the list of all states"""


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    result = []
    for state in storage.all(State).values():
        result.append(state.to_dict())

    return jsonify(result)


"""Retrieve a specific report"""


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


"""Supprimer un état"""


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        """abort immediately stops processing the current request"""
        abort(404)
    state.delete()
    """200 indicates successful request"""
    return jsonify({}), 200


"""Create a new report"""


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """analyzes the request body and attempts to extract
    the JSON data present"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    """**data passes each key-value pair in the data dictionary
    as a named argument when the State object is created."""
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


"""Update an existing report"""


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
