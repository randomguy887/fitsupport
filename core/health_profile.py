"""
health_profile.py
------------------
This file stores lifestyle and health preference options for the user.
It also provides simple functions to get warnings and dietary exclusions.

IMPORTANT: This module does NOT diagnose or treat conditions.
Health inputs are ONLY used to display doctor advisory messages.
Supplement recommendations do NOT change based on health conditions.
"""

# Dropdown options for dietary preference
DIETARY_OPTIONS = {
    "none":         "No specific dietary requirements",
    "vegan":        "Vegan (no animal products)",
    "vegetarian":   "Vegetarian",
    "lactose_free": "Lactose Intolerant / Dairy-Free",
    "gluten_free":  "Gluten-Free",
    "halal":        "Halal certified products only",
}

# Dropdown options for budget range (in UAE Dirhams)
BUDGET_OPTIONS = {
    "low":    "Budget (under 100 AED per supplement)",
    "medium": "Mid-Range (100-250 AED per supplement)",
    "high":   "Premium (250+ AED per supplement)",
}

# Health conditions the user can select
# These are used ONLY to show warning messages — not to change recommendations
HEALTH_CONDITIONS = {
    "none":         "No known health conditions",
    "diabetes":     "Diabetes",
    "hypertension": "High Blood Pressure",
    "heart":        "Heart Condition",
    "kidney":       "Kidney Issues",
    "liver":        "Liver Issues",
    "thyroid":      "Thyroid Condition",
    "arthritis":    "Arthritis / Joint Issues",
    "osteoporosis": "Osteoporosis / Bone Issues",
    "anaemia":      "Anaemia / Iron Deficiency",
    "ibs":          "IBS / Digestive Issues",
    "anxiety":      "Anxiety / Mental Health",
    "pregnancy":    "Pregnant or Breastfeeding",
    "other":        "Other condition",
}

# Warning messages — one for each health condition
# These are shown in the Health Advisory tab
CONDITION_WARNINGS = {
    "diabetes":     "Diabetes: Some supplements may affect blood sugar levels. Please consult your doctor before use.",
    "hypertension": "High Blood Pressure: Caffeine and stimulants may raise blood pressure. Please consult your doctor.",
    "heart":        "Heart Condition: Stimulant supplements are not recommended. Please consult your cardiologist.",
    "kidney":       "Kidney Issues: High protein intake and creatine may not be suitable. Please consult your doctor.",
    "liver":        "Liver Issues: Some supplements are processed by the liver. Please consult your doctor first.",
    "thyroid":      "Thyroid Condition: Some supplements may interact with thyroid medication. Consult your doctor.",
    "arthritis":    "Arthritis: Omega-3 and Vitamin D may support joint health. Confirm with your doctor first.",
    "osteoporosis": "Bone Issues: Calcium and Vitamin D may help. Confirm the correct dosage with your doctor.",
    "anaemia":      "Anaemia: Iron supplements should only be taken under medical supervision.",
    "ibs":          "Digestive Issues: Some supplements may worsen symptoms. Please consult your doctor.",
    "anxiety":      "Anxiety: Caffeine and pre-workout stimulants can worsen anxiety. Speak to your doctor.",
    "pregnancy":    "Pregnant or Breastfeeding: Many supplements are NOT safe during pregnancy. See your doctor immediately.",
    "other":        "Existing Health Condition: Please consult your GP before taking any supplement.",
}

# Supplements to remove from recommendations based on dietary preference
DIETARY_EXCLUSIONS = {
    "vegan":        ["Whey Protein", "Omega-3 Fish Oil (EPA & DHA)"],
    "vegetarian":   ["Omega-3 Fish Oil (EPA & DHA)"],
    "lactose_free": ["Whey Protein"],
    "gluten_free":  [],   # No changes needed — most supplements are gluten-free
    "halal":        [],   # No changes — just advise to check the label
    "none":         [],   # No restrictions
}

# Notes shown when dietary preference removes a supplement
DIETARY_NOTES = {
    "vegan":        "Whey protein and fish oil have been removed as they contain animal products. Plant-based alternatives are shown instead.",
    "vegetarian":   "Fish oil has been removed. Consider an algae-based Omega-3 as a vegetarian alternative.",
    "lactose_free": "Whey protein has been removed. Try Whey Isolate or a plant-based protein instead.",
    "gluten_free":  "No supplements removed — but always check labels for gluten-free certification.",
    "halal":        "No supplements removed — look for Halal-certified labels when purchasing in UAE.",
    "none":         "",
}

# Conditions considered high risk — triggers a stronger warning in the app
HIGH_RISK_CONDITIONS = {"heart", "kidney", "liver", "pregnancy"}


def get_warnings(conditions):
    """
    Takes a list of selected health condition keys.
    Returns a list of warning message strings to display in the app.
    """
    warnings = []
    for condition in conditions:
        # Skip "none" and only add a warning if one exists
        if condition != "none" and condition in CONDITION_WARNINGS:
            warnings.append(CONDITION_WARNINGS[condition])
    return warnings


def get_exclusions(dietary_preference):
    """
    Takes a dietary preference key (e.g. "vegan").
    Returns two things:
      1. A list of supplement names to exclude from recommendations
      2. A note to display explaining what was removed and why
    """
    excluded = DIETARY_EXCLUSIONS.get(dietary_preference, [])
    note     = DIETARY_NOTES.get(dietary_preference, "")
    return excluded, note


def is_high_risk(conditions):
    """
    Takes a list of condition keys.
    Returns True if any of them are considered high-risk (heart, kidney, liver, pregnancy).
    Used to show a stronger red warning at the top of the app.
    """
    return bool(set(conditions) & HIGH_RISK_CONDITIONS)
