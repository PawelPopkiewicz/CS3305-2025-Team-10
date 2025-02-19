"""
Preprocessing functions which transform json training data into a csv
"""

import json
from datetime import datetime
import pandas as pd
from coordinates_mapping import map_coord_to_progress, get_next_stop_distance, v1_get_next_stop_distance
from get_root import get_root


RUSH_HOURS = (
        ("0800", "1100"),
        ("1500", "1800")
        )


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


def create_csv(training_data_filename):
    """Creates a csv training_data"""
    rows = []
    root = get_root()
    json_filename = training_data_filename + ".json"
    training_data_dir = root / "training_data"
    with open(training_data_dir / json_filename, "r", encoding="UTF-8") as json_data:
        data = json.load(json_data)
    for record in data:
        rows += map_record_to_rows(record)
    df = pd.DataFrame(rows)
    csv_filename = "bus_dataset" + ".csv"
    df.to_csv(training_data_dir / csv_filename, index=False)


def map_record_to_rows(record):
    """Maps a record of bus trip to the corresponding rows"""
    trip_id = record["trip_id"]
    direction = bool(record["direction_id"])
    route_id = record["route_id"]
    trip_rows = []  # building it in reverse, oldest record is at index 0
    num_of_updates = len(record["vehicle_updates"])
    for i in range(num_of_updates - 1, -1, -1):
        update = record["vehicle_updates"][i]
        timestamp = int(update["timestamp"])
        progress = map_coord_to_progress(
                trip_id, direction, float(update["latitude"]), float(update["longitude"]))
        is_rush_hour = map_time_to_rush_hours(timestamp)
        is_weekday = map_date_to_weekday(record["start_date"])
        next_stop_progress = v1_get_next_stop_distance(
                progress, trip_id, direction)
        time_to_next_stop = 0
        if trip_rows:
            time_to_next_stop = trip_rows[-1]["timestamp"] - timestamp
        update_row = {
                "trip_id": trip_id,
                "route_id": route_id,
                "direction": direction,
                "timestamp": timestamp,
                "is_rush_hour": is_rush_hour,
                "is_weekday": is_weekday,
                "progress": progress,
                "next_stop_progress": next_stop_progress,
                "time_to_next_stop": time_to_next_stop
                }
        trip_rows.append(update_row)
    trip_rows.reverse()
    # Potentially delete the first record as it does not have the time_to_next_stop with a valid value
    return trip_rows


if __name__ == "__main__":
    create_csv("small_data")
