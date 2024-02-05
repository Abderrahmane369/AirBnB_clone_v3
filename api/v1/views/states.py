#!/usr/bin/python3
"""Module documentation"""
from flask import Flask, jsonify, abort, request
from models.base_model import BaseModel
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """List all states"""
    return jsonify([state.to_dict() for state in storage.all(State).values()])


@app_views.route('/states/<state_id>',
                 methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Get a specific state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a specific state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state"""
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    if 'name' not in body_request:
        abort(400, "Missing name")
    state = State(**body_request)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a specific state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in body_request.items():
        if key not in ignored_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
