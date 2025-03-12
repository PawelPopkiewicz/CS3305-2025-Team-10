"""
Functions which handle the mapping between coordinates and distance travelled
main function is map_coordinates_to_progress
"""
from math import pi, sin, cos, atan2, sqrt

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
    SELECT shape_dist_traveled, shape_pt_lat, shape_pt_lon
    FROM shapes
    WHERE shape_id IN (
        SELECT shape_id FROM trips
        WHERE trip_id = %s AND direction = %s
        )
    ORDER BY POWER(shape_pt_lat - %s, 2) + POWER(shape_pt_lon - %s, 2)
    LIMIT 1;
    """
    cursor = conn.cursor()
    cursor.execute(query, (trip_id, bool(direction), lat, lon))
    dist_travelled = cursor.fetchone()
    close_connection(conn)
    if dist_travelled is not None:
        off_route_distance = meters_between_coords(lat, lon, dist_travelled[1], dist_travelled[2])
        return dist_travelled[0], off_route_distance
    return None


def get_stop_distances_for_trip(trip_id, direction):
    """Returns distance traveled for all the stops on the trip"""
    conn = create_connection()
    query = """
    SELECT s.stop_id AS stop_id,
    (
        SELECT sh.shape_dist_traveled
        FROM shapes AS sh
        WHERE sh.shape_id = (
            SELECT t.shape_id FROM trips AS t
            WHERE t.trip_id = %s AND t.direction = %s
            )
        ORDER BY POWER(sh.shape_pt_lat - s.stop_lat,2) + POWER(sh.shape_pt_lon - s.stop_lon,2)
        LIMIT 1
    ) AS distance,
    st.arrival_time AS scheduled_time,
    st.departure_time AS departure_time
    FROM stops AS s
    JOIN stop_times AS st
    ON s.stop_id = st.stop_id
    AND st.trip_id = %s
    ORDER BY distance;
    """
    cursor = conn.cursor()
    cursor.execute(query, (trip_id, direction, trip_id))
    result = cursor.fetchall()
    return result if result else None


def off_route_distance(trip_id, direction, latitude, longitude):
    """Returns true if the bus is on route and false if it strays"""
    conn = create_connection()
    query = """
        SELECT sh.shape_pt_lat, shape_pt_lon,
        sh.shape_id
        FROM shapes AS sh
        WHERE sh.shape_id = (
            SELECT t.shape_id FROM trips AS t
            WHERE t.trip_id = %s AND t.direction = %s
            )
        ORDER BY POWER(sh.shape_pt_lat - %s,2) + POWER(sh.shape_pt_lon - %s,2)
        LIMIT 1;
    """
    cursor = conn.cursor()
    cursor.execute(query,
                   (trip_id, direction, latitude, longitude))
    result = cursor.fetchone()
    if result is not None:
        distance = meters_between_coords(
                latitude, longitude, result[0], result[1])
        return distance
    return None


def meters_between_coords(lat1, lon1, lat2, lon2):
    """computes the difference in meters between coordinates"""
    R = 6378.137
    d_lat = lat2 * pi / 180 - lat1 * pi / 180
    d_lon = lon2 * pi / 180 - lon1 * pi / 180
    a = sin(d_lat/2) * sin(d_lat/2) + \
        cos(lat1 * pi / 180) * cos(lat2 * pi / 180) * \
        sin(d_lon/2) * sin(d_lon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = R * c
    return d * 1000


if __name__ == "__main__":
    test_conn = create_connection()

    close_connection(test_conn)
