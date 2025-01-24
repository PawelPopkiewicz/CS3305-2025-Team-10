class Bus:
    """A class to represent a bus and its relevant information."""
    all_buses = []

    def __init__(self):
        self.all_buses.append(self)


class Stop:
    """A class to represent a bus stop and its relevant information."""
    all_stops = []

    def __init__(self):
        self.all_stops.append(self)


class Route:
    """A class to represent a bus route and its relevant information."""
    all_routes = []

    def __init__(self):
        self.all_routes.append(self)
