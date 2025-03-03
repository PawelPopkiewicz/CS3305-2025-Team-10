"""
Creation of stop_times for a trip
Provides the estimates for all stop times
per stop
"""

import logging

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

    STOP_THRESHOLD = 10
    OFF_ROUTE_THRESHOLD = 200

    def __init__(self, record):
        self.record = record
        self.trip_id = record["trip_id"]
        self.route_name = get_route_name_from_trip(self.trip_id)
        self.day = map_date_to_day(record["start_date"])
        self.record_id = self.create_id()
        self.start_time = None
        self.start_distance = None
        self.current_delay = None
        self.direction = bool(record["direction_id"])
        self.stop_distances = get_stop_distances_for_trip(
                self.trip_id, self.direction)
        self.stop_times = None

    def check_trip_filters_after(self):
        """Return true if the trip is usable for training"""
        return self.enough_stops_filter()

    def check_trip_filters_before(self):
        """Return true if the trip is eligible for conversion"""
        return self.on_route_filter() and check_trip_id_exists(
                self.trip_id, self.direction)

    def enough_stops_filter(self):
        """Return true if there are enough stops with arrival times"""
        if self.stop_times:
            if len(self.stop_times) > self.STOP_THRESHOLD:
                return True
        return False

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

    def create_stop_row_dict(self, stop_info, stop_time, last_stop=None):
        """Creates one dict which will serve as a row in csv for all stop"""
        if stop_time is None:
            return [None]*2
        scheduled_arrival_time = round(map_strtime_to_timestamp(
            self.record["start_date"], stop_info[2]) - self.start_time, 1)
        scheduled_departure_time = round(map_strtime_to_timestamp(
            self.record["start_date"], stop_info[3]) - self.start_time, 1)
        stop_distance = round(stop_info[1] - self.start_distance, 1)
        last_stop_info = {
                "stop_distance": stop_distance,
                "scheduled_arrival_time": scheduled_arrival_time,
                "scheduled_departure_time": scheduled_departure_time
                }
        time_to_stop, distance_to_stop = 0, 0
        idle_time = 0
        if last_stop is not None:
            time_to_stop = round(scheduled_arrival_time - last_stop["scheduled_arrival_time"], 1)
            distance_to_stop = round(stop_distance - last_stop["stop_distance"], 1)
            idle_time = round(last_stop["scheduled_departure_time"] - last_stop["scheduled_arrival_time"], 1)
        stop_row = {
                "id": self.record_id,
                "route_name": self.route_name,
                "day": self.day,
                "time": map_timestamp_to_minutes(stop_time),
                "stop_id": stop_info[0],
                "distance_to_stop": distance_to_stop,
                "time_to_stop": time_to_stop,
                "idle_time": idle_time,
                "residual_stop_time": round(
                    (stop_time - self.start_time) - scheduled_arrival_time - self.current_delay, 1),
                }
        return stop_row, last_stop_info

    def create_id(self):
        """Create a unique id based on the date and trip_id"""
        return self.trip_id + self.record["start_date"]

    def create_stop_times(self, update_rows):
        """Computes the arrival times for all stops based on the updates"""

        stop_times = []
        stop_index = 0

        # skip the stops which are before the first update
        while self.stop_distances[stop_index][1] < update_rows[0][1]:
            # stop_info = self.stop_distances[stop_index]
            # stop_times.append(self.create_stop_row_dict(
            #     stop_info[0], stop_info[1], None))
            stop_index += 1

            if stop_index >= len(self.stop_distances):
                return stop_times

        last_stop = None
        # Add all the stops which are between updates
        for current_update, next_update in zip(
                update_rows[:-1], update_rows[1:]):

            stop_info = self.stop_distances[stop_index]
            stop_time = calc_interpolation(
                    current_update[1], current_update[0],
                    next_update[1], next_update[0],
                    stop_info[1])

            while stop_time is not None:

                if self.start_time is None:
                    self.start_time = map_strtime_to_timestamp(
                            self.record["start_date"], stop_info[2])
                    self.start_distance = stop_info[1]
                    self.current_delay = stop_time - self.start_time
                row, last_stop = self.create_stop_row_dict(
                        stop_info, stop_time, last_stop)
                if row is not None:
                    stop_times.append(row)
                stop_index += 1

                if stop_index >= len(self.stop_distances):
                    return stop_times

                stop_info = self.stop_distances[stop_index]
                stop_time = calc_interpolation(
                        current_update[1], current_update[0],
                        next_update[1], next_update[0],
                        stop_info[1])

        # Add all stops after the last update
        # for i in range(stop_index, len(self.stop_distances)):
        #     stop_info = self.stop_distances[stop_index]
        #     stop_times.append(self.create_stop_row_dict(
        #         stop_info[0], stop_info[1], None))
        #     stop_index += 1

        return stop_times

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
        update_rows = []
        updates = reversed(self.record["vehicle_updates"])
        for update in updates:
            update_row = self.create_update_row_dict(update)
            update_rows.append(update_row)
        return list(reversed(update_rows))

    def map_record_to_stop_times(self):
        """Maps a record of bus trip to the corresponding rows"""
        if not self.check_trip_filters_before():
            return None
        update_rows = self.create_update_rows()
        self.stop_times = self.create_stop_times(update_rows)
        if not self.check_trip_filters_after():
            return None
        return self.stop_times


if __name__ == "__main__":
    from .json_io import load_json
    data = load_json("test_record")
    test_trip = Trip(data)
    test_stop_times = test_trip.map_record_to_stop_times()
    for stop in test_stop_times:
        logging.info(stop)
