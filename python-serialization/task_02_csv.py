#!/usr/bin/env python3
"""Convert a CSV file into a JSON file."""


import csv
import json


def convert_csv_to_json(filename):
    """Open and read a CSV file."""
    try:
        with open(filename, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            result = list(reader)
    except (FileNotFoundError):
        return False

    with open("data.json", mode="w", encoding="utf-8") as f:
        json.dump(result, f)
        return True
