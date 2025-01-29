"""
Filter the sqlite dbs to only relevant rows
"""

import sqlite3

# conn = sqlite3.connect("gtfsr.db")

# cursor = conn.cursor()

class TableFilter():

    FILTER_ROUTES = """WHERE route_id NOT IN (SELECT route_id FROM route_id_to_name)"""
    FILTER_TRIPS = """WHERE route_id NOT IN (SELECT route_id FROM route_id_to_name)"""
    FILTER_STOP_TIMES = """WHERE trip_id NOT IN (SELECT trip_id FROM trips)"""
    FILTER_STOPS = """WHERE stop_id NOT IN (SELECT stop_id FROM stop_times)"""
    FILTER_SHAPES = """WHERE shape_id NOT IN (SELECT shape_id FROM trips)"""


    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def filter_table(self, name, filter_statement):
        """Filters the provided table with a provided filter where statement"""
        query = f"DELETE FROM {name} {filter_statement};"
        self.cursor.execute(query)
        self.conn.commit()


    def filter_tables(self):
        """Filter out the tables in the db"""
        self.filter_table("routes", self.FILTER_ROUTES)
        self.filter_table("trips", self.FILTER_TRIPS)
        self.filter_table("stop_times", self.FILTER_STOP_TIMES)
        self.filter_table("stops", self.FILTER_STOPS)
        self.filter_table("shapes", self.FILTER_SHAPES)
        self.cursor.execute("VACUUM;")


if __name__ == "__main__":
    filter_table("routes", FILTER_ROUTES)
    # filter_tables()

# conn.close()
