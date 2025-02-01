"""
Convert .txt files into sqlite for easier manipulation and queries
"""

import sqlite3


class TableCreator():
    """Creates sqlite table from the static info text files"""

    SHAPE_TABLE = """
    CREATE TABLE shapes (
    shape_id VARCHAR(10) NOT NULL,
    shape_pt_lat REAL,
    shape_pt_lon REAL,
    shape_pt_sequence INTEGER,
    shape_dist_traveled REAL
    );
    """

    ROUTES_TABLE = """
    CREATE TABLE routes (
    route_id VARCHAR(12) NOT NULL,
    agency_id VARCHAR(10),
    route_short_name VARCHAR(10),
    route_long_name VARCHAR(100)
    );
    """

    TRIPS_TABLE = """
    CREATE TABLE trips (
    route_id VARCHAR(12) NOT NULL,
    service_id VARCHAR(5),
    trip_id VARCHAR(10),
    direction_id VARCHAR(1),shape_id
    shape_id VARCHAR(10)
    );
    """

    STOPS_TABLE = """
    CREATE TABLE stops (
    stop_id VARCHAR(20) NOT NULL,
    stop_name VARCHAR(100),
    stop_lat REAL,
    stop_lon REAL
    );
    """

    STOP_TIMES_TABLE = """
    CREATE TABLE stop_times (
    trip_id VARCHAR(10) NOT NULL,
    arrival_time VARCHAR(8),
    departure_time VARCHAR(8),
    stop_id VARCHAR(20),
    stop_sequence INTEGER,
    pickup_type VARCHAR(1),
    drop_off_type VARCHAR(1),
    timepoint VARCHAR(1)
    );
    """

    AGENCY_TABLE = """
    CREATE TABLE agency (
    agency_id VARCHAR(20),
    agency_name VARCHAR(100)
    );
    """

    CALENDAR_TABLE = """
    CREATE TABLE calendar (
    service_id VARCHAR(5),
    monday VARCHAR(1),
    tuesday VARCHAR(1),
    wednesday VARCHAR(1),
    thursday VARCHAR(1),
    friday VARCHAR(1),
    saturday VARCHAR(1),
    sunday VARCHAR(1),
    start_date VARCHAR(10),
    end_date VARCHAR(10)
    );
    """

    CALENDAR_DATES_TABLE = """
    CREATE TABLE calendar_dates (
    service_id VARCHAR(5),
    date VARCHAR(10),
    exception_type VARCHAR(2)
    );
    """

    ROUTE_ID_TO_NAME_TABLE = """
    CREATE TABLE route_id_to_name (
    route_id VARCHAR(12),
    route_short_name VARCHAR(10)
    );
    """

    CHOSEN_ROUTES_TABLE = """
    CREATE TABLE chosen_routes (
    route_short_name VARCHAR(10)
    );
    """

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def create_table(self, name, table):
        """
        Creates an sqlite table
        """
        self.cursor.execute(f"DROP TABLE IF EXISTS {name}")
        self.cursor.execute(table)
        self.conn.commit()

    def create_tables(self):
        """
        Creates all tables needed
        """
        self.create_table("shapes", self.SHAPE_TABLE)
        self.create_table("routes", self.ROUTES_TABLE)
        self.create_table("trips", self.TRIPS_TABLE)
        self.create_table("stops", self.STOPS_TABLE)
        self.create_table("stop_times", self.STOP_TIMES_TABLE)
        self.create_table("route_id_to_name", self.ROUTE_ID_TO_NAME_TABLE)
        self.create_table("chosen_routes", self.CHOSEN_ROUTES_TABLE)
        self.create_table("agency", self.AGENCY_TABLE)
        self.create_table("calendar", self.CALENDAR_TABLE)
        self.create_table("calendar_dates", self.CALENDAR_DATES_TABLE)


if __name__ == "__main__":
    test_conn = sqlite3.connect("test_gtfsr.db")
    cr = TableCreator(test_conn)
    cr.create_table("chosen_routes", cr.CHOSEN_ROUTES_TABLE)
    cr.create_table("routes", cr.ROUTES_TABLE)
    cr.create_table("route_id_to_name", cr.ROUTE_ID_TO_NAME_TABLE)
    test_conn.close()
