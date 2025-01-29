import sqlite3
import os


def find_db():
    """Finds the gtfsr.db file starting from the current dir"""
    dir_path = os.path.dirname(os.path.realpath(__file__))

    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith("gtfsr.db"):
                return os.path.join(root, file)
    return ""


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
