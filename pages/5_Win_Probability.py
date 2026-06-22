"""Win Probability Predictor — ML-powered live match outcome prediction."""

import streamlit as st

from utils.analytics import get_live_win_model, get_win_model, predict_live_win_probability
from utils.charts import gauge_chart, win_probability_chart
from utils.components import info_banner, page_header, render_footer, render_sidebar_branding, setup_page, stat_banner
from utils.data_loader import get_summary_stats, get_teams, load_deliveries, load_matches

setup_page("Win Probability", "🎯")

deliveries = load_deliveries()
matches = load_matches()
summary = get_summary_stats(deliveries, matches)
teams = get_teams(matches)
render_sidebar_branding(summary)

live_model, live_accuracy = get_live_win_model(deliveries, matches)
prematch_model, prematch_accuracy = get_win_model(matches)

page_header(
    "Win Probability Predictor",
    "AI-powered win probability engine using Random Forest trained on historical IPL chase scenarios.",
    "Predictive ML",
)

st.markdown(
    stat_banner(
        "Live Chase Model Accuracy",
        f"{live_accuracy * 100:.1f}%",
        "RandomForest · 9 in-match features",
    ),
    unsafe_allow_html=True,
)

tab_live, tab_prematch, tab_historical = st.tabs(
    ["🔴 Live Match", "📋 Pre-Match", "📜 Historical"]
)

# ── Live match prediction ───────────────────────────────────────────────────────
with tab_live:
    st.markdown("Enter the current match state to predict the batting team's win probability.")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        batting_team = st.selectbox("Batting Team", teams, key="bat_team")
    with c2:
        bowling_options = [t for t in teams if t != batting_team]
        bowling_team = st.selectbox("Bowling Team", bowling_options, key="bowl_team")

    c3, c4, c5 = st.columns(3, gap="medium")
    with c3:
        current_score = st.number_input("Current Score", min_value=0, max_value=300, value=120)
    with c4:
        target_score = st.number_input("Target Score", min_value=1, max_value=300, value=180)
    with c5:
        overs_completed = st.number_input("Overs Completed", min_value=0.0, max_value=20.0, value=15.0, step=0.1)

    c6, c7 = st.columns(2, gap="large")
    with c6:
        wickets_lost = st.number_input("Wickets Lost", min_value=0, max_value=10, value=4)
    with c7:
        overs_total = st.number_input("Total Overs", min_value=1.0, max_value=20.0, value=20.0, step=0.5)

    if st.button("Calculate Win Probability", type="primary", use_container_width=True):
        win_prob = predict_live_win_probability(
            live_model,
            int(current_score),
            int(target_score),
            float(overs_completed),
            int(wickets_lost),
            float(overs_total),
        )
        lose_prob = 1 - win_prob
        runs_needed = max(0, int(target_score) - int(current_score) + 1)
        overs_left = max(0, float(overs_total) - float(overs_completed))

        st.markdown("---")
        k1, k2, k3 = st.columns(3, gap="medium")
        with k1:
            st.metric("Win Probability", f"{win_prob * 100:.1f}%")
        with k2:
            st.metric("Runs Required", runs_needed)
        with k3:
            st.metric("Overs Remaining", f"{overs_left:.1f}")

        st.markdown(f"**{batting_team}** win chance")
        st.progress(min(win_prob, 1.0))

        v1, v2 = st.columns(2, gap="large")
        with v1:
            st.plotly_chart(
                gauge_chart(win_prob * 100, f"{batting_team} Win %"),
                use_container_width=True,
            )
        with v2:
            st.plotly_chart(
                win_probability_chart(win_prob, lose_prob, batting_team, bowling_team),
                use_container_width=True,
            )

        predicted = batting_team if win_prob >= 0.5 else bowling_team
        confidence = max(win_prob, lose_prob) * 100
        st.markdown(
            info_banner(
                f"🏆 <strong>Prediction:</strong> {predicted} favored to win "
                f"({confidence:.1f}% confidence)"
            ),
            unsafe_allow_html=True,
        )

# ── Pre-match (legacy model preserved) ────────────────────────────────────────
with tab_prematch:
    st.caption(f"Pre-match model accuracy: {prematch_accuracy * 100:.1f}% · Features: target runs & overs")

    col1, col2 = st.columns(2, gap="large")
    with col1:
        team1 = st.selectbox("Team 1 (Batting First)", teams, key="pm_t1")
    with col2:
        team2_options = [t for t in teams if t != team1]
        team2 = st.selectbox("Team 2", team2_options, key="pm_t2")

    p1, p2 = st.columns(2, gap="large")
    with p1:
        target_runs = st.number_input("Target Runs", min_value=100, max_value=250, value=180, key="pm_target")
    with p2:
        target_overs = st.number_input("Target Overs", min_value=10.0, max_value=20.0, value=20.0, step=0.5, key="pm_overs")

    if st.button("Predict Pre-Match", type="primary", use_container_width=True, key="pm_btn"):
        import pandas as pd
        features = pd.DataFrame({"target_runs": [target_runs], "target_overs": [target_overs]})
        proba = prematch_model.predict_proba(features)[0]
        t1_prob, t2_prob = proba[1], proba[0]

        st.progress(t1_prob)
        v1, v2 = st.columns(2, gap="large")
        with v1:
            st.plotly_chart(gauge_chart(t1_prob * 100, f"{team1} Win %"), use_container_width=True)
        with v2:
            st.plotly_chart(win_probability_chart(t1_prob, t2_prob, team1, team2), use_container_width=True)

# ── Historical validation ─────────────────────────────────────────────────────
with tab_historical:
    import pandas as pd
    sample = matches.dropna(subset=["target_runs", "winner"]).head(25).copy()
    features = sample[["target_runs", "target_overs"]].fillna(20)
    sample["predicted_win"] = prematch_model.predict(features)
    sample["confidence"] = prematch_model.predict_proba(features).max(axis=1).round(3)
    display = sample[["season", "team1", "team2", "target_runs", "winner", "predicted_win", "confidence"]]
    display["predicted_win"] = display["predicted_win"].map({1: "Team 1", 0: "Team 2"})
    display.columns = ["Season", "Team 1", "Team 2", "Target", "Actual Winner", "Predicted", "Confidence"]
    st.dataframe(display, use_container_width=True, hide_index=True)

render_footer()
