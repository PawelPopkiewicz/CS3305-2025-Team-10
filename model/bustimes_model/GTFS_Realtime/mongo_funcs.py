"""
Functions to manage the mongo db
"""

import json
from bson import json_util
from .mongo_connection import close_connection, get_connection, COLLECTION_NAME, DATABASE_NAME


class MongoManager():
    """Manages the mongodb"""

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        """Sets up a connection to mongo"""
        self.client = get_connection()
        self.conn = self.client[DATABASE_NAME]
        self.collection = self.conn[COLLECTION_NAME]

    def print_trips(self):
        """Prints the first document in the collection"""
        print(json.dumps(self.get_mongo(), indent=4))

    def get_trips_test(self):
        """Returns a test dict"""
        return {"trips": "Test"}

    def get_trips(self):
        """Return documents in collection"""
        result = self.collection.find({})
        return self.bson_to_json(result)

    def bson_to_json(self, bson):
        """Converts bson to json string"""
        return json_util.dumps(bson)

    def add_trip_update(self, trip, report):
        """Add the trip if one does not exist yet, otherwise updates the vehicle_updates"""
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
        """Extracts the vehicle_update object from trip"""
        trip_info = trip["vehicle"]
        return {"timestamp": trip_info["timestamp"],
                "latitude": trip_info["position"]["latitude"],
                "longitude": trip_info["position"]["longitude"]}

    def extract_trip_filter(self, trip):
        """Extracts filter to find the trip"""
        trip_info = trip["vehicle"]
        return {"trip_id": trip_info["trip"]["trip_id"],
                "start_date": trip_info["trip"]["start_date"]}

    def create_update_operation(self, vehicle_update):
        """Creates operation to update the vehicle_updates array"""
        return {"$push": {"vehicle_updates": vehicle_update}}

    def extract_trip(self, trip, vehicle_update):
        """Extract the trip object from the original formatting"""
        trip_info = trip["vehicle"]
        return {"trip_id": trip_info["trip"]["trip_id"],
                "start_time": trip_info["trip"]["start_time"],
                "start_date": trip_info["trip"]["start_date"],
                "schedule_relationship": trip_info["trip"]["schedule_relationship"],
                "route_id": trip_info["trip"]["route_id"],
                "direction_id": trip_info["trip"]["direction_id"],
                "vehicle_updates": [vehicle_update]}

    def delete_trips(self):
        """Deletes all documents in the collection"""
        self.collection.delete_many({})

    def close_connection(self):
        """Closes the connection to the mongo database"""
        close_connection(self.client)


if __name__ == "__main__":
    mm = MongoManager()
    mm.print_mongo()
