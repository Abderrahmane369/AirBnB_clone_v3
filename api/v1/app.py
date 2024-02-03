#!/usr/bin/python3
"""Application"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def db_close(exception):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """404 not found"""
    return jsonify({
        "error": "Not found"})


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)
