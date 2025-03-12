"""
Pre-process the json data
Returns a csv-format data ready to be fed into the model
"""

import pandas as pd

from preprocessing.trip_to_stop_times import TripGenerator


def process_json(json_data):
    """Convert json to df"""
    tg = TripGenerator(json_data)
    trips = tg.map_record_to_inference_stop_times()
    if trips is not None and len(trips) > 0:
        # Return the latest trip after the potential split
        return trips[-1]
    # return pd.DataFrame(trips[-1])
    return None


if __name__ == "__main__":
    from preprocessing.json_io import load_json
    test_data = load_json("test_record")
    test_data["vehicle_updates"] = test_data["vehicle_updates"][:-5]
    last_trip = process_json(test_data)
    print(last_trip.display_df())
