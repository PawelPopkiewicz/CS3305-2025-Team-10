"""
Populates the tables with data from txt files
"""

from .get_root import get_root


class TablePopulator():
    """Populates the tables with data"""

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def populate_table(self, name, field_indexes):
        """
        Creates a connection to the text file based on the name and calls the given function
        """
        root = get_root()
        filename = name + ".txt"
        textfile_path = root / "GTFS_Static" / "source_text_files" / filename
        with open(textfile_path, "r", encoding="utf-8") as txtconn:
            lines = txtconn.readlines()
            for line in lines[1:]:
                fields = line.strip("\n").split(",")
                insert_field_data = tuple([fields[field_indexes[i]] for i in range(len(field_indexes))])
                query = "INSERT INTO " + name + " VALUES (" + "?, "*(len(field_indexes)-1) + "?);"
                self.cursor.execute(query, insert_field_data)
        self.conn.commit()

    def get_bus_eirann_agency_id(self):
        """
        Returns the agency_id of bus eirann
        """
        query = """
        SELECT agency_id
        FROM agency
        WHERE agency_name = "Bus Éireann";
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return "7778020"

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
        ON r.route_short_name = c.route_short_name AND r.agency_id = ?;
        """
        self.cursor.execute(query, (agency_id,))
        self.conn.commit()

    def populate_tables(self):
        """
        Populates tables
        """
        self.populate_table("shapes", list(range(5)))
        self.populate_table("routes", list(range(4)))
        self.populate_table("stop_times", list(range(5))+list(range(6, 9)))
        self.populate_table("trips", [0, 1, 2, 5, 7])
        self.populate_table("stops", [0, 2, 4, 5])
        self.populate_table("agency", [0, 1])
        self.populate_table("calendar", list(range(10)))
        self.populate_table("calendar_dates", list(range(3)))
        self.populate_table("chosen_routes", [0])
        self.populate_route_id_to_name()


if __name__ == "__main__":
    from .db_connection import create_connection, close_connection
    test_conn = create_connection()
    pt = TablePopulator(test_conn)
    print(pt.get_bus_eirann_agency_id())
    close_connection(test_conn)
