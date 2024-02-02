#!/usr/bin/python3
"""index"""
from api.v1.views import app_views
from flask import Blueprint


@app_views.route('/status')
def status():
    """aaaaa"""
    return {
        'status': 'OK'
    }
