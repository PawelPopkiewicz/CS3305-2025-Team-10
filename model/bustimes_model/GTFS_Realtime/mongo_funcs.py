"""
Functions to manage the mongo db
"""

import pymongo
from GTFS_Static.db_funcs import get_route_id_to_name_dict
from .mongo_connection import get_connection
from .get_root import get_root

class MongoManager():

    def __init__(self):
        self.conn = get_connection()
        self.collection = self.conn["routes"]
        self.route_id_to_name = get_route_id_to_name_dict()

    def make_skeleton(self):
        skeleton = {
                "routes": {route: [] for route in self.route_id_to_name.values()}
                }
        self.collection.insert_one(skeleton)

    def print_mongo(self):
        print(self.collection.find_one())


if __name__ == "__main__":
    mm = MongoManager()
    mm.make_skeleton()
    mm.print_mongo()
