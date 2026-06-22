"""Player Comparison Dashboard — head-to-head player analytics."""

import streamlit as st

from utils.analytics import get_player_comparison
from utils.charts import comparison_bar_chart, radar_chart
from utils.components import kpi_card, page_header, render_footer, render_sidebar_branding, setup_page
from utils.data_loader import get_batters, get_player_stats, get_summary_stats, load_deliveries, load_matches

setup_page("Player Comparison", "🆚")

deliveries = load_deliveries()
matches = load_matches()
summary = get_summary_stats(deliveries, matches)
player_stats = get_player_stats(deliveries)
batters = get_batters(deliveries)
render_sidebar_branding(summary)

page_header(
    "Player Comparison Dashboard",
    "Compare any two IPL batters across runs, strike rate, boundaries, and dismissals with radar and bar charts.",
    "Player Intelligence",
)

c1, c2 = st.columns(2, gap="large")
with c1:
    player_a = st.selectbox(
        "Player A",
        batters,
        index=batters.index("V Kohli") if "V Kohli" in batters else 0,
        key="cmp_a",
    )
with c2:
    default_b = batters.index("RG Sharma") if "RG Sharma" in batters else min(1, len(batters) - 1)
    player_b = st.selectbox("Player B", batters, index=default_b, key="cmp_b")

if player_a == player_b:
    st.warning("Please select two different players to compare.")
    st.stop()

comparison = get_player_comparison(player_stats, player_a, player_b)
sa, sb = comparison["stats_a"], comparison["stats_b"]

# KPI cards
metrics = [
    ("Runs", "runs", "🏏"),
    ("Strike Rate", "strike_rate", "⚡"),
    ("Balls Faced", "balls_faced", "🎯"),
    ("Boundaries", "boundaries", "💥"),
    ("Dismissals", "dismissals", "❌"),
]
cols = st.columns(5, gap="medium")
for col, (label, key, icon) in zip(cols, metrics):
    with col:
        val_a = sa[key]
        val_b = sb[key]
        winner = player_a if val_a >= val_b else player_b
        fmt = f"{val_a:,.0f} vs {val_b:,.0f}"
        if key == "strike_rate":
            fmt = f"{val_a:.1f} vs {val_b:.1f}"
        st.markdown(
            kpi_card(icon, fmt, label, accent="sky" if winner == player_a else "crimson"),
            unsafe_allow_html=True,
        )
        st.caption(f"Edge: **{winner}**")

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

tab_radar, tab_bar, tab_table = st.tabs(["🕸️ Radar Chart", "📊 Bar Chart", "📋 Stats Table"])

categories = ["Runs", "Strike Rate", "Balls", "Boundaries", "Dismissals"]
values_a = [sa["runs"], sa["strike_rate"], sa["balls_faced"], sa["boundaries"], sa["dismissals"]]
values_b = [sb["runs"], sb["strike_rate"], sb["balls_faced"], sb["boundaries"], sb["dismissals"]]

with tab_radar:
    st.plotly_chart(
        radar_chart(categories, values_a, values_b, player_a, player_b, "Player Comparison Radar"),
        use_container_width=True,
    )

with tab_bar:
    st.plotly_chart(
        comparison_bar_chart(categories, values_a, values_b, player_a, player_b, "Head-to-Head Comparison"),
        use_container_width=True,
    )

with tab_table:
    import pandas as pd
    table = pd.DataFrame({
        "Metric": categories,
        player_a: values_a,
        player_b: values_b,
    })
    table["Advantage"] = table.apply(
        lambda r: player_a if r[player_a] >= r[player_b] else player_b, axis=1
    )
    st.dataframe(table, use_container_width=True, hide_index=True)

render_footer()
