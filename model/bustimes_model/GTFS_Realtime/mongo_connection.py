"""
Functions to manage connections to mongodb
"""

import os
from pymongo import MongoClient, errors


def get_connection():
    """Return connection to mongodb"""
    try:
        MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:admin@localhost:27017/bus_data")
        DB_NAME = "bus_data"

        client = MongoClient(MONGO_URI, authSource="admin")
        db = client[DB_NAME]
        client.server_info()
    except errors.ServerSelectionTimeoutError as e:
        print(f"The connection to mongodb failed: {e}")
    except errors.OperationFailure as e:
        print(f"Operational Failure: {e}")
    return db

if __name__ == "__main__":
    db = get_connection()
