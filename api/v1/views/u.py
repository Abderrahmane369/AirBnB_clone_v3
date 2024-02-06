#!/usr/bin/python3
"""Module documentation"""
from flask import Flask, jsonify, abort, request
from models.base_model import BaseModel
from api.v1.views import app_views
from models.state import State
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """get users"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """delete user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create user"""
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    if 'email' not in body_request:
        abort(400, "Missing email")
    if 'password' not in body_request:
        abort(400, "Missing password")
    user = User(**body_request)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in body_request.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
