#!/usr/bin/python3
"""This module handles all default RestFul API actions for State"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    result = []
    for state in storage.all(State).values():
        result.append(state.to_dict())

    return jsonify(result)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    if not state_id:
        abort(404)
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    if not state_id:
        abort(404)

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    state.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State"""
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if data.get('name') is None:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_state = State(**data)
    new_state.save()

    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
