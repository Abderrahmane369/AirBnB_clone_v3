#!/usr/bin/python3
"""Module documentation"""
from flask import Flask, jsonify, abort, request
from models.base_model import BaseModel
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities():
    """List all amenities"""
    vals = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in vals])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Get a specific amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a specific amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity"""
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    if 'name' not in body_request:
        abort(400, "Missing name")
    amenity = Amenity(**body_request)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


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
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in body_request.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
