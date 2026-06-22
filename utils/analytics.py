"""Analytics helpers and ML models for CricIntel."""

import pandas as pd
import streamlit as st


# ── Existing helpers (unchanged behaviour) ────────────────────────────────────

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


# ── Player comparison ─────────────────────────────────────────────────────────

def get_player_comparison(player_stats: pd.DataFrame, player_a: str, player_b: str) -> dict:
    """Return side-by-side stats for two players."""
    stats = player_stats.copy()
    if "boundaries" not in stats.columns:
        stats["boundaries"] = stats.get("fours", 0) + stats.get("sixes", 0)

    a = stats[stats["player"] == player_a].iloc[0]
    b = stats[stats["player"] == player_b].iloc[0]
    metrics = ["runs", "strike_rate", "balls_faced", "boundaries", "dismissals", "fours", "sixes"]
    return {
        "player_a": player_a,
        "player_b": player_b,
        "stats_a": {m: float(a[m]) for m in metrics},
        "stats_b": {m: float(b[m]) for m in metrics},
    }


# ── Team analytics ────────────────────────────────────────────────────────────

def get_team_profile(
    team: str, matches: pd.DataFrame, deliveries: pd.DataFrame, bowler_stats: pd.DataFrame
) -> dict:
    """Detailed profile for a single team."""
    played = matches[(matches["team1"] == team) | (matches["team2"] == team)]
    wins = int((played["winner"] == team).sum())
    matches_played = len(played)

    bat = deliveries[deliveries["batting_team"] == team]
    bowl = deliveries[deliveries["bowling_team"] == team]

    top_batter = (
        bat.groupby("batter")["batsman_runs"].sum().sort_values(ascending=False)
    )
    top_bowler = (
        bowl.groupby("bowler")["is_wicket"].sum().sort_values(ascending=False)
    )

    # Season-wise win rate
    season_perf = []
    for season, grp in played.groupby("season"):
        season_perf.append({
            "season": str(season),
            "matches": len(grp),
            "wins": int((grp["winner"] == team).sum()),
        })
    season_df = pd.DataFrame(season_perf)

    return {
        "team": team,
        "matches_played": matches_played,
        "wins": wins,
        "losses": matches_played - wins,
        "win_pct": round(wins / matches_played * 100, 1) if matches_played else 0,
        "top_batter": top_batter.index[0] if len(top_batter) else "N/A",
        "top_batter_runs": int(top_batter.iloc[0]) if len(top_batter) else 0,
        "top_bowler": top_bowler.index[0] if len(top_bowler) else "N/A",
        "top_bowler_wickets": int(top_bowler.iloc[0]) if len(top_bowler) else 0,
        "season_performance": season_df,
        "total_runs": int(bat["batsman_runs"].sum()),
        "total_wickets": int(bowl["is_wicket"].sum()),
    }


# ── Match-level analysis ───────────────────────────────────────────────────────

def get_match_deliveries(deliveries: pd.DataFrame, match_id: int) -> pd.DataFrame:
    return deliveries[deliveries["match_id"] == match_id].copy()


def get_runs_per_over(match_data: pd.DataFrame) -> pd.DataFrame:
    """Cumulative and per-over runs for each inning."""
    rows = []
    for inning, grp in match_data.groupby("inning"):
        grp = grp.sort_values(["over", "ball"])
        for over, over_grp in grp.groupby("over"):
            rows.append({
                "inning": inning,
                "over": over,
                "runs_in_over": int(over_grp["total_runs"].sum()),
                "cumulative_runs": int(grp[grp["over"] <= over]["total_runs"].sum()),
                "wickets": int(grp[grp["over"] <= over]["is_wicket"].sum()),
            })
    return pd.DataFrame(rows)


def get_wickets_timeline(match_data: pd.DataFrame) -> pd.DataFrame:
    """Each wicket with over and batter dismissed."""
    wickets = match_data[match_data["is_wicket"] == 1].copy()
    wickets["over_ball"] = wickets["over"] + wickets["ball"] / 10
    return wickets[["inning", "over", "ball", "over_ball", "player_dismissed", "bowler", "total_runs"]]


def get_partnerships(match_data: pd.DataFrame, inning: int) -> pd.DataFrame:
    """Compute batting partnerships for an inning."""
    data = match_data[match_data["inning"] == inning].sort_values(["over", "ball"])
    if data.empty:
        return pd.DataFrame(columns=["batter_1", "batter_2", "runs", "balls"])

    partnerships = []
    pair = None
    runs = 0
    balls = 0

    for _, row in data.iterrows():
        current_pair = tuple(sorted([row["batter"], row["non_striker"]]))
        if pair is None:
            pair = current_pair
        elif current_pair != pair:
            partnerships.append({"batter_1": pair[0], "batter_2": pair[1], "runs": runs, "balls": balls})
            pair = current_pair
            runs = 0
            balls = 0

        runs += int(row["total_runs"])
        balls += 1

        if row["is_wicket"] == 1:
            partnerships.append({"batter_1": pair[0], "batter_2": pair[1], "runs": runs, "balls": balls})
            pair = None
            runs = 0
            balls = 0

    if pair and runs > 0:
        partnerships.append({"batter_1": pair[0], "batter_2": pair[1], "runs": runs, "balls": balls})

    df = pd.DataFrame(partnerships)
    if not df.empty:
        df = df.sort_values("runs", ascending=False).reset_index(drop=True)
    return df


def get_match_top_performers(match_data: pd.DataFrame) -> dict:
    top_batter = (
        match_data.groupby("batter")["batsman_runs"]
        .sum()
        .sort_values(ascending=False)
    )
    top_bowler = (
        match_data.groupby("bowler")["is_wicket"]
        .sum()
        .sort_values(ascending=False)
    )
    return {
        "top_batter": top_batter.index[0] if len(top_batter) else "N/A",
        "top_batter_runs": int(top_batter.iloc[0]) if len(top_batter) else 0,
        "top_bowler": top_bowler.index[0] if len(top_bowler) else "N/A",
        "top_bowler_wickets": int(top_bowler.iloc[0]) if len(top_bowler) else 0,
    }


# ── Win probability ML ────────────────────────────────────────────────────────

def _build_live_win_training_data(
    deliveries: pd.DataFrame, matches: pd.DataFrame
) -> tuple[pd.DataFrame, pd.Series]:
    """Build chase-state snapshots from 2nd innings for ML training."""
    meta = matches[["id", "winner", "target_runs", "target_overs"]].rename(columns={"id": "match_id"})
    chase = deliveries[deliveries["inning"] == 2].merge(meta, on="match_id", how="inner")
    chase = chase.dropna(subset=["target_runs"])

    records = []
    for match_id, grp in chase.groupby("match_id"):
        grp = grp.sort_values(["over", "ball"])
        batting_team = grp["batting_team"].iloc[0]
        winner = grp["winner"].iloc[0]
        target = float(grp["target_runs"].iloc[0])
        max_overs = float(grp["target_overs"].dropna().iloc[0]) if grp["target_overs"].notna().any() else 20.0

        for over in sorted(grp["over"].unique()):
            snapshot = grp[grp["over"] <= over]
            current_score = int(snapshot["total_runs"].sum())
            wickets_lost = int(snapshot["is_wicket"].sum())
            overs_completed = float(over)
            overs_remaining = max(0.1, max_overs - overs_completed)
            runs_required = max(0, target - current_score + 1)

            records.append({
                "current_score": current_score,
                "target_score": target,
                "overs_completed": overs_completed,
                "wickets_lost": wickets_lost,
                "runs_required": runs_required,
                "overs_remaining": overs_remaining,
                "current_run_rate": current_score / overs_completed if overs_completed else 0,
                "required_run_rate": runs_required / overs_remaining,
                "wickets_in_hand": 10 - wickets_lost,
                "batting_team_wins": int(batting_team == winner),
            })

    df = pd.DataFrame(records)
    if df.empty:
        return pd.DataFrame(), pd.Series(dtype=int)

    features = df[
        [
            "current_score", "target_score", "overs_completed", "wickets_lost",
            "runs_required", "overs_remaining", "current_run_rate",
            "required_run_rate", "wickets_in_hand",
        ]
    ]
    return features, df["batting_team_wins"]


@st.cache_resource
def get_live_win_model(
    deliveries: pd.DataFrame, matches: pd.DataFrame
):
    """Train RandomForest on live chase states."""
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split

    features, target = _build_live_win_training_data(deliveries, matches)
    if features.empty:
        model = RandomForestClassifier(n_estimators=50, random_state=42)
        return model, 0.0

    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )
    model = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    return model, accuracy


@st.cache_resource
def get_win_model(matches: pd.DataFrame):
    """Pre-match RandomForest win predictor (legacy — kept for historical tab)."""
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split

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


def predict_live_win_probability(
    model,
    current_score: int,
    target_score: int,
    overs_completed: float,
    wickets_lost: int,
    overs_total: float = 20.0,
) -> float:
    """Return win probability (0–1) for the batting team."""
    overs_remaining = max(0.1, overs_total - overs_completed)
    runs_required = max(0, target_score - current_score + 1)
    current_rr = current_score / overs_completed if overs_completed > 0 else 0
    required_rr = runs_required / overs_remaining

    features = pd.DataFrame([{
        "current_score": current_score,
        "target_score": target_score,
        "overs_completed": overs_completed,
        "wickets_lost": wickets_lost,
        "runs_required": runs_required,
        "overs_remaining": overs_remaining,
        "current_run_rate": current_rr,
        "required_run_rate": required_rr,
        "wickets_in_hand": 10 - wickets_lost,
    }])

    if not hasattr(model, "feature_importances_"):
        # Heuristic fallback if model not fitted
        score_ratio = current_score / max(target_score, 1)
        wicket_factor = (10 - wickets_lost) / 10
        rr_factor = min(1.0, current_rr / max(required_rr, 0.1)) if required_rr else 1.0
        return min(0.99, max(0.01, 0.35 * score_ratio + 0.25 * wicket_factor + 0.40 * rr_factor))

    proba = model.predict_proba(features)[0]
    classes = list(model.classes_)
    win_idx = classes.index(1) if 1 in classes else -1
    return float(proba[win_idx])
