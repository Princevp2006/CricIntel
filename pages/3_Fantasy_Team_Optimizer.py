"""Fantasy Team Optimizer — AI-recommended Best XI."""

import streamlit as st

from utils.components import (
    player_card_html,
    render_footer,
    render_sidebar_branding,
    section_header,
    setup_page,
)
from utils.data_loader import get_player_stats, load_deliveries

setup_page("Fantasy Optimizer", "🏆")
render_sidebar_branding()

deliveries = load_deliveries()
player_stats = get_player_stats(deliveries)

section_header(
    "🏆 Fantasy Team Optimizer",
    "Data-driven Best XI selection with captain and vice-captain recommendations.",
)

best_xi = player_stats.sort_values("predicted_points", ascending=False).head(11).reset_index(drop=True)
captain = best_xi.iloc[0]
vice_captain = best_xi.iloc[1]

# Captain / VC highlight
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#1E293B,#292524);
        border:2px solid #F59E0B;border-radius:16px;padding:1.5rem;text-align:center;">
            <div style="font-size:2rem;">👑</div>
            <div style="color:#F59E0B;font-weight:700;font-size:0.8rem;
            text-transform:uppercase;letter-spacing:0.06em;">Captain</div>
            <div style="color:#F8FAFC;font-size:1.5rem;font-weight:800;margin:0.5rem 0;">
                {captain['player']}
            </div>
            <div style="color:#94A3B8;">{captain['predicted_points']:,.0f} fantasy pts · SR {captain['strike_rate']:.1f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#1E293B,#151D2E);
        border:2px solid #94A3B8;border-radius:16px;padding:1.5rem;text-align:center;">
            <div style="font-size:2rem;">🥈</div>
            <div style="color:#94A3B8;font-weight:700;font-size:0.8rem;
            text-transform:uppercase;letter-spacing:0.06em;">Vice Captain</div>
            <div style="color:#F8FAFC;font-size:1.5rem;font-weight:800;margin:0.5rem 0;">
                {vice_captain['player']}
            </div>
            <div style="color:#94A3B8;">{vice_captain['predicted_points']:,.0f} fantasy pts · SR {vice_captain['strike_rate']:.1f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

tab_cards, tab_table = st.tabs(["🃏 Player Cards", "📊 Ranked Table"])

with tab_cards:
    left, right = st.columns(2)
    for i, row in best_xi.iterrows():
        role = ""
        if i == 0:
            role = "captain"
        elif i == 1:
            role = "vice"
        card = player_card_html(
            rank=i + 1,
            name=row["player"],
            points=row["predicted_points"],
            runs=int(row["runs"]),
            sr=row["strike_rate"],
            role=role,
        )
        target = left if i < 6 else right
        with target:
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
        "Fantasy points formula: Runs + (SR × 0.2) + Fours + (Sixes × 2) − (Dismissals × 0.5)"
    )

render_footer()
