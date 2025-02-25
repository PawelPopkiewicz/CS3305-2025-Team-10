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

logging.basicConfig(level=logging.INFO)

RUSH_HOURS = (("0800", "1100"), ("1500", "1800"))


def is_between_time(start_time, end_time, check_time):
    """Return true if check time is between times"""
    return start_time <= check_time <= end_time


def map_time_to_rush_hours(timestamp):
    """Maps times to categorical rush hours"""
    timestamp = int(timestamp)
    check_time = datetime.fromtimestamp(timestamp).strftime("%H%M")
    for start_time, end_time in RUSH_HOURS:
        if is_between_time(start_time, end_time, check_time):
            return True
    return False


def map_date_to_weekday(date):
    """Maps dates to workday categorical"""
    dt = datetime.strptime(date, "%Y%m%d")
    return dt.weekday() < 5


def calc_interpolation(dist_1, t_1, dist_2, t_2, stop_dist):
    """Calculates interpolation"""
    if None in [dist_1, t_1, dist_2, t_2]:
        return None

    if dist_2 > stop_dist >= dist_1:
        ratio = (stop_dist - dist_1) / (dist_2 - dist_1)
        stop_time = t_1 + (t_2 - t_1) * ratio
        return stop_time
    return None


def calc_next_stop_time(current_time, current_distance, trips, stop_dist):
    """
    Calculates the time the next stop is reached
    uses linear interpolation
    """
    if not trips:
        return None

    next_update = trips[-1]
    stop_time = calc_interpolation(
            current_distance, current_time,
            next_update["distance"], next_update["timestamp"],
            stop_dist)
    if stop_time is not None:
        return stop_time

    for current_update, next_update in zip(
            reversed(trips[1:]), reversed(trips[:-1])):
        stop_time = calc_interpolation(
                current_update["distance"], current_update["timestamp"],
                next_update["distance"], next_update["timestamp"],
                stop_dist)

        if stop_time:
            return stop_time

    return None


def calc_time_to_next_stop(
        trips, stop_dist, current_timestamp, current_distance):
    """Calculates the time to reach the next bus stop"""
    stop_time = calc_next_stop_time(
            current_timestamp, current_distance,
            trips, stop_dist)
    if stop_time is not None:
        return stop_time - current_timestamp
    return None


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
        row = map_record_to_rows(record)
        if row is None:
            non_existent += 1
        else:
            rows += row

    print(f"Trips not found {non_existent} out of {num_of_rows_to_process}")
    df = pd.DataFrame(rows)
    csv_filename = csv_filename + ".csv"
    df.to_csv(training_data_dir / csv_filename, index=False)


def get_next_stop_distance(distance, stop_distances):
    """Returns the next distance based on the stop_distances provided"""
    distances = [sd[1] for sd in stop_distances]
    index = bisect.bisect_right(distances, distance)
    if index < len(stop_distances):
        return stop_distances[index][1]
    return None


def create_update_row_dict(trip_rows, record, stop_distances, update, trip_id, direction):
    """Creates the row per update"""
    route_name = get_route_name_from_trip(trip_id)
    timestamp = int(update["timestamp"])
    is_rush_hour = map_time_to_rush_hours(timestamp)
    is_weekday = map_date_to_weekday(record["start_date"])
    distance = map_coord_to_distance(
        trip_id, direction,
        float(update["latitude"]), float(update["longitude"])
    )
    next_stop_distance = get_next_stop_distance(
            distance, stop_distances)
    time_to_next_stop = None
    if next_stop_distance is not None:
        time_to_next_stop = calc_time_to_next_stop(
            trip_rows, next_stop_distance, timestamp, distance
        )

    return {
        "trip_id": trip_id,
        "route_name_from_trip_id": route_name,
        "direction": direction,
        "timestamp": timestamp,
        "is_rush_hour": is_rush_hour,
        "is_weekday": is_weekday,
        "distance": distance,
        "next_stop_distance": next_stop_distance,
        "time_to_next_stop": time_to_next_stop,
    }


def map_record_to_rows(record):
    """Maps a record of bus trip to the corresponding rows"""
    trip_id = record["trip_id"]
    direction = bool(record["direction_id"])
    if not check_trip_id_exists(trip_id, direction):
        return None

    stop_distances = get_stop_distances_for_trip(trip_id, direction)
    # for row in stop_distances:
    #     print(row)

    trip_rows = []
    # building it in reverse, oldest record is at index 0
    updates = reversed(record["vehicle_updates"])
    for update in updates:
        update_row = create_update_row_dict(
                trip_rows, record,
                stop_distances, update,
                trip_id, direction)
        trip_rows.append(update_row)
    return reversed(trip_rows[1:])
    # for i in range(len(record["vehicle_updates"]) - 1, -1, -1):
    #     update = record["vehicle_updates"][i]
    #     update_row = create_update_row_dict(
    #             trip_rows, record,
    #             stop_distances, update,
    #             trip_id, direction)
    #     trip_rows.append(update_row)
    # trip_rows.reverse()
    # # Potentially delete the first record as it does not have the time_to_next_stop valid value
    # return trip_rows


if __name__ == "__main__":
    json_file = "filtered_training_data"  # input("Name of the json file(without .json): ")
    csv_name = "test"  # input("Name of the csv file to be created: ")
    rows_subset = input("Number of rows to process out of the dataset: ")
    if rows_subset == "":
        create_csv(json_file, csv_name)
    create_csv(json_file, csv_name, int(rows_subset))
