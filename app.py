"""
Skill Half-Life in the Age of AI
Research-Grade Analytical Dashboard | Streamlit

This dashboard analyzes how Artificial Intelligence impacts the longevity,
relevance, and reskilling dynamics of professional skills across industries.
Designed for academic panels, AI researchers, and policy evaluators.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------
# Page Configuration
# ------------------------------------------------------
st.set_page_config(
    page_title="Skill Half-Life in the Age of AI",
    layout="wide"
)

# ------------------------------------------------------
# Data Loading
# ------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("skill_half_life_ai.csv")

df = load_data()

# ------------------------------------------------------
# Feature Engineering
# ------------------------------------------------------
df["ai_exposure_band"] = pd.cut(
    df["ai_exposure_level"],
    bins=[0, 40, 70, 100],
    labels=["Low", "Medium", "High"]
)

df["automation_risk_band"] = pd.cut(
    df["automation_risk"],
    bins=[0, 40, 70, 100],
    labels=["Low", "Medium", "High"]
)

# ------------------------------------------------------
# Global Filters
# ------------------------------------------------------
st.sidebar.header("Analytical Scope")

category_filter = st.sidebar.multiselect(
    "Skill Category",
    sorted(df["skill_category"].unique()),
    default=sorted(df["skill_category"].unique())
)

industry_filter = st.sidebar.multiselect(
    "Industry",
    sorted(df["industry"].unique()),
    default=sorted(df["industry"].unique())
)

filtered_df = df[
    (df["skill_category"].isin(category_filter)) &
    (df["industry"].isin(industry_filter))
]

# ======================================================
# SECTION 1 — Research Context
# ======================================================
st.title("Skill Half-Life in the Age of AI")

st.markdown("""
### Research Context

The accelerating integration of Artificial Intelligence into knowledge work is fundamentally
altering how long skills remain economically and socially relevant.
This dashboard models **skill half-life**—the estimated time for a skill’s value to decline by 50%—
under varying levels of AI exposure and automation risk.

**Why this matters globally**
- Education systems must adapt faster than traditional curriculum cycles
- Workforce reskilling policies require evidence-based prioritization
- AI adoption without human-centered planning risks structural displacement

**Decisions this dashboard supports**
- Identifying skills requiring urgent reskilling
- Comparing vulnerability across industries and categories
- Designing resilient learning and workforce strategies
""")

st.divider()

# ======================================================
# SECTION 2 — Key Research KPIs
# ======================================================
st.markdown("## Key Research KPIs")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Mean Skill Half-Life (Years)",
    round(filtered_df["skill_half_life_years"].mean(), 2)
)

k2.metric(
    "High AI Exposure Skills (%)",
    f"{round((filtered_df.ai_exposure_level > 70).mean() * 100, 1)}%"
)

k3.metric(
    "Mean Reskilling Interval (Years)",
    round(filtered_df["reskilling_frequency_years"].mean(), 2)
)

k4.metric(
    "High Automation Risk Skills",
    int((filtered_df.automation_risk > 70).sum())
)

st.divider()

# ======================================================
# SECTION 3 — Core Analytical Visuals
# ======================================================
st.markdown("## Core Analytical Findings")

fig1 = px.bar(
    filtered_df.groupby("skill_category", as_index=False)
    .skill_half_life_years.mean(),
    x="skill_half_life_years",
    y="skill_category",
    orientation="h",
    title="Average Skill Half-Life by Skill Category",
    labels={"skill_half_life_years": "Years", "skill_category": "Skill Category"}
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.scatter(
    filtered_df,
    x="ai_exposure_level",
    y="skill_half_life_years",
    size="current_market_demand",
    color="skill_category",
    title="AI Exposure vs Skill Half-Life",
    labels={"ai_exposure_level": "AI Exposure Level", "skill_half_life_years": "Years"}
)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.histogram(
    filtered_df,
    x="automation_risk",
    nbins=10,
    title="Distribution of Automation Risk",
    labels={"automation_risk": "Automation Risk Level"}
)
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.scatter(
    filtered_df,
    x="automation_risk",
    y="current_market_demand",
    size="skill_half_life_years",
    color="skill_category",
    title="Market Demand vs Automation Risk",
    labels={"automation_risk": "Automation Risk", "current_market_demand": "Market Demand"}
)
st.plotly_chart(fig4, use_container_width=True)

fig5 = px.box(
    filtered_df,
    x="skill_category",
    y="reskilling_frequency_years",
    title="Reskilling Frequency by Skill Category",
    labels={"reskilling_frequency_years": "Years"}
)
st.plotly_chart(fig5, use_container_width=True)

industry_exposure = (
    filtered_df.groupby(["industry", "ai_exposure_band"])
    .size()
    .reset_index(name="count")
)

fig6 = px.bar(
    industry_exposure,
    x="industry",
    y="count",
    color="ai_exposure_band",
    title="Industry Exposure to AI-Driven Skill Decay",
    labels={"count": "Number of Skills"}
)
st.plotly_chart(fig6, use_container_width=True)

# ======================================================
# SECTION 4 — Insight Synthesis
# ======================================================
st.markdown("""
## Insight Synthesis

The analysis indicates that skill vulnerability is driven more by **rate of AI scalability**
than by current demand.
Cognitive and creative skills show greater resilience, while several high-demand technical
skills exhibit rapid decay.
Reskilling frequency emerges as a structural pressure point rather than an individual choice.
""")

# ======================================================
# SECTION 5 — Limitations & Ethics
# ======================================================
st.markdown("""
## Limitations & Ethical Notes

- Data is synthetic and indicative, not predictive
- Cultural, regional, and economic differences are not modeled
- Automation risk does not imply inevitability of displacement
- Human judgment remains critical in AI-augmented systems

This dashboard informs decisions; it does not automate them.
""")
