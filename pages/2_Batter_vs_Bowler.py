"""Batter vs Bowler — head-to-head rivalry analysis."""

import streamlit as st
import plotly.express as px

from utils.analytics import get_head_to_head
from utils.charts import bar_chart, pie_chart
from utils.components import render_footer, render_sidebar_branding, section_header, setup_page
from utils.data_loader import get_batters, get_bowlers, load_deliveries

setup_page("Batter vs Bowler", "⚔️")
render_sidebar_branding()

deliveries = load_deliveries()
batters = get_batters(deliveries)
bowlers = get_bowlers(deliveries)

section_header(
    "⚔️ Batter vs Bowler Analyzer",
    "Explore head-to-head statistics between any batter and bowler combination.",
)

col_sel1, col_sel2 = st.columns(2)
with col_sel1:
    batter = st.selectbox("Select Batter", batters, key="h2h_batter")
with col_sel2:
    bowler = st.selectbox("Select Bowler", bowlers, key="h2h_bowler")

data = get_head_to_head(deliveries, batter, bowler)
runs = int(data["batsman_runs"].sum())
balls = len(data)
dismissals = int(data["is_wicket"].sum())
strike_rate = round((runs / balls) * 100, 2) if balls else 0
dots = int((data["batsman_runs"] == 0).sum()) if balls else 0
boundaries = int(data["batsman_runs"].isin([4, 6]).sum()) if balls else 0

if balls == 0:
    st.warning(f"No recorded deliveries between **{batter}** and **{bowler}**.")
    st.stop()

# KPI row
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Runs Scored", f"{runs:,}")
with k2:
    st.metric("Balls Faced", f"{balls:,}")
with k3:
    st.metric("Strike Rate", strike_rate)
with k4:
    st.metric("Dismissals", dismissals)
with k5:
    st.metric("Boundaries", boundaries)

st.markdown("---")

tab_viz, tab_table = st.tabs(["📊 Visualizations", "📋 Ball-by-Ball"])

with tab_viz:
    v1, v2 = st.columns(2)
    with v1:
        over_runs = data.groupby("over")["batsman_runs"].sum()
        st.plotly_chart(
            bar_chart(over_runs, f"Runs per Over — {batter} vs {bowler}"),
            use_container_width=True,
        )
    with v2:
        outcome_labels = ["Dots", "Singles+", "Boundaries", "Wickets"]
        singles = balls - dots - boundaries - dismissals
        outcome_values = [dots, max(singles, 0), boundaries, dismissals]
        st.plotly_chart(
            pie_chart(outcome_labels, outcome_values, "Ball Outcome Split"),
            use_container_width=True,
        )

    run_values = data["batsman_runs"].value_counts().sort_index()
    fig = px.bar(
        x=run_values.index.astype(str),
        y=run_values.values,
        labels={"x": "Runs off Bat", "y": "Count"},
        color=run_values.values,
        color_continuous_scale=["#1D2951", "#C41E3A", "#F59E0B"],
    )
    fig.update_layout(
        title=dict(text="Runs Distribution per Delivery", font=dict(color="#F8FAFC")),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0"), coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True)

with tab_table:
    display_cols = ["over", "ball", "batsman_runs", "total_runs", "is_wicket", "dismissal_kind"]
    available = [c for c in display_cols if c in data.columns]
    styled = data[available].copy()
    styled["is_wicket"] = styled["is_wicket"].map({1: "✓", 0: ""})
    st.dataframe(
        styled.sort_values(["over", "ball"]),
        use_container_width=True,
        hide_index=True,
        height=400,
    )

render_footer()
