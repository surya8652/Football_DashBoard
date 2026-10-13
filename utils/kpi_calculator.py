"""
utils/kpi_calculator.py
-----------------------
All KPI computation functions. Every value is derived from the
filtered DataFrame — nothing is hardcoded.
"""

import pandas as pd


def total_players(df: pd.DataFrame) -> int:
    """Count of unique players in the filtered dataset."""
    return int(df["player_id"].nunique())


def total_goals(df: pd.DataFrame) -> int:
    """Sum of goals across all rows in the filtered dataset."""
    return int(df["goals"].sum())


def total_assists(df: pd.DataFrame) -> int:
    """Sum of assists across all rows in the filtered dataset."""
    return int(df["assists"].sum())


def total_minutes_played(df: pd.DataFrame) -> int:
    """Sum of minutes played across all rows in the filtered dataset."""
    return int(df["minutes_played"].sum())


def average_rating(df: pd.DataFrame) -> float:
    """Mean player rating across all rows in the filtered dataset."""
    if df.empty:
        return 0.0
    return round(float(df["rating"].mean()), 2)
