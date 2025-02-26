"""
Preprocessing functions which transform json training data into a csv
"""

import json
import bisect
import logging
from datetime import datetime

import pandas as pd

from .coordinates_mapping import (map_coord_to_distance,
                                  check_trip_id_exists,
                                  get_route_name_from_trip,
                                  get_stop_distances_for_trip)
from .get_root import get_root
# from .trip_to_update_times import map_record_to_update_rows
from .trip_to_stop_times import Trip

logging.basicConfig(level=logging.INFO)


def create_csv(raw_json_filename, csv_filename, subset_trips=None):
    """Creates a csv training_data"""
    rows = []
    json_filename = raw_json_filename + ".json"
    training_data_dir = get_root() / "training_data"
    with open(training_data_dir / json_filename,
              "r", encoding="UTF-8") as json_data:
        data = json.load(json_data)

    num_of_rows_to_process = len(data)
    if subset_trips:
        if len(data) < subset_trips:
            raise ValueError(
                    "Subset of trips exceeded the overall number of trips")
        num_of_rows_to_process = subset_trips

    report_freq = min(50, max(num_of_rows_to_process//100, 1))
    non_existent = 0

    for processed, record in enumerate(data[:num_of_rows_to_process]):
        if processed % report_freq == 0:
            logging.info(f"progress = {100*processed/num_of_rows_to_process:.2f}%")

        trip = Trip(record)
        row = trip.map_record_to_stop_rows()
        # row = map_record_to_update_rows(record)
        if row is None:
            non_existent += 1
        else:
            rows += row

    print(f"Trips not found {non_existent} out of {num_of_rows_to_process}")
    df = pd.DataFrame(rows)
    csv_filename = csv_filename + ".csv"
    df.to_csv(training_data_dir / csv_filename, index=False)


if __name__ == "__main__":
    json_file = "filtered_training_data"  # input("Name of the json file(without .json): ")
    csv_name = "test"  # input("Name of the csv file to be created: ")
    rows_subset = input("Number of rows to process out of the dataset: ")
    if rows_subset == "":
        create_csv(json_file, csv_name)
    create_csv(json_file, csv_name, int(rows_subset))
