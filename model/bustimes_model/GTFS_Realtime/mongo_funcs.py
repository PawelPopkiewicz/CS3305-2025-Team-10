"""
Functions to manage the mongo db
"""

import pymongo
from bson import json_util
import json
from GTFS_Static.db_funcs import get_route_id_to_name_dict
from .mongo_connection import get_connection
from .get_root import get_root

class MongoManager():

    def __init__(self):
        self.conn = get_connection()
        self.collection = self.conn["bus_data"]
        self.route_id_to_name = get_route_id_to_name_dict()

    def print_mongo(self):
        print(self.get_mongo())

    def get_mongo_test(self):
        return {"routes": "Test"}

    def get_mongo(self):
        result = self.collection.find_one()
        return self.bson_to_json(result)

    def bson_to_json(self, bson):
        return json_util.dumps(bson)

    def add_trip_update(self, trip, report):
        trip_filter = self.extract_trip_filter(trip)
        vehicle_update = self.extract_vehicle_update(trip)
        result = self.collection.find_one(trip_filter)
        if result:
            result = self.collection.find_one({**trip_filter, "vehicle_updates": {"$elemMatch": vehicle_update}})
            if result:
                return
            update_operation = self.create_update_operation(vehicle_update)
            self.collection.update_one(trip_filter, update_operation)
            report["updated_trips"] = report["updated_trips"] + 1
            return
        self.collection.insert_one(self.extract_trip(trip, vehicle_update))
        report["added_trips"] = report["added_trips"] + 1

    def extract_vehicle_update(self, trip):
        trip_info = trip["vehicle"]
        return {"timestamp": trip_info["timestamp"],
                "latitude": trip_info["position"]["latitude"],
                "longitude": trip_info["position"]["longitude"]}

    def extract_trip_filter(self, trip):
        trip_info = trip["vehicle"]
        return {"trip_id": trip_info["trip"]["trip_id"],
                "start_date": trip_info["trip"]["start_date"]}

    def create_update_operation(self, vehicle_update):
        return {"$push": {"vehicle_updates": vehicle_update}}

    def extract_trip(self, trip, vehicle_update):
        trip_info = trip["vehicle"]
        return {"trip_id": trip_info["trip"]["trip_id"],
                "start_time": trip_info["trip"]["start_time"],
                "start_date": trip_info["trip"]["start_date"],
                "schedule_relationship": trip_info["trip"]["schedule_relationship"],
                "route_id": trip_info["trip"]["route_id"],
                "direction_id": trip_info["trip"]["direction_id"],
                "vehicle_updates": [vehicle_update]}

    def delete_documents(self):
        self.collection.delete_many({})


if __name__ == "__main__":
    mm = MongoManager()
    mm.print_mongo()
