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


@app_views.route('/status')
def get_status():
    """get the status code """
    return jsonify(status='OK')


@app_views.route('/stats')
def get_count():
    """retrieves the number of each objects by type"""

    classes = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    objs = {}
    for k, v in classes.items():
        objs[k] = storage.count(v)

    return jsonify(objs)
