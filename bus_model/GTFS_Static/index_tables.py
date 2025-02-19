"""
Creates indexes on the database
"""


class TableIndexer():
    """Creates indexes on the tables"""

    TRIPS_SHAPE_INDEX = """idx_trips_shape_id ON trips(shape_id)"""
    STOP_TIMES_TRIP_INDEX = """idx_stop_times_trip_id ON stop_times(trip_id)"""
    SHAPE_ID_INDEX = """idx_shape_id ON shapes(shape_id)"""
    TRIPS_TRIP_DIRECTION_INDEX = """idx_trip_route_directon ON trips(trip_id, direction)"""

    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_index(self, index_info):
        """Creates an index by running the query provided"""
        index_query = "CREATE INDEX " + index_info + ";"
        self.cursor.execute(index_query)
        print("Created_index " + index_info.split(" ")[0])

    def create_indexes_before_filter(self):
        """Creates all indexes on the tables, before filtering"""
        self.create_index(self.TRIPS_SHAPE_INDEX)

    def create_indexes_after_filter(self):
        """Creates indexes, run after filtering"""
        self.create_index(self.STOP_TIMES_TRIP_INDEX)
        self.create_index(self.SHAPE_ID_INDEX)
        self.create_index(self.TRIPS_TRIP_DIRECTION_INDEX)
