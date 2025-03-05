"""
Pre-process the json data
Returns a csv-format data ready to be fed into the model
"""

from preprocessing.trip_to_stop_times import TripGenerator


def process_json(json_data):
    """Convert json to csv"""
    tg = TripGenerator(json_data)
    trips = tg.map_record_to_inference_stop_times()
    if trips is not None and len(trips) > 0:
        # Return the latest trip after the potential split
        return trips[-1]
    return None
