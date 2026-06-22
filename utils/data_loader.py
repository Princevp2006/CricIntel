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
def get_batters(deliveries: pd.DataFrame) -> list[str]:
    return sorted(deliveries["batter"].dropna().unique())


@st.cache_data
def get_bowlers(deliveries: pd.DataFrame) -> list[str]:
    return sorted(deliveries["bowler"].dropna().unique())
