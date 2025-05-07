# db/helpers.py
import sqlite3
import os

# You can add more helpers like:
# def get_all_suggestions(): ...
# def delete_suggestion(id): ...
# def update_suggestion(id, ...): ...


# Connect to the SQLite database and return the connection object.
def get_db_connection():

    # Connect to the SQLite database and return the connection object.

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, '..', 'database.db')

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Allows returning rows as dictionaries
    return conn


def insert_suggestion(plant_name, description, location, plant_type, uploader_name, image_filename):
    """
    Insert a new plant suggestion into the suggestions table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO suggestions (
            plant_name, description, location, plant_type, uploader_name, image_filename
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (plant_name, description, location, plant_type, uploader_name, image_filename))

    conn.commit()
    conn.close()
