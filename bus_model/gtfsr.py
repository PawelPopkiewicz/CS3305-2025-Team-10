import requests
import os
import bus_model
import datetime
import time

from dotenv import load_dotenv
from GTFS_Static.db_connection import create_connection, close_connection


load_dotenv()

def manage_read_only_connection(func):
    def wrapper(*args, **kwargs):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            func(cursor, *args, **kwargs)
        finally:
            close_connection(conn)
    return wrapper

class GTFSR:
    """A class to make requests to the GTFSR API. All methods can be used without initialising the class."""
    base_url = "https://api.nationaltransport.ie/gtfsr/v2/"
    format_json = "?format=json"
    api_key = os.getenv("api_key", None)

    @classmethod
    def fetch_vehicles(self) -> dict:
        """
        Fetches the vehicles endpoint from the GTFSR API.

        Returns:
            dict: The response from the GTFSR API
        """
        return self.fetch_endpoint("Vehicles")

    @classmethod
    def fetch_trip_updates(self) -> dict:
        """
        Fetches the trip_updates endpoint from the GTFSR API.

        Returns:
            dict: The response from the GTFSR API
        """
        return self.fetch_endpoint("TripUpdates")

    @classmethod
    def fetch_gtfsr(self) -> dict:
        """
        Fetches the gtfsr endpoint from the GTFSR API.

        Returns:
            dict: The response from the GTFSR API
        """
        return self.fetch_endpoint("gtfsr")

    @classmethod
    def fetch_endpoint(self, endpoint: str) -> dict:
        """
        Makes a request to the GTFSR API at the specified endpoint.

        Returns:
            dict: A JSON formatted response from the GTFSR API
        """
        url = self.base_url + endpoint + self.format_json
        headers = {
            'Cache-Control': 'no-cache',
            'x-api-key': self.api_key
        }

        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            print(e)
            return None
        return response.json()


class StaticGTFSR:
    """A class to parse GTFSR data from the PostgreSQL db."""
    date_format = "%Y%m%d"
    time_format = "%H:%M:%S"


    @classmethod
    @manage_read_only_connection
    def get_routes(cursor, _):
        query = """SELECT * FROM ROUTES"""
        cursor.execute(query)
        res = cursor.fetchall()
        for row in res:
            bus_model.Route(route_id=row[0], agency_id=row[1], route_short_name=row[2], route_long_name=row[3], route_type=row[4])

    @classmethod
    @manage_read_only_connection
    def get_stops(cursor, _):
        query = """SELECT * FROM STOPS"""
        cursor.execute(query)
        res = cursor.fetchall()
        for row in res:
            bus_model.Stop(stop_id=row[0], stop_code=str(int(row[1])), stop_name=row[2], stop_lat=row[3], stop_lon=row[4])

    @classmethod
    @manage_read_only_connection
    def get_agencies(cursor, _):
        query = """SELECT * FROM AGENCY"""
        cursor.execute(query)
        res = cursor.fetchall()
        for row in res:
            bus_model.Agency(agency_id=row[0], agency_name=row[1])

    @classmethod
    @manage_read_only_connection
    def get_calendar(cursor, cls):
        query = """SELECT * FROM CALENDAR"""
        cursor.execute(query)
        res = cursor.fetchall()
        for row in res:
            start_date = datetime.datetime.strptime(row[4], cls.date_format)
            end_date = datetime.datetime.strptime(row[5], cls.date_format)
            bus_model.Service(service_id=row[0], monday=row[1], tuesday=row[2], wednesday=row[3], thursday=row[4], friday=row[5], saturday=row[6], sunday=row[7], start_date=start_date, end_date=end_date)

    @classmethod
    @manage_read_only_connection
    def get_calendar_dates(cursor, cls):
        query = """SELECT * FROM CALENDAR_DATES"""
        cursor.execute(query)
        res = cursor.fetchall()
        for row in res:
            date = datetime.datetime.strptime(row[1], cls.date_format)
            service = bus_model.Service._all[row[0]]
            service.add_exception(date, int(row[2]))

    @classmethod
    @manage_read_only_connection
    def get_shapes(cursor, _):
        query = """SELECT * FROM SHAPES"""
        cursor.execute(query)
        res = cursor.fetchall()
        for row in res:
            shape_id = row[0]
            if shape_id not in bus_model.Shape._all:
                shape = bus_model.Shape(shape_id)
            else:
                shape = bus_model.Shape._all[shape_id]
            shape.add_point(lat=row[1], lon=row[2], sequence=row[3], dist_traveled=row[4])

    @classmethod
    @manage_read_only_connection
    def get_trips(cursor, _):
        query = """SELECT * FROM TRIPS"""
        cursor.execute(query)
        res = cursor.fetchall()
        for row in res:
            bus_model.Trip(route_id=row[0], service_id=row[1], trip_id=row[2], trip_headsign=row[3], trip_short_name=row[4], direction_id=row[5], block_id=row[6], shape_id=row[7])

    @classmethod
    @manage_read_only_connection
    def get_stop_times(cursor, _):
        query = """SELECT * FROM STOP_TIMES"""
        cursor.execute(query)
        res = cursor.fetchall()
        for row in res:
            h, m, s = map(int, row[1].split(":"))
            arrival_delta = datetime.timedelta(hours=h, minutes=m, seconds=s)
            h, m, s = map(int, row[2].split(":"))
            departure_delta = datetime.timedelta(hours=h, minutes=m, seconds=s)
            headsign = row[5] if row[5] != "nan" else None
            bus_model.BusStopVisit(trip_id=row[0], arrival_time=arrival_delta, departure_time=departure_delta, stop_id=row[3], stop_sequence=row[4], stop_headsign=headsign, pickup_type=row[6], drop_off_type=row[7], timepoint=row[8])
    
    @classmethod
    def load_all_files(self):
        t = time.time()
        self.read_agencies()
        print(f"Agencies loaded in {(t1:=time.time()) - t}s")
        self.read_calendar()
        print(f"Calendar loaded in {(t:=time.time()) - t1}s")
        self.read_stops()
        print(f"Stops loaded in {(t1:=time.time()) - t}s")
        self.read_shapes()
        print(f"Shapes loaded in {(t:=time.time()) - t1}s")
        self.read_routes()
        print(f"Routes loaded in {(t1:=time.time()) - t}s")
        self.read_calendar_dates()
        print(f"Calendar dates loaded in {(t:=time.time()) - t1}s")
        self.read_trips()
        print(f"Trips loaded in {(t1:=time.time()) - t}s")
        self.read_stop_times()
        print(f"Stop times loaded in {(t:=time.time()) - t1}s")


if __name__ == "__main__":
    # quick debugging
    import time
    start = time.time()
    StaticGTFSR.load_all_files()
    #print("num visits", len(bus_model.Trip._all))
    print(f"Time taken: {time.time() - start}s")
    input()
