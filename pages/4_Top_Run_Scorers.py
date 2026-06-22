"""Top Run Scorers — interactive leaderboard."""

import streamlit as st

from utils.charts import bar_chart, pie_chart
from utils.components import page_header, render_footer, render_sidebar_branding, setup_page
from utils.data_loader import get_summary_stats, load_deliveries, load_matches

setup_page("Top Run Scorers", "📊")

deliveries = load_deliveries()
matches = load_matches()
summary = get_summary_stats(deliveries, matches)
render_sidebar_branding(summary)

page_header(
    "Top Run Scorers",
    "Interactive leaderboard visualizations with configurable depth, run share analysis, and detailed stat tables.",
    "Leaderboard",
)

top_n = st.slider("Number of batters", min_value=5, max_value=20, value=10, step=1)

top_batters = (
    deliveries.groupby("batter")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
)

tab_bar, tab_pie, tab_table = st.tabs(["📊 Bar Chart", "🥧 Distribution", "📋 Table"])

with tab_bar:
    st.plotly_chart(
        bar_chart(top_batters, f"Top {top_n} Run Scorers — IPL", horizontal=True),
        use_container_width=True,
    )

with tab_pie:
    top5 = top_batters.head(5)
    others = top_batters.iloc[5:].sum() if len(top_batters) > 5 else 0
    labels = list(top5.index)
    values = list(top5.values)
    if others > 0:
        labels.append("Others")
        values.append(others)
    st.plotly_chart(
        pie_chart(labels, values, f"Run Share — Top {min(5, top_n)} vs Rest"),
        use_container_width=True,
    )

with tab_table:
    table_df = top_batters.reset_index()
    table_df.columns = ["Batter", "Total Runs"]
    table_df.index = range(1, len(table_df) + 1)
    table_df.index.name = "Rank"
    balls = deliveries.groupby("batter")["ball"].count().reindex(top_batters.index)
    table_df["Balls Faced"] = balls.values
    table_df["Strike Rate"] = (table_df["Total Runs"] / table_df["Balls Faced"] * 100).round(2)
    st.dataframe(table_df, use_container_width=True)

render_footer()
