"""
Preprocessing functions which transform json training data into a csv
"""

import json
from datetime import time, datetime
import pandas as pd
from coordinates_mapping import map_coord_to_progress, get_next_stop_distance, v1_get_next_stop_distance
from get_root import get_root


RUSH_HOURS = (
        (time(8, 0), time(11, 0)),
        (time(15, 0), time(18, 0))
        )


def is_between_time(start_time, end_time, check_time):
    """Return true if check time is between times"""
    return start_time <= check_time <= end_time


def create_csv():
    """Creates a csv training_data"""
    rows = []
    root = get_root()
    json_filename = "training_data" + ".json"
    training_data_dir = root / "inference" / "training_data"
    with open(training_data_dir / json_filename, "r", encoding="UTF-8") as json_data:
        data = json.load(json_data)
    for record in data:
        rows += map_record_to_rows(record)
    df = pd.DataFrame(rows)
    csv_filename = "bus_dataset" + ".csv"
    df.to_csv(training_data_dir / csv_filename, index=False)


def map_time_to_rush_hours(timestamp):
    """Maps times to categorical rush hours"""
    check_time = time.localtime(timestamp)
    for rush_hours in RUSH_HOURS:
        if is_between_time(rush_hours[0], rush_hours[1], check_time):
            return True
    return False


def map_date_to_weekday(date):
    """Maps dates to workday categorical"""
    date = datetime(date[:4], date[4:6], date[6:])
    return date.weekday() < 5


def map_record_to_rows(record):
    """Maps a record of bus trip to the corresponding rows"""
    trip_id = record["trip_id"]
    direction = record["direction"]
    route_id = record["route_id"]
    trip_rows = []  # building it in reverse, oldest record is at index 0
    num_of_updates = len(record["vehicle_updates"])
    for i in range(num_of_updates - 1, -1, -1):
        update = record["vehicle_updates"][i]
        timestamp = update["timestamp"]
        progress = map_coord_to_progress(trip_id, direction, update["latitude"], update["longitude"])
        is_rush_hour = map_time_to_rush_hours(timestamp)
        is_weekday = map_date_to_weekday(record["start_date"])
        next_stop_progress = v1_get_next_stop_distance(progress, trip_id, direction)
        if trip_rows:
            time_to_next_stop = trip_rows[-1]["timestamp"] - timestamp
        else:
            time_to_next_stop = 0
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
    create_csv()
