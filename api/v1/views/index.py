#!/usr/bin/python3
"""index"""
from flask import Blueprint, jsonify
from models import storage
from models.user import User
from models.state import State

app_views = Blueprint('app_views', __name__,
                      url_prefix='/api/v1')


@app_views.route('/status')
def status():
    """status"""
    return jsonify({'status': 'OK'})


@app_views.route('stats', methods=['GET'], strict_slashes=False)
def stats():
    """stats"""
    return jsonify({
        "Amenities": storage.count(User),
        "State": storage.count(State)})
