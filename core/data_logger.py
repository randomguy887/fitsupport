"""
FitSupport - Data Logger Module
=================================
Saves anonymised session results to a CSV file for academic analysis.

ETHICS COMPLIANCE:
  - NO names, emails, or contact details are collected
  - NO medical history or clinical data is stored
  - Data is used for academic purposes only
  - Each record is assigned a random anonymous session ID

Author: FitSupport Project
University: LJMU BSc Computer Science Top-Up
"""

import csv
import os
import uuid
from datetime import datetime

# Path to the CSV data store (relative to project root)
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "sessions.csv")

# Column headers matching the ethics-approved data collection plan
FIELDNAMES = [
    "session_id",       # Anonymous UUID
    "timestamp",        # Date/time of session (no personal identifier)
    "age",
    "gender",           # Optional – "Not Specified" if skipped
    "weight_kg",
    "height_cm",
    "activity_level",
    "goal",
    "bmr",
    "tdee",
    "daily_calories",
    "protein_g",
    "fat_g",
    "carb_g",
    "water_litres",
    "bmi",
]


def _ensure_file_exists():
    """Creates the CSV file with headers if it does not already exist."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def log_session(profile: dict, results: dict) -> str:
    """
    Appends one anonymised session record to the CSV.

    Parameters
    ----------
    profile : dict  – user inputs (age, weight, etc.)
    results : dict  – calculated outputs from NutritionCalculator

    Returns
    -------
    str : the anonymous session_id assigned to this record
    """
    _ensure_file_exists()

    session_id = str(uuid.uuid4())[:8].upper()   # Short readable ID, e.g. "A3F9C21B"
    timestamp  = datetime.now().strftime("%Y-%m-%d %H:%M")

    row = {
        "session_id":     session_id,
        "timestamp":      timestamp,
        "age":            profile.get("age", ""),
        "gender":         profile.get("gender", "Not Specified"),
        "weight_kg":      profile.get("weight_kg", ""),
        "height_cm":      profile.get("height_cm", ""),
        "activity_level": profile.get("activity_level", ""),
        "goal":           profile.get("goal", ""),
        "bmr":            results.get("bmr", ""),
        "tdee":           results.get("tdee", ""),
        "daily_calories": results.get("daily_calories", ""),
        "protein_g":      results.get("protein_g", ""),
        "fat_g":          results.get("fat_g", ""),
        "carb_g":         results.get("carb_g", ""),
        "water_litres":   results.get("water_litres", ""),
        "bmi":            results.get("bmi", ""),
    }

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)

    return session_id


def load_all_sessions() -> list[dict]:
    """
    Reads all stored sessions from the CSV and returns them as a
    list of dicts. Used in the analytics view for academic analysis.
    """
    _ensure_file_exists()
    sessions = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sessions.append(row)
    return sessions


def count_sessions() -> int:
    """Returns the total number of sessions logged."""
    return len(load_all_sessions())
