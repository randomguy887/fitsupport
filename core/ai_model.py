"""
ai_model.py
------------
This file contains the AI/Machine Learning component of FitSupport.

Model Used: Decision Tree Classifier
Library   : scikit-learn

Why have i used/ implemented a Decision Tree over?
- because it is the most explainable ML model — you can trace every decision
- because it works like a flowchart: "If BMI > 25 AND age > 30 THEN..."
- because there are no black boxes — so every prediction can be explained in plain English
- because it is perfect for a health guidance system where transparency and honesty matters alot

What does it do?
- it will take the user's age, weight, height, activity level, and BMI
-  it will predict which "fitness profile cluster" the user belongs to
-  it will give personalised AI-generated advice based on that cluster
-  it will also show a confidence score for the prediction

Training Data:
- The model is trained on synthetic (very made up but realistic) user data
- This is acceptable for academic projects as real user data would require ethical approval and data collection
- The patterns in the data reflect real nutritional science guidelines

Reference:
- Breiman et al. (1984) - Classification and Regression Trees
- Scikit-learn documentation: Decision Tree Classifier
"""

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from dataclasses import dataclass

from core.supplement_engine import SupplementReport


#  Step 1: this step will basically define what the AI result looks like 

@dataclass
class AIResult:
    predicted_profile:  str    # The predicted fitness profile name
    confidence:         float  # How confident the model is (0-100%)
    advice:             str    # Personalised advice for this profile
    feature_importance: dict   # Which inputs mattered most
    model_explanation:  str    # Plain English explanation of the prediction


#  Step 2: this step will basically define the fitness profile categories

FITNESS_PROFILES = {
    0: "Beginner — Building Foundation",
    1: "Active — Maintaining Progress",
    2: "Athlete — Performance Focused",
    3: "Weight Management — Cutting Phase",
    4: "Senior Active — Health Focused",
}

PROFILE_ADVICE = {
    0: (
        "As someone building their fitness foundation, focus on consistency "
        "over intensity. Your nutrition targets are set to support gradual "
        "progress. Prioritise protein intake and stay hydrated. "
        "Start with basic supplements like a multivitamin and omega-3 "
        "before adding performance supplements."
    ),
    1: (
        "You are in a solid active maintenance phase. Your calorie and macro "
        "targets are well balanced for your activity level. Focus on "
        "recovery between sessions. Creatine and whey protein are your "
        "most evidence-backed supplement choices at this stage."
    ),
    2: (
        "Your profile matches a performance-focused athlete. Your higher "
        "protein targets and calorie surplus are designed to support muscle "
        "growth and training adaptation. Creatine monohydrate and pre-workout "
        "caffeine are strongly supported by evidence at your activity level."
    ),
    3: (
        "Your profile is aligned with a weight management cutting phase. "
        "The 500 kcal daily deficit is evidence-based for safe fat loss. "
        "Keep protein high to preserve muscle. Fibre supplements and "
        "omega-3 will support satiety and recovery during this phase."
    ),
    4: (
        "Your profile reflects an active older adult. Vitamin D3, magnesium, "
        "and omega-3 are particularly important for your age group to support "
        "bone density, joint health, and muscle function. Focus on "
        "maintaining consistent activity rather than high intensity."
    ),
}


#  Step 3: Generating synthetic training data 

def generate_training_data():
    """
    Creates realistic synthetic user data to train the Decision Tree.
    Each row = one user: [age, bmi, activity(0-4), goal(0-2), weight_kg]
    Labels: 0=Beginner, 1=Active, 2=Athlete, 3=WeightMgmt, 4=SeniorActive
    """
    X = np.array([
        # Beginner profiles
        [20, 22.0, 0, 2, 65], [22, 24.0, 1, 2, 70], [19, 21.0, 0, 0, 60],
        [23, 23.0, 1, 1, 68], [21, 22.5, 0, 2, 63], [24, 24.5, 1, 2, 72],
        [20, 21.5, 0, 0, 58], [22, 23.5, 1, 1, 67], [19, 22.0, 0, 2, 61],
        [23, 24.0, 1, 2, 71],

        # Active profiles
        [28, 23.0, 2, 2, 75], [30, 24.0, 2, 2, 80], [27, 22.5, 2, 1, 72],
        [32, 23.5, 2, 2, 78], [29, 24.5, 3, 2, 77], [31, 23.0, 2, 1, 76],
        [28, 22.0, 2, 2, 74], [30, 24.0, 3, 2, 81], [27, 23.5, 2, 1, 73],
        [32, 24.0, 2, 2, 79],

        # Athlete profiles
        [25, 22.0, 4, 1, 82], [27, 21.5, 4, 1, 85], [24, 23.0, 3, 1, 80],
        [26, 22.5, 4, 1, 83], [28, 21.0, 4, 1, 87], [25, 23.5, 4, 1, 81],
        [27, 22.0, 3, 1, 84], [24, 21.5, 4, 1, 79], [26, 23.0, 4, 1, 86],
        [28, 22.5, 4, 1, 88],

        # Weight management profiles
        [35, 28.0, 1, 0, 90], [40, 30.0, 2, 0, 95], [38, 29.0, 1, 0, 92],
        [42, 31.0, 2, 0, 98], [36, 28.5, 1, 0, 91], [39, 29.5, 2, 0, 94],
        [35, 30.5, 1, 0, 97], [41, 28.0, 2, 0, 93], [37, 31.5, 1, 0, 96],
        [43, 29.0, 2, 0, 99],

        # Senior active profiles
        [55, 25.0, 2, 2, 78], [60, 26.0, 1, 2, 80], [58, 24.5, 2, 2, 76],
        [62, 25.5, 1, 2, 82], [56, 26.5, 2, 2, 79], [61, 24.0, 1, 2, 77],
        [55, 27.0, 2, 2, 81], [59, 25.0, 1, 2, 75], [63, 26.0, 2, 2, 83],
        [57, 24.5, 1, 2, 78],
    ])

    y = np.array([0]*10 + [1]*10 + [2]*10 + [3]*10 + [4]*10)
    return X, y


#  Step 4: Training the Decision Tree 

def train_model():
    """
    Trains a Decision Tree classifier on the synthetic data.
    max_depth=4 keeps the tree simple and explainable.
    """
    X, y = generate_training_data()
    model = DecisionTreeClassifier(
        max_depth=4,
        random_state=42,
        min_samples_split=4,
    )
    model.fit(X, y)
    return model


#  Step 5: Looking up tables 

ACTIVITY_TO_NUM = {
    "sedentary": 0, "light": 1, "moderate": 2,
    "active": 3, "very_active": 4,
}

GOAL_TO_NUM = {
    "weight_loss": 0, "muscle_gain": 1, "maintenance": 2,
}

FEATURE_NAMES = ["Age", "BMI", "Activity Level", "Fitness Goal", "Weight (kg)"]


#  Step 6: this is the main prediction function 

def run_ai_model(age, bmi, activity_level, fitness_goal, weight_kg):
    """
    Takes a user's profile and returns an AI prediction.

    1. Trains the Decision Tree on synthetic data
    2. Converts user inputs to numbers
    3. Makes a prediction
    4. Returns profile, confidence, advice, and explanation
    """
    model = train_model()

    # Convert text inputs to numbers
    activity_num = ACTIVITY_TO_NUM.get(activity_level, 2)
    goal_num     = GOAL_TO_NUM.get(fitness_goal, 2)

    # Create input array
    user_input = np.array([[age, bmi, activity_num, goal_num, weight_kg]])

    # Make prediction
    prediction    = model.predict(user_input)[0]
    probabilities = model.predict_proba(user_input)[0]
    confidence    = round(probabilities[prediction] * 100, 1)

    # Get feature importance
    importance_scores  = model.feature_importances_
    feature_importance = {}
    for i, name in enumerate(FEATURE_NAMES):
        feature_importance[name] = round(importance_scores[i] * 100, 1)

    # Sort by importance (highest first)
    feature_importance = dict(
        sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    )

    # Build plain English explanation
    top_feature = list(feature_importance.keys())[0]
    explanation = (
        f"The Decision Tree analysed your profile across 5 features: "
        f"age, BMI, activity level, fitness goal, and weight. "
        f"The most influential factor was '{top_feature}' "
        f"({feature_importance[top_feature]}% importance). "
        f"The model classified you as '{FITNESS_PROFILES[prediction]}' "
        f"with {confidence}% confidence, based on patterns from "
        f"50 synthetic user profiles representing different fitness archetypes."
    )

    return AIResult(
        predicted_profile  = FITNESS_PROFILES[prediction],
        confidence         = confidence,
        advice             = PROFILE_ADVICE[prediction],
        feature_importance = feature_importance,
        model_explanation  = explanation,
    )



