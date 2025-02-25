"""
Filter the documents which have faulty fields
"""

import json

from .coordinates_mapping import check_trip_id_exists
from .get_root import get_root


def filter_trips(raw_json_filename):
    """Filters the trips where their trip id expired"""
    json_filename = raw_json_filename + ".json"
    training_data_dir = get_root() / "training_data"
    with open(training_data_dir / json_filename,
              "r", encoding="UTF-8") as json_data:
        data = json.load(json_data)
    filtered_data = list(filter(trip_filter, data))
    return filtered_data


def trip_filter(record):
    """Combines specific filters into on func"""
    return trip_exists_for_record(record) and trip_has_enough_updates(record)


def trip_exists_for_record(record):
    """Returns True if the record has a valid trip_id"""
    trip_id = record["trip_id"]
    direction = bool(record["direction_id"])
    return check_trip_id_exists(trip_id, direction)


def trip_has_enough_updates(record):
    """Return true if the number of trip updates is higher than a threshold"""
    return len(record["vehicle_updates"]) >= 10


def create_json_file(json_data, filename):
    """Creates the json file"""
    training_data_dir = get_root() / "training_data"
    filename = filename + ".json"
    with open(training_data_dir / filename,
              "+w", encoding="UTF-8") as json_file:
        json.dump(json_data, json_file)


def filter_store(raw_json_filename, filtered_json_filename):
    """Filter the json data and store it"""
    filtered_data = filter_trips(raw_json_filename)
    create_json_file(filtered_data, filtered_json_filename)


if __name__ == "__main__":
    RAW_JSON = "training_data"
    FILTER_JSON = "filtered_training_data"
    filter_store(RAW_JSON, FILTER_JSON)
