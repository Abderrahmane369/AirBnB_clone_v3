#!/usr/bin/python3
"""Module documentation"""
from flask import Flask, jsonify, abort, request
from models.base_model import BaseModel
from api.v1.views import app_views
from models.place import Place
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews(place_id):
    """List all reviews for a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])



@app_views.route('/places/<place_id>/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(place_id, review_id):
    """Delete a specific review"""
    review = storage.get(Review, review_id)
    place = storage.get(Place, place_id)

    if not review or not place:
        abort(404)
    if review not in place.reviews:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}),   200



@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new review for a place"""
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    if 'text' not in body_request:
        abort(400, "Missing text")
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    body_request['place_id'] = place_id
    review = Review(**body_request)
    review.save()
    return jsonify(review.to_dict()),   201



@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a specific review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")
    ignored_keys = ['id', 'created_at', 'updated_at', 'place_id']
    for key, value in body_request.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()),   200