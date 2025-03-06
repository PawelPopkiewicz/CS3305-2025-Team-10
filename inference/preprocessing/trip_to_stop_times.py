"""
Creation of stop_times for a trip
Provides the estimates for all stop times
per stop
"""

import logging
import numpy as np
import pandas as pd

from .coordinates_mapping import (map_coord_to_distance,
                                  check_trip_id_exists,
                                  get_route_name_from_trip,
                                  get_stop_distances_for_trip,
                                  off_route_distance)

from .preprocessing_helper import (calc_interpolation,
                                   map_timestamp_to_minutes,
                                   map_date_to_day,
                                   map_strtime_to_timestamp)

logging.basicConfig(level=logging.INFO)


class Trip():
    """Manages the trip and provides methods to create stop times csv"""

    TRAINING_STOP_THRESHOLD = 10
    INFERENCE_STOP_THRESHOLD = 3
    MAX_TARGET_STOPS = 15

    def __init__(self, record, counter):
        self.observed_stops = []
        self.target_stops = []
        self.remaining_stops = []
        self.record = record
        self.trip_id = record["trip_id"]
        self.route_name = get_route_name_from_trip(self.trip_id)
        self.day = map_date_to_day(record["start_date"])
        self.record_id = self.create_id(counter)
        self.start_time = None
        self.start_distance = None
        self.current_delay = None
        self.direction = bool(record["direction_id"])
        self.configured = False

    def create_id(self, counter):
        """Create a unique id based on the date and trip_id"""
        return self.trip_id + self.record["start_date"] + str(counter)

    def config(self, start_time, start_distance, stop_time):
        """Configures the start times needed for normalization, etc"""
        self.start_time = start_time
        self.start_distance = start_distance
        self.current_delay = stop_time - start_time
        self.configured = True


    def inference_eligible(self):
        """Returns true if the trip is ready to be inferred upon"""
        return self.enough_inference_stops_filter()


    def enough_training_stops_filter(self):
        """Return true if there are enough stops with arrival times"""
        if self.observed_stops and len(self.observed_stops) > self.TRAINING_STOP_THRESHOLD:
            return True
        return False

    def enough_inference_stops_filter(self):
        """Returns true if there are enough stops for inference"""
        if self.observed_stops and len(self.observed_stops) > self.INFERENCE_STOP_THRESHOLD:
            return True
        return False

    def add_stop(self, stop_info, stop_time=None, last_stop_metadata=None, reached_idle=False):
        """Add a stop row to the array"""
        stop_metadata = self.create_stop_metadata(stop_info)
        stop_row = self.create_stop_row_dict(
                stop_info, stop_time, stop_metadata, last_stop_metadata)
        if stop_row is not None:
            if stop_time is not None:
                self.observed_stops.append(stop_row)
            elif len(self.target_stops) < self.MAX_TARGET_STOPS and not reached_idle:
                self.target_stops.append(stop_row)
            else:
                self.remaining_stops.append(stop_row)
            return stop_metadata
        return None

    def create_stop_metadata(self, stop_info):
        """Creates the info/metadata about a stop"""
        scheduled_arrival_time = round(map_strtime_to_timestamp(
            self.record["start_date"], stop_info[2]) - self.start_time, 1)
        scheduled_departure_time = round(map_strtime_to_timestamp(
            self.record["start_date"], stop_info[3]) - self.start_time, 1)
        stop_distance = round(stop_info[1] - self.start_distance, 1)
        return {
                "stop_distance": stop_distance,
                "scheduled_arrival_time": scheduled_arrival_time,
                "scheduled_departure_time": scheduled_departure_time
                }

    def get_observed_df(self):
        """Returns the training dataframe"""
        return pd.DataFrame(self.observed_stops)

    def get_target_df(self):
        """Return the target dataframe"""
        return pd.DataFrame(self.target_stops)

    def get_remaining_df(self):
        """Return the remaining dataframe"""
        return pd.DataFrame(self.remaining_stops)

    observed_df = property(get_observed_df)
    target_df = property(get_target_df)
    remaining_df = property(get_remaining_df)

    def display_df(self):
        """Return all of the stops with proper flags"""
        # stop_id, scheduled_arrival_time, predicted_time (None for remaining), flag (Observed, Predicted, Scheduled)
        observed_df = self.observed_df.copy() if not self.observed_df.empty else pd.DataFrame()
        target_df = self.target_df.copy() if not self.target_df.empty else pd.DataFrame()
        remaining_df = self.remaining_df.copy() if not self.remaining_df.empty else pd.DataFrame()

        if not observed_df.empty:
            observed_df["residual_stop_time"] = observed_df["residual_stop_time"].fillna(0).infer_objects(copy=False)
            observed_df["arrival_time"] = (
                observed_df["scheduled_arrival_time"].fillna(0) +
                observed_df["residual_stop_time"] +
                self.current_delay +
                self.start_time
            )
            observed_df["type"] = "Observed"

        if not target_df.empty:
            target_df["residual_stop_time"] = target_df["residual_stop_time"].fillna(0).infer_objects(copy=False)
            target_df["arrival_time"] = (
                target_df["scheduled_arrival_time"].fillna(0) +
                target_df["residual_stop_time"] +
                self.current_delay +
                self.start_time
            )
            target_df["type"] = "Predicted"

        if not remaining_df.empty:
            remaining_df["arrival_time"] = None  # Explicitly set to NaN
            remaining_df["type"] = "Scheduled"

        # Exclude empty DataFrames before concatenation
        dfs_to_concat = [df for df in [observed_df, target_df, remaining_df] if not df.empty]
        display_df = pd.concat(dfs_to_concat, ignore_index=True) if dfs_to_concat else pd.DataFrame()
        display_df["scheduled_arrival_time"] = display_df["scheduled_arrival_time"] + self.start_time
        display_df["scheduled_departure_time"] = display_df["scheduled_departure_time"] + self.start_time

        display_df = display_df.drop(columns=["id", "route_name", "day", "time", "distance_to_stop", "time_to_stop", "residual_stop_time"])

        return display_df
        # observed_df = self.observed_df
        # observed_df["arrival_time"] = observed_df["scheduled_arrival_time"] + observed_df["residual_stop_time"]
        # observed_df["arrival_time"] += self.current_delay + self.start_time
        # target_df = self.target_df
        # target_df["arrival_time"] = target_df["scheduled_arrival_time"] + target_df["residual_stop_time"]
        # target_df["arrival_time"] += self.current_delay + self.start_time
        # remaining_df = self.remaining_df
        # remaining_df["arrival_time"] = np.nan
        # display_df = pd.concat([self.observed_df, self.target_df, self.remaining_df], ignore_index=True)
        # return display_df

    def add_predictions(self, predictions):
        """Add the predictions(vector) to the target_stops"""
        target_df = self.target_df
        target_df["residual_stop_time"] = predictions
        self.target_stops = target_df.to_dict("records")

    def create_stop_row_dict(self, stop_info, stop_time, stop_metadata, last_stop_metadata=None):
        """Creates one dict which will serve as a row in csv for all stop"""
        residual_stop_time = None
        if stop_time is not None:
            residual_stop_time = round(
                    (stop_time - self.start_time) - stop_metadata["scheduled_arrival_time"] - self.current_delay, 1)

        time_to_stop, distance_to_stop = 0, 0
        if last_stop_metadata is not None:
            time_to_stop = round(stop_metadata["scheduled_arrival_time"] - last_stop_metadata["scheduled_arrival_time"], 1)
            distance_to_stop = round(stop_metadata["stop_distance"] - last_stop_metadata["stop_distance"], 1)
        time = map_timestamp_to_minutes(
                stop_metadata["scheduled_arrival_time"] + self.start_time + self.current_delay)
        return {
                "id": self.record_id,
                "route_name": self.route_name,
                "day": self.day,
                "time": time,
                "stop_id": stop_info[0],
                "scheduled_arrival_time": stop_metadata["scheduled_arrival_time"],
                "scheduled_departure_time": stop_metadata["scheduled_departure_time"],
                "distance_to_stop": distance_to_stop,
                "time_to_stop": time_to_stop,
                "residual_stop_time": residual_stop_time,
                }


class TripGenerator():
    """Manages the trip and provides methods to create stop times csv"""

    OFF_ROUTE_THRESHOLD = 200

    def __init__(self, record):
        self.record = record
        self.trip_id = record["trip_id"]
        self.route_name = get_route_name_from_trip(self.trip_id)
        self.day = map_date_to_day(record["start_date"])
        self.direction = bool(record["direction_id"])
        self.stop_distances = get_stop_distances_for_trip(
                self.trip_id, self.direction)
        self.trips = []

    def check_trip_filters_after(self):
        """Filter all of the trips which are not suitable for training"""
        for i in range(len(self.trips)-1, -1, -1):
            if not self.trips[i].enough_training_stops_filter():
                self.trips.pop(i)

    def check_trip_filters_before(self):
        """Return true if the trip is eligible for conversion"""
        exists = check_trip_id_exists(self.trip_id, self.direction)
        return exists

    def on_route_filter(self):
        """Checks if any of the updates are not on route"""
        updates = self.record["vehicle_updates"]
        not_on_route_counter = 0
        for update in updates:
            if not self.update_on_route(
                    float(update["latitude"]), float(update["longitude"])):
                not_on_route_counter += 1
                if not_on_route_counter >= 3:
                    return False
        return True

    def update_on_route(self, latitude, longitude):
        """Returns true if the bus is on route"""
        distance = off_route_distance(
                self.trip_id, self.direction, latitude, longitude)
        if distance is not None and distance < self.OFF_ROUTE_THRESHOLD:
            return True
        return False

    def is_idle_stop(self, check_stop):
        """
        Checks if the stop had idle time
        Will be used to split the trips apart to remove the inconsistency
        """
        idle_time = round(
                check_stop["scheduled_departure_time"] - check_stop["scheduled_arrival_time"], 1)
        if idle_time > 30:
            return True
        return False

    def get_stop_time(self, stop_info, current_update, next_update):
        """Returns interpolated stop_time and stop_info by index"""
        stop_time = calc_interpolation(
                current_update[1], current_update[0],
                next_update[1], next_update[0],
                stop_info[1])
        return stop_time

    def skip_invalid_stop(self, update_rows):
        """Skips the stops for which we have no data"""
        stop_index = 0
        while self.stop_distances[stop_index][1] < update_rows[0][1]:
            stop_index += 1
            if stop_index >= len(self.stop_distances):
                return None
        return stop_index

    def add_unobserved_stops(self, stop_index):
        """
        Adds the remaining stops for which we have no updates
        """
        if len(self.trips) == 0:
            return
        last_trip = self.trips[-1]
        if not last_trip.configured:
            return
        last_stop = None
        reached_idle = False
        for i in range(stop_index, len(self.stop_distances)):
            stop_info = self.stop_distances[i]
            if last_stop is not None and self.is_idle_stop(last_stop):
                reached_idle = True
            # Initiate the config data for a trip
            last_stop = last_trip.add_stop(
                    stop_info=stop_info, last_stop_metadata=last_stop, reached_idle=reached_idle)

    def add_update_stops(self, update_rows, stop_index):
        """Adds the trips and their stops for which we have updates"""
        last_stop = None
        trip = Trip(self.record, 0)
        # Add all the stops which are between updates
        for current_update, next_update in zip(
                update_rows[:-1], update_rows[1:]):

            stop_info = self.stop_distances[stop_index]
            stop_time = self.get_stop_time(
                    stop_info, current_update, next_update)

            while stop_time is not None:
                # Split the trips
                if last_stop is not None and self.is_idle_stop(last_stop):
                    self.trips.append(trip)
                    trip = Trip(self.record, len(self.trips))
                    last_stop = None
                # Initiate the config data for a trip
                if not trip.configured:
                    trip.config(map_strtime_to_timestamp(
                            self.record["start_date"], stop_info[2]),
                            stop_info[1],
                            stop_time)
                # Add the stop row to the trip
                last_stop = trip.add_stop(stop_info, stop_time, last_stop)
                stop_index += 1
                # Exit if we reach the end of stops in the while loop
                if stop_index >= len(self.stop_distances):
                    self.trips.append(trip)
                    # return self.trips
                    return stop_index
                # Get the next stop_time data
                stop_info = self.stop_distances[stop_index]
                stop_time = self.get_stop_time(
                        stop_info, current_update, next_update)

        self.trips.append(trip)
        return stop_index

    def create_inference_trips(self, update_rows):
        """Creates the trips to infer on"""
        stop_index = self.skip_invalid_stop(update_rows)
        if stop_index is None:
            return

        stop_index = self.add_update_stops(update_rows, stop_index)

        self.add_unobserved_stops(stop_index)

    def create_training_trips(self, update_rows):
        """Computes the arrival times for all stops based on the updates"""
        stop_index = self.skip_invalid_stop(update_rows)
        if stop_index is None:
            return

        stop_index = self.add_update_stops(update_rows, stop_index)

    def create_update_row_dict(self, update):
        """Creates the row per update"""
        timestamp = int(update["timestamp"])
        distance, off_route = map_coord_to_distance(
            self.trip_id, self.direction,
            float(update["latitude"]), float(update["longitude"])
        )
        return (timestamp, distance), off_route

    def create_update_rows(self):
        """Creates a list of timestamp and distance for updates"""
        # building it in reverse, oldest record is at index 0
        update_rows = []
        updates = reversed(self.record["vehicle_updates"])
        for update in updates:
            update_row, off_route = self.create_update_row_dict(update)
            if off_route > self.OFF_ROUTE_THRESHOLD:
                return None
            update_rows.append(update_row)
        return list(reversed(update_rows))

    def map_record_to_training_stop_times(self):
        """Maps a record of bus trip to the corresponding rows"""
        if not self.check_trip_filters_before():
            return None
        update_rows = self.create_update_rows()
        if update_rows is None:
            return None
        self.create_training_trips(update_rows)
        self.check_trip_filters_after()
        return self.trips

    def map_record_to_inference_stop_times(self):
        """Maps a record to inference stop time data"""
        if not self.check_trip_filters_before():
            return None
        update_rows = self.create_update_rows()
        if update_rows is None:
            return None
        self.create_inference_trips(update_rows)
        # self.check_trip_filters_after()
        return self.trips


if __name__ == "__main__":
    from .json_io import load_json
    data = load_json("test_record")
