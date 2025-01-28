"""
testing the databases
"""

import sqlite3

conn = sqlite3.connect("gtfsr.db")

cursor = conn.cursor()

# cursor.execute("SELECT * FROM trips LIMIT 50;")
cursor.execute("SELECT COUNT(*) FROM shapes;")
rows = cursor.fetchall()
for row in rows:
    print(row)
