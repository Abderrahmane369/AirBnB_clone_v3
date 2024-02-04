#!/usr/bin/python3
"""index"""
from api.v1.views import app_views
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from flask import jsonify


@app_views.route('/status', methods=['GET'],
                 strict_slashes=False)
def status():
    """status"""
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'],
                 strict_slashes=False)
def stats():
    """stats"""
    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    })
