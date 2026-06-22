"""Match Insights — tournament-level analytics dashboard."""

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.analytics import get_match_insights
from utils.charts import apply_chart_layout, bar_chart, pie_chart
from utils.components import info_banner, page_header, render_footer, render_sidebar_branding, setup_page
from utils.data_loader import get_summary_stats, load_deliveries, load_matches

setup_page("Match Insights", "📋")

deliveries = load_deliveries()
matches = load_matches()
summary = get_summary_stats(deliveries, matches)
render_sidebar_branding(summary)
insights = get_match_insights(matches)

page_header(
    "Match Insights Dashboard",
    "Tournament-level analytics covering venues, teams, season trends, and toss impact across the IPL archive.",
    "Tournament Intelligence",
)

k1, k2, k3, k4 = st.columns(4, gap="medium")
venue_label = insights["top_venue"]
if len(venue_label) > 18:
    venue_label = venue_label[:18] + "…"
with k1:
    st.metric("Total Matches", f"{insights['total_completed']:,}")
with k2:
    st.metric("Avg Target", insights["avg_target"])
with k3:
    st.metric("Toss → Win Rate", f"{insights['toss_win_pct']}%")
with k4:
    st.metric("Top Venue", venue_label)

st.markdown(
    info_banner(f"🏅 Most Player of the Match — <strong>{insights['most_pom']}</strong>"),
    unsafe_allow_html=True,
)

tab_venue, tab_team, tab_season, tab_toss = st.tabs(
    ["🏟️ Venues", "🏏 Teams", "📅 Seasons", "🪙 Toss Impact"]
)

with tab_venue:
    venue_counts = matches["venue"].value_counts().head(10)
    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        st.plotly_chart(bar_chart(venue_counts, "Top 10 Venues by Matches"), use_container_width=True)
    with col2:
        venue_runs = (
            deliveries.merge(matches[["id", "venue"]], left_on="match_id", right_on="id")
            .groupby("venue")["batsman_runs"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )
        st.plotly_chart(
            bar_chart(venue_runs.round(1), "Avg Runs per Delivery"),
            use_container_width=True,
        )

with tab_team:
    win_data = {
        team: int((matches["winner"] == team).sum())
        for team in pd.concat([matches["team1"], matches["team2"]]).unique()
    }
    win_series = pd.Series(win_data).sort_values(ascending=False).head(10)
    st.plotly_chart(bar_chart(win_series, "Wins by Team"), use_container_width=True)

with tab_season:
    season_matches = matches.groupby("season").size()
    fig = px.line(
        x=season_matches.index.astype(str),
        y=season_matches.values,
        markers=True,
        labels={"x": "Season", "y": "Matches"},
    )
    fig.update_traces(
        line=dict(color="#E63946", width=3),
        marker=dict(size=9, color="#F4A261", line=dict(width=2, color="#060A14")),
        fill="tozeroy",
        fillcolor="rgba(230,57,70,0.08)",
    )
    st.plotly_chart(
        apply_chart_layout(fig, "Matches per Season"),
        use_container_width=True,
    )

with tab_toss:
    completed = matches.dropna(subset=["winner", "toss_winner"])
    toss_win = int((completed["toss_winner"] == completed["winner"]).sum())
    toss_lose = len(completed) - toss_win
    st.plotly_chart(
        pie_chart(
            ["Toss Winner Won", "Toss Winner Lost"],
            [toss_win, toss_lose],
            "Toss Impact on Match Outcome",
        ),
        use_container_width=True,
    )

    bat_first = completed[completed["toss_decision"] == "field"]
    bat_second = completed[completed["toss_decision"] == "bat"]
    if len(bat_first) and len(bat_second):
        c1, c2 = st.columns(2, gap="large")
        with c1:
            bf_win = (bat_first["toss_winner"] == bat_first["winner"]).mean() * 100
            st.metric("Chose to Bowl — Toss Win %", f"{bf_win:.1f}%")
        with c2:
            bs_win = (bat_second["toss_winner"] == bat_second["winner"]).mean() * 100
            st.metric("Chose to Bat — Toss Win %", f"{bs_win:.1f}%")

render_footer()
