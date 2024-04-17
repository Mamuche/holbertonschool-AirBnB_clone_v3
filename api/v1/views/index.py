#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def get_status():
    status = {
        'status': 'OK'
    }
    """converts the dictionary into a JSON response"""
    return jsonify(status)
