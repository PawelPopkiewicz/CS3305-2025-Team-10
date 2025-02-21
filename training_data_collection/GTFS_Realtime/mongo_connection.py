"""
Functions to manage connections to mongodb
"""

import os
from pymongo import MongoClient, errors

COLLECTION_NAME = "bus_data"
DATABASE_NAME = "bus_data"


def get_connection():
    """Return client to mongodb"""
    try:
        mongo_uri = os.getenv("MONGO_URI")
        client = MongoClient(mongo_uri, authSource="admin")
        return client
    except errors.ServerSelectionTimeoutError as e:
        print(f"The connection to mongodb failed: {e}")
    except errors.OperationFailure as e:
        print(f"Operational Failure: {e}")
    return None


def close_connection(client):
    """close the client connection"""
    client.close()


if __name__ == "__main__":
    db_test = get_connection()
