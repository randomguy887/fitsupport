"""
nutrition_engine.py
--------------------
This file does all the nutrition calculations for FitSupport.
It uses simple maths formulas from nutrition science research.
No complex logic — just functions that take numbers and return numbers.
"""

# We use 'dataclass' to create simple data containers (like a form)
from dataclasses import dataclass
from typing import Optional


# ── Step 1: Define what a "User Profile" looks like ──────────
# This is like a form — it stores everything the user types in

@dataclass
class UserProfile:
    age:            int           # e.g. 25
    weight_kg:      float         # e.g. 75.0
    height_cm:      float         # e.g. 175.0
    activity_level: str           # e.g. "moderate"
    fitness_goal:   str           # e.g. "muscle_gain"
    gender:         Optional[str] = None  # "male", "female", or None


# ── Step 2: Define what a "Nutrition Result" looks like ──────
# This stores all the calculated values we show to the user

@dataclass
class NutritionResult:
    bmr:               float   # Basal Metabolic Rate (calories at rest)
    tdee:              float   # Total Daily Energy Expenditure
    target_calories:   float   # Final calorie goal after adjustment
    protein_g:         float   # Protein in grams per day
    carbs_g:           float   # Carbohydrates in grams per day
    fat_g:             float   # Fat in grams per day
    water_ml:          float   # Water in millilitres per day
    bmi:               float   # Body Mass Index
    bmi_category:      str     # e.g. "Normal Weight"
    calorie_adjustment: float  # How many calories we added or removed
    goal_rationale:    str     # A sentence explaining the adjustment


# ── Step 3: Lookup tables (simple dictionaries) ───────────────
# These are used to multiply BMR by activity level

ACTIVITY_MULTIPLIERS = {
    "sedentary":   1.2,    # Desk job, no exercise
    "light":       1.375,  # Light exercise 1-3 days a week
    "moderate":    1.55,   # Moderate exercise 3-5 days a week
    "active":      1.725,  # Hard exercise 6-7 days a week
    "very_active": 1.9,    # Physical job or twice-a-day training
}

# Human-readable labels shown in the app dropdown
ACTIVITY_LABELS = {
    "sedentary":   "Sedentary (little/no exercise)",
    "light":       "Lightly Active (1-3 days/week)",
    "moderate":    "Moderately Active (3-5 days/week)",
    "active":      "Very Active (6-7 days/week)",
    "very_active": "Extra Active (physical job or 2x training)",
}

# How many calories to add or remove based on the user's goal
GOAL_ADJUSTMENTS = {
    "weight_loss":  -500,  # Remove 500 calories to lose ~0.5kg per week
    "muscle_gain":  +300,  # Add 300 calories to support muscle growth
    "maintenance":     0,  # No change — just maintain current weight
}

# Human-readable labels for fitness goals
GOAL_LABELS = {
    "weight_loss": "Weight Loss",
    "muscle_gain": "Muscle Gain",
    "maintenance": "Maintenance",
}

# How much protein per kg of bodyweight, depending on goal
PROTEIN_PER_KG = {
    "weight_loss": 2.0,  # Higher protein helps preserve muscle during a diet
    "muscle_gain": 2.2,  # Higher protein supports muscle building
    "maintenance": 1.6,  # Standard recommendation for active adults
}


# ── Step 4: The calculation functions ────────────────────────

def calculate_bmr(profile):
    """
    Calculates Basal Metabolic Rate using the Mifflin-St Jeor Equation (1990).
    BMR = the number of calories your body needs just to stay alive (at rest).

    Formula:
      Male   : (10 x weight) + (6.25 x height) - (5 x age) + 5
      Female : (10 x weight) + (6.25 x height) - (5 x age) - 161
      Unknown: average of both
    """
    # This part of the formula is the same for everyone
    base = (10 * profile.weight_kg) + (6.25 * profile.height_cm) - (5 * profile.age)

    if profile.gender == "male":
        bmr = base + 5
    elif profile.gender == "female":
        bmr = base - 161
    else:
        # If gender not provided, take the average of both
        bmr = (base + 5 + base - 161) / 2

    return round(bmr, 1)


def calculate_tdee(bmr, activity_level):
    """
    Calculates Total Daily Energy Expenditure.
    TDEE = BMR multiplied by an activity level number.
    This gives us how many calories the user burns in a full day.
    """
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
    tdee = bmr * multiplier
    return round(tdee, 1)


def calculate_target_calories(tdee, fitness_goal):
    """
    Adjusts the TDEE based on the user's fitness goal.
    Returns the target calories, the adjustment amount, and an explanation.
    """
    adjustment = GOAL_ADJUSTMENTS.get(fitness_goal, 0)
    target     = tdee + adjustment

    # Simple explanation sentences for each goal
    explanations = {
        "weight_loss": f"A daily deficit of 500 kcal has been applied to support gradual fat loss of approximately 0.5 kg per week.",
        "muscle_gain": f"A daily surplus of 300 kcal has been applied to support lean muscle growth without excessive fat gain.",
        "maintenance": f"No adjustment applied. Your target matches your daily energy expenditure to maintain your current weight.",
    }

    explanation = explanations.get(fitness_goal, "")
    return round(target, 1), adjustment, explanation


def calculate_macros(target_calories, fitness_goal, weight_kg):
    """
    Calculates daily protein, carbohydrate, and fat targets in grams.

    Rules:
      - Protein  : based on bodyweight (see PROTEIN_PER_KG above)
      - Fat      : 25% of total calories, converted to grams (1g fat = 9 kcal)
      - Carbs    : whatever calories are left, converted to grams (1g carb = 4 kcal)
    """
    protein_g = PROTEIN_PER_KG.get(fitness_goal, 1.6) * weight_kg

    fat_g = (target_calories * 0.25) / 9  # 25% of calories from fat

    # Remaining calories after protein and fat are accounted for
    remaining_calories = target_calories - (protein_g * 4) - (fat_g * 9)
    carbs_g = max(remaining_calories, 0) / 4  # Convert remaining to grams

    return round(protein_g, 1), round(carbs_g, 1), round(fat_g, 1)


def calculate_water(weight_kg, activity_level):
    """
    Calculates daily water intake in millilitres.
    Base formula: 35ml per kg of bodyweight.
    Extra water is added for more active people to account for sweat loss.
    """
    base_water = 35 * weight_kg

    # Extra water based on activity level
    activity_bonus = {
        "sedentary":   0,
        "light":       200,
        "moderate":    400,
        "active":      600,
        "very_active": 800,
    }

    bonus = activity_bonus.get(activity_level, 0)
    return round(base_water + bonus, 0)


def calculate_bmi(weight_kg, height_cm):
    """
    Calculates Body Mass Index.
    Formula: weight (kg) divided by height (metres) squared.
    Returns the BMI value and a category label.
    """
    height_m = height_cm / 100  # Convert cm to metres
    bmi      = weight_kg / (height_m ** 2)

    # WHO classification categories
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25.0:
        category = "Normal Weight"
    elif bmi < 30.0:
        category = "Overweight"
    else:
        category = "Obese"

    return round(bmi, 1), category


def run_nutrition_engine(profile):
    """
    Main function — runs all calculations in order and returns one result object.
    This is the only function called from app.py.
    """
    bmr = calculate_bmr(profile)
    tdee = calculate_tdee(bmr, profile.activity_level)
    target_calories, adjustment, explanation = calculate_target_calories(tdee, profile.fitness_goal)
    protein_g, carbs_g, fat_g = calculate_macros(target_calories, profile.fitness_goal, profile.weight_kg)
    water_ml = calculate_water(profile.weight_kg, profile.activity_level)
    bmi, bmi_category = calculate_bmi(profile.weight_kg, profile.height_cm)

    # Pack everything into the result container and return it
    return NutritionResult(
        bmr               = bmr,
        tdee              = tdee,
        target_calories   = target_calories,
        protein_g         = protein_g,
        carbs_g           = carbs_g,
        fat_g             = fat_g,
        water_ml          = water_ml,
        bmi               = bmi,
        bmi_category      = bmi_category,
        calorie_adjustment = adjustment,
        goal_rationale    = explanation,
    )
