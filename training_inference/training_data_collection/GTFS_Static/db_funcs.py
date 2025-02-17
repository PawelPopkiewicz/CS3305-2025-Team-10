"""
Helper functions to retrieve data from sqlite db
"""

from .db_connection import close_connection, create_connection


def get_route_id_to_name_dict():
    """returns a dict which maps route_id to route_short_name"""
    query = """
    SELECT * FROM route_id_to_name;
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    route_dict = {route_id:route_name for route_id, route_name in rows}
    close_connection(conn)
    return route_dict


if __name__ == "__main__":
    print(get_route_id_to_name_dict())
