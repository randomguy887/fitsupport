"""
FitSupport - Main Streamlit Application
Entry point for the FitSupport system.
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from core.nutrition_engine import run_nutrition_engine, UserProfile, ACTIVITY_LABELS, GOAL_LABELS
from core.supplement_engine import run_supplement_engine
from core.data_store import initialise_database, log_session, save_feedback
from core.uae_market import get_uae_info
from core.health_profile import (
    DIETARY_OPTIONS, BUDGET_OPTIONS, HEALTH_CONDITIONS,
    get_warnings, get_exclusions, is_high_risk
)
from core.email_feedback import send_feedback_email

# ── Page Configuration ──────────────────────────────────────
st.set_page_config(
    page_title="FitSupport",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Initialise Database ─────────────────────────────────────
initialise_database()

# ── Custom CSS ──────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .main-header h1 { color: #e94560; font-size: 2.8rem; margin-bottom: 0.2rem; }
    .main-header p  { color: #a8b2d8; font-size: 1.05rem; }

    .metric-card {
        background: #16213e;
        border: 1px solid #0f3460;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        margin-bottom: 0.8rem;
    }
    .metric-card .label { color: #a8b2d8; font-size: 0.85rem; text-transform: uppercase; }
    .metric-card .value { color: #e94560; font-size: 2rem; font-weight: 700; }
    .metric-card .unit  { color: #a8b2d8; font-size: 0.9rem; }

    .supplement-card {
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    .primary-card   { background: #0d2137; border-color: #e94560; }
    .secondary-card { background: #0d2137; border-color: #f5a623; }
    .general-card   { background: #0d2137; border-color: #4ecdc4; }

    .uae-card {
        background: #0d1f0d;
        border: 1px solid #2d6a2d;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .store-tag {
        display: inline-block;
        background: #1a3a1a;
        color: #69db7c;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.78rem;
        margin: 0.2rem;
    }
    .price-tag {
        display: inline-block;
        background: #3a2800;
        color: #ffd43b;
        padding: 0.2rem 0.7rem;
        border-radius: 12px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .warning-box {
        background: #2a1000;
        border-left: 4px solid #f5a623;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1rem;
        color: #ffc078;
        margin-bottom: 0.6rem;
        font-size: 0.9rem;
    }
    .danger-box {
        background: #2a0000;
        border: 1px solid #e94560;
        border-radius: 8px;
        padding: 1rem;
        color: #ff8787;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    .success-box {
        background: #0d2a0d;
        border-left: 4px solid #69db7c;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1rem;
        color: #69db7c;
        margin-bottom: 0.6rem;
        font-size: 0.9rem;
    }
    .rationale-box {
        background: #0a1628;
        border-left: 3px solid #4ecdc4;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        color: #a8b2d8;
        font-size: 0.92rem;
        margin-top: 0.5rem;
    }
    .disclaimer-box {
        background: #1a0a0a;
        border: 1px solid #e94560;
        border-radius: 8px;
        padding: 1rem;
        color: #ff8787;
        font-size: 0.88rem;
        margin-top: 1rem;
    }
    .section-title {
        color: #e94560;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        border-bottom: 2px solid #0f3460;
        padding-bottom: 0.4rem;
    }
    .badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.4rem;
    }
    .badge-strong    { background: #1a472a; color: #69db7c; }
    .badge-moderate  { background: #4a3400; color: #ffd43b; }
    .badge-primary   { background: #4a0010; color: #ff6b81; }
    .badge-secondary { background: #4a3000; color: #ffc078; }
    .badge-general   { background: #003a38; color: #63e6be; }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>💪 FitSupport</h1>
    <p>Personalised Nutrition & Supplement Guidance System</p>
    <p style="color:#4ecdc4; font-size:0.85rem;">
        For educational purposes only · Not medical advice · UAE Market Edition
    </p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 👤 Your Profile")

    age       = st.number_input("Age *", min_value=16, max_value=80, value=25, step=1)
    gender    = st.selectbox(
        "Gender (optional)",
        options=["prefer_not_to_say", "male", "female"],
        format_func=lambda x: {"prefer_not_to_say": "Prefer not to say", "male": "Male", "female": "Female"}[x],
    )
    weight_kg = st.number_input("Weight (kg) *", min_value=30.0, max_value=250.0, value=75.0, step=0.5)
    height_cm = st.number_input("Height (cm) *", min_value=100.0, max_value=250.0, value=175.0, step=0.5)
    activity_level = st.selectbox(
        "Activity Level *",
        options=list(ACTIVITY_LABELS.keys()),
        format_func=lambda x: ACTIVITY_LABELS[x],
        index=2,
    )
    fitness_goal = st.selectbox(
        "Fitness Goal *",
        options=list(GOAL_LABELS.keys()),
        format_func=lambda x: GOAL_LABELS[x],
    )

    st.divider()
    st.markdown("## 🥗 Lifestyle & Health")

    dietary_preference = st.selectbox(
        "Dietary Preference",
        options=list(DIETARY_OPTIONS.keys()),
        format_func=lambda x: DIETARY_OPTIONS[x],
    )

    budget = st.selectbox(
        "Budget (UAE)",
        options=list(BUDGET_OPTIONS.keys()),
        format_func=lambda x: BUDGET_OPTIONS[x],
        index=1,
    )

    health_conditions = st.multiselect(
        "Any health conditions? (optional)",
        options=list(HEALTH_CONDITIONS.keys()),
        format_func=lambda x: HEALTH_CONDITIONS[x],
        default=["none"],
        help="Used only to show relevant doctor advisories. Does not change supplement recommendations.",
    )

    st.divider()
    calculate_btn = st.button("Calculate My Plan", use_container_width=True, type="primary")

    st.markdown("""
    <div style="font-size:0.78rem; color:#666; margin-top:0.5rem;">
    No personal data is stored. Health conditions are used only
    to display doctor advisory messages.
    </div>
    """, unsafe_allow_html=True)


# ── Main Results ─────────────────────────────────────────────
if calculate_btn:

    # Build profile
    profile = UserProfile(
        age=age,
        weight_kg=weight_kg,
        height_cm=height_cm,
        activity_level=activity_level,
        fitness_goal=fitness_goal,
        gender=gender if gender != "prefer_not_to_say" else None,
    )

    # Run the engines
    with st.spinner("Calculating your personalised plan..."):
        nutrition   = run_nutrition_engine(profile)

        # Get dietary exclusions
        excluded_supplements, dietary_note = get_exclusions(dietary_preference)

        supplements = run_supplement_engine(
            fitness_goal=fitness_goal,
            activity_level=activity_level,
            bmi_category=nutrition.bmi_category,
            weight_kg=weight_kg,
        )

        # Filter out excluded supplements based on dietary preference
        def filter_supplements(supplement_list):
            return [s for s in supplement_list if s.name not in excluded_supplements]

        filtered_primary   = filter_supplements(supplements.primary)
        filtered_secondary = filter_supplements(supplements.secondary)
        filtered_general   = filter_supplements(supplements.general)

        # Get all recommended supplement names (filtered)
        all_recommended = (
            [s.name for s in filtered_primary] +
            [s.name for s in filtered_secondary] +
            [s.name for s in filtered_general]
        )

        # Get health warnings
        health_warnings = get_warnings(health_conditions)
        high_risk       = is_high_risk(health_conditions)

        session_id = log_session(profile, nutrition, len(all_recommended))

    # Show high-risk warning at the top if needed
    if high_risk:
        st.markdown("""
        <div class="danger-box">
            <strong>⛔ Important Medical Advisory</strong><br>
            You have selected a serious health condition. Please consult your doctor
            or specialist BEFORE using any supplement. Do not rely on this system
            for medical decisions.
        </div>
        """, unsafe_allow_html=True)

    # ── Tabs ────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Nutrition",
        "💊 Supplements",
        "🇦🇪 UAE Market",
        "🏥 Health Advisory",
        "📈 Charts",
        "📝 Feedback",
    ])

    # ════════════════════════════════════════════════════════
    # TAB 1 — NUTRITION DASHBOARD
    # ════════════════════════════════════════════════════════
    with tab1:
        st.markdown(f"""
        <p style="color:#a8b2d8;">
            Goal: <strong style="color:#4ecdc4;">{GOAL_LABELS[fitness_goal]}</strong>
            &nbsp;·&nbsp;
            Activity: <strong style="color:#4ecdc4;">{ACTIVITY_LABELS[activity_level]}</strong>
        </p>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""<div class="metric-card">
                <div class="label">Daily Target</div>
                <div class="value">{nutrition.target_calories:,.0f}</div>
                <div class="unit">kcal / day</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="metric-card">
                <div class="label">BMR</div>
                <div class="value">{nutrition.bmr:,.0f}</div>
                <div class="unit">kcal / day</div></div>""", unsafe_allow_html=True)
        with col3:
            bmi_colour = {"Underweight":"#ffd43b","Normal Weight":"#69db7c","Overweight":"#f5a623","Obese":"#e94560"}.get(nutrition.bmi_category,"#a8b2d8")
            st.markdown(f"""<div class="metric-card">
                <div class="label">BMI</div>
                <div class="value" style="color:{bmi_colour};">{nutrition.bmi}</div>
                <div class="unit">{nutrition.bmi_category}</div></div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""<div class="metric-card">
                <div class="label">Daily Water</div>
                <div class="value">{nutrition.water_ml/1000:.1f}</div>
                <div class="unit">litres / day</div></div>""", unsafe_allow_html=True)

        st.divider()
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="section-title">Macronutrient Targets</div>', unsafe_allow_html=True)
            macros_data = {
                "Macronutrient": ["Protein", "Carbohydrates", "Fat"],
                "Grams / day":   [nutrition.protein_g, nutrition.carbs_g, nutrition.fat_g],
                "Calories (kcal)": [round(nutrition.protein_g*4), round(nutrition.carbs_g*4), round(nutrition.fat_g*9)],
            }
            df = pd.DataFrame(macros_data)
            df["% of Total"] = (df["Calories (kcal)"] / nutrition.target_calories * 100).round(1).astype(str) + "%"
            st.dataframe(df, use_container_width=True, hide_index=True)

        with col_b:
            st.markdown('<div class="section-title">Calorie Breakdown</div>', unsafe_allow_html=True)
            energy_data = {
                "Component": ["BMR (Base)", "Activity Bonus", "Goal Adjustment"],
                "kcal": [nutrition.bmr, round(nutrition.tdee - nutrition.bmr), nutrition.calorie_adjustment],
            }
            st.dataframe(pd.DataFrame(energy_data), use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div class="rationale-box">
            <strong style="color:#4ecdc4;">Why this calorie target?</strong><br>
            {nutrition.goal_rationale}
        </div>""", unsafe_allow_html=True)

        with st.expander("View Full Calculation Breakdown"):
            st.markdown(f"""
**Step 1 - BMR (Basal Metabolic Rate)**
Formula: (10 x weight) + (6.25 x height) - (5 x age) +/- gender constant
Result: **{nutrition.bmr:,.1f} kcal/day**

**Step 2 - TDEE (Total Daily Energy Expenditure)**
BMR multiplied by activity level multiplier
Result: **{nutrition.tdee:,.1f} kcal/day**

**Step 3 - Goal Adjustment**
Adjustment: **{nutrition.calorie_adjustment:+.0f} kcal**
Final Target: **{nutrition.target_calories:,.1f} kcal/day**

**Step 4 - Macronutrients**
Protein: **{nutrition.protein_g}g** | Carbs: **{nutrition.carbs_g}g** | Fat: **{nutrition.fat_g}g**

**Step 5 - Water Target**
**{nutrition.water_ml:.0f} ml/day**

**Step 6 - BMI**
**{nutrition.bmi}** — {nutrition.bmi_category}
            """)

    # ════════════════════════════════════════════════════════
    # TAB 2 — SUPPLEMENTS
    # ════════════════════════════════════════════════════════
    with tab2:

        # Show dietary note if applicable
        if dietary_note:
            st.markdown(f"""
            <div class="success-box">
                🥗 <strong>Dietary filter applied:</strong> {dietary_note}
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="rationale-box">
            <strong style="color:#4ecdc4;">Goal Summary:</strong><br>
            {supplements.goal_summary}
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="disclaimer-box">
            {supplements.disclaimer}
        </div>""", unsafe_allow_html=True)

        def render_card(s, card_class):
            priority_colours = {"Primary": "badge-primary", "Secondary": "badge-secondary"}
            evidence_colours = {"Strong": "badge-strong", "Moderate": "badge-moderate"}
            p_cls = priority_colours.get(s.priority, "badge-general")
            e_cls = evidence_colours.get(s.evidence_level, "badge-moderate")
            st.markdown(f"""
            <div class="supplement-card {card_class}">
                <strong style="color:#e2e8f0; font-size:1.05rem;">💊 {s.name}</strong>
                <span style="color:#a8b2d8;"> · {s.category}</span><br>
                <span class="badge {p_cls}">{s.priority} Priority</span>
                <span class="badge {e_cls}">Evidence: {s.evidence_level}</span>
                <br><br>
                <strong style="color:#4ecdc4;">What it is:</strong>
                <span style="color:#c8d3e8;"> {s.description}</span><br><br>
                <strong style="color:#4ecdc4;">Why recommended:</strong>
                <span style="color:#c8d3e8;"> {s.benefit}</span><br><br>
                <strong style="color:#4ecdc4;">Dosage:</strong>
                <span style="color:#c8d3e8;"> {s.dosage_guidance}</span><br>
                <strong style="color:#4ecdc4;">Timing:</strong>
                <span style="color:#c8d3e8;"> {s.timing}</span><br><br>
                <strong style="color:#f5a623;">Cautions:</strong>
                <span style="color:#c8d3e8;"> {s.cautions}</span>
            </div>""", unsafe_allow_html=True)

        if filtered_primary:
            st.markdown("### 🔴 Primary Recommendations")
            for s in filtered_primary:
                render_card(s, "primary-card")

        if filtered_secondary:
            st.markdown("### 🟡 Secondary Recommendations")
            for s in filtered_secondary:
                render_card(s, "secondary-card")

        if filtered_general:
            st.markdown("### 🟢 General Wellness")
            for s in filtered_general:
                render_card(s, "general-card")

        if not all_recommended:
            st.info("No supplements recommended for your current profile. Focus on whole foods and rest.")

    # ════════════════════════════════════════════════════════
    # TAB 3 — UAE MARKET
    # ════════════════════════════════════════════════════════
    with tab3:
        st.markdown("### 🇦🇪 Where to Buy in the UAE")
        st.markdown("Based on your recommendations, here is where you can buy each supplement across the UAE.")

        # Budget label
        budget_labels = {"low": "under 100 AED", "medium": "100–250 AED", "high": "250+ AED"}
        st.info(f"Budget filter: **{BUDGET_OPTIONS[budget]}**")

        if not all_recommended:
            st.warning("No supplements recommended yet. Fill in your profile and click Calculate first.")
        else:
            for supp_name in all_recommended:
                uae_info = get_uae_info(supp_name)

                if uae_info:
                    # Filter brands by budget
                    brands = uae_info["brands"]
                    if budget == "low":
                        brands = [b for b in brands if int(b["price_aed"].split("-")[0].strip()) < 100]

                    st.markdown(f"""
                    <div class="uae-card">
                        <strong style="color:#69db7c; font-size:1.05rem;">🛒 {supp_name}</strong><br>
                        <span style="color:#a8b2d8; font-size:0.88rem;">{uae_info["tip"]}</span>
                        <br><br>
                    """, unsafe_allow_html=True)

                    # Stores
                    st.markdown("**Where to buy:**")
                    store_tags = ""
                    for store in uae_info["stores"]:
                        store_tags += f'<span class="store-tag">🏪 {store["name"]}</span>'
                    st.markdown(store_tags, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # Brands & prices
                    if brands:
                        st.markdown("**Popular brands & prices:**")
                        for brand in brands:
                            st.markdown(f"""
                            <span style="color:#e2e8f0;">• <strong>{brand["brand"]}</strong> — {brand["product"]}</span>
                            &nbsp;<span class="price-tag">💰 {brand["price_aed"]} AED</span><br>
                            """, unsafe_allow_html=True)
                    elif budget == "low":
                        st.markdown("*No budget-friendly options found. Try Mid-Range filter.*")

                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**{supp_name}** — Available at major UAE pharmacies and health stores.")

    # ════════════════════════════════════════════════════════
    # TAB 4 — HEALTH ADVISORY
    # ════════════════════════════════════════════════════════
    with tab4:
        st.markdown("### 🏥 Health & Lifestyle Advisory")

        selected_conditions = [c for c in health_conditions if c != "none"]

        if not selected_conditions:
            st.markdown("""
            <div class="success-box">
                ✅ No health conditions selected. Your supplement recommendations
                are based on your fitness goal and activity level only.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="danger-box">
                <strong>⚠️ Please read all advisories below carefully.</strong><br>
                These messages are shown because you selected one or more health conditions.
                FitSupport does NOT provide medical advice. Always consult a qualified
                healthcare professional before taking any supplement.
            </div>""", unsafe_allow_html=True)

            for warning in health_warnings:
                st.markdown(f"""
                <div class="warning-box">
                    ⚠️ {warning}
                </div>""", unsafe_allow_html=True)

        st.divider()

        # UAE Healthcare Resources
        st.markdown("### 🏨 UAE Healthcare Resources")
        st.markdown("If you need professional advice before supplementing, here are trusted UAE resources:")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Hospitals & Clinics**
            - Cleveland Clinic Abu Dhabi
            - American Hospital Dubai
            - Mediclinic (multiple UAE locations)
            - Aster Hospitals UAE
            - Saudi German Hospital UAE
            """)
        with col2:
            st.markdown("""
            **Nutrition & Dietitian Services**
            - Emirates Dietetic Association
            - Dubai Nutrition Association
            - Life Pharmacy in-store consultations
            - Holland & Barrett UAE nutrition advice
            - NMC Healthcare UAE
            """)

        st.divider()

        # Dietary preference summary
        st.markdown("### 🥗 Your Dietary Preference Summary")
        _, note = get_exclusions(dietary_preference)

        if note:
            st.markdown(f"""
            <div class="success-box">
                🥗 {note}
            </div>""", unsafe_allow_html=True)
        else:
            st.success("No dietary restrictions applied to your recommendations.")

    # ════════════════════════════════════════════════════════
    # TAB 5 — CHARTS
    # ════════════════════════════════════════════════════════
    with tab5:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Macronutrient Split")
            fig_pie = go.Figure(data=[go.Pie(
                labels=["Protein", "Carbohydrates", "Fat"],
                values=[round(nutrition.protein_g*4), round(nutrition.carbs_g*4), round(nutrition.fat_g*9)],
                hole=0.45,
                marker=dict(colors=["#e94560", "#4ecdc4", "#f5a623"]),
                textinfo="label+percent",
            )])
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font=dict(color="#a8b2d8"), showlegend=False,
                                  margin=dict(t=20,b=20,l=20,r=20))
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            st.markdown("#### Energy Flow (kcal/day)")
            fig_bar = go.Figure(go.Bar(
                x=["BMR", "TDEE", "Target"],
                y=[nutrition.bmr, nutrition.tdee, nutrition.target_calories],
                marker_color=["#4ecdc4", "#f5a623", "#e94560"],
                text=[f"{nutrition.bmr:,.0f}", f"{nutrition.tdee:,.0f}", f"{nutrition.target_calories:,.0f}"],
                textposition="auto",
            ))
            fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font=dict(color="#a8b2d8"),
                                  yaxis=dict(color="#a8b2d8", gridcolor="#1a2a4a", title="kcal/day"),
                                  xaxis=dict(color="#a8b2d8"), margin=dict(t=20,b=20,l=20,r=20))
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("#### BMI Gauge")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=nutrition.bmi,
            number={"font": {"color": "#e94560", "size": 40}},
            gauge={
                "axis": {"range": [10, 40], "tickcolor": "#a8b2d8"},
                "bar":  {"color": "#e94560"},
                "steps": [
                    {"range": [10,   18.5], "color": "#2c3e6b"},
                    {"range": [18.5, 25],   "color": "#1a472a"},
                    {"range": [25,   30],   "color": "#4a3400"},
                    {"range": [30,   40],   "color": "#4a0010"},
                ],
                "bgcolor": "rgba(0,0,0,0)",
            },
        ))
        fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#a8b2d8"),
                                height=250, margin=dict(t=20,b=0,l=40,r=40))
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown("#### Daily Macros in Grams")
        fig_grams = go.Figure(go.Bar(
            x=["Protein", "Carbohydrates", "Fat"],
            y=[nutrition.protein_g, nutrition.carbs_g, nutrition.fat_g],
            marker_color=["#e94560", "#4ecdc4", "#f5a623"],
            text=[f"{nutrition.protein_g}g", f"{nutrition.carbs_g}g", f"{nutrition.fat_g}g"],
            textposition="auto",
        ))
        fig_grams.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                font=dict(color="#a8b2d8"),
                                yaxis=dict(color="#a8b2d8", gridcolor="#1a2a4a", title="grams/day"),
                                xaxis=dict(color="#a8b2d8"), margin=dict(t=10,b=10,l=20,r=20))
        st.plotly_chart(fig_grams, use_container_width=True)

    # ════════════════════════════════════════════════════════
    # TAB 6 — FEEDBACK
    # ════════════════════════════════════════════════════════
    with tab6:
        st.markdown("### 📝 Usability Feedback")
        st.markdown("Your anonymous feedback helps improve FitSupport. Do not enter personal information.")

        with st.form("feedback_form"):
            usability  = st.slider("How easy was the system to use?",         1, 5, 3)
            accuracy   = st.slider("How accurate do the results feel?",        1, 5, 3)
            usefulness = st.slider("How useful was the information provided?",  1, 5, 3)
            comments   = st.text_area("Additional comments (optional)", max_chars=500)
            submitted  = st.form_submit_button("Submit Feedback", type="primary")

            if submitted:
                save_feedback(session_id, usability, accuracy, usefulness, comments)
                st.success("Thank you! Your anonymous feedback has been recorded.")

                # Try to send an email notification to the project owner.
                # This only works if secrets.toml has been filled in correctly.
                try:
                    sender   = st.secrets["SENDER_EMAIL"]
                    password = st.secrets["APP_PASSWORD"]
                    receiver = st.secrets["RECEIVER_EMAIL"]

                    email_sent = send_feedback_email(
                        sender_email=sender,
                        app_password=password,
                        receiver_email=receiver,
                        usability=usability,
                        accuracy=accuracy,
                        usefulness=usefulness,
                        comments=comments,
                        session_id=session_id,
                    )
                    # We don't show a message either way — feedback is already saved
                    # to the database regardless of whether the email succeeds.
                except Exception:
                    # If secrets are not set up yet, the app still works fine —
                    # feedback is saved to the database either way.
                    pass

# ── Landing Page (shown before Calculate is clicked) ────────
else:
    st.markdown("""
    <div style="text-align:center; padding:3rem 2rem; color:#a8b2d8;">
        <h3 style="color:#4ecdc4;">How to use FitSupport</h3>
        <ol style="text-align:left; max-width:500px; margin:0 auto; line-height:2.2;">
            <li>Enter your profile in the left sidebar</li>
            <li>Select your dietary preference and budget</li>
            <li>Optionally select any health conditions</li>
            <li>Click <strong style="color:#e94560;">Calculate My Plan</strong></li>
            <li>View your nutrition, supplements, and UAE market info</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**📊 Nutrition Engine**\nBMR, TDEE, macros and hydration calculated using peer-reviewed formulas.")
    with col2:
        st.info("**💊 Supplement Engine**\nPersonalised recommendations filtered by your goal, diet and activity level.")
    with col3:
        st.info("**🇦🇪 UAE Market Tab**\nSee exactly where to buy your supplements in the UAE with prices in AED.")
