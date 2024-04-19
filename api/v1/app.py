#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)


"""register the blueprint"""
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """remove the current session"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """return a JSON-formatted 404"""
    error = {
        'error': 'Not found'
    }
    return jsonify(error), 404


if __name__ == '__main__':
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port, threaded=True)
