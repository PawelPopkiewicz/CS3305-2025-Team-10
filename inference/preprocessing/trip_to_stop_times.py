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


# def calc_next_stop_time(current_time, current_distance, trips, stop_dist):
#     """
#     Calculates the time the next stop is reached
#     uses linear interpolation
#     """
#     if not trips:
#         return None
# 
#     next_update = trips[-1]
#     stop_time = calc_interpolation(
#             current_distance, current_time,
#             next_update["distance"], next_update["timestamp"],
#             stop_dist)
#     if stop_time is not None:
#         return stop_time
# 
#     for current_update, next_update in zip(
#             reversed(trips[1:]), reversed(trips[:-1])):
#         stop_time = calc_interpolation(
#                 current_update["distance"], current_update["timestamp"],
#                 next_update["distance"], next_update["timestamp"],
#                 stop_dist)
# 
#         if stop_time:
#             return stop_time
# 
#     return None


# def calc_time_to_next_stop(
#         trips, stop_dist, current_timestamp, current_distance):
#     """Calculates the time to reach the next bus stop"""
#     stop_time = calc_next_stop_time(
#             current_timestamp, current_distance,
#             trips, stop_dist)
#     if stop_time is not None:
#         return stop_time - current_timestamp
#     return None


# def get_next_stop_distance(distance, stop_distances):
#     """Returns the next distance based on the stop_distances provided"""
#     distances = [sd[1] for sd in stop_distances]
#     index = bisect.bisect_right(distances, distance)
#     if index < len(stop_distances):
#         return stop_distances[index][1]
#     return None


def create_stop_row_dict(stop_id, stop_dist, stop_time):
    """Creates one dict which will serve as a row in csv for all stop"""
    return {
            "stop_id": stop_id,
            "stop_distance": stop_dist,
            "stop_time": stop_time
            }


def create_stop_rows(stop_distances, update_rows):
    """Computes the arrival times for all stops based on the updates"""
    stop_rows = []
    stop_index = 0
    for current_update, next_update in zip(update_rows[:-1], update_rows[1:]):

        stop_info = stop_distances[stop_index]
        stop_time = calc_interpolation(
                current_update[1], current_update[0],
                next_update[1], next_update[0],
                stop_info[1])

        while stop_time is not None:
            stop_rows.append(create_stop_row_dict(
                stop_info[0], stop_info[1], stop_time))
            stop_index += 1

            stop_info = stop_distances[stop_index]
            stop_time = calc_interpolation(
                    current_update[1], current_update[0],
                    next_update[1], next_update[0],
                    stop_info[1])

    return stop_rows


def create_update_row_dict(update, trip_id, direction):
    """Creates the row per update"""
    timestamp = int(update["timestamp"])
    distance = map_coord_to_distance(
        trip_id, direction,
        float(update["latitude"]), float(update["longitude"])
    )
    return (timestamp, distance)


def create_update_rows(record, trip_id, direction):
    """Creates a list of timestamp and distance for updates"""
    # building it in reverse, oldest record is at index 0
    # Create a csv which has timestamps and distances at those timestamp
    update_rows = []
    updates = reversed(record["vehicle_updates"])
    for update in updates:
        update_row = create_update_row_dict(update, trip_id, direction)
        update_rows.append(update_row)
    return reversed(update_rows)


def map_record_to_stop_rows(record):
    """Maps a record of bus trip to the corresponding rows"""
    trip_id = record["trip_id"]
    direction = bool(record["direction_id"])
    if not check_trip_id_exists(trip_id, direction):
        return None

    stop_distances = get_stop_distances_for_trip(trip_id, direction)

    for stop in stop_distances:
        print(stop)

    update_rows = create_update_rows(record, trip_id, direction)
    # Create a csv per stop, using linear interpolation to determine the arrival times at bus stops
    # Go through all of the updates and start adding arrival times in the stops, keeping track of the index
    # Add all of the metadata to the rows, plus the unique identifier of the trip
    stop_rows = (stop_distances, update_rows)

    return stop_rows


if __name__ == "__main__":

    from .json_io import load_json
    data = load_json("test_record")
    stop_rows = map_record_to_stop_rows(data)

    test_record = {
"_id": {
  "$oid": "67a91801538170c283819c4e"
},
"trip_id": "4497_62500",
"start_time": "20:20:00",
"start_date": "20250209",
"schedule_relationship": "SCHEDULED",
"route_id": "4476_87348",
"direction_id": 1,
"vehicle_updates": [
  {
    "timestamp": "1739134948",
    "latitude": 51.8910141,
    "longitude": -8.46386909
  },
  {
    "timestamp": "1739135006",
    "latitude": 51.89328,
    "longitude": -8.46582413
  },
  {
    "timestamp": "1739135067",
    "latitude": 51.89328,
    "longitude": -8.46582413
  },
  {
    "timestamp": "1739135123",
    "latitude": 51.8933449,
    "longitude": -8.46582413
  },
  {
    "timestamp": "1739135210",
    "latitude": 51.8943825,
    "longitude": -8.46680164
  },
  {
    "timestamp": "1739135248",
    "latitude": 51.895546,
    "longitude": -8.47223282
  },
  {
    "timestamp": "1739135305",
    "latitude": 51.8966446,
    "longitude": -8.47462177
  },
  {
    "timestamp": "1739135395",
    "latitude": 51.8966446,
    "longitude": -8.47462177
  },
  {
    "timestamp": "1739135426",
    "latitude": 51.8966446,
    "longitude": -8.47462177
  },
  {
    "timestamp": "1739135514",
    "latitude": 51.8978767,
    "longitude": -8.47646809
  },
  {
    "timestamp": "1739135576",
    "latitude": 51.8976822,
    "longitude": -8.47788
  },
  {
    "timestamp": "1739135600",
    "latitude": 51.8976173,
    "longitude": -8.47874928
  },
  {
    "timestamp": "1739135660",
    "latitude": 51.8974876,
    "longitude": -8.47994423
  },
  {
    "timestamp": "1739135722",
    "latitude": 51.8974876,
    "longitude": -8.47994423
  },
  {
    "timestamp": "1739135813",
    "latitude": 51.8974876,
    "longitude": -8.47994423
  },
  {
    "timestamp": "1739135843",
    "latitude": 51.8974876,
    "longitude": -8.47994423
  },
  {
    "timestamp": "1739135907",
    "latitude": 51.8965187,
    "longitude": -8.48450565
  },
  {
    "timestamp": "1739135963",
    "latitude": 51.8956757,
    "longitude": -8.48841572
  },
  {
    "timestamp": "1739136055",
    "latitude": 51.8950272,
    "longitude": -8.49265099
  },
  {
    "timestamp": "1739136086",
    "latitude": 51.8947678,
    "longitude": -8.4941721
  },
  {
    "timestamp": "1739136143",
    "latitude": 51.8942528,
    "longitude": -8.49699593
  },
  {
    "timestamp": "1739136232",
    "latitude": 51.8923111,
    "longitude": -8.50579262
  },
  {
    "timestamp": "1739136290",
    "latitude": 51.8911438,
    "longitude": -8.50644493
  },
  {
    "timestamp": "1739136325",
    "latitude": 51.8889427,
    "longitude": -8.50753117
  },
  {
    "timestamp": "1739136382",
    "latitude": 51.8885574,
    "longitude": -8.51296234
  },
  {
    "timestamp": "1739136469",
    "latitude": 51.8888779,
    "longitude": -8.52425671
  },
  {
    "timestamp": "1739136504",
    "latitude": 51.8888168,
    "longitude": -8.52697277
  },
  {
    "timestamp": "1739136597",
    "latitude": 51.8890724,
    "longitude": -8.53348923
  },
  {
    "timestamp": "1739136620",
    "latitude": 51.8891373,
    "longitude": -8.5339241
  },
  {
    "timestamp": "1739136684",
    "latitude": 51.8906937,
    "longitude": -8.53968
  },
  {
    "timestamp": "1739136776",
    "latitude": 51.8921165,
    "longitude": -8.55119324
  },
  {
    "timestamp": "1739136806",
    "latitude": 51.8922462,
    "longitude": -8.55879593
  },
  {
    "timestamp": "1739136859",
    "latitude": 51.8921814,
    "longitude": -8.56205368
  },
  {
    "timestamp": "1739136949",
    "latitude": 51.8899155,
    "longitude": -8.57411
  },
  {
    "timestamp": "1739136984",
    "latitude": 51.8896561,
    "longitude": -8.5771513
  },
  {
    "timestamp": "1739137039",
    "latitude": 51.8887482,
    "longitude": -8.58290672
  },
  {
    "timestamp": "1739137099",
    "latitude": 51.8881035,
    "longitude": -8.58812141
  },
  {
    "timestamp": "1739137164",
    "latitude": 51.8880386,
    "longitude": -8.5927906
  },
  {
    "timestamp": "1739137227",
    "latitude": 51.8877792,
    "longitude": -8.59887314
  },
  {
    "timestamp": "1739137318",
    "latitude": 51.8859673,
    "longitude": -8.60984325
  },
  {
    "timestamp": "1739137345",
    "latitude": 51.8857727,
    "longitude": -8.61701107
  },
  {
    "timestamp": "1739137429",
    "latitude": 51.8816948,
    "longitude": -8.62689495
  },
  {
    "timestamp": "1739137459",
    "latitude": 51.8816948,
    "longitude": -8.62689495
  },
  {
    "timestamp": "1739137523",
    "latitude": 51.8803368,
    "longitude": -8.63634396
  },
  {
    "timestamp": "1739137586",
    "latitude": 51.8745117,
    "longitude": -8.63341141
  },
  {
    "timestamp": "1739137677",
    "latitude": 51.8759346,
    "longitude": -8.6463356
  }
]
}
    print(test_record)

