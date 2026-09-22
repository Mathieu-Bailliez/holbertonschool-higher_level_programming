#!/usr/bin/env python3
"""Create a class , serialise the instance with pickle and deserialize."""


import pickle


class CustomObject:
    """Class that represent a person."""

    def __init__(self, name, age, is_student):
        """Initialise the instance."""
        self.name = name
        self.age = age
        self.is_student = is_student

    def display(self):
        """Display the information about the person."""
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Is Student: {self.is_student}")

    def serialize(self, filename):
        """Serialize objet with pickle module and save it
        in a given filename."""
        try:
            with open(filename, mode="wb") as f:
                pickle.dump(self, f)
        except (OSError, pickle.PicklingError):
            return None

    @classmethod
    def deserialize(cls, filename):
        """Deserialize a binary file and return a python objet."""
        try:
            with open(filename, mode="rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError, EOFError):
            return None
