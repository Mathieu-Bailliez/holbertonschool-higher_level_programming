#!/usr/bin/env python3
"""Create my first API using Flask python module."""

from flask import Flask
from flask import jsonify


app = Flask(__name__)


users = {}


@app.route("/")
def home():
    return "Welcome to the Flask API!"


@app.route("/data")
def data():
    return jsonify(list(users.keys()))


@app.route("/status")
def status():
    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
