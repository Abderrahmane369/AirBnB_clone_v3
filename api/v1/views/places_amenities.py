#!/usr/bin/python3
"""Module documentation"""
from flask import Flask, jsonify, abort, request
from models.base_model import BaseModel
from api.v1.views import app_views
from models.place import Place
from models import storage
from models import storage_t
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

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}),  200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_amenity(place_id, amenity_id):
    """Create a new amenity for a place"""
    amenity = storage.get(Amenity, amenity_id)
    place = storage.get(Place, place_id)

    if not amenity or not place:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    return jsonify(place.amenities.append(amenity)),  201
