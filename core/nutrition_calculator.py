"""
FitSupport - Nutrition Calculator Module
=========================================
Handles all BMR, TDEE, macronutrient, and water calculations.
Formulas used are well-established in sports nutrition science.

Author: FitSupport Project
University: LJMU BSc Computer Science Top-Up
"""


# ------------------------------------------------------------------
# Activity level multipliers (Mifflin-St Jeor / Harris-Benedict scale)
# ------------------------------------------------------------------
ACTIVITY_MULTIPLIERS = {
    "Sedentary (little or no exercise)":        1.2,
    "Lightly Active (1–3 days/week)":           1.375,
    "Moderately Active (3–5 days/week)":        1.55,
    "Very Active (6–7 days/week)":              1.725,
    "Extra Active (physical job / twice daily)": 1.9,
}

# Goal-based calorie adjustments (relative to TDEE)
GOAL_CALORIE_ADJUSTMENTS = {
    "Weight Loss":   -500,   # 0.5 kg/week deficit
    "Muscle Gain":   +300,   # Lean bulk surplus
    "Maintenance":      0,   # No adjustment
}

# Protein targets (g per kg of body weight) by goal
PROTEIN_TARGETS = {
    "Weight Loss":  1.8,   # Higher protein preserves muscle during deficit
    "Muscle Gain":  2.2,   # Elevated for hypertrophy
    "Maintenance":  1.6,   # General fitness
}

# Fat targets (g per kg of body weight) – moderate across goals
FAT_TARGET_PER_KG = 1.0

# Water recommendation (ml per kg of body weight per day)
WATER_ML_PER_KG = 35


class NutritionCalculator:
    """
    Calculates personalised nutrition targets from a user profile.

    All calculations are deterministic and rule-based – no ML required.
    The Mifflin-St Jeor equation is used for BMR as it is widely
    regarded as the most accurate for general populations.
    """

    def __init__(self, age: int, gender: str, weight_kg: float,
                 height_cm: float, activity_level: str, goal: str):
        self.age = age
        self.gender = gender
        self.weight_kg = weight_kg
        self.height_cm = height_cm
        self.activity_level = activity_level
        self.goal = goal

    # ------------------------------------------------------------------
    # BMR  (Mifflin-St Jeor, 1990)
    # ------------------------------------------------------------------
    def calculate_bmr(self) -> float:
        """
        Returns Basal Metabolic Rate in kcal/day.

        Formula:
            Male:   (10 × weight_kg) + (6.25 × height_cm) − (5 × age) + 5
            Female: (10 × weight_kg) + (6.25 × height_cm) − (5 × age) − 161
            Other:  average of male and female values
        """
        base = (10 * self.weight_kg) + (6.25 * self.height_cm) - (5 * self.age)
        if self.gender == "Male":
            return round(base + 5, 1)
        elif self.gender == "Female":
            return round(base - 161, 1)
        else:
            # Gender not specified → use average
            return round(base - 78, 1)

    # ------------------------------------------------------------------
    # TDEE  (Total Daily Energy Expenditure)
    # ------------------------------------------------------------------
    def calculate_tdee(self) -> float:
        """
        TDEE = BMR × activity multiplier.
        Returns kcal/day before goal adjustment.
        """
        multiplier = ACTIVITY_MULTIPLIERS.get(self.activity_level, 1.2)
        return round(self.calculate_bmr() * multiplier, 1)

    # ------------------------------------------------------------------
    # Daily calorie target (goal-adjusted)
    # ------------------------------------------------------------------
    def calculate_daily_calories(self) -> float:
        """
        Adjusts TDEE by the goal-based calorie offset.
        Enforces a minimum of 1200 kcal/day for safety.
        """
        tdee = self.calculate_tdee()
        adjustment = GOAL_CALORIE_ADJUSTMENTS.get(self.goal, 0)
        target = tdee + adjustment
        return round(max(target, 1200), 1)   # 1200 kcal safety floor

    # ------------------------------------------------------------------
    # Macronutrient targets
    # ------------------------------------------------------------------
    def calculate_macros(self) -> dict:
        """
        Returns a dict with protein, fat, and carbohydrate targets in grams.

        Logic:
          1. Protein = goal-specific g/kg × weight
          2. Fat     = 1 g/kg × weight
          3. Carbs   = remaining calories ÷ 4  (carbs = 4 kcal/g)
        """
        daily_cals = self.calculate_daily_calories()

        protein_g = round(PROTEIN_TARGETS[self.goal] * self.weight_kg, 1)
        fat_g     = round(FAT_TARGET_PER_KG * self.weight_kg, 1)

        protein_cals = protein_g * 4
        fat_cals     = fat_g * 9
        carb_cals    = max(daily_cals - protein_cals - fat_cals, 0)
        carb_g       = round(carb_cals / 4, 1)

        return {
            "protein_g": protein_g,
            "fat_g":     fat_g,
            "carb_g":    carb_g,
        }

    # ------------------------------------------------------------------
    # Water recommendation
    # ------------------------------------------------------------------
    def calculate_water(self) -> float:
        """
        Returns recommended daily water intake in litres.
        Formula: 35 ml × body weight (kg)
        """
        ml = WATER_ML_PER_KG * self.weight_kg
        return round(ml / 1000, 2)

    # ------------------------------------------------------------------
    # BMI (informational only – not used for recommendations)
    # ------------------------------------------------------------------
    def calculate_bmi(self) -> float:
        """
        BMI = weight (kg) / height (m)²
        Displayed for information; not used in recommendation logic.
        """
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m ** 2), 1)

    # ------------------------------------------------------------------
    # Full results bundle
    # ------------------------------------------------------------------
    def get_all_results(self) -> dict:
        """Returns all calculated values as a single dictionary."""
        macros = self.calculate_macros()
        return {
            "bmr":             self.calculate_bmr(),
            "tdee":            self.calculate_tdee(),
            "daily_calories":  self.calculate_daily_calories(),
            "protein_g":       macros["protein_g"],
            "fat_g":           macros["fat_g"],
            "carb_g":          macros["carb_g"],
            "water_litres":    self.calculate_water(),
            "bmi":             self.calculate_bmi(),
            "goal":            self.goal,
            "activity_level":  self.activity_level,
        }
