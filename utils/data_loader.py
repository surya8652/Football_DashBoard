"""
utils/data_loader.py
--------------------
Handles loading and filtering of football_players.csv.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).parent.parent / "football_players.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load the dataset from CSV. Raises a clear error if the file is missing."""
    if not DATA_PATH.exists():
        st.error(
            f"Dataset not found at `{DATA_PATH}`. "
            "Please run `python data_generator.py` first to generate the dataset."
        )
        st.stop()
    df = pd.read_csv(DATA_PATH)
    # Ensure correct dtypes
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0.0)
    for col in ["goals", "assists", "shots", "shots_on_target",
                "defensive_actions", "minutes_played", "matches_played",
                "yellow_cards", "red_cards", "clean_sheets", "age"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    df["pass_accuracy"] = pd.to_numeric(df["pass_accuracy"], errors="coerce").fillna(0.0)
    return df


def filter_data(
    df: pd.DataFrame,
    seasons: list[str],
    teams: list[str],
    positions: list[str],
    player: str | None = None,
) -> pd.DataFrame:
    """
    Apply sidebar filter selections to the full DataFrame.
    Returns the filtered DataFrame (may be empty — callers must handle that).
    """
    filtered = df.copy()

    if seasons:
        filtered = filtered[filtered["season"].isin(seasons)]
    if teams:
        filtered = filtered[filtered["team"].isin(teams)]
    if positions:
        filtered = filtered[filtered["position"].isin(positions)]
    if player:
        filtered = filtered[filtered["player_name"] == player]

    return filtered.reset_index(drop=True)
