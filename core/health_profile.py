"""
Health & Lifestyle Profile Module
-----------------------------------
This module stores the lifestyle and health options
that users can select in the app.

It also provides simple helper functions to:
- Get a warning message for any health condition selected
- Check which supplements to exclude based on diet type

IMPORTANT: This module does NOT diagnose or treat any condition.
Health condition inputs are only used to show a doctor referral message.
"""

# Dietary preference options shown in the app sidebar
DIETARY_OPTIONS = {
    "none":         "No specific dietary requirements",
    "vegan":        "Vegan (no animal products)",
    "vegetarian":   "Vegetarian",
    "lactose_free": "Lactose Intolerant / Dairy-Free",
    "gluten_free":  "Gluten-Free",
    "halal":        "Halal certified products only",
}

# Budget options for filtering UAE supplement prices
BUDGET_OPTIONS = {
    "low":    "Budget (under 100 AED per supplement)",
    "medium": "Mid-Range (100–250 AED)",
    "high":   "Premium (250+ AED)",
}

# Health conditions — used ONLY to show a doctor advisory message
# These do NOT change supplement recommendations
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

# Warning messages shown when a health condition is selected
CONDITION_WARNINGS = {
    "diabetes":     "Diabetes: Some supplements may affect blood sugar. Please consult your doctor before use.",
    "hypertension": "High Blood Pressure: Caffeine and stimulants may raise blood pressure. Please consult your doctor.",
    "heart":        "Heart Condition: Stimulant supplements are not recommended. Please consult your cardiologist.",
    "kidney":       "Kidney Issues: High protein and creatine may not be suitable. Please consult your doctor.",
    "liver":        "Liver Issues: Some supplements are processed by the liver. Please consult your doctor.",
    "thyroid":      "Thyroid Condition: Some supplements may interact with thyroid medication. Consult your doctor.",
    "arthritis":    "Arthritis: Omega-3 and Vitamin D may help joints, but confirm with your doctor first.",
    "osteoporosis": "Bone Issues: Calcium and Vitamin D may be beneficial. Confirm dosage with your doctor.",
    "anaemia":      "Anaemia: Iron supplements should only be taken under medical supervision.",
    "ibs":          "Digestive Issues: Fibre supplements may affect symptoms. Please consult your doctor.",
    "anxiety":      "Anxiety: Caffeine and stimulants can worsen anxiety. Please speak to your doctor.",
    "pregnancy":    "Pregnant / Breastfeeding: Many supplements are NOT safe during pregnancy. Consult your doctor immediately.",
    "other":        "Existing Health Condition: Please consult your GP before taking any supplement.",
}

# Supplements to exclude based on dietary preference
DIETARY_EXCLUSIONS = {
    "vegan":        ["Whey Protein", "Omega-3 Fish Oil (EPA & DHA)"],
    "vegetarian":   ["Omega-3 Fish Oil (EPA & DHA)"],
    "lactose_free": ["Whey Protein"],
    "gluten_free":  [],
    "halal":        [],
    "none":         [],
}

# Notes to show when a dietary preference affects recommendations
DIETARY_NOTES = {
    "vegan":        "Whey protein and fish oil excluded — they contain animal products. Plant-based alternatives shown instead.",
    "vegetarian":   "Fish oil excluded. Consider algae-based Omega-3 as a vegetarian alternative.",
    "lactose_free": "Whey protein excluded due to dairy content. Try Whey Isolate or a plant-based protein instead.",
    "gluten_free":  "No supplements removed — but always check labels for gluten-free certification.",
    "halal":        "No supplements removed — but look for Halal-certified labels when buying in UAE.",
    "none":         "",
}


def get_warnings(conditions):
    """
    Takes a list of selected health conditions.
    Returns a list of warning messages to display.
    """
    warnings = []
    for condition in conditions:
        if condition != "none" and condition in CONDITION_WARNINGS:
            warnings.append(CONDITION_WARNINGS[condition])
    return warnings


def get_exclusions(dietary_preference):
    """
    Takes a dietary preference string.
    Returns the list of supplements to exclude and a note to display.
    """
    excluded = DIETARY_EXCLUSIONS.get(dietary_preference, [])
    note = DIETARY_NOTES.get(dietary_preference, "")
    return excluded, note


def is_high_risk(conditions):
    """
    Returns True if any serious condition is selected.
    Used to show a stronger warning message in the app.
    """
    high_risk = {"heart", "kidney", "liver", "pregnancy"}
    return bool(set(conditions) & high_risk)