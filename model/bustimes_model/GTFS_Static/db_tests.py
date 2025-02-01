"""
testing the databases
"""

from .db_connection import close_connection, create_connection

conn = create_connection()
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM shapes;")
rows = cursor.fetchall()
for row in rows:
    print(row)
close_connection(conn)
