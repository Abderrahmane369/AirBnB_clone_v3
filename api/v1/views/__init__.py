#!/usr/bin/python3
"""init"""
<<<<<<< HEAD
=======
from flask import Blueprint
>>>>>>> refs/remotes/origin/master
from api.v1.views import index
from flask import Blueprint
import states

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
