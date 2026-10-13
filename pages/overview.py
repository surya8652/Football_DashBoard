"""
pages/overview.py
-----------------
Overview page: KPI cards + top-N charts.
All values are derived from the filtered DataFrame in session_state.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.kpi_calculator import (
    average_rating,
    total_assists,
    total_goals,
    total_minutes_played,
    total_players,
)

PLOTLY_THEME = "plotly_dark"
BG_COLOR = "#0d1117"
PAPER_COLOR = "#161b22"
GREEN = "#2ea043"


def render():
    st.title("📊 Overview")
    st.markdown("High-level performance summary across the selected filters.")

    df: pd.DataFrame = st.session_state.get("df_filtered", pd.DataFrame())

    if df.empty:
        st.warning(
            "No data matches the selected filters. "
            "Please adjust your Season, Team, or Position selections in the sidebar."
        )
        return

    # ── KPI Cards ─────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("👥 Total Players", f"{total_players(df):,}")
    k2.metric("⚽ Total Goals", f"{total_goals(df):,}")
    k3.metric("🎯 Total Assists", f"{total_assists(df):,}")
    k4.metric("⏱️ Minutes Played", f"{total_minutes_played(df):,}")
    k5.metric("⭐ Avg Rating", f"{average_rating(df):.2f}")

    st.markdown("---")

    # ── Top 10 Players by Goals ────────────────────────────────────────────
    col_l, col_r = st.columns(2)

    top_goals = (
        df.groupby("player_name", as_index=False)["goals"]
        .sum()
        .sort_values("goals", ascending=False)
        .head(10)
    )
    fig_goals = px.bar(
        top_goals,
        x="goals",
        y="player_name",
        orientation="h",
        title="🏆 Top 10 Players by Goals",
        labels={"goals": "Goals", "player_name": "Player"},
        color="goals",
        color_continuous_scale=[[0, "#1a3a1a"], [1, GREEN]],
        template=PLOTLY_THEME,
    )
    fig_goals.update_layout(
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    col_l.plotly_chart(fig_goals, use_container_width=True)

    # ── Top 10 Players by Assists ──────────────────────────────────────────
    top_assists = (
        df.groupby("player_name", as_index=False)["assists"]
        .sum()
        .sort_values("assists", ascending=False)
        .head(10)
    )
    fig_assists = px.bar(
        top_assists,
        x="assists",
        y="player_name",
        orientation="h",
        title="🎯 Top 10 Players by Assists",
        labels={"assists": "Assists", "player_name": "Player"},
        color="assists",
        color_continuous_scale=[[0, "#1a1a3a"], [1, "#58a6ff"]],
        template=PLOTLY_THEME,
    )
    fig_assists.update_layout(
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    col_r.plotly_chart(fig_assists, use_container_width=True)

    st.markdown("---")

    # ── Top 5 Teams by Total Goals ─────────────────────────────────────────
    top_teams = (
        df.groupby("team", as_index=False)["goals"]
        .sum()
        .sort_values("goals", ascending=False)
        .head(5)
    )
    fig_teams = px.bar(
        top_teams,
        x="team",
        y="goals",
        title="🏟️ Top 5 Teams by Total Goals",
        labels={"goals": "Total Goals", "team": "Club"},
        color="goals",
        color_continuous_scale=[[0, "#1a3a1a"], [1, GREEN]],
        text="goals",
        template=PLOTLY_THEME,
    )
    fig_teams.update_traces(textposition="outside")
    fig_teams.update_layout(
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig_teams, use_container_width=True)


render()
