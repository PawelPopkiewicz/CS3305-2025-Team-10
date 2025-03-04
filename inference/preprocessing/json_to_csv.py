"""
Preprocessing functions which transform json training data into a csv
"""

import json
import logging

import pandas as pd

from .coordinates_mapping import (map_coord_to_distance,
                                  check_trip_id_exists,
                                  get_route_name_from_trip,
                                  get_stop_distances_for_trip)
from .get_root import get_root
# from .trip_to_update_times import map_record_to_update_rows
from .trip_to_stop_times import TripGenerator

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
    processed_trips = 0

    for processed, record in enumerate(data[:num_of_rows_to_process]):
        if processed % report_freq == 0:
            logging.info(f"progress = {100*processed/num_of_rows_to_process:.2f}%")

        tg = TripGenerator(record)
        trips = tg.map_record_to_training_stop_times()
        if trips is not None and len(trips) > 0:
            for trip in trips:
                rows += trip.stops
            processed_trips += 1

    logging.info(f"Processed {processed_trips} out of {num_of_rows_to_process}, {num_of_rows_to_process - processed_trips} removed")
    df = pd.DataFrame(rows)
    csv_filename = csv_filename + ".csv"
    df.to_csv(training_data_dir / csv_filename, index=False)


if __name__ == "__main__":
    json_file = "filtered_training_data"  # input("Name of the json file(without .json): ")
    csv_name = "test"  # input("Name of the csv file to be created: ")
    rows_subset = input("Number of rows to process out of the dataset: ")
    if rows_subset == "":
        create_csv(json_file, csv_name)
    else:
        create_csv(json_file, csv_name, int(rows_subset))
