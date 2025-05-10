# db/helpers.py
import io
from PIL import Image
import sqlite3
import os
from flask import current_app as app

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


def update_suggestion(id, plant_name, description, plant_type, location, image_filename=None, benefits=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    benefits = benefits.strip() if benefits else ''

    if image_filename:
        cursor.execute('''
            UPDATE suggestions
            SET plant_name = ?, description = ?, plant_type = ?, location = ?, image_filename = ?, benefits = ?
            WHERE id = ?
        ''', (plant_name, description, plant_type, location, image_filename, benefits, id))
    else:
        cursor.execute('''
            UPDATE suggestions
            SET plant_name = ?, description = ?, plant_type = ?, location = ?, benefits = ?
            WHERE id = ?
        ''', (plant_name, description, plant_type, location, benefits, id))

    conn.commit()
    conn.close()


def insert_plant_from_suggestion(suggestion):
    # benefits = suggestion['benefits'] if suggestion['benefits'] else ''
    benefits = suggestion['benefits'].strip() if suggestion['benefits'] else ''

    description = suggestion['description'] if suggestion['description'] else 'No description provided.'
    location = suggestion['location'] if suggestion['location'] else 'Unknown'
    uploader_name = suggestion['uploader_name'] if suggestion['uploader_name'] else 'Anonymous'

    app.logger.info(f"Inserting plant: {suggestion['plant_name']}")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO plants (
            plant_name, description, location, plant_type, uploader_name, image_filename, benefits
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        suggestion['plant_name'],
        description,
        location,
        suggestion['plant_type'],
        uploader_name,
        suggestion['image_filename'],
        benefits
    ))

    conn.commit()
    conn.close()


def delete_suggestion_by_id(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM suggestions WHERE id = ?', (id,))
    conn.commit()
    conn.close()


def get_suggestion_by_id(id):
    conn = get_db_connection()
    suggestion = conn.execute(
        'SELECT * FROM suggestions WHERE id = ?', (id,)).fetchone()
    conn.close()
    return suggestion


# approved plants fetching (in dashboard for deletion)

def get_all_plants():
    conn = get_db_connection()
    plants = conn.execute('SELECT * FROM plants ORDER BY id DESC').fetchall()
    conn.close()
    return plants


# image compression from PIL:


def compress_and_save_image(image_file, save_path, max_size_kb=100, max_dim=500):
    img = Image.open(image_file)

    # Convert to RGB if needed (JPEG/WebP can't store alpha)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Resize to fit within max_dim x max_dim box
    img.thumbnail((max_dim, max_dim), Image.LANCZOS)

    # Try saving with decreasing quality until it's under the limit
    quality = 85  # start high
    while quality > 10:
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality,
                 optimize=True, progressive=True)
        size_kb = buffer.tell() / 1024

        if size_kb <= max_size_kb:
            with open(save_path, 'wb') as f:
                f.write(buffer.getvalue())
            return

        quality -= 5  # lower quality step by step

    # If it still didn't fit, save the smallest attempt anyway
    with open(save_path, 'wb') as f:
        f.write(buffer.getvalue())
