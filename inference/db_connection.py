"""
Provides functions which manage the connection to the postgresql database
"""

import psycopg
from os import getenv
from get_root import get_root


def create_connection():
    """Creates connection to the main gtfsr database"""
    # db_host = getenv("POSTGRES_HOST")
    # db_port = getenv("POSTGRES_PORT")
    # db_name = getenv("POSTGRES_DB")
    # db_user = getenv("POSTGRES_USER"T")
    # db_password = getenv("POSTGRES_PT"ASSWORD")
    # connect_data = "dbname=%s user=%s password=%s host=%s port=%s" % (db_name, db_user, db_password, db_host, db_port)
    postgres_uri = getenv("POSTGRES_URI")
    conn = psycopg.connect(postgres_uri)
    return conn


def close_connection(conn):
    """Closes the provided connection"""
    conn.close()


if __name__ == "__main__":
    print(find_db())
