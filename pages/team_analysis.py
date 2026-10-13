"""
pages/team_analysis.py
----------------------
Team Analysis page:
  - Grouped bar chart: Goals & Assists per team
  - Stacked bar chart: Player count by position per team
  - Scatter: Average team rating vs total goals
  - Team summary table
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

PLOTLY_THEME = "plotly_dark"
BG_COLOR = "#0d1117"
PAPER_COLOR = "#161b22"
GREEN = "#2ea043"


def render():
    st.title("🏆 Team Analysis")
    st.markdown("Aggregate performance metrics broken down by club.")

    df: pd.DataFrame = st.session_state.get("df_filtered", pd.DataFrame())

    if df.empty:
        st.warning(
            "No data matches the selected filters. "
            "Adjust Season, Team, or Position in the sidebar."
        )
        return

    # ── Team-level aggregation ─────────────────────────────────────────────
    team_stats = (
        df.groupby("team", as_index=False)
        .agg(
            total_goals=("goals", "sum"),
            total_assists=("assists", "sum"),
            avg_rating=("rating", "mean"),
            player_count=("player_id", "nunique"),
        )
        .sort_values("total_goals", ascending=False)
    )
    team_stats["avg_rating"] = team_stats["avg_rating"].round(2)

    # ── 1. Grouped Bar: Goals & Assists per Team ───────────────────────────
    st.subheader("⚽ Goals & Assists per Club")
    fig_ga = go.Figure()
    fig_ga.add_trace(
        go.Bar(
            name="Goals",
            x=team_stats["team"],
            y=team_stats["total_goals"],
            marker_color=GREEN,
            text=team_stats["total_goals"],
            textposition="outside",
        )
    )
    fig_ga.add_trace(
        go.Bar(
            name="Assists",
            x=team_stats["team"],
            y=team_stats["total_assists"],
            marker_color="#58a6ff",
            text=team_stats["total_assists"],
            textposition="outside",
        )
    )
    fig_ga.update_layout(
        barmode="group",
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        template=PLOTLY_THEME,
        legend=dict(font=dict(color="#e6edf3")),
        xaxis_title="Club",
        yaxis_title="Count",
        margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig_ga, use_container_width=True)

    st.markdown("---")

    # ── 2. Stacked Bar: Player Count by Position per Team ─────────────────
    st.subheader("🎽 Squad Composition by Position")
    pos_counts = (
        df.groupby(["team", "position"], as_index=False)["player_id"]
        .nunique()
        .rename(columns={"player_id": "players"})
    )
    fig_pos = px.bar(
        pos_counts,
        x="team",
        y="players",
        color="position",
        barmode="stack",
        color_discrete_map={
            "GK": "#f0883e",
            "DEF": "#58a6ff",
            "MID": GREEN,
            "FWD": "#f85149",
        },
        labels={"players": "Players", "team": "Club", "position": "Position"},
        template=PLOTLY_THEME,
    )
    fig_pos.update_layout(
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        legend=dict(font=dict(color="#e6edf3")),
        margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig_pos, use_container_width=True)

    st.markdown("---")

    # ── 3. Scatter: Avg Rating vs Total Goals ─────────────────────────────
    st.subheader("⭐ Average Rating vs Total Goals")
    fig_sc = px.scatter(
        team_stats,
        x="total_goals",
        y="avg_rating",
        text="team",
        size="player_count",
        color="avg_rating",
        color_continuous_scale=[[0, "#1a3a1a"], [1, GREEN]],
        labels={
            "total_goals": "Total Goals",
            "avg_rating": "Avg Rating",
            "player_count": "Players",
        },
        template=PLOTLY_THEME,
    )
    fig_sc.update_traces(textposition="top center", marker=dict(line=dict(width=1, color="#30363d")))
    fig_sc.update_layout(
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig_sc, use_container_width=True)

    st.markdown("---")

    # ── 4. Team Summary Table ──────────────────────────────────────────────
    st.subheader("📋 Team Summary")
    display = team_stats.rename(
        columns={
            "team": "Club",
            "total_goals": "Goals",
            "total_assists": "Assists",
            "avg_rating": "Avg Rating",
            "player_count": "Players",
        }
    )
    st.dataframe(display, use_container_width=True, hide_index=True)


render()
