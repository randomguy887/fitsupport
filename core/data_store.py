"""
data_store.py
--------------
This file handles saving user session data to a local SQLite database.
SQLite is a simple file-based database — no server needed.

Ethics note:
  - No names or contact details are stored
  - Only anonymous fitness data (age, weight, goal, results)
  - Used only for academic evaluation purposes
"""

import sqlite3   # Built into Python — no installation needed
import os        # Used to find the file path
from datetime import datetime  # Used to record when a session happened

# Path to the database file — stored in the 'data' folder
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "fitsupport.db")


def get_connection():
    """Opens a connection to the SQLite database file. Creates it if it doesn't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # Create 'data' folder if needed
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row  # Lets us access columns by name
    return connection


def initialise_database():
    """
    Creates the database tables if they don't already exist.
    Called once when the app starts.

    Table 1: sessions — stores one row for each time someone uses the app
    Table 2: feedback — stores usability ratings from users
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Create the sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp        TEXT,
            age              INTEGER,
            weight_kg        REAL,
            height_cm        REAL,
            activity_level   TEXT,
            fitness_goal     TEXT,
            bmr              REAL,
            tdee             REAL,
            target_calories  REAL,
            protein_g        REAL,
            carbs_g          REAL,
            fat_g            REAL,
            water_ml         REAL,
            bmi              REAL,
            bmi_category     TEXT,
            supplements_count INTEGER
        )
    """)

    # Create the feedback table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id  INTEGER,
            timestamp   TEXT,
            usability   INTEGER,
            accuracy    INTEGER,
            usefulness  INTEGER,
            comments    TEXT
        )
    """)

    conn.commit()
    conn.close()


def log_session(profile, nutrition, supplements_count):
    """
    Saves one anonymised session to the database.
    Called every time the user clicks 'Calculate My Plan'.
    Returns the session ID so we can link feedback to it later.
    """
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sessions (
            timestamp, age, weight_kg, height_cm, activity_level, fitness_goal,
            bmr, tdee, target_calories, protein_g, carbs_g, fat_g,
            water_ml, bmi, bmi_category, supplements_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),   # Current date and time
        profile.age,
        profile.weight_kg,
        profile.height_cm,
        profile.activity_level,
        profile.fitness_goal,
        nutrition.bmr,
        nutrition.tdee,
        nutrition.target_calories,
        nutrition.protein_g,
        nutrition.carbs_g,
        nutrition.fat_g,
        nutrition.water_ml,
        nutrition.bmi,
        nutrition.bmi_category,
        supplements_count,
    ))

    session_id = cursor.lastrowid  # Get the ID of the row we just inserted
    conn.commit()
    conn.close()
    return session_id


def save_feedback(session_id, usability, accuracy, usefulness, comments):
    """
    Saves a user's feedback ratings to the database.
    Linked to a specific session via session_id.
    """
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (session_id, timestamp, usability, accuracy, usefulness, comments)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (session_id, datetime.now().isoformat(), usability, accuracy, usefulness, comments))

    conn.commit()
    conn.close()
