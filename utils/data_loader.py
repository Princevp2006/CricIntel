"""Data loading and caching for CricIntel."""

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


def _resolve_csv(name: str) -> Path:
    """Return path to CSV, checking data/ then project root."""
    for path in (DATA_DIR / name, ROOT / name):
        if path.exists():
            return path
    return DATA_DIR / name


@st.cache_data(show_spinner="Loading IPL datasets…")
def load_deliveries() -> pd.DataFrame:
    path = _resolve_csv("deliveries.csv")
    if not path.exists():
        st.error(
            f"**deliveries.csv** not found. Place it in `{DATA_DIR}` "
            "or the project root."
        )
        st.stop()
    return pd.read_csv(path)


@st.cache_data(show_spinner="Loading match metadata…")
def load_matches() -> pd.DataFrame:
    path = _resolve_csv("matches.csv")
    if not path.exists():
        st.error(
            f"**matches.csv** not found. Place it in `{DATA_DIR}` "
            "or the project root."
        )
        st.stop()
    return pd.read_csv(path)


@st.cache_data
def get_player_stats(deliveries: pd.DataFrame) -> pd.DataFrame:
    stats = (
        deliveries.groupby("batter")
        .agg(
            runs=("batsman_runs", "sum"),
            balls_faced=("ball", "count"),
            dismissals=("is_wicket", "sum"),
            fours=("batsman_runs", lambda s: (s == 4).sum()),
            sixes=("batsman_runs", lambda s: (s == 6).sum()),
        )
        .reset_index()
        .rename(columns={"batter": "player"})
    )
    stats["boundaries"] = stats["fours"] + stats["sixes"]
    stats["strike_rate"] = (stats["runs"] / stats["balls_faced"] * 100).round(2)
    stats["average"] = stats.apply(
        lambda r: round(r["runs"] / r["dismissals"], 2) if r["dismissals"] > 0 else float(r["runs"]),
        axis=1,
    )
    stats["fantasy_points"] = (
        stats["runs"]
        + stats["strike_rate"] * 0.2
        + stats["fours"] * 1
        + stats["sixes"] * 2
        - stats["dismissals"] * 0.5
    ).round(1)
    stats["predicted_points"] = stats["fantasy_points"]
    return stats.sort_values("runs", ascending=False)


@st.cache_data
def get_bowler_stats(deliveries: pd.DataFrame) -> pd.DataFrame:
    stats = (
        deliveries.groupby("bowler")
        .agg(
            wickets=("is_wicket", "sum"),
            balls=("ball", "count"),
            runs_conceded=("total_runs", "sum"),
        )
        .reset_index()
        .rename(columns={"bowler": "player"})
    )
    stats["economy"] = (stats["runs_conceded"] / stats["balls"] * 6).round(2)
    return stats.sort_values("wickets", ascending=False)


@st.cache_data
def get_summary_stats(deliveries: pd.DataFrame, matches: pd.DataFrame) -> dict:
    return {
        "total_deliveries": len(deliveries),
        "total_matches": deliveries["match_id"].nunique(),
        "total_players": deliveries["batter"].nunique(),
        "total_teams": pd.concat([matches["team1"], matches["team2"]]).nunique(),
        "total_seasons": matches["season"].nunique(),
        "total_runs": int(deliveries["batsman_runs"].sum()),
        "total_wickets": int(deliveries["is_wicket"].sum()),
    }


@st.cache_data
def get_teams(matches: pd.DataFrame) -> list[str]:
    return sorted(set(matches["team1"].dropna()) | set(matches["team2"].dropna()))


@st.cache_data
def get_venues(matches: pd.DataFrame) -> list[str]:
    return sorted(matches["venue"].dropna().unique())


@st.cache_data
def get_batters(deliveries: pd.DataFrame) -> list[str]:
    return sorted(deliveries["batter"].dropna().unique())


@st.cache_data
def get_bowlers(deliveries: pd.DataFrame) -> list[str]:
    return sorted(deliveries["bowler"].dropna().unique())


@st.cache_data
def get_match_options(matches: pd.DataFrame) -> pd.DataFrame:
    """Return match catalogue for selectors."""
    options = matches[["id", "season", "date", "team1", "team2", "venue", "winner"]].copy()
    options["label"] = options.apply(
        lambda r: f"#{int(r['id'])} · {r['season']} · {r['team1']} vs {r['team2']}",
        axis=1,
    )
    return options.sort_values("id", ascending=False)


@st.cache_data
def get_inning_totals(deliveries: pd.DataFrame, matches: pd.DataFrame) -> pd.DataFrame:
    """Total runs per match/inning with venue metadata."""
    totals = (
        deliveries.groupby(["match_id", "inning", "batting_team"])["total_runs"]
        .sum()
        .reset_index()
        .rename(columns={"total_runs": "innings_score"})
    )
    meta = matches[["id", "venue", "winner"]].rename(columns={"id": "match_id"})
    return totals.merge(meta, on="match_id", how="left")


@st.cache_data
def get_venue_analytics(matches: pd.DataFrame, inning_totals: pd.DataFrame) -> pd.DataFrame:
    """Aggregate venue-level scoring and win statistics."""
    venue_matches = matches.groupby("venue").agg(
        matches_played=("id", "count"),
        avg_target=("target_runs", "mean"),
    ).reset_index()

    scores = inning_totals.groupby("venue")["innings_score"].agg(
        avg_score="mean",
        highest_score="max",
        lowest_score="min",
    ).reset_index()

    # Batting-first win rate at venue (toss winner wins)
    completed = matches.dropna(subset=["winner", "toss_winner"])
    toss_wins = (
        completed.groupby("venue")
        .apply(lambda g: (g["toss_winner"] == g["winner"]).mean() * 100)
        .reset_index(name="win_pct")
    )

    result = venue_matches.merge(scores, on="venue", how="left").merge(toss_wins, on="venue", how="left")
    result["avg_score"] = result["avg_score"].round(1)
    result["avg_target"] = result["avg_target"].round(1)
    result["win_pct"] = result["win_pct"].round(1)
    return result.sort_values("matches_played", ascending=False)


@st.cache_data
def get_team_analytics(matches: pd.DataFrame, deliveries: pd.DataFrame) -> pd.DataFrame:
    """Per-team match record."""
    records = []
    for team in get_teams(matches):
        played = matches[(matches["team1"] == team) | (matches["team2"] == team)]
        wins = (played["winner"] == team).sum()
        records.append({
            "team": team,
            "matches_played": len(played),
            "wins": int(wins),
            "losses": int(len(played) - wins),
            "win_pct": round(wins / len(played) * 100, 1) if len(played) else 0,
        })
    return pd.DataFrame(records).sort_values("wins", ascending=False)
