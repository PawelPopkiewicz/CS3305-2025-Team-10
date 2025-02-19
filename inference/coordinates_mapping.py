"""
Functions which handle the mapping between coordinates and distance travelled
main function is map_coordinates_to_progress
"""

from db_connection import create_connection, close_connection


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


def v1_get_next_stop_distance(distance, trip_id, direction):
    """prototyping the mapping"""
    direction = bool(direction)
    get_query = """
    SELECT sh.shape_dist_traveled
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
    ORDER BY (sh.shape_pt_lat - stop.stop_lat)^2 + (sh.shape_pt_lon - stop.stop_lon)^2
    LIMIT 1;
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(get_query, (trip_id, trip_id, direction, distance))
    result = cursor.fetchall()
    close_connection(conn)
    return result[0][0] if result else None


if __name__ == "__main__":
    test_conn = create_connection()

    close_connection(test_conn)
