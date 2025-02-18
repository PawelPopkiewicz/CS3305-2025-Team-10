"""
testing the databases
"""

from .db_connection import close_connection, create_connection

conn = create_connection()
cursor = conn.cursor()
test_query = """
DELETE FROM routes
WHERE route_id NOT IN (
    SELECT route_id
    FROM route_id_to_name
    );
"""
test_query_2 = """
SELECT *
FROM routes;
"""
print("Deleting the routes")
cursor.execute(test_query)
conn.commit()
print("Deleted the routes")
cursor.execute(test_query_2)
rows = cursor.fetchall()
for row in rows:
    print(row)
close_connection(conn)
