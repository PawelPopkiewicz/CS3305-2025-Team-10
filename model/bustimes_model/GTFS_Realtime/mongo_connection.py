"""
Functions to manage connections to mongodb
"""

import os
from pymongo import MongoClient


def get_connection():
    """Return connection to mongodb"""
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:admin@localhost:27017/")
    DB_NAME = "bus_data"

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db
