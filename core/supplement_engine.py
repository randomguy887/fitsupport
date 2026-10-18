"""
FitSupport – Supplement Recommendation Engine
==============================================
Applies rule-based logic to recommend supplements appropriate to
the user's fitness goal, activity level, and BMI category.

IMPORTANT DISCLAIMER
--------------------
All supplement information provided by this module is strictly
EDUCATIONAL and INFORMATIONAL. It does NOT constitute medical advice,
diagnosis, or treatment. Users should consult a qualified healthcare
professional before beginning any supplementation programme.

Design Pattern: Rule-based decision engine
  - Each supplement has defined eligibility criteria
  - Goals and activity levels are used as logical filters
  - Priority tiers (Primary / Secondary / General) structure output
"""

from dataclasses import dataclass, field
from typing import Optional


# ──────────────────────────────────────────────
# Data Structures
# ──────────────────────────────────────────────

@dataclass
class Supplement:
    """Represents a single supplement recommendation with full context."""
    name: str
    category: str
    priority: str            # Primary | Secondary | General
    description: str
    benefit: str
    dosage_guidance: str
    timing: str
    evidence_level: str      # Strong / Moderate / Limited
    cautions: str
    goals: list = field(default_factory=list)
    min_activity: str = "sedentary"


@dataclass
class SupplementReport:
    """Returned to app.py with the full recommendation set."""
    primary: list
    secondary: list
    general: list
    goal_summary: str
    total_count: int
    disclaimer: str


# ──────────────────────────────────────────────
# Supplement Database
# ──────────────────────────────────────────────

SUPPLEMENT_DATABASE = [

    Supplement(
        name="Whey Protein",
        category="Protein",
        priority="Primary",
        description=(
            "A fast-digesting complete protein derived from milk, rich in all "
            "essential amino acids (EAAs) including branched-chain amino acids (BCAAs)."
        ),
        benefit=(
            "Supports muscle protein synthesis (MPS) post-exercise. "
            "Particularly effective for increasing daily protein intake when whole-food "
            "sources are insufficient. Meta-analyses consistently show significant lean "
            "mass gains when combined with resistance training (Morton et al., 2018)."
        ),
        dosage_guidance="20–40 g per serving, 1–2 servings per day.",
        timing="Within 30–60 minutes post-workout, or between meals to hit daily protein targets.",
        evidence_level="Strong",
        cautions=(
            "Avoid if lactose intolerant (use isolate or plant-based alternatives). "
            "Not required if dietary protein is already sufficient."
        ),
        goals=["muscle_gain", "weight_loss"],
        min_activity="light",
    ),

    Supplement(
        name="Plant-Based Protein (Pea / Soy)",
        category="Protein",
        priority="Secondary",
        description="A dairy-free complete protein alternative derived from peas or soy.",
        benefit=(
            "Provides EAAs for muscle repair and growth. Pea protein shows comparable "
            "muscle gains to whey when matched for protein content (Babault et al., 2015)."
        ),
        dosage_guidance="20–40 g per serving, as needed to meet daily protein targets.",
        timing="Post-workout or between meals.",
        evidence_level="Moderate",
        cautions="Soy may interact with certain hormone medications. Consult a doctor if concerned.",
        goals=["muscle_gain", "weight_loss", "maintenance"],
        min_activity="light",
    ),

    Supplement(
        name="Creatine Monohydrate",
        category="Performance",
        priority="Primary",
        description=(
            "The most studied performance supplement in sports nutrition. "
            "Increases phosphocreatine stores in muscle, enhancing ATP regeneration "
            "during high-intensity activity."
        ),
        benefit=(
            "Improves strength, power output, and training volume. "
            "The ISSN (2017) concludes creatine monohydrate is the single most "
            "effective ergogenic supplement for increasing high-intensity exercise "
            "capacity and lean body mass."
        ),
        dosage_guidance="3–5 g per day. Optional loading phase: 20 g/day for 5–7 days.",
        timing="Any time of day; post-workout with carbohydrates may enhance uptake.",
        evidence_level="Strong",
        cautions=(
            "Generally safe for healthy adults. May cause temporary water retention. "
            "Those with pre-existing kidney conditions should consult a healthcare professional."
        ),
        goals=["muscle_gain"],
        min_activity="moderate",
    ),

    Supplement(
        name="Multivitamin & Mineral Complex",
        category="Micronutrients",
        priority="General",
        description=(
            "A broad-spectrum supplement providing essential vitamins (A, B-complex, "
            "C, D, E, K) and minerals (zinc, magnesium, selenium)."
        ),
        benefit=(
            "Active individuals have higher micronutrient turnover. Deficiencies in "
            "vitamins D, B12, and iron are common in UK adults (NHS, 2021) and can "
            "impair energy metabolism, immunity, and recovery."
        ),
        dosage_guidance="1 tablet/capsule per day with food.",
        timing="Morning, with breakfast.",
        evidence_level="Moderate",
        cautions=(
            "Not a substitute for a balanced diet. Fat-soluble vitamins (A, D, E, K) "
            "can accumulate to toxic levels — do not exceed recommended doses."
        ),
        goals=["weight_loss", "muscle_gain", "maintenance"],
        min_activity="sedentary",
    ),

    Supplement(
        name="Omega-3 Fish Oil (EPA & DHA)",
        category="Recovery & Health",
        priority="General",
        description="Polyunsaturated fatty acids from oily fish. EPA and DHA are the two active forms.",
        benefit=(
            "Reduces exercise-induced muscle soreness and inflammation, supporting "
            "faster recovery. Also associated with cardiovascular health, joint mobility, "
            "and cognitive function (Smith et al., 2011)."
        ),
        dosage_guidance="1–3 g combined EPA + DHA per day.",
        timing="With meals to improve absorption and reduce fishy aftertaste.",
        evidence_level="Strong",
        cautions=(
            "High doses (>3 g/day) may have blood-thinning effects. "
            "Use algae-based omega-3 for vegan options."
        ),
        goals=["weight_loss", "muscle_gain", "maintenance"],
        min_activity="sedentary",
    ),

    Supplement(
        name="Vitamin D3",
        category="Micronutrients",
        priority="General",
        description=(
            "A fat-soluble vitamin widely deficient in populations with limited sunlight."
        ),
        benefit=(
            "Critical for calcium absorption, bone density, immune function, and "
            "muscle performance. NHS recommends supplementation during autumn and winter "
            "for all UK adults."
        ),
        dosage_guidance="10–25 mcg (400–1000 IU) per day.",
        timing="With a meal containing fat to improve absorption.",
        evidence_level="Strong",
        cautions="Excessive supplementation (>100 mcg/day) can cause hypercalcaemia.",
        goals=["weight_loss", "muscle_gain", "maintenance"],
        min_activity="sedentary",
    ),

    Supplement(
        name="Caffeine (Pre-Workout)",
        category="Performance",
        priority="Secondary",
        description="A central nervous system stimulant common in pre-workout formulas.",
        benefit=(
            "Significantly improves endurance, strength, power, and perceived exertion "
            "during exercise (Grgic et al., 2019). Also temporarily increases metabolic "
            "rate by 3–11%, supporting fat oxidation during weight loss phases."
        ),
        dosage_guidance="3–6 mg per kg body weight, 30–60 minutes before exercise.",
        timing="30–60 minutes pre-workout. Avoid within 6 hours of bedtime.",
        evidence_level="Strong",
        cautions=(
            "May cause anxiety, elevated heart rate, or insomnia at high doses. "
            "Not recommended for those with cardiovascular conditions or caffeine sensitivity."
        ),
        goals=["weight_loss", "muscle_gain"],
        min_activity="moderate",
    ),

    Supplement(
        name="BCAAs (Branched-Chain Amino Acids)",
        category="Recovery",
        priority="Secondary",
        description="Leucine, isoleucine, and valine — three essential amino acids for muscle protein synthesis.",
        benefit=(
            "Useful for reducing muscle soreness and preventing muscle breakdown "
            "during calorie-restricted training."
        ),
        dosage_guidance="5–10 g per day, typically a 2:1:1 leucine:isoleucine:valine ratio.",
        timing="During or immediately after training.",
        evidence_level="Moderate",
        cautions="Largely redundant if total protein intake is already adequate (≥1.6 g/kg/day).",
        goals=["muscle_gain", "weight_loss"],
        min_activity="moderate",
    ),

    Supplement(
        name="Magnesium (Glycinate or Citrate)",
        category="Recovery & Health",
        priority="Secondary",
        description="An essential mineral involved in energy production, muscle contraction, and protein synthesis.",
        benefit=(
            "Athletes frequently have lower magnesium levels due to sweat losses. "
            "Supplementation supports sleep quality, muscle recovery, and reduces cramps (Volpe, 2013)."
        ),
        dosage_guidance="200–400 mg per day (glycinate or citrate preferred for absorption).",
        timing="Evening, 30–60 minutes before sleep.",
        evidence_level="Moderate",
        cautions="Excessive intake can cause digestive upset. Citrate form has a mild laxative effect.",
        goals=["muscle_gain", "maintenance", "weight_loss"],
        min_activity="light",
    ),

    Supplement(
        name="Fibre Supplement (Psyllium Husk)",
        category="Digestive Health",
        priority="Secondary",
        description="A soluble fibre that forms a gel in the digestive tract, increasing satiety.",
        benefit=(
            "Increases satiety and reduces calorie intake in weight loss phases. "
            "Also supports gut health, cholesterol regulation, and blood sugar stability (Anderson et al., 2009)."
        ),
        dosage_guidance="5–10 g per day mixed in water or a shake.",
        timing="Before meals to promote fullness.",
        evidence_level="Moderate",
        cautions=(
            "Always take with plenty of water. Introduce gradually to avoid bloating. "
            "May slow absorption of some medications."
        ),
        goals=["weight_loss", "maintenance"],
        min_activity="sedentary",
    ),
]

ACTIVITY_ORDER = ["sedentary", "light", "moderate", "active", "very_active"]


def _meets_activity_threshold(user_level: str, min_level: str) -> bool:
    try:
        return ACTIVITY_ORDER.index(user_level) >= ACTIVITY_ORDER.index(min_level)
    except ValueError:
        return True


def run_supplement_engine(
    fitness_goal: str,
    activity_level: str,
    bmi_category: str,
    weight_kg: float,
) -> SupplementReport:
    """
    Filters the supplement database against the user's profile and
    returns a tiered SupplementReport.
    """
    eligible = []

    for s in SUPPLEMENT_DATABASE:
        goal_match     = fitness_goal in s.goals
        activity_match = _meets_activity_threshold(activity_level, s.min_activity)
        if goal_match and activity_match:
            eligible.append(s)

    primary   = [s for s in eligible if s.priority == "Primary"]
    secondary = [s for s in eligible if s.priority == "Secondary"]
    general   = [s for s in eligible if s.priority == "General"]

    goal_summaries = {
        "weight_loss": (
            "Your recommendations prioritise supplements that support fat metabolism, "
            "preserve lean muscle during a calorie deficit, and enhance workout performance. "
            "Protein and omega-3 are the most evidence-backed choices here."
        ),
        "muscle_gain": (
            "Your recommendations focus on maximising muscle protein synthesis and "
            "training performance. Whey protein and creatine monohydrate have the "
            "strongest scientific support for this goal."
        ),
        "maintenance": (
            "Your recommendations focus on general health, recovery, and micronutrient "
            "adequacy. The priority is long-term wellbeing rather than performance optimisation."
        ),
    }

    disclaimer = (
        "DISCLAIMER: All supplement information provided by FitSupport is strictly "
        "educational and informational. These recommendations do NOT constitute medical "
        "advice, diagnosis, or treatment. Always consult a qualified healthcare professional "
        "or registered dietitian before starting any supplementation programme."
    )

    return SupplementReport(
        primary=primary,
        secondary=secondary,
        general=general,
        goal_summary=goal_summaries.get(fitness_goal, ""),
        total_count=len(eligible),
        disclaimer=disclaimer,
    )
