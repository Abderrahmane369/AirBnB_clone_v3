#!/usr/bin/python3
"""loooog"""
from flask import abort, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views, cities


@app_views.route('/states', methods=['GET'],
                 strict_slashes=False)
def states():
    """states"""
    return list(map(lambda v: v.to_dict(),
                    storage.all(State).values()))


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def getState(state_id):
    """get"""
    if storage.get(State, state_id):
        return storage.get(State, state_id).to_dict()
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteState(state_id):
    """delete"""
    if storage.get(State, state_id):
        storage.delete(storage.get(State, state_id))
        storage.save()
        return {}, 202

    abort(404)


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def createState():
    """create"""
    data = request.get_json()
    state = State(**data)

    if not data:
        abort(400, description='Not a JSON')
    elif 'name' not in data:
        abort(400, description='Missing name')

    storage.new(state)
    storage.save()

    return state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def updateState(state_id):
    """update"""
    data = request.get_json()
    state = storage.get(State, state_id)

    if not data:
        abort(400, description='Not a JSON')
    elif not state:
        abort(404)

    icu = {'id', 'created_at', 'updated_at'}

    storage.delete(state)

    for a, v in data.items():
        if hasattr(state, a) and a not in icu:
            setattr(state, a, v)

    storage.new(state)
    storage.save()

    return state.to_dict().pop(cities), 200
