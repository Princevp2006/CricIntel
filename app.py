"""CricIntel — AI-Powered Cricket Analytics Platform."""

import streamlit as st

from utils.analytics import get_match_insights, get_top_performers
from utils.charts import bar_chart, pie_chart
from utils.components import (
    inject_styles,
    kpi_card,
    performer_card_html,
    render_footer,
    render_sidebar_branding,
)
from utils.data_loader import (
    get_player_stats,
    get_summary_stats,
    load_deliveries,
    load_matches,
)

st.set_page_config(
    page_title="CricIntel | Home",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_styles()
render_sidebar_branding()

deliveries = load_deliveries()
matches = load_matches()
player_stats = get_player_stats(deliveries)
summary = get_summary_stats(deliveries, matches)
insights = get_match_insights(matches)
performers = get_top_performers(player_stats)

# Hero
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-badge">IPL Analytics · Machine Learning</div>
        <h1 class="hero-title">🏏 CricIntel</h1>
        <p class="hero-subtitle">AI-Powered Cricket Analytics Platform</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "Unlock deep insights from IPL ball-by-ball data — player performance, "
    "head-to-head rivalries, fantasy team optimization, and predictive analytics "
    "powered by machine learning."
)

# Key statistics
st.markdown("### 📊 Platform Overview")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(kpi_card("🏟️", f"{summary['total_matches']:,}", "Total Matches"), unsafe_allow_html=True)
with c2:
    st.markdown(kpi_card("👤", f"{summary['total_players']:,}", "Total Players"), unsafe_allow_html=True)
with c3:
    st.markdown(kpi_card("⚾", f"{summary['total_deliveries']:,}", "Total Deliveries"), unsafe_allow_html=True)
with c4:
    st.markdown(kpi_card("🏆", f"{summary['total_seasons']}", "Seasons Covered"), unsafe_allow_html=True)

st.markdown("---")

# Tabs for dashboard sections
tab_overview, tab_performers, tab_insights = st.tabs(
    ["📈 Quick Stats", "⭐ Top Performers", "🔍 Match Insights"]
)

with tab_overview:
    col_a, col_b = st.columns(2)
    with col_a:
        top5 = player_stats.head(5).set_index("player")["runs"]
        st.plotly_chart(bar_chart(top5, "Top 5 Run Scorers"), use_container_width=True)
    with col_b:
        labels = ["Runs", "Wickets", "Teams", "Venues"]
        values = [
            summary["total_runs"],
            summary["total_wickets"],
            summary["total_teams"],
            matches["venue"].nunique(),
        ]
        st.plotly_chart(pie_chart(labels, values, "Dataset Composition"), use_container_width=True)

with tab_performers:
    st.markdown("#### 🌟 IPL Elite Performers")
    p1, p2, p3 = st.columns(3)
    top = performers["Top Scorer"]
    best_sr = performers["Best Strike Rate"]
    most_6s = performers["Most Sixes"]
    with p1:
        st.markdown(
            performer_card_html("Top Scorer", top["player"], f"{int(top['runs']):,} runs"),
            unsafe_allow_html=True,
        )
    with p2:
        st.markdown(
            performer_card_html(
                "Best Strike Rate (500+ balls)",
                best_sr["player"],
                f"SR {best_sr['strike_rate']:.1f}",
            ),
            unsafe_allow_html=True,
        )
    with p3:
        st.markdown(
            performer_card_html(
                "Most Sixes", most_6s["player"], f"{int(most_6s['sixes'])} sixes"
            ),
            unsafe_allow_html=True,
        )

with tab_insights:
    i1, i2, i3, i4 = st.columns(4)
    with i1:
        st.metric("Completed Matches", f"{insights['total_completed']:,}")
    with i2:
        st.metric("Avg Target Score", insights["avg_target"])
    with i3:
        st.metric("Toss → Win Rate", f"{insights['toss_win_pct']}%")
    with i4:
        st.metric("Top Venue", insights["top_venue"][:20] + "…" if len(insights["top_venue"]) > 20 else insights["top_venue"])

    st.info(f"🏅 Most Player of the Match awards: **{insights['most_pom']}**")

# Module cards
st.markdown("### 🧭 Explore Modules")
st.markdown("Use the sidebar to navigate between analytics modules.")

modules = [
    ("🏏", "Batter Analyzer", "Deep-dive into individual batting performance"),
    ("⚔️", "Batter vs Bowler", "Head-to-head rivalry statistics"),
    ("🏆", "Fantasy Optimizer", "AI-recommended Best XI with captain picks"),
    ("📊", "Top Run Scorers", "Interactive leaderboard visualizations"),
    ("🎯", "Win Probability", "ML-powered match outcome predictor"),
    ("📋", "Match Insights", "Tournament-level analytics dashboard"),
]
cols = st.columns(3)
for i, (icon, name, desc) in enumerate(modules):
    with cols[i % 3]:
        with st.container(border=True):
            st.markdown(f"#### {icon} {name}")
            st.caption(desc)

render_footer()
