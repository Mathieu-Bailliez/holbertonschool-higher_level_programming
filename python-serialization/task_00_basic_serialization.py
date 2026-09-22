#!/usr/bin/env python3
"""Module : Provide two function, one for serialize and the other for
deserialize."""

import json


def serialize_and_save_to_file(data, filename):
    """Open a file, serialise the python objet into a JSON format."""
    with open(filename, mode="w", encoding="utf-8") as f:
        json.dump(data, f)


def load_and_deserialize(filename):
    """Open a file, read it, and return a python object."""
    with open(filename, mode="r", encoding="utf-8") as f:
        return json.load(f)
