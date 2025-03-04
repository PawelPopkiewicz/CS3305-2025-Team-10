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

    def __init__(self, record, counter):
        self.stops = []
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

    def enough_stops_filter(self):
        """Return true if there are enough stops with arrival times"""
        if self.stops:
            if len(self.stops) > self.STOP_THRESHOLD:
                return True
        return False

    def add_stop(self, stop_info, stop_time=None, last_stop_metadata=None):
        """Add a stop row to the array"""
        stop_metadata = self.create_stop_metadata(stop_info)
        stop_row = self.create_stop_row_dict(
                stop_info, stop_time, stop_metadata, last_stop_metadata)
        if stop_row is not None:
            self.stops.append(stop_row)
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

    def create_stop_row_dict(self, stop_info, stop_time, stop_metadata, last_stop_metadata=None):
        """Creates one dict which will serve as a row in csv for all stop"""
        residual_stop_time = None
        if stop_time is not None:
            residual_stop_time = round(
                    (stop_time - self.start_time) - stop_metadata["scheduled_arrival_time"] - self.current_delay, 1)
        # stop_metadata = self.create_last_stop_info(stop_info)

        # scheduled_arrival_time = round(map_strtime_to_timestamp(
        #     self.record["start_date"], stop_info[2]) - self.start_time, 1)
        # scheduled_departure_time = round(map_strtime_to_timestamp(
        #     self.record["start_date"], stop_info[3]) - self.start_time, 1)
        # stop_distance = round(stop_info[1] - self.start_distance, 1)
        # last_stop_info = {
        #         "stop_distance": stop_distance,
        #         "scheduled_arrival_time": scheduled_arrival_time,
        #         "scheduled_departure_time": scheduled_departure_time
        #         }

        time_to_stop, distance_to_stop = 0, 0
        if last_stop_metadata is not None:
            time_to_stop = round(stop_metadata["scheduled_arrival_time"] - last_stop_metadata["scheduled_arrival_time"], 1)
            distance_to_stop = round(stop_metadata["stop_distance"] - last_stop_metadata["stop_distance"], 1)

        return {
                "id": self.record_id,
                "route_name": self.route_name,
                "day": self.day,
                "time": map_timestamp_to_minutes(stop_time),
                "stop_id": stop_info[0],
                "distance_to_stop": distance_to_stop,
                "time_to_stop": time_to_stop,
                "residual_stop_time": residual_stop_time,
                }


class TripGenerator():
    """Manages the trip and provides methods to create stop times csv"""

    STOP_THRESHOLD = 10
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
            if not self.trips[i].enough_stops_filter():
                self.trips.pop(i)

    def check_trip_filters_before(self):
        """Return true if the trip is eligible for conversion"""
        return check_trip_id_exists(self.trip_id, self.direction)

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

    def add_remaining_stops(self, stop_index):
        """
        Adds the remaining stops for which we have no updates
        Adds only to the last trip, does not create new ones after idle stops
        """
        if len(self.trips) == 0:
            return
        last_trip = self.trips[-1]
        if not last_trip.configured:
            return
        last_stop = None
        for i in range(stop_index, len(self.stop_distances)):
            stop_info = self.stop_distances[i]
            if last_stop is not None and self.is_idle_stop(last_stop):
                # Reached an idle stop
                return
            # Initiate the config data for a trip
            last_stop = last_trip.add_stop(
                    stop_info=stop_info, last_stop=last_stop)

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
            # stop_info = self.stop_distances[stop_index]
            # stop_time = calc_interpolation(
            #         current_update[1], current_update[0],
            #         next_update[1], next_update[0],
            #         stop_info[1])

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
                # stop_info = self.stop_distances[stop_index]
                # stop_time = calc_interpolation(
                #         current_update[1], current_update[0],
                #         next_update[1], next_update[0],
                #         stop_info[1])
        self.trips.append(trip)
        return stop_index

    def create_inference_trips(self, update_rows):
        """Creates the trips to infer on"""
        stop_index = self.skip_invalid_stop(update_rows)
        if stop_index is None:
            return

        stop_index = self.add_update_stops(update_rows, stop_index)

        self.add_remaining_stops(stop_index)

    def create_training_trips(self, update_rows):
        """Computes the arrival times for all stops based on the updates"""
        # trip_counter = 1  # no need for it, just add it to self.trips and check len
        # trip = Trip(self.record, trip_counter)

        stop_index = self.skip_invalid_stop(update_rows)
        if stop_index is None:
            return

        stop_index = self.add_update_stops(update_rows, stop_index)

        # self.add_remaining_stops(stop_index)

        # last_stop = None
        # # Add all the stops which are between updates
        # for current_update, next_update in zip(
        #         update_rows[:-1], update_rows[1:]):

        #     stop_info, stop_time = self.get_stop_info_by_index(
        #             stop_index, current_update, next_update)
        #     # stop_info = self.stop_distances[stop_index]
        #     # stop_time = calc_interpolation(
        #     #         current_update[1], current_update[0],
        #     #         next_update[1], next_update[0],
        #     #         stop_info[1])

        #     while stop_time is not None:
        #         # Split the trips
        #         if last_stop is not None and self.is_idle_stop(last_stop):
        #             self.trips.append(trip)
        #             trip_counter += 1
        #             trip = Trip(self.record, trip_counter)
        #             last_stop = None
        #         # Initiate the config data for a trip
        #         if not trip.configured:
        #             trip.config(map_strtime_to_timestamp(
        #                     self.record["start_date"], stop_info[2]),
        #                     stop_info[1],
        #                     stop_time)
        #         # Add the stop row to the trip
        #         last_stop = trip.add_stop(stop_info, stop_time, last_stop)
        #         stop_index += 1
        #         # Exit if we reach the end of stops in the while loop
        #         if stop_index >= len(self.stop_distances):
        #             self.trips.append(trip)
        #             return self.trips
        #         # Get the next stop_time data
        #         stop_info, stop_time = self.get_stop_info_by_index(
        #             stop_index, current_update, next_update)
        #         # stop_info = self.stop_distances[stop_index]
        #         # stop_time = calc_interpolation(
        #         #         current_update[1], current_update[0],
        #         #         next_update[1], next_update[0],
        #         #         stop_info[1])

        # self.trips.append(trip)
        # return self.trips

        # add the remaining stops

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
        self.check_trip_filters_after()
        return self.trips


if __name__ == "__main__":
    from .json_io import load_json
    data = load_json("test_record")
