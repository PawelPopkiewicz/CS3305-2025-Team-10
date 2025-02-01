"""
Fetch the api data, process it and store it in the mongodb
"""

import json
import os
from .gtfsr import GTFSR
from .json_processor import JsonProcessor
from .mongo_funcs import MongoManager

class VehicleUpdates():

    def __init__(self):
        self.mongo_manager = MongoManager()
        self.gtfsr = GTFSR()
        self.json_processor = JsonProcessor()

    def fetch_trips(self):
        vehicle_trips = self.gtfsr.fetch_vehicles()
        self.json_processor.filter_vehicles(vehicle_trips)
        return vehicle_trips

    def store_trips(self, trips):
        report = {"updated_trips": 0,
                  "added_trips": 0}
        for trip in trips["entity"]:
            self.mongo_manager.add_trip_update(trip, report)
        return report

    def update_trips(self):
        return self.store_trips(self.fetch_trips())


if __name__ == "__main__":
    vu = VehicleUpdates()
    vu.update_trips()
    mm = MongoManager()
    mm.print_mongo()
