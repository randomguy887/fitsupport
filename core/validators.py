"""
FitSupport - Input Validation Module
======================================
Centralises all validation logic so the UI stays clean and
validation rules are testable independently.

Author: FitSupport Project
University: LJMU BSc Computer Science Top-Up
"""

# ------------------------------------------------------------------
# Acceptable input ranges
# ------------------------------------------------------------------
AGE_MIN, AGE_MAX           = 16, 80        # years
WEIGHT_MIN, WEIGHT_MAX     = 30.0, 300.0   # kg
HEIGHT_MIN, HEIGHT_MAX     = 100.0, 250.0  # cm

VALID_GOALS = ["Weight Loss", "Muscle Gain", "Maintenance"]

VALID_ACTIVITY_LEVELS = [
    "Sedentary (little or no exercise)",
    "Lightly Active (1–3 days/week)",
    "Moderately Active (3–5 days/week)",
    "Very Active (6–7 days/week)",
    "Extra Active (physical job / twice daily)",
]

VALID_GENDERS = ["Male", "Female", "Prefer not to say"]


# ------------------------------------------------------------------
# Validation result helper
# ------------------------------------------------------------------

def _error(message: str) -> dict:
    return {"valid": False, "message": message}

def _ok() -> dict:
    return {"valid": True, "message": ""}


# ------------------------------------------------------------------
# Individual field validators
# ------------------------------------------------------------------

def validate_age(age) -> dict:
    try:
        age = int(age)
    except (TypeError, ValueError):
        return _error("Age must be a whole number.")
    if not (AGE_MIN <= age <= AGE_MAX):
        return _error(f"Age must be between {AGE_MIN} and {AGE_MAX}.")
    return _ok()


def validate_weight(weight) -> dict:
    try:
        weight = float(weight)
    except (TypeError, ValueError):
        return _error("Weight must be a number.")
    if not (WEIGHT_MIN <= weight <= WEIGHT_MAX):
        return _error(f"Weight must be between {WEIGHT_MIN} and {WEIGHT_MAX} kg.")
    return _ok()


def validate_height(height) -> dict:
    try:
        height = float(height)
    except (TypeError, ValueError):
        return _error("Height must be a number.")
    if not (HEIGHT_MIN <= height <= HEIGHT_MAX):
        return _error(f"Height must be between {HEIGHT_MIN} and {HEIGHT_MAX} cm.")
    return _ok()


def validate_goal(goal: str) -> dict:
    if goal not in VALID_GOALS:
        return _error(f"Goal must be one of: {', '.join(VALID_GOALS)}.")
    return _ok()


def validate_activity(activity: str) -> dict:
    if activity not in VALID_ACTIVITY_LEVELS:
        return _error("Please select a valid activity level.")
    return _ok()


# ------------------------------------------------------------------
# Full profile validator (used before running calculations)
# ------------------------------------------------------------------

def validate_profile(profile: dict) -> tuple[bool, list[str]]:
    """
    Validates a complete user profile dict.

    Returns
    -------
    (is_valid: bool, errors: list of error strings)
    """
    checks = [
        validate_age(profile.get("age")),
        validate_weight(profile.get("weight_kg")),
        validate_height(profile.get("height_cm")),
        validate_goal(profile.get("goal", "")),
        validate_activity(profile.get("activity_level", "")),
    ]

    errors = [c["message"] for c in checks if not c["valid"]]
    return (len(errors) == 0, errors)
