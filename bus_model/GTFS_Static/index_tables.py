"""
Creates indexes on the database
"""


class TableIndexer():
    """Creates indexes on the tables"""

    TRIPS_SHAPE_INDEX = """idx_trips_shape_id ON trips(shape_id)"""
    STOP_TIMES_ROUTE_INDEX = """idx_stop_times_route_id ON stop_times(route_id)"""
    SHAPE_ID_INDEX = """idx_shape_id ON shapes(shape_id)"""
    TRIPS_ROUTE_DIRECTION_INDEX = """idx_trip_route_directon ON trips(route_id, direction)"""

    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_index(self, index_info):
        """Creates an index by running the query provided"""
        index_query = "CREATE INDEX " + index_info + ";"
        self.cursor.execute(index_query)
        print("Created_index " + index_info.split(" ")[0])

    def create_indexes(self):
        """Creates all indexes on the tables"""
        self.create_index(self.TRIPS_SHAPE_INDEX)
        self.create_index(self.STOP_TIMES_ROUTE_INDEX)
        self.create_index(self.SHAPE_ID_INDEX)
        self.create_index(self.TRIPS_ROUTE_DIRECTION_INDEX)
