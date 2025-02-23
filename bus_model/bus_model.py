from datetime import datetime, timedelta

class Bus:
    """A class to represent a bus and its relevant information."""
    _all: dict[str, 'Bus'] = {}

    STYLE_NULL = 0
    STYLE_COACH = 1
    STYLE_DOUBLE_DECKER = 2
    STYLE_MINIBUS = 3    
    STYLE_TRAM = 4
    STYLE_ARTICULATED = 5

    FUEL_NULL = 0
    FUEL_DIESEL = 1
    FUEL_ELECTRIC = 2
    FUEL_HYBRID = 3
    FUEL_GAS = 4
    FUEL_HYDROGEN = 5


    def __init__(self, bus_id: str):
        self._all[bus_id] = self
        self.bus_id = bus_id
    
    def set_details(self, reg: str, fleet_code: str, slug: str, name: str, style: int, fuel: int, double_decker: bool, coach: bool, electric: bool, livery: int, withdrawn: bool, special_features: str):
        """Sets the details of the bus."""
        self.reg = reg
        self.fleet_code = fleet_code
        self.slug = slug
        self.name = name
        self.style = style
        self.fuel = fuel
        self.double_decker = double_decker
        self.coach = coach
        self.electric = electric
        self.livery = livery
        self.withdrawn = withdrawn
        self.special_features = special_features
    
    def get_info(self) -> dict[str, str]:
        """Returns the bus's information in a dictionary."""
        return {
            "bus_id": self.bus_id,
            "reg": self.reg,
            "fleet_code": self.fleet_code,
            "slug": self.slug,
            "vehicle_details": {
                "name": self.name,
                "style": self.style,
                "fuel": self.fuel,
                "double_decker": self.double_decker,
                "coach": self.coach,
                "electric": self.electric
                },
            "livery": self.livery,
            "withdrawn": self.withdrawn,
            "special_features": self.special_features
        }


class Stop:
    """A class to represent a bus stop and its relevant information."""
    _all: dict[str, "Stop"] = {}

    def __init__(self, stop_id: str, stop_code: str, stop_name: str, stop_lat: float, stop_lon: float):
        self._all[stop_id] = self
        self.stop_id = stop_id
        self.stop_code = stop_code
        self.stop_name = stop_name
        self.stop_lat = stop_lat
        self.stop_lon = stop_lon
        self.bus_visits: list[BusStopVisit] = [] # List of BusStopVisit objects at this stop
        self.routes: set[Route] = set()
        self.trips: set[Trip] = set()
    
    def get_info(self) -> dict[str, str]:
        """Returns the stop's information in a dictionary."""
        return {
            "stop_id": self.stop_id,
            "stop_code": self.stop_code,
            "stop_name": self.stop_name,
            "stop_lat": self.stop_lat,
            "stop_lon": self.stop_lon
        }

class Route:
    """A class to represent a bus route and its relevant information."""
    _all: dict[str, 'Route'] = {}

    def __init__(self, route_id: str, agency_id: str, route_short_name: str, route_long_name: str, route_type: int):
        self._all[route_id] = self
        self.route_id = route_id
        self.agency = Agency._all[agency_id]
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        self.route_type = route_type
        self.all_trips: list[Trip] = []
        self.all_stops: set[Stop] = set()

    def get_info(self) -> dict[str, str]:
        """Returns the route's information in a dictionary."""
        return {
            "route_id": self.route_id,
            "agency_id": self.agency.agency_id,
            "route_short_name": self.route_short_name,
            "route_long_name": self.route_long_name,
            "route_type": self.route_type
        }
    
    def add_stop(self, stop: Stop):
        """Adds a stop to the route's list of stops."""
        self.all_stops.add(stop)
    
    def enumerate_stops(self):
        for trip in self.all_trips:
            for bus_stop_visit in trip.bus_stop_times:
                self.add_stop(bus_stop_visit.stop.stop_id)
        for stop in self.all_stops:
            stop.routes.add(self)
    
class Trip:
    """A class to represent a trip and its relevant information."""
    _all: dict[str, "Trip"] = {}

    def __init__(self, trip_id: str, route_id: str, service_id: str, shape_id: str, trip_headsign: str, trip_short_name: str, direction_id: bool, block_id: str):
        self._all[trip_id] = self
        self.trip_id = trip_id
        self.route = Route._all[route_id]
        self.service = Service._all[service_id]
        self.shape = Shape._all.get(shape_id, None)
        self.trip_headsign = trip_headsign
        self.trip_short_name = trip_short_name
        self.direction_id = direction_id
        self.block_id = block_id
        self.bus_stop_times: list[BusStopVisit] = []
        self.stop_id_stop_seq: dict[str, int] = {}

        self.route.all_trips.append(self)
    
    def get_info(self) -> dict[str, str]:
        """Returns the trip's information in a dictionary."""
        return {
            "trip_id": self.trip_id,
            "route_id": self.route.route_id,
            "service_id": self.service.service_id,
            "shape_id": self.shape.shape_id,
            "trip_headsign": self.trip_headsign,
            "trip_short_name": self.trip_short_name,
            "direction_id": self.direction_id,
            "block_id": self.block_id
        }
    
    def get_times(self) -> list[datetime]:
        """Returns a list of all timestamps for the trip.""" # this sort of should be returning something else, maybe combine into stop -> routes -> trips -> times
        timestamps: list[datetime] = []
        current_date = self.service.start_date
        while current_date <= self.service.end_date:
            day = current_date.weekday()
            if self.service.schedule_days[day]:
                if current_date not in self.service.cancelled_exceptions:
                    for visit in self.bus_stop_times:
                        new_timestamp = current_date.combine(current_date, visit.arrival_time)
                        timestamps.append(new_timestamp)
        for exception in self.service.extra_exceptions:
            if exception not in self.service.cancelled_exceptions:
                for visit in self.bus_stop_times:
                    new_timestamp = exception.combine(exception, visit.arrival_time)
                    timestamps.append(new_timestamp)
        return timestamps


    
    @classmethod
    def filter_by_routes(cls, route_ids: list|str) -> list[dict[str, str]]:
        """Filters the list of all trips by specified route IDs."""
        if isinstance(route_ids, str):
            route_ids = [route_ids]
        return [trip.get_info() for trip in cls._all.values() if trip.route.route_id in route_ids]
    
class BusStopVisit:
    """A class to record the time of a stop in a trip."""

    def __init__(self, trip_id: str, stop_id: str, arrival_time: timedelta, departure_time: timedelta, stop_sequence: int, stop_headsign: str, pickup_type: bool, drop_off_type: bool, timepoint_type: bool):
        self.trip = Trip._all[trip_id]
        self.stop = Stop._all[stop_id]
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.stop_sequence = stop_sequence
        self.stop_headsign = stop_headsign
        self.pickup_type = pickup_type
        self.drop_off_type = drop_off_type
        self.timepoint_type = timepoint_type

        self.stop.bus_visits.append(self)
        self.trip.bus_stop_times.append(self)
        self.stop.trips.add(self.trip)
        self.trip.stop_id_stop_seq[stop_sequence] = stop_id


class Service:
    """Represents a weekly schedule through a set of booleans"""
    _all: dict[str, 'Service'] = {}
    ADDED_EXCEPTION = 1
    REMOVED_EXCEPTION = 2

    def __init__(self, service_id: str, monday: bool, tuesday: bool, wednesday: bool, thursday: bool, friday: bool, saturday: bool, sunday: bool, start_date: datetime, end_date: datetime):
        self._all[service_id] = self
        self.service_id = service_id
        self.schedule_days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
        self.start_date = start_date
        self.end_date = end_date
        self.extra_exceptions: list[datetime] = []
        self.cancelled_exceptions: list[datetime] = []
    
    def add_exception(self, date: datetime, exception_type: int):
        """Records an exception to the schedule, to be parsed on schedule generation in a different method."""
        if exception_type == self.ADDED_EXCEPTION:
            self.extra_exceptions.append(date)
        elif exception_type == self.REMOVED_EXCEPTION:
            self.cancelled_exceptions.append(date)
        else:
            raise ValueError("Invalid exception type.")

class Agency:
    """A class to represent a bus agency and its relevant information."""
    _all: dict[str, 'Agency'] = {}

    def __init__(self, agency_id: str, agency_name: str):
        self._all[agency_id] = self
        self.agency_id = agency_id
        self.agency_name = agency_name

    def get_info(self) -> dict[str, str]:
        """Returns the agency's ID and name."""
        return {
            "agency_id": self.agency_id,
            "agency_name": self.agency_name
        }

class Shape:
    """A class representing a trip's journey via sequence of coordinates."""
    _all: dict[str, 'Shape'] = {}

    def __init__(self, shape_id: str):
        self._all[shape_id] = self
        self.shape_id = shape_id
        self.shape_coords: list[Point] = []
    
    def add_point(self, lat: float, lon: float, sequence: int, dist_traveled: float):
        """Adds a point to the shape."""
        self.shape_coords.append(Point(lat, lon, sequence, dist_traveled))

    def get_info(self) -> list[dict[str, float]]:
        """Returns a list of the coordinates of the shape."""
        return [point.get_info() for point in self.shape_coords]

class Point:
    """A class representing a latitude and longitude coordinate."""

    def __init__(self, lat: float, lon: float, sequence: int, dist_traveled: float):
        self.lat = lat
        self.lon = lon
        self.sequence = sequence
        self.dist_traveled = dist_traveled

    def get_info(self) -> dict[str, float]:
        """Returns the latitude and longitude of the point."""
        return {
            "lat": self.lat,
            "lon": self.lon,
            "sequence": self.sequence,
            "dist_traveled": self.dist_traveled
        }


def search_attribute(cls, attribute: str, value: str) -> list:
    """Fetches all instances of a class with a certain attribute value."""
    return [instance for instance in cls._all.values() if getattr(instance, attribute) == value]