from datetime import datetime

class Bus:
    """A class to represent a bus and its relevant information."""
    all_buses = {}

    def __init__(self, bus_id):
        self.all_buses[bus_id] = self


class Stop:
    """A class to represent a bus stop and its relevant information."""
    all_stops = {}

    def __init__(self, stop_id: str, stop_code: int, stop_name: str, stop_lat: float, stop_lon: float):
        self.all_stops[stop_id] = self
        self.stop_id = stop_id
        self.stop_code = stop_code
        self.stop_name = stop_name
        self.stop_lat = stop_lat
        self.stop_lon = stop_lon
        self.bus_visits = [] # List of BusStopVisit objects at this stop


class Route:
    """A class to represent a bus route and its relevant information."""
    all_routes = {}

    def __init__(self, route_id: int, agency_id: int, route_short_name: str, route_long_name: str, route_type: int):
        self.all_routes[route_id] = self
        self.route_id = route_id
        self.agency = Agency.all_agencies[agency_id]
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        self.route_type = route_type
        self.all_trips = []

class Trip:
    """A class to represent a trip and its relevant information."""
    all_trips = {}

    def __init__(self, trip_id: int, route_id: int, service_id: int, shape_id: int, trip_headsign: str, trip_short_name: str, direction_id: int, block_id: str):
        self.all_trips[trip_id] = self
        self.trip_id = trip_id
        self.route = Route.all_routes[route_id]
        self.service = Service.all_services[service_id]
        self.shape = Shape.all_shapes[shape_id]
        self.trip_headsign = trip_headsign
        self.trip_short_name = trip_short_name
        self.direction_id = direction_id
        self.block_id = block_id
        self.bus_stop_times = []
        self.stop_id_stop_seq = {}

        self.route.all_trips.append(self)
    
class BusStopVisit:
    """A class to record the time of a stop in a trip."""

    def __init__(self, trip_id: int, stop_id: int, arrival_time: datetime, departure_time: datetime, stop_sequence: int, stop_headsign: str, pickup_type: int, drop_off_type: int, timepoint_type: int):
        self.trip = Trip.all_trips[trip_id]
        self.stop = Stop.all_stops[stop_id]
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.stop_sequence = stop_sequence
        self.stop_headsign = stop_headsign
        self.pickup_type = pickup_type
        self.drop_off_type = drop_off_type
        self.timepoint_type = timepoint_type

        self.stop.bus_visits.append(self)
        self.trip.bus_stop_times.append(self)
        self.trip.stop_id_stop_seq[stop_sequence] = stop_id


class Service:
    """Represents a weekly schedule through a set of booleans"""
    all_services = {}
    ADDED_EXCEPTION = 1
    REMOVED_EXCEPTION = 2

    def __init__(self, service_id: int, monday: bool, tuesday: bool, wednesday: bool, thursday: bool, friday: bool, saturday: bool, sunday: bool, start_date: datetime, end_date: datetime):
        self.all_services[service_id] = self
        self.service_id = service_id
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday
        self.start_date = start_date
        self.end_date = end_date
        self.exceptions = []
    
    def add_exception(self, date: datetime, exception_type: int):
        """Records an exception to the schedule, to be parsed on schedule generation in a different method."""
        self.exceptions.append((date, exception_type))

class Agency:
    """A class to represent a bus agency and its relevant information."""
    all_agencies = {}

    def __init__(self, agency_id: int, agency_name: str):
        self.all_agencies[agency_id] = self
        self.agency_id = agency_id
        self.agency_name = agency_name

class Shape:
    """A class representing a trip's journey via sequence of coordinates."""
    all_shapes = {}

    def __init__(self, shape_id: int):
        self.all_shapes[shape_id] = self
        self.shape_id = shape_id
        self.shape_coords: list[Point] = []
    
    def add_point(self, lat: float, lon: float):
        self.shape_coords.append(Point(lat, lon))

class Point:
    """A class representing a latitude and longitude coordinate."""

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon