"""Win Probability Predictor — ML-powered match outcome prediction."""

import pandas as pd
import streamlit as st

from utils.analytics import get_win_model
from utils.charts import gauge_chart, win_probability_chart
from utils.components import render_footer, render_sidebar_branding, section_header, setup_page
from utils.data_loader import load_matches

setup_page("Win Probability", "🎯")
render_sidebar_branding()

matches = load_matches()
model, accuracy = get_win_model(matches)

section_header(
    "🎯 Win Probability Predictor",
    "Random Forest model trained on IPL match data to estimate team win probability.",
)

st.markdown(
    f"""
    <div style="background:#1E293B;border:1px solid #334155;border-radius:12px;
    padding:1rem 1.25rem;margin-bottom:1.5rem;">
        <span style="color:#94A3B8;">Model Accuracy:</span>
        <span style="color:#10B981;font-weight:700;font-size:1.1rem;">
            {accuracy * 100:.1f}%
        </span>
        <span style="color:#64748B;"> · RandomForest · Features: target runs & overs</span>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_predict, tab_historical = st.tabs(["🔮 Predict Match", "📜 Historical Matches"])

with tab_predict:
    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("Team 1 (Batting First)", sorted(matches["team1"].unique()))
    with col2:
        team2 = st.selectbox(
            "Team 2",
            sorted(set(matches["team1"].unique()) | set(matches["team2"].unique())),
            index=1,
        )

    c1, c2 = st.columns(2)
    with c1:
        target_runs = st.number_input("Target Runs", min_value=100, max_value=250, value=180)
    with c2:
        target_overs = st.number_input("Target Overs", min_value=10.0, max_value=20.0, value=20.0, step=0.5)

    if st.button("Predict Win Probability", type="primary", use_container_width=True):
        features = pd.DataFrame({"target_runs": [target_runs], "target_overs": [target_overs]})
        proba = model.predict_proba(features)[0]
        team1_prob = proba[1]
        team2_prob = proba[0]

        v1, v2 = st.columns(2)
        with v1:
            st.plotly_chart(
                gauge_chart(team1_prob * 100, f"{team1} Win %"),
                use_container_width=True,
            )
        with v2:
            st.plotly_chart(
                win_probability_chart(team1_prob, team2_prob, team1, team2),
                use_container_width=True,
            )

        winner = team1 if team1_prob > team2_prob else team2
        st.success(f"🏆 Predicted winner: **{winner}** ({max(team1_prob, team2_prob)*100:.1f}% confidence)")

with tab_historical:
    sample = matches.dropna(subset=["target_runs", "winner"]).head(20).copy()
    sample["team1_win"] = (sample["winner"] == sample["team1"]).astype(int)
    features = sample[["target_runs", "target_overs"]].fillna(20)
    sample["predicted_win"] = model.predict(features)
    sample["confidence"] = model.predict_proba(features).max(axis=1).round(3)

    display = sample[["season", "team1", "team2", "target_runs", "winner", "predicted_win", "confidence"]]
    display["predicted_win"] = display["predicted_win"].map({1: "Team 1", 0: "Team 2"})
    display.columns = ["Season", "Team 1", "Team 2", "Target", "Actual Winner", "Predicted", "Confidence"]
    st.dataframe(display, use_container_width=True, hide_index=True)

render_footer()
