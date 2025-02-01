"""
Provides functions which manage the connection to the sqlite3 database
"""

import sqlite3
from .get_root import get_root


def find_db():
    """Finds the gtfsr.db file starting from the current dir"""
    root = get_root()
    db_path = root / "GTFS_Static" / "gtfsr.db"
    return db_path


def create_connection():
    """Creates connection to the main gtfsr database"""
    db_path = find_db()
    conn = sqlite3.connect(db_path)
    return conn


def close_connection(conn):
    """Closes the provided connection"""
    conn.close()


if __name__ == "__main__":
    print(find_db())
