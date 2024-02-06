#!/usr/bin/python3
"""Module documentation"""
from flask import Flask, jsonify, abort, request
from models.base_model import BaseModel
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def places(city_id):
    """List all places"""
    if not storage.get(City, city_id):
        abort(404)

    places = storage.get(City, city_id).places
    return jsonify([e.to_dict() for e in places])


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Get a specific place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a specific place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}),  200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new place"""
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    if 'name' not in body_request:
        abort(400, "Missing name")
    if 'user_id' not in body_request:
        abort(400, "Missing user_id")
    if not storage.get(City, city_id):
        abort(404)
    if not storage.get(User, body_request['user_id']):
        abort(404)

    body_request['city_id'] = city_id
    place = Place(**body_request)
    place.save()
    return jsonify(place.to_dict()),  201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a specific place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    ignored_keys = ['id', 'created_at',
                    'updated_at', 'user_id',
                    'city_id']
    for key, value in body_request.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()),  200
