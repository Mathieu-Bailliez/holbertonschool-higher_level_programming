#!/usr/bin/env python3
"""Serialize and deserialize a Python dictionary with XML."""

import xml.etree.ElementTree as ET


def serialize_to_xml(dictionary, filename):
    """Serialize a dictionary into XML and save it to filename."""
    root = ET.Element("data")
    for key, value in dictionary.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ")
    tree.write(filename)


def deserialize_from_xml(filename):
    """Read XML from filename and return the reconstructed dictionary."""
    tree = ET.parse(filename)
    root = tree.getroot()
    result = {}
    for child in root:
        result[child.tag] = child.text
    return result
