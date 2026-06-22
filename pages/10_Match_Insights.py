"""Match Insights — ball-by-ball analysis for a selected match."""

import streamlit as st

from utils.analytics import (
    get_match_deliveries,
    get_match_top_performers,
    get_partnerships,
    get_runs_per_over,
    get_wickets_timeline,
)
from utils.charts import cumulative_runs_chart, runs_per_over_chart, wickets_timeline_chart
from utils.components import info_banner, page_header, render_footer, render_sidebar_branding, setup_page
from utils.data_loader import get_match_options, get_summary_stats, load_deliveries, load_matches

setup_page("Match Insights", "📊")

deliveries = load_deliveries()
matches = load_matches()
summary = get_summary_stats(deliveries, matches)
match_options = get_match_options(matches)
render_sidebar_branding(summary)

page_header(
    "Match Insights Dashboard",
    "Deep ball-by-ball analysis — runs per over, wicket timeline, partnerships, and top performers.",
    "Match Intelligence",
)

# Match selector
labels = match_options["label"].tolist()
ids = match_options["id"].tolist()
selected_label = st.selectbox("Select Match", labels)
match_id = int(ids[labels.index(selected_label)])

match_meta = matches[matches["id"] == match_id].iloc[0]
match_data = get_match_deliveries(deliveries, match_id)

if match_data.empty:
    st.error(f"No delivery data found for match #{match_id}.")
    st.stop()

performers = get_match_top_performers(match_data)
runs_over = get_runs_per_over(match_data)
wickets = get_wickets_timeline(match_data)

st.markdown(
    info_banner(
        f"📍 <strong>{match_meta['venue']}</strong> · "
        f"{match_meta['team1']} vs {match_meta['team2']} · "
        f"Winner: <strong>{match_meta.get('winner', 'N/A')}</strong>"
    ),
    unsafe_allow_html=True,
)

k1, k2, k3, k4 = st.columns(4, gap="medium")
with k1:
    st.metric("Total Deliveries", len(match_data))
with k2:
    st.metric("Total Runs", int(match_data["total_runs"].sum()))
with k3:
    st.metric("Top Batter", performers["top_batter"])
with k4:
    st.metric("Top Bowler", performers["top_bowler"])

st.caption(
    f"Top batter: {performers['top_batter_runs']} runs · "
    f"Top bowler: {performers['top_bowler_wickets']} wickets"
)

tab_runs, tab_wickets, tab_partnerships = st.tabs(
    ["📈 Runs Analysis", "🎯 Wickets Timeline", "🤝 Partnerships"]
)

with tab_runs:
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.plotly_chart(
            runs_per_over_chart(runs_over, f"Match #{match_id} — Runs per Over"),
            use_container_width=True,
        )
    with c2:
        st.plotly_chart(
            cumulative_runs_chart(runs_over, f"Match #{match_id} — Score Progression"),
            use_container_width=True,
        )

with tab_wickets:
    st.plotly_chart(
        wickets_timeline_chart(wickets, f"Match #{match_id} — Wicket Fall Timeline"),
        use_container_width=True,
    )
    if not wickets.empty:
        display = wickets[["inning", "over", "player_dismissed", "bowler"]].copy()
        display.columns = ["Inning", "Over", "Batter Out", "Bowler"]
        st.dataframe(display, use_container_width=True, hide_index=True)

with tab_partnerships:
    inning_choice = st.radio("Select Inning", [1, 2], horizontal=True)
    partnerships = get_partnerships(match_data, inning_choice)

    if partnerships.empty:
        st.info("No partnership data available for this inning.")
    else:
        c1, c2 = st.columns([2, 1], gap="large")
        with c1:
            from utils.charts import bar_chart
            top_part = partnerships.head(8).copy()
            top_part["pair"] = top_part["batter_1"] + " & " + top_part["batter_2"]
            st.plotly_chart(
                bar_chart(
                    top_part.set_index("pair")["runs"],
                    f"Inning {inning_choice} — Top Partnerships",
                    horizontal=True,
                ),
                use_container_width=True,
            )
        with c2:
            display = partnerships.head(10)[["batter_1", "batter_2", "runs", "balls"]].copy()
            display.columns = ["Batter 1", "Batter 2", "Runs", "Balls"]
            st.dataframe(display, use_container_width=True, hide_index=True)

render_footer()
