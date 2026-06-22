"""Batter Analyzer — individual batting performance."""

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.analytics import get_batter_phase_stats, get_batter_run_distribution
from utils.charts import apply_chart_layout, bar_chart, phase_bar_chart, pie_chart
from utils.components import page_header, render_footer, render_sidebar_branding, setup_page
from utils.data_loader import get_batters, get_summary_stats, load_deliveries, load_matches

setup_page("Batter Analyzer", "🏏")

deliveries = load_deliveries()
matches = load_matches()
summary = get_summary_stats(deliveries, matches)
render_sidebar_branding(summary)
batters = get_batters(deliveries)

page_header(
    "Batter Analyzer",
    "Deep-dive into individual batting performance with phase-wise breakdowns, scoring patterns, and over-by-over trends.",
    "Performance Intelligence",
)

batter = st.selectbox(
    "Select Batter",
    batters,
    index=batters.index("V Kohli") if "V Kohli" in batters else 0,
)

batter_data = deliveries[deliveries["batter"] == batter]
runs = int(batter_data["batsman_runs"].sum())
balls = len(batter_data)
dismissals = int(batter_data["is_wicket"].sum())
fours = int((batter_data["batsman_runs"] == 4).sum())
sixes = int((batter_data["batsman_runs"] == 6).sum())
strike_rate = round((runs / balls) * 100, 2) if balls else 0
average = round(runs / dismissals, 2) if dismissals else runs

k1, k2, k3, k4, k5, k6 = st.columns(6, gap="medium")
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

st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

tab_phase, tab_scoring, tab_timeline = st.tabs(
    ["📊 Phase Analysis", "🎯 Scoring Breakdown", "📈 Over-by-Over"]
)

with tab_phase:
    phase_stats = get_batter_phase_stats(batter_data)
    col1, col2 = st.columns([3, 2], gap="large")
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
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.plotly_chart(
            bar_chart(pd.Series(scoring), f"{batter} — Ball Outcomes"),
            use_container_width=True,
        )
    with col2:
        st.markdown(
            '<div class="glass-panel"><div class="glass-panel-header">Scoring Distribution</div>',
            unsafe_allow_html=True,
        )
        for label, count in scoring.items():
            pct = round(count / balls * 100, 1) if balls else 0
            st.progress(min(pct / 100, 1.0), text=f"{label}: {count:,} ({pct}%)")
        st.markdown("</div>", unsafe_allow_html=True)

with tab_timeline:
    over_runs = batter_data.groupby("over")["batsman_runs"].sum().reset_index()
    fig = px.area(
        over_runs,
        x="over",
        y="batsman_runs",
        color_discrete_sequence=["#E63946"],
        labels={"over": "Over", "batsman_runs": "Runs"},
    )
    fig.update_traces(
        fillcolor="rgba(230,57,70,0.15)",
        line=dict(width=2.5, color="#E63946"),
    )
    st.plotly_chart(
        apply_chart_layout(fig, f"{batter} — Runs by Over"),
        use_container_width=True,
    )

render_footer()
