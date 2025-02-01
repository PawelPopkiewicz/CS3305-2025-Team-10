"""
Fetch the api data, process it and store it in the mongodb
"""

from .gtfsr import GTFSR
from .json_processor import JsonProcessor
from .mongo_funcs import MongoManager


class VehicleUpdates():
    """Provides functionality to manage fetching and storing data from GTFSR api"""

    def __init__(self):
        self.mongo_manager = MongoManager()
        self.gtfsr = GTFSR()
        self.json_processor = JsonProcessor()

    def fetch_trips(self):
        """Fetch, filter and return the vehicle json from GTFSR api"""
        vehicle_trips = self.gtfsr.fetch_vehicles()
        self.json_processor.filter_vehicles(vehicle_trips)
        return vehicle_trips

    def store_trips(self, trips):
        """Store the provided trips inside the mongodb"""
        report = {"updated_trips": 0,
                  "added_trips": 0}
        for trip in trips["entity"]:
            self.mongo_manager.add_trip_update(trip, report)
        return report

    def update_trips(self):
        """Fetch, filter, store the trips"""
        report = self.store_trips(self.fetch_trips())
        self.close_connections()
        return report

    def close_connections(self):
        """Closes all connections"""
        self.mongo_manager.close_connection()


if __name__ == "__main__":
    vu = VehicleUpdates()
    vu.update_trips()
