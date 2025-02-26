"""
Creation of stop_rows for a trip
Provides the estimates for all stop times
per stop
"""

import logging

from .coordinates_mapping import (map_coord_to_distance,
                                  check_trip_id_exists,
                                  get_route_name_from_trip,
                                  get_stop_distances_for_trip)

from .preprocessing_helper import (map_time_to_rush_hours,
                                   map_date_to_weekday,
                                   calc_interpolation)

logging.basicConfig(level=logging.INFO)


class Trip():
    """Manages the trip and provides methods to create stop times csv"""

    def __init__(self, record):
        self.record = record
        self.trip_id = record["trip_id"]
        self.route_name = get_route_name_from_trip(self.trip_id)
        self.is_weekday = map_date_to_weekday(record["start_date"])
        self.record_id = self.create_id()
        self.start_time = None
        self.direction = bool(record["direction_id"])
        self.stop_distances = get_stop_distances_for_trip(self.trip_id, self.direction)

    def create_stop_row_dict(self, stop_id, stop_dist, stop_time):
        """Creates one dict which will serve as a row in csv for all stop"""
        return {
                "id": self.record_id,
                "route_name": self.route_name,
                "is_weekday": self.is_weekday,
                "is_rush_hour": map_time_to_rush_hours(stop_time) if stop_time else None,
                "stop_id": stop_id,
                "stop_distance": stop_dist,
                "stop_time": (stop_time - self.start_time) if stop_time else None,
                }

    def create_id(self):
        """Create a unique id based on the date and trip_id"""
        return self.trip_id + self.record["start_date"]

    def create_stop_rows(self, update_rows):
        """Computes the arrival times for all stops based on the updates"""

        stop_rows = []
        stop_index = 0

        # skip the stops which are before the first update
        while self.stop_distances[stop_index][1] < update_rows[0][1]:
            stop_info = self.stop_distances[stop_index]
            stop_rows.append(self.create_stop_row_dict(
                stop_info[0], stop_info[1], None))
            stop_index += 1

        # Add all the stops which are between updates
        for current_update, next_update in zip(update_rows[:-1], update_rows[1:]):

            stop_info = self.stop_distances[stop_index]
            stop_time = calc_interpolation(
                    current_update[1], current_update[0],
                    next_update[1], next_update[0],
                    stop_info[1])

            while stop_time is not None:

                if self.start_time is None:
                    self.start_time = stop_time

                stop_rows.append(self.create_stop_row_dict(
                    stop_info[0], stop_info[1], stop_time))
                stop_index += 1

                stop_info = self.stop_distances[stop_index]
                stop_time = calc_interpolation(
                        current_update[1], current_update[0],
                        next_update[1], next_update[0],
                        stop_info[1])

        # Add all stops after the last update
        for _ in range(stop_index, len(self.stop_distances)):
            stop_info = self.stop_distances[stop_index]
            stop_rows.append(self.create_stop_row_dict(
                stop_info[0], stop_info[1], None))
            stop_index += 1

        return stop_rows

    def create_update_row_dict(self, update):
        """Creates the row per update"""
        timestamp = int(update["timestamp"])
        distance = map_coord_to_distance(
            self.trip_id, self.direction,
            float(update["latitude"]), float(update["longitude"])
        )
        return (timestamp, distance)

    def create_update_rows(self):
        """Creates a list of timestamp and distance for updates"""
        # building it in reverse, oldest record is at index 0
        # Create a csv which has timestamps and distances at those timestamp
        update_rows = []
        updates = reversed(self.record["vehicle_updates"])
        for update in updates:
            update_row = self.create_update_row_dict(update)
            update_rows.append(update_row)
        return list(reversed(update_rows))

    def map_record_to_stop_rows(self):
        """Maps a record of bus trip to the corresponding rows"""
        if not check_trip_id_exists(self.trip_id, self.direction):
            return None

        stop_distances = get_stop_distances_for_trip(self.trip_id, self.direction)

        update_rows = self.create_update_rows()
        logging.info(f"Number of updates = {len(update_rows)}")
        # Create a csv per stop, using linear interpolation to determine the arrival times at bus stops
        # Go through all of the updates and start adding arrival times in the stops, keeping track of the index
        # Add all of the metadata to the rows, plus the unique identifier of the trip
        stop_rows = self.create_stop_rows(update_rows)

        return stop_rows


if __name__ == "__main__":

    from .json_io import load_json
    data = load_json("test_record")
    test_trip = Trip(data)
    test_stop_rows = test_trip.map_record_to_stop_rows()
    for stop in test_stop_rows:
        logging.info(stop)
