"""Venue Analytics Dashboard — stadium-level IPL intelligence."""

import streamlit as st

from utils.charts import bar_chart, pie_chart
from utils.components import page_header, render_footer, render_sidebar_branding, setup_page
from utils.data_loader import (
    get_inning_totals,
    get_summary_stats,
    get_venue_analytics,
    get_venues,
    load_deliveries,
    load_matches,
)

setup_page("Venue Analytics", "🏟️")

deliveries = load_deliveries()
matches = load_matches()
summary = get_summary_stats(deliveries, matches)
inning_totals = get_inning_totals(deliveries, matches)
venue_df = get_venue_analytics(matches, inning_totals)
venues = get_venues(matches)
render_sidebar_branding(summary)

page_header(
    "Venue Analytics Dashboard",
    "Stadium-level scoring patterns, win rates, and historical performance across every IPL venue.",
    "Venue Intelligence",
)

# Filters
f1, f2 = st.columns([2, 1], gap="large")
with f1:
    venue_filter = st.multiselect(
        "Filter Venues",
        venues,
        default=venues[:5] if len(venues) >= 5 else venues,
    )
with f2:
    min_matches = st.slider("Min Matches Played", 1, 50, 5)

filtered = venue_df[venue_df["venue"].isin(venue_filter)] if venue_filter else venue_df
filtered = filtered[filtered["matches_played"] >= min_matches]

if filtered.empty:
    st.warning("No venues match the selected filters.")
    st.stop()

selected = st.selectbox("Inspect Venue", filtered["venue"].tolist())

venue_row = filtered[filtered["venue"] == selected].iloc[0]

k1, k2, k3, k4, k5 = st.columns(5, gap="medium")
with k1:
    st.metric("Avg Score", venue_row["avg_score"])
with k2:
    st.metric("Highest Score", int(venue_row["highest_score"]))
with k3:
    st.metric("Lowest Score", int(venue_row["lowest_score"]))
with k4:
    st.metric("Matches Played", int(venue_row["matches_played"]))
with k5:
    st.metric("Toss Win %", f"{venue_row['win_pct']:.1f}%")

tab_charts, tab_ranking = st.tabs(["📊 Visualizations", "📋 Venue Ranking"])

with tab_charts:
    c1, c2 = st.columns(2, gap="large")
    with c1:
        top_avg = filtered.set_index("venue")["avg_score"].sort_values(ascending=False).head(10)
        st.plotly_chart(bar_chart(top_avg, "Average Innings Score by Venue"), use_container_width=True)
    with c2:
        top_matches = filtered.set_index("venue")["matches_played"].sort_values(ascending=False).head(8)
        st.plotly_chart(
            pie_chart(list(top_matches.index), list(top_matches.values), "Match Distribution"),
            use_container_width=True,
        )

    score_range = filtered.set_index("venue")[["highest_score", "lowest_score"]].head(10)
    import plotly.graph_objects as go
    from utils.charts import apply_chart_layout, COLORS
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Highest", x=score_range.index, y=score_range["highest_score"],
                         marker_color=COLORS["gold"], marker=dict(cornerradius=5)))
    fig.add_trace(go.Bar(name="Lowest", x=score_range.index, y=score_range["lowest_score"],
                         marker_color=COLORS["sky"], marker=dict(cornerradius=5)))
    fig.update_layout(barmode="group")
    st.plotly_chart(apply_chart_layout(fig, "Score Range by Venue"), use_container_width=True)

with tab_ranking:
    display = filtered[
        ["venue", "matches_played", "avg_score", "highest_score", "lowest_score", "win_pct"]
    ].copy()
    display.columns = ["Venue", "Matches", "Avg Score", "Highest", "Lowest", "Toss Win %"]
    display = display.sort_values("Matches", ascending=False).reset_index(drop=True)
    display.index = display.index + 1
    display.index.name = "Rank"
    st.dataframe(display, use_container_width=True)

render_footer()
