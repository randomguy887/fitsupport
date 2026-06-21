"""
FitSupport – Test Suite: Nutrition Engine
==========================================
Unit tests for all calculation functions in nutrition_engine.py.

Testing approach: Black-box & White-box unit testing
  - Each function is tested with multiple valid inputs
  - Edge cases are included (min/max values, gender variants)
  - All expected values are manually pre-calculated for verification

Run with:
    python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from core.nutrition_engine import (
    UserProfile,
    calculate_bmr,
    calculate_tdee,
    calculate_target_calories,
    calculate_macros,
    calculate_water,
    calculate_bmi,
    run_nutrition_engine,
)


# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def male_profile():
    return UserProfile(
        age=25, weight_kg=80.0, height_cm=180.0,
        activity_level="moderate", fitness_goal="muscle_gain", gender="male"
    )

@pytest.fixture
def female_profile():
    return UserProfile(
        age=30, weight_kg=65.0, height_cm=165.0,
        activity_level="light", fitness_goal="weight_loss", gender="female"
    )

@pytest.fixture
def neutral_profile():
    return UserProfile(
        age=40, weight_kg=90.0, height_cm=175.0,
        activity_level="sedentary", fitness_goal="maintenance", gender=None
    )


# ──────────────────────────────────────────────
# BMR Tests
# ──────────────────────────────────────────────

class TestBMR:

    def test_male_bmr(self, male_profile):
        """
        Manual: (10×80) + (6.25×180) − (5×25) + 5
              = 800 + 1125 − 125 + 5 = 1805.0
        """
        bmr = calculate_bmr(male_profile)
        assert bmr == pytest.approx(1805.0, abs=0.5)

    def test_female_bmr(self, female_profile):
        """
        Manual: (10×65) + (6.25×165) − (5×30) − 161
              = 650 + 1031.25 − 150 − 161 = 1370.25
        """
        bmr = calculate_bmr(female_profile)
        assert bmr == pytest.approx(1370.25, abs=0.5)

    def test_neutral_gender_bmr_is_average(self, neutral_profile):
        """Gender-neutral BMR should equal the average of male and female equations."""
        p_male   = UserProfile(**{**neutral_profile.__dict__, "gender": "male"})
        p_female = UserProfile(**{**neutral_profile.__dict__, "gender": "female"})
        expected = (calculate_bmr(p_male) + calculate_bmr(p_female)) / 2
        assert calculate_bmr(neutral_profile) == pytest.approx(expected, abs=0.5)

    def test_bmr_increases_with_weight(self):
        """BMR should increase as weight increases (all else equal)."""
        p_light = UserProfile(age=25, weight_kg=60.0, height_cm=175.0,
                              activity_level="moderate", fitness_goal="maintenance", gender="male")
        p_heavy = UserProfile(age=25, weight_kg=100.0, height_cm=175.0,
                              activity_level="moderate", fitness_goal="maintenance", gender="male")
        assert calculate_bmr(p_heavy) > calculate_bmr(p_light)

    def test_bmr_decreases_with_age(self):
        """BMR should decrease as age increases (all else equal)."""
        p_young = UserProfile(age=20, weight_kg=75.0, height_cm=175.0,
                              activity_level="moderate", fitness_goal="maintenance", gender="female")
        p_old   = UserProfile(age=60, weight_kg=75.0, height_cm=175.0,
                              activity_level="moderate", fitness_goal="maintenance", gender="female")
        assert calculate_bmr(p_young) > calculate_bmr(p_old)

    def test_bmr_always_positive(self, male_profile, female_profile, neutral_profile):
        for p in [male_profile, female_profile, neutral_profile]:
            assert calculate_bmr(p) > 0


# ──────────────────────────────────────────────
# TDEE Tests
# ──────────────────────────────────────────────

class TestTDEE:

    def test_sedentary_multiplier(self):
        """TDEE = BMR × 1.2 for sedentary."""
        bmr  = 1800.0
        tdee = calculate_tdee(bmr, "sedentary")
        assert tdee == pytest.approx(1800 * 1.2, abs=0.5)

    def test_moderate_multiplier(self):
        bmr  = 1800.0
        tdee = calculate_tdee(bmr, "moderate")
        assert tdee == pytest.approx(1800 * 1.55, abs=0.5)

    def test_very_active_multiplier(self):
        bmr  = 1800.0
        tdee = calculate_tdee(bmr, "very_active")
        assert tdee == pytest.approx(1800 * 1.9, abs=0.5)

    def test_tdee_always_greater_than_bmr(self):
        bmr = 1500.0
        for level in ["sedentary", "light", "moderate", "active", "very_active"]:
            assert calculate_tdee(bmr, level) >= bmr

    def test_higher_activity_yields_higher_tdee(self):
        bmr = 1600.0
        assert (calculate_tdee(bmr, "sedentary") <
                calculate_tdee(bmr, "light") <
                calculate_tdee(bmr, "moderate") <
                calculate_tdee(bmr, "active") <
                calculate_tdee(bmr, "very_active"))


# ──────────────────────────────────────────────
# Target Calorie Tests
# ──────────────────────────────────────────────

class TestTargetCalories:

    def test_weight_loss_deficit(self):
        target, adj, _ = calculate_target_calories(2000.0, "weight_loss")
        assert adj == -500.0
        assert target == pytest.approx(1500.0, abs=0.1)

    def test_muscle_gain_surplus(self):
        target, adj, _ = calculate_target_calories(2000.0, "muscle_gain")
        assert adj == 300.0
        assert target == pytest.approx(2300.0, abs=0.1)

    def test_maintenance_no_adjustment(self):
        target, adj, _ = calculate_target_calories(2000.0, "maintenance")
        assert adj == 0.0
        assert target == pytest.approx(2000.0, abs=0.1)

    def test_rationale_is_non_empty(self):
        for goal in ["weight_loss", "muscle_gain", "maintenance"]:
            _, _, rationale = calculate_target_calories(2000.0, goal)
            assert isinstance(rationale, str)
            assert len(rationale) > 20


# ──────────────────────────────────────────────
# Macro Tests
# ──────────────────────────────────────────────

class TestMacros:

    def test_muscle_gain_protein_is_2_2_per_kg(self):
        protein_g, _, _ = calculate_macros(2500.0, "muscle_gain", 80.0)
        assert protein_g == pytest.approx(2.2 * 80, abs=0.5)

    def test_weight_loss_protein_is_2_per_kg(self):
        protein_g, _, _ = calculate_macros(1800.0, "weight_loss", 70.0)
        assert protein_g == pytest.approx(2.0 * 70, abs=0.5)

    def test_maintenance_protein_is_1_6_per_kg(self):
        protein_g, _, _ = calculate_macros(2000.0, "maintenance", 75.0)
        assert protein_g == pytest.approx(1.6 * 75, abs=0.5)

    def test_fat_is_25_percent_of_calories(self):
        target = 2000.0
        _, _, fat_g = calculate_macros(target, "maintenance", 75.0)
        assert fat_g == pytest.approx((target * 0.25) / 9, abs=0.5)

    def test_calories_roughly_balance(self):
        """Protein + Carb + Fat calories should ≈ target calories (within small rounding error)."""
        target = 2200.0
        p, c, f = calculate_macros(target, "muscle_gain", 80.0)
        total = (p * 4) + (c * 4) + (f * 9)
        assert abs(total - target) < 20  # Allow small rounding margin

    def test_carbs_never_negative(self):
        """Even with very high protein targets, carbs should not go negative."""
        _, carbs, _ = calculate_macros(1200.0, "muscle_gain", 100.0)
        assert carbs >= 0


# ──────────────────────────────────────────────
# Water Tests
# ──────────────────────────────────────────────

class TestWater:

    def test_base_water_formula(self):
        """Base = 35 ml × weight. Sedentary has no bonus."""
        water = calculate_water(70.0, "sedentary")
        assert water == pytest.approx(35 * 70, abs=1)

    def test_activity_bonus_increases_water(self):
        w_sed = calculate_water(70.0, "sedentary")
        w_act = calculate_water(70.0, "active")
        assert w_act > w_sed

    def test_water_never_zero(self):
        assert calculate_water(30.0, "sedentary") > 0


# ──────────────────────────────────────────────
# BMI Tests
# ──────────────────────────────────────────────

class TestBMI:

    def test_normal_bmi(self):
        bmi, cat = calculate_bmi(70.0, 175.0)
        assert bmi == pytest.approx(22.9, abs=0.2)
        assert cat == "Normal Weight"

    def test_underweight(self):
        _, cat = calculate_bmi(45.0, 175.0)
        assert cat == "Underweight"

    def test_overweight(self):
        _, cat = calculate_bmi(85.0, 175.0)
        assert cat == "Overweight"

    def test_obese(self):
        _, cat = calculate_bmi(110.0, 175.0)
        assert cat == "Obese"

    def test_bmi_formula(self):
        """BMI = weight / height_m²"""
        weight = 75.0
        height = 180.0
        bmi, _ = calculate_bmi(weight, height)
        expected = weight / ((height / 100) ** 2)
        assert bmi == pytest.approx(expected, abs=0.1)


# ──────────────────────────────────────────────
# Integration Test
# ──────────────────────────────────────────────

class TestIntegration:

    def test_full_pipeline_returns_result(self, male_profile):
        result = run_nutrition_engine(male_profile)
        assert result.bmr > 0
        assert result.tdee > result.bmr
        assert result.target_calories > 0
        assert result.protein_g > 0
        assert result.carbs_g >= 0
        assert result.fat_g > 0
        assert result.water_ml > 0
        assert result.bmi > 0
        assert result.bmi_category in ["Underweight", "Normal Weight", "Overweight", "Obese"]

    def test_muscle_gain_target_above_tdee(self, male_profile):
        result = run_nutrition_engine(male_profile)
        assert result.target_calories > result.tdee

    def test_weight_loss_target_below_tdee(self, female_profile):
        result = run_nutrition_engine(female_profile)
        assert result.target_calories < result.tdee

    def test_maintenance_target_equals_tdee(self, neutral_profile):
        result = run_nutrition_engine(neutral_profile)
        assert result.target_calories == pytest.approx(result.tdee, abs=0.1)
