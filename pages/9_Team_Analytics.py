"""Team Analytics Dashboard — franchise performance intelligence."""

import plotly.express as px
import streamlit as st

from utils.analytics import get_team_profile
from utils.charts import apply_chart_layout, bar_chart
from utils.components import info_banner, page_header, render_footer, render_sidebar_branding, setup_page
from utils.data_loader import (
    get_bowler_stats,
    get_summary_stats,
    get_team_analytics,
    get_teams,
    load_deliveries,
    load_matches,
)

setup_page("Team Analytics", "🏏")

deliveries = load_deliveries()
matches = load_matches()
summary = get_summary_stats(deliveries, matches)
bowler_stats = get_bowler_stats(deliveries)
teams = get_teams(matches)
team_df = get_team_analytics(matches, deliveries)
render_sidebar_branding(summary)

page_header(
    "Team Analytics Dashboard",
    "Franchise-level performance — win rates, top performers, and season-by-season trends.",
    "Team Intelligence",
)

team = st.selectbox("Select Team", teams)

profile = get_team_profile(team, matches, deliveries, bowler_stats)

k1, k2, k3, k4 = st.columns(4, gap="medium")
with k1:
    st.metric("Matches Played", profile["matches_played"])
with k2:
    st.metric("Wins", profile["wins"])
with k3:
    st.metric("Win Percentage", f"{profile['win_pct']}%")
with k4:
    st.metric("Total Runs", f"{profile['total_runs']:,}")

st.markdown(
    info_banner(
        f"⭐ Top Batter: <strong>{profile['top_batter']}</strong> ({profile['top_batter_runs']:,} runs) · "
        f"Top Bowler: <strong>{profile['top_bowler']}</strong> ({profile['top_bowler_wickets']} wickets)"
    ),
    unsafe_allow_html=True,
)

tab_perf, tab_compare, tab_leaders = st.tabs(
    ["📈 Season Performance", "🏆 Team Comparison", "👥 Top Performers"]
)

with tab_perf:
    season_df = profile["season_performance"]
    if not season_df.empty:
        fig = px.bar(
            season_df,
            x="season",
            y="wins",
            color="wins",
            color_continuous_scale=[[0, "#132038"], [0.5, "#E63946"], [1, "#F4A261"]],
            labels={"season": "Season", "wins": "Wins"},
        )
        fig.update_layout(coloraxis_showscale=False)
        fig.update_traces(marker=dict(cornerradius=6))
        st.plotly_chart(
            apply_chart_layout(fig, f"{team} — Wins by Season"),
            use_container_width=True,
        )
    else:
        st.info("No season data available for this team.")

with tab_compare:
    compare_df = team_df.set_index("team")[["wins", "win_pct"]].sort_values("wins", ascending=False).head(10)
    st.plotly_chart(bar_chart(compare_df["wins"], "Top 10 Teams by Wins"), use_container_width=True)

    win_pct_series = team_df.set_index("team")["win_pct"].sort_values(ascending=False).head(10)
    st.plotly_chart(
        bar_chart(win_pct_series, "Win Percentage by Team (Top 10)"),
        use_container_width=True,
    )

with tab_leaders:
    bat = deliveries[deliveries["batting_team"] == team]
    bowl = deliveries[deliveries["bowling_team"] == team]

    c1, c2 = st.columns(2, gap="large")
    with c1:
        top_batters = bat.groupby("batter")["batsman_runs"].sum().sort_values(ascending=False).head(10)
        st.plotly_chart(
            bar_chart(top_batters, f"{team} — Top Batters", horizontal=True),
            use_container_width=True,
        )
    with c2:
        top_bowlers = bowl.groupby("bowler")["is_wicket"].sum().sort_values(ascending=False).head(10)
        st.plotly_chart(
            bar_chart(top_bowlers, f"{team} — Top Bowlers", horizontal=True),
            use_container_width=True,
        )

render_footer()
