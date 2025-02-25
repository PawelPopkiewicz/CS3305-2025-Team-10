"""
Functions which handle the mapping between coordinates and distance travelled
main function is map_coordinates_to_progress
"""

from .db_connection import create_connection, close_connection


def get_route_name_from_trip(trip_id):
    """Returns the name of the route from the trip_id"""
    conn = create_connection()
    query = """
    SELECT r_n.route_short_name
    FROM route_id_to_name AS r_n
    WHERE r_n.route_id = (
        SELECT t.route_id
        FROM trips AS t
        WHERE t.trip_id = %s
    );
    """
    cursor = conn.cursor()
    cursor.execute(query, (trip_id,))
    route_name = cursor.fetchone()
    return route_name[0] if route_name else None


def get_route_name_from_route_id(route_id):
    """Returns the route name from route_id"""
    conn = create_connection()
    query = """
    SELECT route_short_name
    FROM route_id_to_name
    WHERE route_id = %s;
    """
    cursor = conn.cursor()
    cursor.execute(query, (route_id,))
    route_name = cursor.fetchone()
    return route_name[0] if route_name else None


def trip_among_stops(trip_id, stop_id):
    """Returns the trip_id from stop_id"""
    conn = create_connection()
    query = """
    SELECT EXISTS (
        SELECT 1
        FROM stop_times as st
        WHERE stop_id = %s AND trip_id = %s
    ) AS trip_exists;
    """
    cursor = conn.cursor()
    cursor.execute(query, (stop_id, trip_id))
    trip_exists = cursor.fetchone()
    return trip_exists[0] if trip_exists else None


def get_stops_on_trip(trip_id):
    """Returns all of the stops on a trip"""
    conn = create_connection()
    query = """
    SELECT s.stop_name
    FROM stops AS s
    WHERE s.stop_id IN (
        SELECT st.stop_id FROM stop_times AS st
        WHERE st.trip_id = %s
    );
    """
    cursor = conn.cursor()
    cursor.execute(query, (trip_id,))
    result = cursor.fetchall()
    print(f"Number of stops: {len(result)}")
    return result if result else None


def check_trip_id_exists(trip_id, direction):
    """Returns True if the trip_id is in the database"""
    conn = create_connection()
    query = """
    SELECT trip_id FROM trips
    WHERE trip_id = %s AND direction = %s;
    """
    cursor = conn.cursor()
    cursor.execute(query, (trip_id, direction))
    result = cursor.fetchone()
    return bool(result)


def map_coord_to_distance(trip_id, direction, lat, lon):
    """Maps a coordinate to a distance for a specific trip"""
    conn = create_connection()
    query = """
    SELECT shape_dist_traveled FROM shapes
    WHERE shape_id IN (
        SELECT shape_id FROM trips
        WHERE trip_id = %s AND direction = %s
        )
    ORDER BY ABS(shape_pt_lat - %s) + ABS(shape_pt_lon - %s)
    LIMIT 1;
    """
    cursor = conn.cursor()
    cursor.execute(query, (trip_id, bool(direction), lat, lon))
    dist_travelled = cursor.fetchone()
    close_connection(conn)
    return dist_travelled[0] if dist_travelled else None


def get_stop_distances_for_trip(trip_id, direction):
    """Returns distance traveled for all the stops on the trip"""
    conn = create_connection()
    query = """
    SELECT stop.stop_id,
    (
        SELECT sh.shape_dist_traveled
        FROM shapes AS sh
        WHERE sh.shape_id = (
            SELECT t.shape_id FROM trips AS t
            WHERE t.trip_id = %s AND t.direction = %s
            )
        ORDER BY POWER(sh.shape_pt_lat - stop.stop_lat,2) + POWER(sh.shape_pt_lon - stop.stop_lon,2)
        LIMIT 1
    ) AS distance
    FROM (
        SELECT *
        FROM stops AS s
        WHERE s.stop_id IN (
            SELECT st.stop_id FROM stop_times AS st
            WHERE st.trip_id = %s
        )
    ) AS stop
    ORDER BY distance;
    """
    cursor = conn.cursor()
    cursor.execute(query, (trip_id, direction, trip_id))
    result = cursor.fetchall()
    return result if result else None


def v1_get_next_stop_distance(distance, trip_id, direction):
    """prototyping the mapping"""
    direction = bool(direction)
    get_query = """
    SELECT sh.shape_dist_traveled, stop.stop_id, stop.stop_lat, stop.stop_lon
    FROM (
        SELECT *
        FROM stops AS s
        WHERE s.stop_id IN (
            SELECT st.stop_id FROM stop_times AS st
            WHERE st.trip_id = %s
        )
    ) AS stop
    JOIN shapes AS sh
        ON sh.shape_id = (
            SELECT t.shape_id FROM trips AS t
            WHERE t.trip_id = %s AND t.direction = %s
            )
        AND sh.shape_dist_traveled > %s
    ORDER BY ((sh.shape_pt_lat - stop.stop_lat)^2 + (sh.shape_pt_lon - stop.stop_lon)^2)
    LIMIT 1;
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(get_query, (trip_id, trip_id, direction, distance))
    result = cursor.fetchall()
    close_connection(conn)
    return result[0] if result else [None, None, None, None]


if __name__ == "__main__":
    test_conn = create_connection()

    close_connection(test_conn)
