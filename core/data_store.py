"""
FitSupport – Data Storage Module
=================================
Handles anonymous session logging to SQLite for evaluation purposes.

Ethics compliance:
  - No names, emails, or contact details are stored
  - No medical history is collected
  - Only anonymised fitness metrics and outputs are saved
  - Data is used exclusively for academic evaluation

Database: SQLite (file-based, no server required)
Library  : Python built-in 'sqlite3'
"""

import sqlite3
import os
from datetime import datetime


DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "fitsupport.db")


def get_connection() -> sqlite3.Connection:
    """Returns a connection to the SQLite database, creating the file if needed."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialise_database() -> None:
    """
    Creates the database tables if they do not already exist.
    Call once at app startup.

    Tables:
      sessions   – one row per user interaction (anonymised)
      feedback   – optional post-session usability rating
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp       TEXT    NOT NULL,
            age             INTEGER,
            weight_kg       REAL,
            height_cm       REAL,
            activity_level  TEXT,
            fitness_goal    TEXT,
            bmr             REAL,
            tdee            REAL,
            target_calories REAL,
            protein_g       REAL,
            carbs_g         REAL,
            fat_g           REAL,
            water_ml        REAL,
            bmi             REAL,
            bmi_category    TEXT,
            supplements_count INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id    INTEGER REFERENCES sessions(id),
            timestamp     TEXT    NOT NULL,
            usability     INTEGER,   -- 1–5 rating
            accuracy      INTEGER,   -- 1–5 rating
            usefulness    INTEGER,   -- 1–5 rating
            comments      TEXT       -- Optional free text (no personal info)
        )
    """)

    conn.commit()
    conn.close()


def log_session(profile, nutrition, supplements_count: int) -> int:
    """
    Saves an anonymised session record to the database.

    Parameters:
        profile           : UserProfile dataclass
        nutrition         : NutritionResult dataclass
        supplements_count : number of supplements recommended

    Returns:
        session_id : the auto-assigned row ID for this session
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sessions (
            timestamp, age, weight_kg, height_cm, activity_level, fitness_goal,
            bmr, tdee, target_calories, protein_g, carbs_g, fat_g,
            water_ml, bmi, bmi_category, supplements_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
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

    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id


def save_feedback(session_id: int, usability: int, accuracy: int,
                  usefulness: int, comments: str = "") -> None:
    """
    Saves optional usability feedback linked to a session.
    Comments field must NOT contain personal identifying information.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (session_id, timestamp, usability, accuracy, usefulness, comments)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        session_id,
        datetime.now().isoformat(),
        usability,
        accuracy,
        usefulness,
        comments,
    ))

    conn.commit()
    conn.close()


def get_all_sessions() -> list:
    """Returns all anonymised session records as a list of dicts."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions ORDER BY timestamp DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_session_count() -> int:
    """Returns the total number of sessions logged."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sessions")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_feedback_summary() -> dict:
    """Returns average ratings from the feedback table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            COUNT(*)           AS total_responses,
            AVG(usability)     AS avg_usability,
            AVG(accuracy)      AS avg_accuracy,
            AVG(usefulness)    AS avg_usefulness
        FROM feedback
    """)
    row = dict(cursor.fetchone())
    conn.close()
    return row
