"""
Create the databases from txt files and filter them to include only cork city routes
"""

import sqlite3
from .convert_txt_to_sqlite import TableCreator, TablePopulator
from .filter_db import TableFilter

if __name__ == "__main__":
    conn = sqlite3.connect("gtfsr.db")
    tc = TableCreator(conn)
    tp = TablePopulator(conn)
    tf = TableFilter(conn)
    tc.create_tables()
    tp.populate_tables()
    tf.filter_tables()
    conn.close()
