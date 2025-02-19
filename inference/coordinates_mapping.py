"""
Functions which handle the mapping between coordinates and distance travelled
main function is map_coordinates_to_progress
"""

from db_connection import create_connection, close_connection


def map_coord_to_progress(trip_id, direction, lat, lon):
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


def get_next_stop_distance(distance, trip_id, direction):
    """Returns the distance of the next stop in this trip"""
    direction = bool(direction)
    conn = create_connection()
    query = """
    SELECT stop_id
    FROM stop_distance
    WHERE trip_id = %s AND direction = %s AND distance > %s
    ORDER BY ABS(distance - %s)
    LIMIT 1;
    """
    cursor = conn.cursor()
    cursor.execute(query, (trip_id, direction, distance, distance))
    stop_id = cursor.fetchone()
    close_connection(conn)
    return stop_id[0] if stop_id else None


def create_trip_distance_table(conn):
    """Creates/updates the trip_distance table in postgres"""
    conn.execute("DROP TABLE IF EXISTS stop_distance;")
    create_query = """
    CREATE TABLE stop_distance (
        trip_id VARCHAR(12),
        stop_id VARCHAR(20),
        direction BOOLEAN,
        distance DOUBLE PRECISION
        );
    """
    conn.execute(create_query)
    conn.commit()


def populate_trip_distance_table(conn):
    """Populates the trip_distance table with data"""
    populate_query = """
    INSERT INTO stop_distance(trip_id, direction, stop_id, distance)
    SELECT
        t.trip_id,
        t.direction,
        s.stop_id,
        sh.shape_dist_traveled
    FROM stops AS s
    JOIN trips AS t ON TRUE
    JOIN LATERAL (
        SELECT shape_dist_traveled
        FROM shapes AS sh
        WHERE sh.shape_id = t.shape_id
        ORDER BY (sh.shape_pt_lat - s.stop_lat)^2 + (sh.shape_pt_lon - s.stop_lon)^2
        LIMIT 1
    ) AS sh ON TRUE;
    """
    conn.execute(populate_query)
    conn.commit()


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
