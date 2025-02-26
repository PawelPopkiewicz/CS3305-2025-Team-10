"""
Provides the connection to GTFS_Static data in the bus_model container
"""

import os
import requests


def get_route_id_to_name():
    """Gets the route_id to name mapping from bus_model"""
    bus_model_uri = os.getenv("BUS_MODEL_URI")
    response = requests.get(bus_model_uri + "/route_id_to_name", timeout=10)
    return dict(response.json())


if __name__ == "__main__":
    print(get_route_id_to_name())
