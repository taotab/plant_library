# import sqlite3

# conn = sqlite3.connect('.\dat.db')
# print ("Opened database successfully")

# conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
# print ("Table created successfully")
# conn.close()


import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
schema_path = os.path.join(base_dir, 'schema.sql')

with open(schema_path) as f:
    conn = sqlite3.connect(os.path.join(base_dir, 'database.db'))
    conn.executescript(f.read())
    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # to access columns by name
    return conn
