"""
Fetches the training data from the training_data_collection container and stores it
"""

import os
import json
import requests
from .get_root import get_root


def fetch_training_data(filename):
    """Fetch training data and store it"""
    training_data_collection_uri = os.getenv("TRAINING_URI")
    try:
        response = requests.get(training_data_collection_uri + "/trips", timeout=10)
        json_data = response.json()
        training_data_dir = get_root() / "training_data"
        filename = filename + ".json"
        with open(training_data_dir / filename, "+w", encoding="UTF-8") as json_file:
            json.dump(json_data, json_file)
    except Exception as e:
        print(f"Error occured when fetching the json file: {e}")
