"""
Primitive test functions to see if postgresql works
"""

from .db_connection import create_connection, close_connection


def test_connection():
    """Fetches 10 rows from shapes"""
    conn = create_connection()
    test_query = """
    SELECT * FROM shapes
    LIMIT 10;
    """
    cursor = conn.cursor()
    cursor.execute(test_query)
    result = cursor.fetchall()
    close_connection(conn)
    return result


def count_stops_trips_join():
    """Reports how many lines are there after joining trips with stops"""
    conn = create_connection()
    test_query = """
    SELECT COUNT(*)
    FROM stops CROSS JOIN trips;
    """
    cursor = conn.cursor()
    cursor.execute(test_query)
    result = cursor.fetchall()
    close_connection(conn)
    return result


def return_query(query):
    """Executes the given query and returns the result"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    close_connection(conn)
    return result


if __name__ == "__main__":
    # join_count = count_stops_trips_join()
    stop_times_count_query = """
    SELECT COUNT(*) FROM stop_times;
    """
    print(return_query(stop_times_count_query))
