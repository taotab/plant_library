import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
schema_path = os.path.join(base_dir, 'schema.sql')
db_path = os.path.join(base_dir, 'database.db')


with open(schema_path) as f:
    conn = sqlite3.connect(db_path)
    conn.executescript(f.read())
    conn.commit()
    conn.close()

print("Initialized the database. Existing tables are preserved.")
