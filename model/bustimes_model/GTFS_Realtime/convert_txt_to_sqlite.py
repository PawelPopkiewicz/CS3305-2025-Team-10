"""
Convert .txt files into sqlite for easier manipulation and queries
"""

import sqlite3

class TableCreator():

# conn = sqlite3.connect("gtfsr.db")

# cursor = conn.cursor()

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


class TablePopulator():
    """Populates the tables with data"""

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.agency_id = "7778020"

    def populate_chosen_routes(self):
        """Populates the chosen_routes table with predefined values"""
        with open("chosen_routes.txt", "r", encoding="utf-8") as txtconn:
            lines = txtconn.readlines()
            for line in lines:
                route = line.strip("\n")
                self.cursor.execute("INSERT INTO chosen_routes VALUES (?)",
                                    (route,))
        self.conn.commit()

    def populate_shapes(self):
        """
        Populates the shapes table
        """
        with open("source_text_files/shapes.txt", "r", encoding="utf-8") as txtconn:
            lines = txtconn.readlines()
            for line in lines[1:]:
                shape_id, lat, lon, seq, distance = line.strip("\n").split(",")
                # print(f"shape_id={shape_id}")
                # print(line)
                self.cursor.execute("INSERT INTO shapes VALUES (?, ?, ?, ?, ?)",
                               (shape_id, float(lat), float(lon), int(seq), float(distance)))
        self.conn.commit()

    def populate_routes(self):
        """
        Populates the routes table
        """
        with open("source_text_files/routes.txt", "r", encoding="utf-8") as txtconn:
            lines = txtconn.readlines()
            for line in lines[1:]:
                fields = line.strip("\n").split(",")
                # print(f"shape_id={shape_id}")
                # print(line)
                self.cursor.execute("INSERT INTO routes VALUES (?, ?, ?, ?)", tuple(fields[:4]))
        self.conn.commit()

    def populate_stop_times(self):
        """
        Populates the stop_times table
        """
        with open("source_text_files/stop_times.txt", "r", encoding="utf-8") as txtconn:
            lines = txtconn.readlines()
            for line in lines[1:]:
                fields = line.strip("\n").split(",")
                # print(f"shape_id={shape_id}")
                # print(line)
                self.cursor.execute("INSERT INTO stop_times VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                               tuple(fields[:5]+fields[6:9]))
        self.conn.commit()

    def populate_trips(self):
        """
        Populates the trips table
        """
        with open("source_text_files/trips.txt", "r", encoding="utf-8") as txtconn:
            lines = txtconn.readlines()
            for line in lines[1:]:
                fields = line.strip("\n").split(",")
                # print(f"shape_id={shape_id}")
                # print(line)
                self.cursor.execute("INSERT INTO trips VALUES (?, ?, ?, ?, ?)", tuple(fields[:3]+[fields[5], fields[7]]))
        self.conn.commit()

    def populate_stops(self):
        """
        Populates the stops table
        """
        with open("source_text_files/stops.txt", "r", encoding="utf-8") as txtconn:
            lines = txtconn.readlines()
            for line in lines[1:]:
                fields = line.strip("\n").split(",")
                # print(f"shape_id={shape_id}")
                # print(line)
                self.cursor.execute("INSERT INTO stops VALUES (?, ?, ?, ?)", tuple([fields[0], fields[2]]+fields[4:6]))
        self.conn.commit()

    def populate_route_id_to_name(self):
        """
        Populates the route_id_to_name table
        """
        query = """
        INSERT INTO route_id_to_name (route_id, route_short_name)
        SELECT r.route_id, r.route_short_name
        FROM routes AS r
        INNER JOIN chosen_routes AS c
        ON r.route_short_name = c.route_short_name AND r.agency_id = 7778020;
        """
        self.cursor.execute(query)
#         with open("source_text_files/route_id_to_name.txt", "r", encoding="utf-8") as txtconn:
#             lines = txtconn.readlines()
#             for line in lines[1:]:
#                 fields = line.strip("\n").split(",")
#                 # print(f"shape_id={shape_id}")
#                 # print(line)
#                 self.cursor.execute("INSERT INTO route_id_to_name VALUES (?, ?)",
#                                tuple(fields))
        self.conn.commit()

    def populate_tables(self):
        """
        Populates tables
        """
        self.populate_trips()
        self.populate_stops()
        self.populate_stop_times()
        self.populate_routes()
        self.populate_shapes()
        self.populate_chosen_routes()
        self.populate_route_id_to_name()


if __name__ == "__main__":
    conn = sqlite3.connect("test_gtfsr.db")
    cr = TableCreator(conn)
    po = TablePopulator(conn)
    cr.create_table("chosen_routes", cr.CHOSEN_ROUTES_TABLE)
    cr.create_table("routes", cr.ROUTES_TABLE)
    cr.create_table("route_id_to_name", cr.ROUTE_ID_TO_NAME_TABLE)
    po.populate_chosen_routes()
    po.cursor.execute("SELECT * FROM chosen_routes;")
    print(po.cursor.fetchall())
    po.populate_routes()
    po.populate_route_id_to_name()
    po.cursor.execute("SELECT * FROM route_id_to_name;")
    [print(row) for row in po.cursor.fetchall()]
    conn.close()
