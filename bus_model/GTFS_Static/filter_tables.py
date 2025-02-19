"""
Filter the sqlite dbs to only relevant rows
"""


class TableFilter():
    """Filters the tables so they relate only to Cork city"""

    FILTER_ROUTES = """WHERE route_id NOT IN (SELECT route_id FROM route_id_to_name)"""
    FILTER_TRIPS = """WHERE route_id NOT IN (SELECT route_id FROM route_id_to_name)"""
    FILTER_STOP_TIMES = """WHERE NOT EXISTS (SELECT 1 FROM trips WHERE trips.trip_id = stop_times.trip_id)"""
    FILTER_STOPS = """WHERE stop_id NOT IN (SELECT DISTINCT stop_id FROM stop_times)"""
    FILTER_SHAPES = """WHERE NOT EXISTS (SELECT 1 FROM trips WHERE trips.shape_id = shapes.shape_id)"""
    FILTER_CALENDAR = """WHERE service_id NOT IN (SELECT service_id FROM trips)"""
    FILTER_CALENDAR_DATES = """WHERE service_id NOT IN (SELECT service_id FROM trips)"""

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def filter_table(self, name, filter_statement):
        """Filters the provided table with a provided filter where statement"""
        query = f"DELETE FROM {name} {filter_statement};"
        self.cursor.execute(query)
        print(f"Filtered {name} table")

    def filter_tables(self):
        """Filter out the tables in the db"""
        if not self.conn.autocommit:
            self.conn.autocommit = True
        self.filter_table("routes", self.FILTER_ROUTES)
        self.filter_table("trips", self.FILTER_TRIPS)
        self.filter_table("stop_times", self.FILTER_STOP_TIMES)
        self.filter_table("stops", self.FILTER_STOPS)
        self.filter_table("shapes", self.FILTER_SHAPES)
        self.filter_table("calendar", self.FILTER_CALENDAR)
        self.filter_table("calendar_dates", self.FILTER_CALENDAR_DATES)
        self.cursor.execute("VACUUM;")


if __name__ == "__main__":
    from GTFS_Static.db_connection import create_connection, close_connection
    conn = create_connection()
    tf = TableFilter(conn)
    tf.filter_tables()
    close_connection(conn)
