#!/usr/bin/python3
"""Module documentation"""
from flask import Flask, jsonify, abort, request
from models.base_model import BaseModel
from api.v1.views import app_views
from models.place import Place
from models import storage
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def amenities(place_id):
    """List all amenities for a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """Delete a specific amenity"""
    amenity = storage.get(Amenity, amenity_id)
    place = storage.get(Place, place_id)

    if not amenity or not place:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}),  200


@app_views.route('/places/<place_id>/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity(place_id):
    """Create a new amenity for a place"""
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    if 'name' not in body_request:
        abort(400, "Missing name")
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    body_request['place_id'] = place_id
    amenity = Amenity(**body_request)
    amenity.save()
    return jsonify(amenity.to_dict()),  201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update a specific amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    ignored_keys = ['id', 'created_at', 'updated_at', 'place_id']
    for key, value in body_request.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()),  200
