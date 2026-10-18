"""
FitSupport – Test Suite: Supplement Engine
==========================================
Unit tests for supplement recommendation logic.

Run with:
    python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from core.supplement_engine import run_supplement_engine


class TestSupplementEngine:

    def test_muscle_gain_has_creatine(self):
        report = run_supplement_engine("muscle_gain", "moderate", "Normal Weight", 80.0)
        names = [s.name for s in report.primary + report.secondary + report.general]
        assert "Creatine Monohydrate" in names

    def test_weight_loss_has_whey(self):
        report = run_supplement_engine("weight_loss", "light", "Overweight", 90.0)
        names = [s.name for s in report.primary + report.secondary + report.general]
        assert "Whey Protein" in names

    def test_all_goals_have_vitamin_d(self):
        for goal in ["weight_loss", "muscle_gain", "maintenance"]:
            report = run_supplement_engine(goal, "sedentary", "Normal Weight", 70.0)
            names = [s.name for s in report.primary + report.secondary + report.general]
            assert "Vitamin D3" in names

    def test_creatine_not_for_sedentary(self):
        """Creatine requires at least moderate activity."""
        report = run_supplement_engine("muscle_gain", "sedentary", "Normal Weight", 80.0)
        names = [s.name for s in report.primary + report.secondary + report.general]
        assert "Creatine Monohydrate" not in names

    def test_disclaimer_present(self):
        report = run_supplement_engine("maintenance", "sedentary", "Normal Weight", 70.0)
        assert len(report.disclaimer) > 50

    def test_total_count_matches_lists(self):
        report = run_supplement_engine("muscle_gain", "active", "Normal Weight", 80.0)
        actual = len(report.primary) + len(report.secondary) + len(report.general)
        assert actual == report.total_count

    def test_goal_summary_non_empty(self):
        for goal in ["weight_loss", "muscle_gain", "maintenance"]:
            report = run_supplement_engine(goal, "moderate", "Normal Weight", 75.0)
            assert len(report.goal_summary) > 20
