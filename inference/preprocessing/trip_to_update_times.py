"""
Creation of update_rows for a trip
Provides the estimates for next stop arrival times
per update
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
from .preprocessing_helper import (map_time_to_rush_hours,
                                   map_date_to_weekday,
                                   calc_interpolation)

logging.basicConfig(level=logging.INFO)


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


def map_record_to_update_rows(record):
    """Maps a record of bus trip to the corresponding rows"""
    trip_id = record["trip_id"]
    direction = bool(record["direction_id"])
    if not check_trip_id_exists(trip_id, direction):
        return None

    stop_distances = get_stop_distances_for_trip(trip_id, direction)
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
