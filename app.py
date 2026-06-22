"""CricIntel — AI-Powered Cricket Analytics Platform."""

import streamlit as st

from utils.analytics import get_match_insights, get_top_performers
from utils.charts import bar_chart, pie_chart
from utils.components import (
    hero_premium_html,
    info_banner,
    inject_styles,
    kpi_card,
    module_card,
    performer_card_html,
    render_footer,
    render_sidebar_branding,
    section_header,
    LOGO_PATH,
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

deliveries = load_deliveries()
matches = load_matches()
player_stats = get_player_stats(deliveries)
summary = get_summary_stats(deliveries, matches)
insights = get_match_insights(matches)
performers = get_top_performers(player_stats)

render_sidebar_branding(summary)

# ── Premium hero ──────────────────────────────────────────────────────────────
st.markdown(
    hero_premium_html(
        title="CricIntel",
        subtitle="AI-Powered Cricket Analytics Platform",
        description=(
            "Enterprise-grade IPL intelligence — player performance, head-to-head rivalries, "
            "fantasy optimization, win probability ML, and ball-by-ball match insights."
        ),
        logo_path=LOGO_PATH,
    ),
    unsafe_allow_html=True,
)

# ── KPI row ───────────────────────────────────────────────────────────────────
section_header(
    "Platform Overview",
    "Real-time metrics across the complete IPL ball-by-ball archive.",
    "Dashboard",
)

c1, c2, c3, c4 = st.columns(4, gap="medium")
with c1:
    st.markdown(
        kpi_card("🏟️", f"{summary['total_matches']:,}", "Total Matches", delay=0.05, trend="IPL archive"),
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        kpi_card("👤", f"{summary['total_players']:,}", "Total Players", delay=0.12, accent="sky"),
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        kpi_card("⚾", f"{summary['total_deliveries']:,}", "Deliveries", delay=0.19),
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        kpi_card("🏆", f"{summary['total_seasons']}", "Seasons", delay=0.26, accent="gold"),
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

# ── Analytics tabs ──────────────────────────────────────────────────────────────
tab_overview, tab_performers, tab_insights = st.tabs(
    ["📈 Analytics", "⭐ Top Performers", "🔍 Tournament Pulse"]
)

with tab_overview:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        top5 = player_stats.head(5).set_index("player")["runs"]
        st.plotly_chart(bar_chart(top5, "Top 5 Run Scorers"), use_container_width=True)
    with col_b:
        labels = ["Total Runs", "Wickets", "Teams", "Venues"]
        values = [
            summary["total_runs"],
            summary["total_wickets"],
            summary["total_teams"],
            matches["venue"].nunique(),
        ]
        st.plotly_chart(pie_chart(labels, values, "Dataset Composition"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_performers:
    st.markdown(
        '<div class="glass-panel"><div class="glass-panel-header">🌟 IPL Elite Performers</div>',
        unsafe_allow_html=True,
    )
    p1, p2, p3 = st.columns(3, gap="medium")
    top = performers["Top Scorer"]
    best_sr = performers["Best Strike Rate"]
    most_6s = performers["Most Sixes"]
    with p1:
        st.markdown(
            performer_card_html("Top Scorer", top["player"], f"{int(top['runs']):,} career runs"),
            unsafe_allow_html=True,
        )
    with p2:
        st.markdown(
            performer_card_html(
                "Best Strike Rate",
                best_sr["player"],
                f"SR {best_sr['strike_rate']:.1f} · 500+ balls",
            ),
            unsafe_allow_html=True,
        )
    with p3:
        st.markdown(
            performer_card_html(
                "Most Sixes", most_6s["player"], f"{int(most_6s['sixes'])} maximums"
            ),
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

with tab_insights:
    i1, i2, i3, i4 = st.columns(4, gap="medium")
    venue_label = insights["top_venue"]
    if len(venue_label) > 18:
        venue_label = venue_label[:18] + "…"
    with i1:
        st.metric("Completed Matches", f"{insights['total_completed']:,}")
    with i2:
        st.metric("Avg Target", insights["avg_target"])
    with i3:
        st.metric("Toss → Win", f"{insights['toss_win_pct']}%")
    with i4:
        st.metric("Top Venue", venue_label)

    st.markdown(
        info_banner(f"🏅 Most Player of the Match — <strong>{insights['most_pom']}</strong>"),
        unsafe_allow_html=True,
    )

# ── Module grid ─────────────────────────────────────────────────────────────────
section_header(
    "Analytics Modules",
    "Select a module from the sidebar to explore deep cricket intelligence.",
    "Explore",
)

modules = [
    ("🏏", "Batter Analyzer", "Phase-wise batting KPIs & scoring patterns"),
    ("⚔️", "Batter vs Bowler", "Head-to-head rivalry analytics"),
    ("🏆", "Fantasy Optimizer", "AI Best XI with captain picks"),
    ("📊", "Top Run Scorers", "Interactive leaderboards"),
    ("🎯", "Win Probability", "Live ML win predictor"),
    ("🆚", "Player Comparison", "Radar & bar chart comparisons"),
    ("🏟️", "Venue Analytics", "Stadium scoring intelligence"),
    ("🏏", "Team Analytics", "Franchise performance trends"),
    ("📋", "Tournament Insights", "Season & toss analytics"),
    ("📊", "Match Insights", "Ball-by-ball match deep-dive"),
]

rows = [modules[i : i + 3] for i in range(0, len(modules), 3)]
for row in rows:
    cols = st.columns(3, gap="medium")
    for col, (icon, name, desc) in zip(cols, row):
        with col:
            st.markdown(module_card(icon, name, desc), unsafe_allow_html=True)

render_footer()
