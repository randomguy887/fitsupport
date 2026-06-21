"""
supplement_engine.py
---------------------
This file contains the supplement recommendation logic.
It works by storing a list of supplements, each with rules about
who they are suitable for. It then filters the list based on the
user's goal and activity level.

Design: Rule-based filtering (no machine learning, no complex AI).
"""

from dataclasses import dataclass, field


# ── Step 1: Define what a Supplement looks like ──────────────

@dataclass
class Supplement:
    name:           str        # e.g. "Whey Protein"
    category:       str        # e.g. "Protein"
    priority:       str        # "Primary", "Secondary", or "General"
    description:    str        # What it is
    benefit:        str        # Why it is recommended
    dosage_guidance: str       # How much to take
    timing:         str        # When to take it
    evidence_level: str        # "Strong", "Moderate", or "Limited"
    cautions:       str        # Who should be careful or avoid it
    goals:          list = field(default_factory=list)  # Which goals it suits
    min_activity:   str  = "sedentary"                  # Minimum activity level needed


# ── Step 2: Define what a SupplementReport looks like ────────

@dataclass
class SupplementReport:
    primary:      list   # Most important supplements for the goal
    secondary:    list   # Useful but less essential
    general:      list   # Good for everyone
    goal_summary: str    # A sentence explaining the recommendations
    total_count:  int    # Total number of supplements recommended
    disclaimer:   str    # Legal/ethical disclaimer


# ── Step 3: The supplement database (a simple list) ──────────
# Each supplement has rules: which goals it suits, minimum activity level.
# The engine filters this list based on the user's profile.

ALL_SUPPLEMENTS = [

    Supplement(
        name           = "Whey Protein",
        category       = "Protein",
        priority       = "Primary",
        description    = "A fast-digesting complete protein from milk, containing all essential amino acids.",
        benefit        = "Helps meet daily protein targets to support muscle repair and growth after exercise.",
        dosage_guidance= "20-40g per serving, 1-2 times per day.",
        timing         = "Within 30-60 minutes after your workout.",
        evidence_level = "Strong",
        cautions       = "Avoid if lactose intolerant. Use isolate version or plant protein instead.",
        goals          = ["muscle_gain", "weight_loss"],
        min_activity   = "light",
    ),

    Supplement(
        name           = "Plant-Based Protein (Pea / Soy)",
        category       = "Protein",
        priority       = "Secondary",
        description    = "A dairy-free protein powder made from peas or soy beans.",
        benefit        = "Same muscle-building benefits as whey but suitable for vegans and lactose-intolerant users.",
        dosage_guidance= "20-40g per serving, as needed to reach daily protein target.",
        timing         = "After workouts or between meals.",
        evidence_level = "Moderate",
        cautions       = "Soy may interact with certain hormone medications. Check with your doctor.",
        goals          = ["muscle_gain", "weight_loss", "maintenance"],
        min_activity   = "light",
    ),

    Supplement(
        name           = "Creatine Monohydrate",
        category       = "Performance",
        priority       = "Primary",
        description    = "A natural compound found in meat and fish that helps muscles produce energy.",
        benefit        = "Increases strength and power output during resistance training, leading to more muscle over time.",
        dosage_guidance= "3-5g per day. No loading phase required.",
        timing         = "Any time of day. After workout is slightly better.",
        evidence_level = "Strong",
        cautions       = "May cause slight water retention. Not recommended if you have kidney issues.",
        goals          = ["muscle_gain"],
        min_activity   = "moderate",
    ),

    Supplement(
        name           = "Multivitamin & Mineral Complex",
        category       = "Micronutrients",
        priority       = "General",
        description    = "A tablet or capsule containing a range of essential vitamins and minerals.",
        benefit        = "Fills nutritional gaps in the diet, especially for active people with higher vitamin needs.",
        dosage_guidance= "1 tablet per day with food.",
        timing         = "Morning with breakfast.",
        evidence_level = "Moderate",
        cautions       = "Do not exceed the recommended dose. Not a substitute for eating well.",
        goals          = ["weight_loss", "muscle_gain", "maintenance"],
        min_activity   = "sedentary",
    ),

    Supplement(
        name           = "Omega-3 Fish Oil (EPA & DHA)",
        category       = "Recovery & Health",
        priority       = "General",
        description    = "Healthy fats from oily fish that reduce inflammation in the body.",
        benefit        = "Reduces muscle soreness after exercise and supports heart and joint health.",
        dosage_guidance= "1-3g of combined EPA and DHA per day.",
        timing         = "With a meal to improve absorption.",
        evidence_level = "Strong",
        cautions       = "Use algae-based omega-3 if vegan. High doses may thin the blood.",
        goals          = ["weight_loss", "muscle_gain", "maintenance"],
        min_activity   = "sedentary",
    ),

    Supplement(
        name           = "Vitamin D3",
        category       = "Micronutrients",
        priority       = "General",
        description    = "A vitamin produced by the body when skin is exposed to sunlight.",
        benefit        = "Supports bone strength, immune function, and muscle performance. Deficiency is very common.",
        dosage_guidance= "10-25 mcg (400-1000 IU) per day.",
        timing         = "With a meal containing fat.",
        evidence_level = "Strong",
        cautions       = "Do not take very high doses without a blood test and doctor advice.",
        goals          = ["weight_loss", "muscle_gain", "maintenance"],
        min_activity   = "sedentary",
    ),

    Supplement(
        name           = "Caffeine (Pre-Workout)",
        category       = "Performance",
        priority       = "Secondary",
        description    = "A stimulant that increases alertness and reduces feelings of tiredness.",
        benefit        = "Improves training performance, endurance, and focus. Also slightly raises metabolic rate.",
        dosage_guidance= "3-6mg per kg of bodyweight, 30-60 minutes before exercise.",
        timing         = "30-60 minutes before training. Avoid after 2pm to protect sleep.",
        evidence_level = "Strong",
        cautions       = "Can cause anxiety or raised heart rate. Avoid if sensitive to caffeine.",
        goals          = ["weight_loss", "muscle_gain"],
        min_activity   = "moderate",
    ),

    Supplement(
        name           = "BCAAs (Branched-Chain Amino Acids)",
        category       = "Recovery",
        priority       = "Secondary",
        description    = "Three amino acids (leucine, isoleucine, valine) that help with muscle repair.",
        benefit        = "Helps reduce muscle breakdown during intense training or when in a calorie deficit.",
        dosage_guidance= "5-10g per day.",
        timing         = "During or immediately after training.",
        evidence_level = "Moderate",
        cautions       = "Not very useful if your protein intake is already high. Prioritise food first.",
        goals          = ["muscle_gain", "weight_loss"],
        min_activity   = "moderate",
    ),

    Supplement(
        name           = "Magnesium (Glycinate or Citrate)",
        category       = "Recovery & Health",
        priority       = "Secondary",
        description    = "A mineral involved in over 300 body processes including muscle function and sleep.",
        benefit        = "Improves sleep quality, reduces muscle cramps, and supports recovery after training.",
        dosage_guidance= "200-400mg per day. Glycinate or citrate forms absorb best.",
        timing         = "30-60 minutes before bed.",
        evidence_level = "Moderate",
        cautions       = "High doses can cause loose stools. Start with a lower dose.",
        goals          = ["muscle_gain", "maintenance", "weight_loss"],
        min_activity   = "light",
    ),

    Supplement(
        name           = "Fibre Supplement (Psyllium Husk)",
        category       = "Digestive Health",
        priority       = "Secondary",
        description    = "A natural plant fibre that swells in the stomach and helps you feel full.",
        benefit        = "Reduces hunger during a calorie deficit, supports digestion and gut health.",
        dosage_guidance= "5-10g mixed in water, once per day.",
        timing         = "Before meals to reduce appetite.",
        evidence_level = "Moderate",
        cautions       = "Always drink plenty of water with it. Introduce gradually to avoid bloating.",
        goals          = ["weight_loss", "maintenance"],
        min_activity   = "sedentary",
    ),
]

# Activity levels in order from least to most active
ACTIVITY_ORDER = ["sedentary", "light", "moderate", "active", "very_active"]

DISCLAIMER = (
    "DISCLAIMER: All supplement information is strictly educational. "
    "It does NOT constitute medical advice, diagnosis, or treatment. "
    "Always consult a qualified healthcare professional before starting any supplement."
)

GOAL_SUMMARIES = {
    "weight_loss": "Recommendations focus on preserving muscle, reducing hunger, and supporting performance during a calorie deficit.",
    "muscle_gain": "Recommendations focus on maximising muscle protein synthesis and training performance.",
    "maintenance": "Recommendations focus on general health, recovery, and filling nutritional gaps.",
}


# ── Step 4: The recommendation function ──────────────────────

def run_supplement_engine(fitness_goal, activity_level, bmi_category, weight_kg):
    """
    Filters the supplement list based on the user's goal and activity level.
    Returns a SupplementReport with supplements sorted into three priority tiers.

    How it works:
    1. Loop through every supplement in ALL_SUPPLEMENTS
    2. Check if the user's goal is in the supplement's 'goals' list
    3. Check if the user is active enough for the supplement
    4. If both match, add it to the recommended list
    5. Split the list into Primary, Secondary, and General tiers
    """
    recommended = []

    for supplement in ALL_SUPPLEMENTS:
        # Check if this supplement matches the user's goal
        goal_matches = fitness_goal in supplement.goals

        # Check if the user meets the minimum activity level
        user_activity_index = ACTIVITY_ORDER.index(activity_level) if activity_level in ACTIVITY_ORDER else 0
        min_activity_index  = ACTIVITY_ORDER.index(supplement.min_activity) if supplement.min_activity in ACTIVITY_ORDER else 0
        activity_matches    = user_activity_index >= min_activity_index

        # Only add if both conditions are true
        if goal_matches and activity_matches:
            recommended.append(supplement)

    # Split into priority tiers
    primary   = [s for s in recommended if s.priority == "Primary"]
    secondary = [s for s in recommended if s.priority == "Secondary"]
    general   = [s for s in recommended if s.priority == "General"]

    return SupplementReport(
        primary      = primary,
        secondary    = secondary,
        general      = general,
        goal_summary = GOAL_SUMMARIES.get(fitness_goal, ""),
        total_count  = len(recommended),
        disclaimer   = DISCLAIMER,
    )
