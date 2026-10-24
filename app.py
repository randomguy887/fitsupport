"""
FitSupport - Main Streamlit Application
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
from core.ai_model import run_ai_model

st.set_page_config(
    page_title="FitSupport",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialise_database()

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: linear-gradient(160deg, #0f0c29 0%, #302b63 50%, #24243e 100%); min-height: 100vh; }

    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.1) !important;
    }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stNumberInput label,
    [data-testid="stSidebar"] .stMultiSelect label { color: #94a3b8 !important; font-size: 0.82rem !important; font-weight: 500 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; }

    .main-header {
        background: linear-gradient(135deg, rgba(99,102,241,0.3) 0%, rgba(168,85,247,0.3) 50%, rgba(236,72,153,0.3) 100%);
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(20px);
        padding: 3rem 2rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 25px 50px rgba(0,0,0,0.4);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 60%);
        animation: pulse 4s ease-in-out infinite;
    }
    @keyframes pulse { 0%,100% { transform: scale(1); opacity: 0.5; } 50% { transform: scale(1.1); opacity: 1; } }
    .main-header h1 { color: #ffffff; font-size: 3rem; font-weight: 800; margin-bottom: 0.3rem; letter-spacing: -0.02em; }
    .main-header .subtitle { color: #c4b5fd; font-size: 1.1rem; font-weight: 300; }
    .main-header .tagline { color: rgba(255,255,255,0.5); font-size: 0.82rem; margin-top: 0.5rem; }

    .glass-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .glass-card:hover { transform: translateY(-2px); box-shadow: 0 20px 40px rgba(0,0,0,0.3); }

    .metric-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 1.5rem 1rem;
        text-align: center;
        margin-bottom: 0.8rem;
        transition: transform 0.2s;
        position: relative;
        overflow: hidden;
    }
    .metric-card::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
    }
    .metric-card:hover { transform: translateY(-3px); }
    .metric-card .label { color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; }
    .metric-card .value { color: #ffffff; font-size: 2.2rem; font-weight: 800; line-height: 1.1; margin: 0.3rem 0; }
    .metric-card .unit  { color: #6366f1; font-size: 0.85rem; font-weight: 500; }

    .supplement-card {
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
        transition: all 0.2s;
    }
    .supplement-card:hover { background: rgba(255,255,255,0.06); transform: translateX(4px); }
    .primary-card   { border-left-color: #ec4899; }
    .secondary-card { border-left-color: #f59e0b; }
    .general-card   { border-left-color: #10b981; }

    .uae-card {
        background: rgba(16,185,129,0.05);
        border: 1px solid rgba(16,185,129,0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.2s;
    }
    .uae-card:hover { background: rgba(16,185,129,0.08); }

    .store-tag {
        display: inline-block;
        background: rgba(16,185,129,0.15);
        color: #34d399;
        border: 1px solid rgba(16,185,129,0.3);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.78rem;
        margin: 0.2rem;
        text-decoration: none;
        transition: all 0.2s;
        font-weight: 500;
    }
    .store-tag:hover { background: rgba(16,185,129,0.3); color: #ffffff; }

    .price-tag {
        display: inline-block;
        background: rgba(245,158,11,0.15);
        color: #fbbf24;
        border: 1px solid rgba(245,158,11,0.3);
        padding: 0.25rem 0.7rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .badge { display: inline-block; padding: 0.25rem 0.7rem; border-radius: 20px; font-size: 0.72rem; font-weight: 700; margin-right: 0.4rem; letter-spacing: 0.03em; }
    .badge-strong    { background: rgba(16,185,129,0.2);  color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
    .badge-moderate  { background: rgba(245,158,11,0.2);  color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
    .badge-primary   { background: rgba(236,72,153,0.2);  color: #f472b6; border: 1px solid rgba(236,72,153,0.3); }
    .badge-secondary { background: rgba(245,158,11,0.2);  color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
    .badge-general   { background: rgba(16,185,129,0.2);  color: #34d399; border: 1px solid rgba(16,185,129,0.3); }

    .info-box {
        background: rgba(99,102,241,0.1);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        color: #c4b5fd;
        font-size: 0.92rem;
        margin: 0.8rem 0;
    }
    .warning-box {
        background: rgba(245,158,11,0.1);
        border-left: 4px solid #f59e0b;
        border-radius: 0 12px 12px 0;
        padding: 0.8rem 1rem;
        color: #fbbf24;
        margin-bottom: 0.6rem;
        font-size: 0.9rem;
    }
    .danger-box {
        background: rgba(236,72,153,0.1);
        border: 1px solid rgba(236,72,153,0.3);
        border-radius: 12px;
        padding: 1rem;
        color: #f472b6;
        margin-bottom: 1rem;
    }
    .success-box {
        background: rgba(16,185,129,0.1);
        border-left: 4px solid #10b981;
        border-radius: 0 12px 12px 0;
        padding: 0.8rem 1rem;
        color: #34d399;
        margin-bottom: 0.6rem;
    }
    .disclaimer-box {
        background: rgba(236,72,153,0.08);
        border: 1px solid rgba(236,72,153,0.2);
        border-radius: 12px;
        padding: 1rem;
        color: #f9a8d4;
        font-size: 0.85rem;
        margin-top: 1rem;
    }
    .rationale-box {
        background: rgba(99,102,241,0.08);
        border-left: 4px solid #6366f1;
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.2rem;
        color: #c4b5fd;
        font-size: 0.92rem;
        margin: 0.8rem 0;
    }
    .section-title {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }

    .ai-profile-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.2) 0%, rgba(168,85,247,0.2) 100%);
        border: 1px solid rgba(99,102,241,0.4);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .landing-feature-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s;
        height: 100%;
    }
    .landing-feature-card:hover { background: rgba(255,255,255,0.08); transform: translateY(-5px); }
    .landing-feature-card .icon { font-size: 2.5rem; margin-bottom: 1rem; }
    .landing-feature-card h4 { color: #ffffff; font-weight: 700; margin-bottom: 0.5rem; }
    .landing-feature-card p { color: #94a3b8; font-size: 0.9rem; line-height: 1.6; }

    div[data-testid="stTabs"] button {
        color: #94a3b8 !important;
        font-weight: 500 !important;
        border-radius: 10px 10px 0 0 !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #ffffff !important;
        background: rgba(99,102,241,0.2) !important;
        border-bottom: 2px solid #6366f1 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 15px rgba(99,102,241,0.4) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99,102,241,0.6) !important;
    }

    div[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
    .stDataFrame { background: rgba(255,255,255,0.03) !important; }

    h1,h2,h3,h4,h5,h6 { color: #ffffff !important; }
    p, li, span { color: #e2e8f0; }
    .stMarkdown p { color: #cbd5e1; }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); }
    ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.5); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>💪 FitSupport</h1>
    <p class="subtitle">Personalised Nutrition & Supplement Guidance System</p>
    <p class="subtitle">For educational purposes only  · Please note that this system DOES NOT AT ALL offer PROFESSIONAL medical advice</p>
    <p class="tagline">✨ Powered by peer-reviewed science &nbsp;·&nbsp; 🇦🇪 UAE Market Edition &nbsp;·&nbsp; 🤖 AI-Enhanced</p>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 👤 Your Profile")
    age            = st.number_input("Age", min_value=16, max_value=80, value=25, step=1)
    gender         = st.selectbox("Gender (optional)", options=["prefer_not_to_say","male","female"],
                       format_func=lambda x: {"prefer_not_to_say":"Prefer not to say","male":"Male","female":"Female"}[x])
    weight_kg      = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=75.0, step=0.5)
    height_cm      = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=175.0, step=0.5)
    activity_level = st.selectbox("Activity Level", options=list(ACTIVITY_LABELS.keys()),
                       format_func=lambda x: ACTIVITY_LABELS[x], index=2)
    fitness_goal   = st.selectbox("Fitness Goal", options=list(GOAL_LABELS.keys()),
                       format_func=lambda x: GOAL_LABELS[x])
    st.divider()
    st.markdown("## 🥗 Lifestyle & Health")
    dietary_preference = st.selectbox("Dietary Preference", options=list(DIETARY_OPTIONS.keys()),
                           format_func=lambda x: DIETARY_OPTIONS[x])
    budget             = st.selectbox("Budget (AED)", options=list(BUDGET_OPTIONS.keys()),
                           format_func=lambda x: BUDGET_OPTIONS[x], index=1)
    health_conditions  = st.multiselect("Health Conditions (optional)",
                           options=list(HEALTH_CONDITIONS.keys()),
                           format_func=lambda x: HEALTH_CONDITIONS[x], default=["none"])
    st.divider()
    calculate_btn = st.button("🚀 Calculate My Plan", use_container_width=True, type="primary")
    st.markdown('<p style="color:rgba(255,255,255,0.3); font-size:0.75rem; text-align:center; margin-top:0.5rem;">No personal data is stored</p>', unsafe_allow_html=True)


# ── Main Results ─────────────────────────────────────────────
if calculate_btn:

    profile = UserProfile(
        age=age, weight_kg=weight_kg, height_cm=height_cm,
        activity_level=activity_level, fitness_goal=fitness_goal,
        gender=gender if gender != "prefer_not_to_say" else None,
    )

    with st.spinner("✨ Calculating your personalised plan..."):
        nutrition    = run_nutrition_engine(profile)
        excluded, dietary_note = get_exclusions(dietary_preference)
        supplements  = run_supplement_engine(fitness_goal, activity_level, nutrition.bmi_category, weight_kg)

        def filter_supps(lst): return [s for s in lst if s.name not in excluded]
        fp = filter_supps(supplements.primary)
        fs = filter_supps(supplements.secondary)
        fg = filter_supps(supplements.general)
        all_rec = [s.name for s in fp + fs + fg]

        health_warns = get_warnings(health_conditions)
        high_risk    = is_high_risk(health_conditions)
        session_id   = log_session(profile, nutrition, len(all_rec))
        ai_result    = run_ai_model(age, nutrition.bmi, activity_level, fitness_goal, weight_kg)

    if high_risk:
        st.markdown('<div class="danger-box"><strong>⛔ Important Medical Advisory</strong><br>You selected a serious health condition. Consult your doctor BEFORE using any supplement.</div>', unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Nutrition", "💊 Supplements", "🇦🇪 UAE Market",
        "🏥 Health", "📈 Charts", "🤖 AI Insights", "📝 Feedback",
    ])

    # ════════════════════════════════
    # TAB 1 — NUTRITION
    # ════════════════════════════════
    with tab1:
        st.markdown(f'<div class="info-box">🎯 Goal: <strong>{GOAL_LABELS[fitness_goal]}</strong> &nbsp;·&nbsp; 🏃 Activity: <strong>{ACTIVITY_LABELS[activity_level]}</strong></div>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        bmi_colour = {"Underweight":"#fbbf24","Normal Weight":"#34d399","Overweight":"#f59e0b","Obese":"#ec4899"}.get(nutrition.bmi_category,"#e2e8f0")

        with c1:
            st.markdown(f'<div class="metric-card"><div class="label">Daily Target</div><div class="value">{nutrition.target_calories:,.0f}</div><div class="unit">kcal / day</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="label">BMR</div><div class="value">{nutrition.bmr:,.0f}</div><div class="unit">kcal / day</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="label">BMI</div><div class="value" style="color:{bmi_colour};">{nutrition.bmi}</div><div class="unit">{nutrition.bmi_category}</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-card"><div class="label">Daily Water</div><div class="value">{nutrition.water_ml/1000:.1f}L</div><div class="unit">litres / day</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        ca, cb = st.columns(2)

        with ca:
            st.markdown('<div class="section-title">📐 Macronutrient Targets</div>', unsafe_allow_html=True)
            df = pd.DataFrame({
                "Macronutrient": ["Protein", "Carbohydrates", "Fat"],
                "Grams/day":     [nutrition.protein_g, nutrition.carbs_g, nutrition.fat_g],
                "Calories":      [round(nutrition.protein_g*4), round(nutrition.carbs_g*4), round(nutrition.fat_g*9)],
            })
            df["% of Total"] = (df["Calories"] / nutrition.target_calories * 100).round(1).astype(str) + "%"
            st.dataframe(df, use_container_width=True, hide_index=True)

        with cb:
            st.markdown('<div class="section-title">⚡ Calorie Breakdown</div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame({
                "Component": ["BMR (Base)", "Activity Bonus", "Goal Adjustment"],
                "kcal":      [nutrition.bmr, round(nutrition.tdee - nutrition.bmr), nutrition.calorie_adjustment],
            }), use_container_width=True, hide_index=True)

        st.markdown(f'<div class="rationale-box"><strong>📌 Why this target?</strong><br>{nutrition.goal_rationale}</div>', unsafe_allow_html=True)

        with st.expander("🔬 Full Calculation Breakdown"):
            st.markdown(f"""
**Step 1 — BMR** (Mifflin-St Jeor, 1990): **{nutrition.bmr:,.1f} kcal/day**

**Step 2 — TDEE** (BMR × activity multiplier): **{nutrition.tdee:,.1f} kcal/day**

**Step 3 — Goal Adjustment** ({nutrition.calorie_adjustment:+.0f} kcal): **{nutrition.target_calories:,.1f} kcal/day**

**Step 4 — Macros**: Protein **{nutrition.protein_g}g** · Carbs **{nutrition.carbs_g}g** · Fat **{nutrition.fat_g}g**

**Step 5 — Water**: **{nutrition.water_ml:.0f} ml/day** (35ml/kg + activity bonus)

**Step 6 — BMI**: **{nutrition.bmi}** → {nutrition.bmi_category}
            """)

    # ════════════════════════════════
    # TAB 2 — SUPPLEMENTS
    # ════════════════════════════════
    with tab2:
        if dietary_note:
            st.markdown(f'<div class="success-box">🥗 {dietary_note}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="rationale-box">🎯 <strong>Goal Summary:</strong> {supplements.goal_summary}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="disclaimer-box">⚠️ {supplements.disclaimer}</div>', unsafe_allow_html=True)

        def render_card(s, card_class):
            pc = {"Primary":"badge-primary","Secondary":"badge-secondary"}.get(s.priority,"badge-general")
            ec = {"Strong":"badge-strong","Moderate":"badge-moderate"}.get(s.evidence_level,"badge-moderate")
            st.markdown(f"""
            <div class="supplement-card {card_class}">
                <strong style="color:#ffffff; font-size:1.05rem;">💊 {s.name}</strong>
                <span style="color:#94a3b8; font-size:0.82rem;"> · {s.category}</span><br>
                <span class="badge {pc}">{s.priority}</span>
                <span class="badge {ec}">Evidence: {s.evidence_level}</span><br><br>
                <strong style="color:#6366f1;">What it is:</strong> <span style="color:#cbd5e1;">{s.description}</span><br><br>
                <strong style="color:#6366f1;">Why recommended:</strong> <span style="color:#cbd5e1;">{s.benefit}</span><br><br>
                <strong style="color:#6366f1;">Dosage:</strong> <span style="color:#cbd5e1;">{s.dosage_guidance}</span><br>
                <strong style="color:#6366f1;">Timing:</strong> <span style="color:#cbd5e1;">{s.timing}</span><br><br>
                <strong style="color:#f59e0b;">⚠ Cautions:</strong> <span style="color:#cbd5e1;">{s.cautions}</span>
            </div>""", unsafe_allow_html=True)

        if fp:
            st.markdown("### 🔴 Primary Recommendations")
            st.caption("Strongest evidence — most directly aligned with your goal")
            for s in fp: render_card(s, "primary-card")
        if fs:
            st.markdown("### 🟡 Secondary Recommendations")
            st.caption("Beneficial additions once primary needs are covered")
            for s in fs: render_card(s, "secondary-card")
        if fg:
            st.markdown("### 🟢 General Wellness")
            st.caption("Broadly beneficial regardless of goal")
            for s in fg: render_card(s, "general-card")
        if not all_rec:
            st.info("No supplements recommended for your current profile. Focus on whole foods and rest.")

    # ════════════════════════════════
    # TAB 3 — UAE MARKET
    # ════════════════════════════════
    with tab3:
        st.markdown("### 🇦🇪 Where to Buy in the UAE")
        st.markdown(f'<div class="info-box">💰 Budget filter: <strong>{BUDGET_OPTIONS[budget]}</strong> — showing matching products below</div>', unsafe_allow_html=True)

        if not all_rec:
            st.warning("No supplements recommended yet. Fill in your profile and click Calculate first.")
        else:
            for supp_name in all_rec:
                info = get_uae_info(supp_name)
                if info:
                    brands = info["brands"]
                    if budget == "low":
                        brands = [b for b in brands if int(b["price_aed"].split("-")[0].strip()) < 100]

                    st.markdown(f"""
                    <div class="uae-card">
                        <strong style="color:#34d399; font-size:1.1rem;">🛒 {supp_name}</strong><br>
                        <span style="color:#94a3b8; font-size:0.85rem;">💡 {info["tip"]}</span>
                        <br><br><strong style="color:#e2e8f0;">Where to buy:</strong><br>
                    """, unsafe_allow_html=True)

                    store_html = ""
                    for store in info["stores"]:
                        url = store["url"] if store["url"].startswith("http") else "https://" + store["url"]
                        store_html += f'<a href="{url}" target="_blank" class="store-tag">🏪 {store["name"]}</a>'
                    st.markdown(store_html + "<br><br>", unsafe_allow_html=True)

                    if brands:
                        st.markdown("<strong style='color:#e2e8f0;'>Popular brands & prices:</strong>", unsafe_allow_html=True)
                        for b in brands:
                            url = b.get("url","#")
                            st.markdown(f'<span style="color:#cbd5e1;">• <a href="{url}" target="_blank" style="color:#a78bfa; text-decoration:none;"><strong>{b["brand"]}</strong></a> — {b["product"]}</span> &nbsp;<span class="price-tag">💰 {b["price_aed"]} AED</span><br>', unsafe_allow_html=True)
                    elif budget == "low":
                        st.markdown('<span style="color:#94a3b8;">*No budget-friendly options found. Try Mid-Range filter.*</span>', unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

    # ════════════════════════════════
    # TAB 4 — HEALTH
    # ════════════════════════════════
    with tab4:
        st.markdown("### 🏥 Health & Lifestyle Advisory")
        selected = [c for c in health_conditions if c != "none"]

        if not selected:
            st.markdown('<div class="success-box">✅ No health conditions selected. Recommendations are based on your fitness goal and activity level only.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="danger-box"><strong>⚠️ Please read all advisories carefully.</strong><br>FitSupport does NOT provide medical advice. Always consult a qualified healthcare professional before supplementing.</div>', unsafe_allow_html=True)
            for w in health_warns:
                st.markdown(f'<div class="warning-box">⚠️ {w}</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown("### 🏨 UAE Healthcare Resources")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
**Hospitals & Clinics**
- [Cleveland Clinic Abu Dhabi](https://www.clevelandclinicabudhabi.ae)
- [American Hospital Dubai](https://www.ahdubai.com)
- [Mediclinic UAE](https://www.mediclinic.ae)
- [Aster Hospitals UAE](https://www.asterhospitals.ae)
- [Saudi German Hospital](https://sghgroup.com)
            """)
        with c2:
            st.markdown("""
**Nutrition & Dietitian Services**
- [NMC Healthcare UAE](https://www.nmchealth.com)
- [Life Pharmacy](https://www.lifepharmacy.com)
- [Holland & Barrett UAE](https://www.hollandandbarrett.ae)
- [Boots UAE](https://www.boots.ae)
- [iHerb UAE](https://ae.iherb.com)
            """)

        st.divider()
        _, note = get_exclusions(dietary_preference)
        if note:
            st.markdown(f'<div class="success-box">🥗 {note}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-box">✅ No dietary restrictions applied to your recommendations.</div>', unsafe_allow_html=True)

    # ════════════════════════════════
    # TAB 5 — CHARTS
    # ════════════════════════════════
    with tab5:
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### 🍽️ Macronutrient Split")
            fig = go.Figure(data=[go.Pie(
                labels=["Protein","Carbohydrates","Fat"],
                values=[round(nutrition.protein_g*4), round(nutrition.carbs_g*4), round(nutrition.fat_g*9)],
                hole=0.55,
                marker=dict(colors=["#ec4899","#6366f1","#f59e0b"],
                           line=dict(color="rgba(0,0,0,0.3)", width=2)),
                textinfo="label+percent",
                textfont=dict(color="white", size=12),
            )])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0", family="Inter"),
                showlegend=False, margin=dict(t=20,b=20,l=20,r=20),
                annotations=[dict(text=f"<b>{nutrition.target_calories:,.0f}</b><br>kcal", x=0.5, y=0.5, font_size=14, font_color="white", showarrow=False)]
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown("#### ⚡ Energy Flow")
            fig2 = go.Figure(go.Bar(
                x=["BMR", "TDEE", "Target"],
                y=[nutrition.bmr, nutrition.tdee, nutrition.target_calories],
                marker=dict(
                    color=["#6366f1","#a855f7","#ec4899"],
                    line=dict(color="rgba(255,255,255,0.1)", width=1),
                ),
                text=[f"{nutrition.bmr:,.0f}",f"{nutrition.tdee:,.0f}",f"{nutrition.target_calories:,.0f}"],
                textposition="auto",
                textfont=dict(color="white", size=13, family="Inter"),
            ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.02)",
                font=dict(color="#e2e8f0", family="Inter"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="kcal/day", color="#94a3b8"),
                xaxis=dict(color="#94a3b8"),
                margin=dict(t=20,b=20,l=20,r=20),
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("#### 🎯 BMI Scale")
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=nutrition.bmi,
            number={"font":{"color":"#ffffff","size":44,"family":"Inter"}},
            gauge={
                "axis":{"range":[10,40],"tickcolor":"#94a3b8","tickfont":{"color":"#94a3b8"}},
                "bar":{"color":"#6366f1","thickness":0.3},
                "steps":[
                    {"range":[10,18.5],"color":"rgba(99,102,241,0.2)"},
                    {"range":[18.5,25], "color":"rgba(16,185,129,0.2)"},
                    {"range":[25,30],   "color":"rgba(245,158,11,0.2)"},
                    {"range":[30,40],   "color":"rgba(236,72,153,0.2)"},
                ],
                "threshold":{"line":{"color":"white","width":3},"thickness":0.75,"value":nutrition.bmi},
                "bgcolor":"rgba(0,0,0,0)",
            },
        ))
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0", family="Inter"),
            height=260, margin=dict(t=20,b=0,l=40,r=40),
        )
        _, cg, _ = st.columns([1,2,1])
        with cg: st.plotly_chart(fig3, use_container_width=True)

        bmi_labels = ["Underweight\n(<18.5)", "Normal\n(18.5–25)", "Overweight\n(25–30)", "Obese\n(>30)"]
        bmi_colours = ["#6366f1","#10b981","#f59e0b","#ec4899"]
        st.markdown('<p style="text-align:center; color:#94a3b8; font-size:0.85rem;">BMI Categories: Underweight &lt;18.5 · Normal 18.5–25 · Overweight 25–30 · Obese &gt;30</p>', unsafe_allow_html=True)

        st.markdown("#### 📊 Daily Macros in Grams")
        fig4 = go.Figure(go.Bar(
            x=["Protein","Carbohydrates","Fat"],
            y=[nutrition.protein_g, nutrition.carbs_g, nutrition.fat_g],
            marker=dict(
                color=["#ec4899","#6366f1","#f59e0b"],
                line=dict(color="rgba(255,255,255,0.1)", width=1),
            ),
            text=[f"{nutrition.protein_g}g",f"{nutrition.carbs_g}g",f"{nutrition.fat_g}g"],
            textposition="auto",
            textfont=dict(color="white", size=13),
        ))
        fig4.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.02)",
            font=dict(color="#e2e8f0", family="Inter"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="grams/day", color="#94a3b8"),
            xaxis=dict(color="#94a3b8"),
            margin=dict(t=10,b=10,l=20,r=20),
        )
        st.plotly_chart(fig4, use_container_width=True)

    # ════════════════════════════════
    # TAB 6 — AI INSIGHTS
    # ════════════════════════════════
    with tab6:
        st.markdown("### 🤖 AI Fitness Profile Prediction")
        st.markdown('<p style="color:#94a3b8;">Using a Decision Tree Classifier trained on 50 synthetic user profiles to predict your fitness archetype.</p>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ai-profile-card">
            <p style="color:#c4b5fd; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.15em; margin-bottom:0.5rem;">AI Predicted Profile</p>
            <h2 style="color:#ffffff; font-size:1.8rem; font-weight:800; margin:0.3rem 0;">{ai_result.predicted_profile}</h2>
            <p style="color:#a78bfa; font-size:1rem;">Confidence Score: <strong>{ai_result.confidence}%</strong></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 💡 Personalised AI Advice")
        st.markdown(f'<div class="rationale-box">{ai_result.advice}</div>', unsafe_allow_html=True)

        st.divider()

        st.markdown("#### 📊 Feature Importance — What Influenced This Prediction?")
        st.caption("Shows which of your inputs had the most impact on the AI decision (higher = more important).")

        features = list(ai_result.feature_importance.keys())
        values   = list(ai_result.feature_importance.values())

        fig_ai = go.Figure(go.Bar(
            x=values, y=features, orientation="h",
            marker=dict(
                color=["#6366f1","#a855f7","#ec4899","#f59e0b","#10b981"],
                line=dict(color="rgba(255,255,255,0.1)", width=1),
            ),
            text=[f"{v}%" for v in values],
            textposition="auto",
            textfont=dict(color="white"),
        ))
        fig_ai.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.02)",
            font=dict(color="#e2e8f0", family="Inter"),
            xaxis=dict(color="#94a3b8", title="Importance (%)"),
            yaxis=dict(color="#94a3b8"),
            margin=dict(t=10,b=10,l=10,r=10), height=220,
        )
        st.plotly_chart(fig_ai, use_container_width=True)

        st.markdown("#### 🔬 Model Explanation")
        st.markdown(f'<div class="rationale-box">{ai_result.model_explanation}</div>', unsafe_allow_html=True)

        with st.expander("ℹ️ About the AI Model"):
            st.markdown("""
**Model Type:** Decision Tree Classifier (scikit-learn)

**Why Decision Tree?**
A Decision Tree is the most explainable ML model available.
It works like a flowchart — at each step it asks a question about your
data (e.g. "Is BMI > 25?") and follows the matching branch until it
reaches a prediction. Every decision is fully traceable.

**Training Data:** 50 synthetic user profiles across 5 fitness archetypes.
Synthetic data was used to avoid ethical issues with real personal data.

**Features Used:** Age · BMI · Activity Level · Fitness Goal · Weight

**Reference:** Breiman et al. (1984). *Classification and Regression Trees.* Wadsworth & Brooks.
            """)

    # ════════════════════════════════
    # TAB 7 — FEEDBACK
    # ════════════════════════════════
    with tab7:
        st.markdown("### 📝 Usability Feedback")
        st.markdown('<p style="color:#94a3b8;">Your anonymous feedback helps improve FitSupport. No personal information is stored.</p>', unsafe_allow_html=True)

        with st.form("feedback_form"):
            usability  = st.slider("How easy was the system to use?",          1, 5, 3)
            accuracy   = st.slider("How accurate do the results feel?",         1, 5, 3)
            usefulness = st.slider("How useful was the information provided?",   1, 5, 3)
            comments   = st.text_area("Additional comments (optional)", max_chars=500,
                                       placeholder="Tell us what you thought...")
            if st.form_submit_button("✅ Submit Feedback", type="primary"):
                save_feedback(session_id, usability, accuracy, usefulness, comments)
                st.success("✅ Thank you! Your anonymous feedback has been recorded.")
                try:
                    send_feedback_email(st.secrets["SENDER_EMAIL"], st.secrets["APP_PASSWORD"],
                                       st.secrets["RECEIVER_EMAIL"], usability, accuracy,
                                       usefulness, comments, session_id)
                except Exception:
                    pass

# ── Landing Page ─────────────────────────────────────────────
else:
    st.markdown("""
    <div style="text-align:center; padding:2rem 0 3rem 0;">
        <h3 style="color:#c4b5fd; font-size:1.1rem; font-weight:400; letter-spacing:0.05em;">
            Fill in your profile on the left and click Calculate to get started
        </h3>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("📊", "Nutrition Engine", "Calculates BMR, TDEE, macros, and hydration using peer-reviewed scientific formulas."),
        ("💊", "Supplement Engine", "Rule-based recommendations personalised to your goal, diet type, and activity level."),
        ("🇦🇪", "UAE Market", "Direct buy links and AED prices for every supplement at UAE stores."),
        ("🤖", "AI Insights", "Decision Tree ML model predicts your fitness profile and gives personalised advice."),
    ]
    for col, (icon, title, desc) in zip([c1,c2,c3,c4], cards):
        with col:
            st.markdown(f"""
            <div class="landing-feature-card">
                <div class="icon">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; color:rgba(255,255,255,0.2); font-size:0.8rem; padding-top:1rem; border-top: 1px solid rgba(255,255,255,0.05);">
        FitSupport · LJMU BSc Computer Science Final Year Project · Educational purposes only · PLEASE NOTE THAT THIS IS NOT MEDICAL ADVICE
    </div>
    """, unsafe_allow_html=True)