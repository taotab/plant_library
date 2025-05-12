-- schema.sql

-- This SQL script creates the necessary tables for the plant suggestion application.
-- Use below query command to delete all entried (fresh start) for the particular table in the database.
-- DROP TABLE IF EXISTS <table_name>;


CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_name TEXT NOT NULL,
    description TEXT,
    location TEXT,
    plant_type TEXT NOT NULL,
    uploader_name TEXT,
    image_filename TEXT NOT NULL,
    benefits TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS plants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_name TEXT NOT NULL,
    description TEXT,
    location TEXT,
    plant_type TEXT NOT NULL,
    uploader_name TEXT,
    image_filename TEXT NOT NULL,
    benefits TEXT,
    approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
