"""
Provides simple functions to read and write json data
"""

import json

from .get_root import get_root


def load_json(json_filename):
    """Returns json data"""
    json_filename += ".json"
    training_data_dir = get_root() / "training_data"
    with open(training_data_dir / json_filename,
              "r", encoding="UTF-8") as json_data:
        data = json.load(json_data)
    return data
