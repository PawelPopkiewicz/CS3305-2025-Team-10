class Bus:
    """A class to represent a bus and its relevant information."""
    all_buses = {}

    def __init__(self, bus_id):
        self.all_buses[bus_id] = self


class Stop:
    """A class to represent a bus stop and its relevant information."""
    all_stops = {}

    def __init__(self, stop_id):
        self.all_stops[stop_id] = self


class Route:
    """A class to represent a bus route and its relevant information."""
    all_routes = {}

    def __init__(self, route_id: int, agency_id: int, route_short_name: str, route_long_name: str, route_type: int):
        self.all_routes[route_id] = self
        self.route_id = route_id
        self.agency_id = agency_id
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        self.route_type = route_type

class Agency:
    """A class to represent a bus agency and its relevant information."""
    all_agencies = {}

    def __init__(self, agency_id: int, agency_name: str):
        self.all_agencies[agency_id] = self
        self.agency_id = agency_id
        self.agency_name = agency_name