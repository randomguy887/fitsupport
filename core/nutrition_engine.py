"""
FitSupport – Nutrition Calculation Engine
==========================================
Handles all BMR, TDEE, macro, and hydration calculations.
All formulas are sourced from peer-reviewed literature and are
clearly documented for academic traceability.

References:
  - Mifflin-St Jeor Equation (1990) for BMR
  - Harris-Benedict Activity Multipliers
  - Dietary Reference Intakes (IOM, 2005) for protein/water
"""

from dataclasses import dataclass
from typing import Optional


# ──────────────────────────────────────────────
# Data Structures
# ──────────────────────────────────────────────

@dataclass
class UserProfile:
    """Stores the raw inputs collected from the user interface."""
    age: int
    weight_kg: float
    height_cm: float
    activity_level: str          # sedentary | light | moderate | active | very_active
    fitness_goal: str            # weight_loss | muscle_gain | maintenance
    gender: Optional[str] = None # male | female | prefer_not_to_say


@dataclass
class NutritionResult:
    """Holds all computed nutrition values returned to the UI."""
    bmr: float                   # Basal Metabolic Rate (kcal/day)
    tdee: float                  # Total Daily Energy Expenditure (kcal/day)
    target_calories: float       # Adjusted for goal (kcal/day)
    protein_g: float             # Daily protein target (grams)
    carbs_g: float               # Daily carbohydrate target (grams)
    fat_g: float                 # Daily fat target (grams)
    water_ml: float              # Daily water intake target (ml)
    bmi: float                   # Body Mass Index
    bmi_category: str            # Underweight / Normal / Overweight / Obese
    calorie_adjustment: float    # Surplus or deficit applied (kcal)
    goal_rationale: str          # Human-readable explanation of the adjustment


# ──────────────────────────────────────────────
# Activity Level Multipliers
# (Harris-Benedict revised multipliers)
# ──────────────────────────────────────────────

ACTIVITY_MULTIPLIERS: dict[str, float] = {
    "sedentary":   1.2,    # Little or no exercise
    "light":       1.375,  # Light exercise 1–3 days/week
    "moderate":    1.55,   # Moderate exercise 3–5 days/week
    "active":      1.725,  # Hard exercise 6–7 days/week
    "very_active": 1.9,    # Very hard exercise / physical job
}

ACTIVITY_LABELS: dict[str, str] = {
    "sedentary":   "Sedentary (little/no exercise)",
    "light":       "Lightly Active (1–3 days/week)",
    "moderate":    "Moderately Active (3–5 days/week)",
    "active":      "Very Active (6–7 days/week)",
    "very_active": "Extra Active (physical job or 2× training)",
}

# ──────────────────────────────────────────────
# Goal Calorie Adjustments
# ──────────────────────────────────────────────

GOAL_ADJUSTMENTS: dict[str, float] = {
    "weight_loss":  -500.0,   # ~0.5 kg/week deficit (safe range)
    "muscle_gain":  +300.0,   # Lean bulk surplus
    "maintenance":  0.0,
}

GOAL_LABELS: dict[str, str] = {
    "weight_loss": "Weight Loss",
    "muscle_gain": "Muscle Gain",
    "maintenance": "Maintenance",
}


# ──────────────────────────────────────────────
# Calculation Functions
# ──────────────────────────────────────────────

def calculate_bmr(profile: UserProfile) -> float:
    """
    Mifflin-St Jeor Equation (1990).
    Chosen over Harris-Benedict (1918) because it is more accurate
    for modern, sedentary populations (systematic review: Frankenfield 2005).

    Male   : BMR = (10 × weight_kg) + (6.25 × height_cm) − (5 × age) + 5
    Female : BMR = (10 × weight_kg) + (6.25 × height_cm) − (5 × age) − 161
    Unknown: Average of both equations used as a neutral estimate.
    """
    base = (10 * profile.weight_kg) + (6.25 * profile.height_cm) - (5 * profile.age)

    if profile.gender == "male":
        return round(base + 5, 2)
    elif profile.gender == "female":
        return round(base - 161, 2)
    else:
        # Use gender-neutral average when gender not provided
        male_bmr   = base + 5
        female_bmr = base - 161
        return round((male_bmr + female_bmr) / 2, 2)


def calculate_tdee(bmr: float, activity_level: str) -> float:
    """
    Total Daily Energy Expenditure = BMR × Activity Multiplier.
    Multipliers from the revised Harris-Benedict paper (Roza & Shizgal 1984).
    """
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
    return round(bmr * multiplier, 2)


def calculate_target_calories(tdee: float, fitness_goal: str) -> tuple[float, float, str]:
    """
    Applies a calorie adjustment on top of TDEE based on the user's goal.

    Returns:
        target_calories : adjusted daily calorie target
        adjustment      : the delta applied (positive = surplus, negative = deficit)
        rationale       : human-readable explanation string
    """
    adjustment = GOAL_ADJUSTMENTS.get(fitness_goal, 0.0)
    target     = round(tdee + adjustment, 2)

    rationales = {
        "weight_loss": (
            f"A daily deficit of {abs(adjustment):.0f} kcal has been applied. "
            "This is a moderate, evidence-based reduction that supports approximately "
            "0.5 kg of fat loss per week while preserving lean muscle mass."
        ),
        "muscle_gain": (
            f"A daily surplus of {adjustment:.0f} kcal has been applied. "
            "This conservative 'lean bulk' approach promotes muscle growth "
            "while minimising unnecessary fat accumulation."
        ),
        "maintenance": (
            "No calorie adjustment has been applied. "
            "Your target matches your estimated daily energy expenditure "
            "to support a stable body composition."
        ),
    }

    rationale = rationales.get(fitness_goal, "No adjustment applied.")
    return target, adjustment, rationale


def calculate_macros(
    target_calories: float,
    fitness_goal: str,
    weight_kg: float
) -> tuple[float, float, float]:
    """
    Calculates protein, carbohydrate, and fat targets in grams.

    Protein targets:
      Weight loss  : 2.0 g/kg  (high protein to preserve muscle during deficit)
      Muscle gain  : 2.2 g/kg  (supports muscle protein synthesis)
      Maintenance  : 1.6 g/kg  (general health recommendation, ACSM/ADA/DC 2016)

    Fat target    : ~25 % of total calories (consistent across goals)
    Carbohydrates : Remaining calories after protein and fat are allocated.

    Energy constants:
      Protein = 4 kcal/g  |  Carbohydrate = 4 kcal/g  |  Fat = 9 kcal/g
    """
    protein_per_kg = {
        "weight_loss": 2.0,
        "muscle_gain": 2.2,
        "maintenance": 1.6,
    }

    protein_g = round(protein_per_kg.get(fitness_goal, 1.6) * weight_kg, 1)
    fat_g     = round((target_calories * 0.25) / 9, 1)

    protein_kcal  = protein_g * 4
    fat_kcal      = fat_g * 9
    remaining_kcal = target_calories - protein_kcal - fat_kcal
    carbs_g        = round(max(remaining_kcal, 0) / 4, 1)

    return protein_g, carbs_g, fat_g


def calculate_water(weight_kg: float, activity_level: str) -> float:
    """
    Daily water recommendation.

    Base formula: 35 ml × body weight in kg (European Hydration Institute).
    Activity bonus applied for moderate-to-high activity levels.

    Returns value in millilitres (ml).
    """
    base_water = 35 * weight_kg

    activity_bonus = {
        "sedentary":   0,
        "light":       200,
        "moderate":    400,
        "active":      600,
        "very_active": 800,
    }

    bonus = activity_bonus.get(activity_level, 0)
    return round(base_water + bonus, 0)


def calculate_bmi(weight_kg: float, height_cm: float) -> tuple[float, str]:
    """
    Body Mass Index = weight (kg) / height (m)²

    WHO classification:
      < 18.5  : Underweight
      18.5–24.9: Normal weight
      25.0–29.9: Overweight
      ≥ 30.0  : Obese

    Note: BMI is a population-level screening tool and has limitations
    for individual assessment (e.g. does not account for muscle mass).
    """
    height_m = height_cm / 100
    bmi      = round(weight_kg / (height_m ** 2), 1)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25.0:
        category = "Normal Weight"
    elif bmi < 30.0:
        category = "Overweight"
    else:
        category = "Obese"

    return bmi, category


# ──────────────────────────────────────────────
# Main Entry Point
# ──────────────────────────────────────────────

def run_nutrition_engine(profile: UserProfile) -> NutritionResult:
    """
    Orchestrates all calculations in sequence and returns a
    fully populated NutritionResult dataclass.

    This is the single public interface used by app.py.
    """
    bmr = calculate_bmr(profile)
    tdee = calculate_tdee(bmr, profile.activity_level)
    target_calories, adjustment, rationale = calculate_target_calories(
        tdee, profile.fitness_goal
    )
    protein_g, carbs_g, fat_g = calculate_macros(
        target_calories, profile.fitness_goal, profile.weight_kg
    )
    water_ml = calculate_water(profile.weight_kg, profile.activity_level)
    bmi, bmi_category = calculate_bmi(profile.weight_kg, profile.height_cm)

    return NutritionResult(
        bmr=bmr,
        tdee=tdee,
        target_calories=target_calories,
        protein_g=protein_g,
        carbs_g=carbs_g,
        fat_g=fat_g,
        water_ml=water_ml,
        bmi=bmi,
        bmi_category=bmi_category,
        calorie_adjustment=adjustment,
        goal_rationale=rationale,
    )
