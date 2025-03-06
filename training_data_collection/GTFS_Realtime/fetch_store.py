"""
Fetch the api data, process it and store it in the mongodb
"""

from GTFS_Realtime import json_processor

from .gtfsr import GTFSR
from .json_processor import JsonProcessor
from .mongo_funcs import MongoManager


class VehicleUpdates:
    """Provides functionality to manage fetching and storing data from GTFSR api"""

    def __init__(self):
        self.mongo_manager = MongoManager()
        self.gtfsr = GTFSR()
        self.json_processor = JsonProcessor()

    def _fetch_trips(self):
        """Fetch and return the vehicle json from GTFSR api"""
        vehicle_trips = self.gtfsr.fetch_vehicles()
        return vehicle_trips

    def _filter_trips(self, vehicle_trips):
        """Filters the provided vehicles"""
        self.json_processor.filter_vehicles(vehicle_trips)

    def _store_trips(self, trips):
        """Store the provided trips inside the mongodb"""
        report = self.mongo_manager.add_trips(trips)
        return report

    def fetch_update_trips(self):
        """Fetch, filter, store the trips"""
        trips = self._fetch_trips()
        self._filter_trips(trips)
        report = self._store_trips(trips)
        return report

    def update_trips(self, vehicle_trips):
        """receives raw vehicles json, filters it and updates it"""
        self._filter_trips(vehicle_trips)
        report = self._store_trips(vehicle_trips)
        return report

    def get_trips(self):
        """Returns the content of the mongodb"""
        mongo_contents = self.mongo_manager.get_trips()
        return mongo_contents

    def get_trips_str(self):
        """Returns the contents of the mongodb as a string"""
        return self.mongo_manager.get_trips_string()

    def generate_report(self):
        """Generates a report on how the collection is going"""
        report = self.mongo_manager.generate_report()
        return report

    def delete_trips(self):
        """
        Deletes the contents
        As of now it returns an error, only way to delete is from server
        """
        return {"Error": "Can delete only from the server"}

    def update_route_id_to_name(self, route_id_to_name):
        """Updates the route_id_to_name dict"""
        self.json_processor.update_route_id_to_name(route_id_to_name)


if __name__ == "__main__":
    vu = VehicleUpdates()
    print(vu.fetch_update_trips())
