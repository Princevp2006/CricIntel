"""Fantasy Team Optimizer — AI-recommended Best XI."""

import streamlit as st

from utils.components import (
    page_header,
    player_card_html,
    render_footer,
    render_sidebar_branding,
    setup_page,
    spotlight_card,
)
from utils.data_loader import get_player_stats, get_summary_stats, load_deliveries, load_matches

setup_page("Fantasy Optimizer", "🏆")

deliveries = load_deliveries()
matches = load_matches()
summary = get_summary_stats(deliveries, matches)
render_sidebar_branding(summary)
player_stats = get_player_stats(deliveries)

page_header(
    "Fantasy Team Optimizer",
    "Data-driven Best XI selection powered by a composite fantasy points model with captain and vice-captain recommendations.",
    "Fantasy Intelligence",
)

best_xi = player_stats.sort_values("predicted_points", ascending=False).head(11).reset_index(drop=True)
captain = best_xi.iloc[0]
vice_captain = best_xi.iloc[1]

c1, c2 = st.columns(2, gap="large")
with c1:
    st.markdown(
        spotlight_card(
            "Captain",
            captain["player"],
            f"{captain['predicted_points']:,.0f} pts · SR {captain['strike_rate']:.1f} · {int(captain['runs']):,} runs",
            "captain",
        ),
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        spotlight_card(
            "Vice Captain",
            vice_captain["player"],
            f"{vice_captain['predicted_points']:,.0f} pts · SR {vice_captain['strike_rate']:.1f} · {int(vice_captain['runs']):,} runs",
            "vice",
        ),
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

tab_cards, tab_table = st.tabs(["🃏 Player Cards", "📊 Ranked Table"])

with tab_cards:
    left, right = st.columns(2, gap="medium")
    for i, row in best_xi.iterrows():
        role = "captain" if i == 0 else "vice" if i == 1 else ""
        card = player_card_html(
            rank=i + 1,
            name=row["player"],
            points=row["predicted_points"],
            runs=int(row["runs"]),
            sr=row["strike_rate"],
            role=role,
        )
        with (left if i < 6 else right):
            st.markdown(card, unsafe_allow_html=True)

with tab_table:
    display_df = best_xi[
        ["player", "runs", "balls_faced", "strike_rate", "fours", "sixes", "dismissals", "predicted_points"]
    ].copy()
    display_df.columns = [
        "Player", "Runs", "Balls", "Strike Rate", "4s", "6s", "Dismissals", "Fantasy Pts"
    ]
    display_df.index = range(1, len(display_df) + 1)
    display_df.index.name = "Rank"
    st.dataframe(display_df, use_container_width=True)
    st.caption(
        "Fantasy points = Runs + (SR × 0.2) + Fours + (Sixes × 2) − (Dismissals × 0.5)"
    )

render_footer()
