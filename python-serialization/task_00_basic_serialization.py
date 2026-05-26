#!/usr/bin/python3


import json


"""
The function serialize_and_save_to_file take
2 parameters:

# data: A Python Dictionary with data
# filename: The filename of the output JSON file.

If the output file already exists it should be
replaced.
"""


def serialize_and_save_to_file(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file)


"""
The function load_and_deserialize take
1 parameters:

# filename: The filename of the input JSON file
This function returns a Python Dictionary
with the deserialized JSON data from the file.
"""


def load_and_deserialize(filename):
    with open(filename, "r") as file:
        return json.load(file)
