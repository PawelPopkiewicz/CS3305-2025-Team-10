"""
Provides functions which manage the connection to the postgresql database
"""

from os import getenv
import psycopg


def create_connection():
    """Creates connection to the main gtfsr database"""
    postgres_uri = getenv("POSTGRES_URI")
    conn = psycopg.connect(postgres_uri)
    return conn


def close_connection(conn):
    """Closes the provided connection"""
    conn.close()


if __name__ == "__main__":
    print(type(create_connection()))
