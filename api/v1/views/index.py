#!/usr/bin/python3
"""index"""
from flask import Blueprint, jsonify

app_views = Blueprint('app_views', __name__,
                      url_prefix='/api/v1')


@app_views.route('/status', strict_slashes=False)
def status():
    """aaaaa"""
    return jsonify({'status': 'OK'})
