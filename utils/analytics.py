"""Analytics helpers and ML models for CricIntel."""

import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


@st.cache_resource
def get_win_model(matches: pd.DataFrame) -> tuple[RandomForestClassifier, float]:
    """Train RandomForest win predictor on match features."""
    df = matches.copy()
    df["team1_win"] = (df["winner"] == df["team1"]).astype(int)
    features = df[["target_runs", "target_overs"]].fillna(0)
    target = df["team1_win"]

    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    return model, accuracy


def get_batter_phase_stats(batter_data: pd.DataFrame) -> dict[str, int]:
    powerplay = batter_data[batter_data["over"] <= 6]
    middle = batter_data[(batter_data["over"] > 6) & (batter_data["over"] <= 15)]
    death = batter_data[batter_data["over"] > 15]
    return {
        "Powerplay (1–6)": int(powerplay["batsman_runs"].sum()),
        "Middle (7–15)": int(middle["batsman_runs"].sum()),
        "Death (16–20)": int(death["batsman_runs"].sum()),
    }


def get_batter_run_distribution(batter_data: pd.DataFrame) -> dict[str, int]:
    runs = batter_data["batsman_runs"]
    return {
        "Dots (0)": int((runs == 0).sum()),
        "Singles (1)": int((runs == 1).sum()),
        "Twos (2)": int((runs == 2).sum()),
        "Threes (3)": int((runs == 3).sum()),
        "Fours (4)": int((runs == 4).sum()),
        "Sixes (6)": int((runs == 6).sum()),
    }


def get_head_to_head(
    deliveries: pd.DataFrame, batter: str, bowler: str
) -> pd.DataFrame:
    return deliveries[
        (deliveries["batter"] == batter) & (deliveries["bowler"] == bowler)
    ].copy()


def get_top_performers(player_stats: pd.DataFrame) -> dict[str, pd.Series]:
    return {
        "Top Scorer": player_stats.iloc[0],
        "Best Strike Rate": player_stats[player_stats["balls_faced"] >= 500]
        .sort_values("strike_rate", ascending=False)
        .iloc[0],
        "Most Sixes": player_stats.sort_values("sixes", ascending=False).iloc[0],
    }


def get_match_insights(matches: pd.DataFrame) -> dict:
    completed = matches.dropna(subset=["winner"])
    toss_wins = completed[completed["toss_winner"] == completed["winner"]]
    return {
        "total_completed": len(completed),
        "avg_target": round(completed["target_runs"].dropna().mean(), 1),
        "toss_win_pct": round(len(toss_wins) / len(completed) * 100, 1),
        "top_venue": completed["venue"].value_counts().index[0],
        "most_pom": completed["player_of_match"].value_counts().index[0],
    }
