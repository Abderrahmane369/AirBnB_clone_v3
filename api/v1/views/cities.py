#!/usr/bin/python3
"""Module documentation"""
from flask import Flask, jsonify, abort, request
from models.base_model import BaseModel
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities(state_id):
    """cities"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """get cities"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """delete city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """create city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    if 'name' not in body_request:
        abort(400, "Missing name")
    body_request["state_id"] = state_id
    city = City(**body_request)
    city.save()
    # storage.new(city)
    # storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in body_request.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    # storage.save(city)
    city.save()
    return jsonify(city.to_dict()), 200
