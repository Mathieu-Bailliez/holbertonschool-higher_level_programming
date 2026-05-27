#!/usr/bin/env python3


import csv
import json


def convert_csv_to_json(filename):
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)
        with open("data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
            return True
    except Exception:
        return False
