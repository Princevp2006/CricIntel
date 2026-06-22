"""Batter Analyzer — individual batting performance."""

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.analytics import get_batter_phase_stats, get_batter_run_distribution
from utils.charts import bar_chart, phase_bar_chart, pie_chart
from utils.components import render_footer, render_sidebar_branding, section_header, setup_page
from utils.data_loader import get_batters, load_deliveries

setup_page("Batter Analyzer", "🏏")
render_sidebar_branding()

deliveries = load_deliveries()
batters = get_batters(deliveries)

section_header(
    "🏏 Batter Analyzer",
    "Analyze individual batting performance with phase-wise breakdowns and scoring patterns.",
)

batter = st.selectbox("Select Batter", batters, index=batters.index("V Kohli") if "V Kohli" in batters else 0)

batter_data = deliveries[deliveries["batter"] == batter]
runs = int(batter_data["batsman_runs"].sum())
balls = len(batter_data)
dismissals = int(batter_data["is_wicket"].sum())
fours = int((batter_data["batsman_runs"] == 4).sum())
sixes = int((batter_data["batsman_runs"] == 6).sum())
strike_rate = round((runs / balls) * 100, 2) if balls else 0
average = round(runs / dismissals, 2) if dismissals else runs

# KPI cards
k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    st.metric("Runs", f"{runs:,}")
with k2:
    st.metric("Balls Faced", f"{balls:,}")
with k3:
    st.metric("Strike Rate", strike_rate)
with k4:
    st.metric("Average", average)
with k5:
    st.metric("Fours", fours)
with k6:
    st.metric("Sixes", sixes)

st.markdown("---")

tab_phase, tab_scoring, tab_timeline = st.tabs(
    ["📊 Phase Analysis", "🎯 Scoring Breakdown", "📈 Over-by-Over"]
)

with tab_phase:
    phase_stats = get_batter_phase_stats(batter_data)
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(
            phase_bar_chart(phase_stats, f"{batter} — Runs by Phase"),
            use_container_width=True,
        )
    with col2:
        st.plotly_chart(
            pie_chart(list(phase_stats.keys()), list(phase_stats.values()), "Phase Distribution"),
            use_container_width=True,
        )

with tab_scoring:
    scoring = get_batter_run_distribution(batter_data)
    col1, col2 = st.columns(2)
    with col1:
        scoring_series = pd.Series(scoring)
        st.plotly_chart(
            bar_chart(scoring_series, f"{batter} — Ball Outcomes"),
            use_container_width=True,
        )
    with col2:
        st.markdown("#### Scoring Summary")
        for label, count in scoring.items():
            pct = round(count / balls * 100, 1) if balls else 0
            st.progress(min(pct / 100, 1.0), text=f"{label}: {count:,} ({pct}%)")

with tab_timeline:
    over_runs = (
        batter_data.groupby("over")["batsman_runs"]
        .sum()
        .reset_index()
    )
    fig = px.area(
        over_runs, x="over", y="batsman_runs",
        color_discrete_sequence=["#C41E3A"],
        labels={"over": "Over", "batsman_runs": "Runs"},
    )
    fig.update_layout(
        title=dict(text=f"{batter} — Cumulative Runs by Over", font=dict(color="#F8FAFC")),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0"),
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,0.15)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.15)")
    st.plotly_chart(fig, use_container_width=True)

render_footer()
