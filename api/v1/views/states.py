#!/usr/bin/python3
"""loooog"""
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'],
                 strict_slashes=False)
def states():
    """states"""
    return list(map(lambda v: v.to_dict(),
                    storage.all(State).values()))


@app_views.route('/state/<state_id>', methods=['GET'],
                 strict_slashes=False)
def state(state_id):
    """state"""
    return storage.get(State, state_id).to_dict() || 404
