"""
Populates the tables with data from txt files
"""

from io import StringIO
import pandas as pd
from .get_root import get_root


class AgencyNotFoundError(Exception):
    """Custom exception for when the bus agency is not found in the db"""


class TablePopulator():
    """Populates the tables with data"""

    ROUTES_FIELDS = [0, 1, 2, 3]
    TRIPS_FIELDS = [0, 1, 2, 5, 7]
    STOPS_FIELDS = [0, 2, 4, 5]
    STOP_TIMES_FIELDS = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    SHAPES_FIELDS = [0, 1, 2, 3, 4]
    AGENCY_FIELDS = [0, 1]
    CALENDAR_FIELDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    CALENDAR_DATES_FIELDS = [0, 1, 2]
    CHOSEN_ROUTES_FIELDS = [0]

    ROUTES_MASK = ["str", "str", "str", "str"]
    TRIPS_MASK = ["str", "str", "str", "bool", "str"]
    STOPS_MASK = ["str", "str", "float", "float"]
    STOP_TIMES_MASK = ["str", "str", "str", "str", "int", "str", "bool", "bool", "bool"]
    SHAPES_MASK = ["str", "float", "float", "int", "float"]
    AGENCY_MASK = ["str", "str"]
    CALENDAR_MASK = ["str"] + ["bool"]*7 + ["str", "str"]
    CALENDAR_DATES_MASK = ["str", "str", "str"]
    CHOSEN_ROUTES_MASK = ["str"]

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def create_df(self, name, field_indexes, field_mask):
        """
        Creates the dataframe from a csv file specified by name
        casts the value to the correct type
        """
        root = get_root()
        filename = name + ".txt"
        textfile_path = root / "GTFS_Static" / "source_text_files" / filename
        df = pd.read_csv(textfile_path, low_memory=False)
        df = df.iloc[:, field_indexes]
        for i, mask in enumerate(field_mask):
            col_name = df.columns[i]
            match mask:
                case "str":
                    df[col_name] = df[col_name].astype(str)
                case "bool":
                    df[col_name] = df[col_name].astype(bool)
                case "int":
                    df[col_name] = df[col_name].astype(int)
                case "float":
                    df[col_name] = df[col_name].astype(float).round(6)
        if name == "shapes":
            df = df.drop_duplicates(subset=["shape_id", "shape_pt_lat", "shape_pt_lon"])
        return df

    def insert_df(self, name, df):
        """
        Insert the dataframe into the table
        """
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False, header=False)
        csv_buffer.seek(0)
        copy_query = "COPY " + name + " FROM STDIN (FORMAT CSV)"
        with self.cursor.copy(copy_query) as copy:
            while data := csv_buffer.read(100):
                copy.write(data)

    def populate_table(self, name, field_indexes, field_mask):
        """Populates the table"""
        df = self.create_df(name, field_indexes, field_mask)
        self.insert_df(name, df)
        print("Populated " + name + " table")

    def get_bus_eirann_agency_id(self):
        """
        Returns the agency_id of bus eirann
        """
        query = """
        SELECT agency_id
        FROM agency
        WHERE agency_name = 'Bus Éireann';
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            print("Found Bus Éireann agency_id: " + result[0])
            return result[0]
        raise AgencyNotFoundError("Bus Eirrean not found in the database")

    def populate_route_id_to_name(self):
        """
        Populates the route_id_to_name table
        """
        agency_id = self.get_bus_eirann_agency_id()
        query = """
        INSERT INTO route_id_to_name (route_id, route_short_name)
        SELECT r.route_id, r.route_short_name
        FROM routes AS r
        INNER JOIN chosen_routes AS c
        ON r.route_short_name = c.route_short_name AND r.agency_id = %s;
        """
        self.cursor.execute(query, (agency_id,))

    def index_shape_id_on_trips(self):
        """Creates an index on shape_id in trips table"""
        index_query = """CREATE INDEX idx_trips_shape_id ON trips(shape_id);"""
        self.cursor.execute(index_query)
        print("Indexed shape_id in trips table")

    def populate_tables(self):
        """
        Populates tables
        """
        self.conn.autocommit = True
        self.populate_table("routes", self.ROUTES_FIELDS, self.ROUTES_MASK)
        self.populate_table("trips", self.TRIPS_FIELDS, self.TRIPS_MASK)
        self.populate_table("stops", self.STOPS_FIELDS, self.STOPS_MASK)
        self.populate_table("stop_times", self.STOP_TIMES_FIELDS, self.STOP_TIMES_MASK)
        self.populate_table("shapes", self.SHAPES_FIELDS, self.SHAPES_MASK)
        self.populate_table("agency", self.AGENCY_FIELDS, self.AGENCY_MASK)
        self.populate_table("calendar", self.CALENDAR_FIELDS, self.CALENDAR_MASK)
        self.populate_table("calendar_dates", self.CALENDAR_DATES_FIELDS, self.CALENDAR_DATES_MASK)
        self.populate_table("chosen_routes", self.CHOSEN_ROUTES_FIELDS, self.CHOSEN_ROUTES_MASK)
        self.populate_route_id_to_name()
        self.index_shape_id_on_trips()
        self.conn.autocommit = False


if __name__ == "__main__":
    from .db_connection import create_connection, close_connection
    test_conn = create_connection()
    pt = TablePopulator(test_conn)
    print(pt.get_bus_eirann_agency_id())
    close_connection(test_conn)
