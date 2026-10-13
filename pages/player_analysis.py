"""
pages/player_analysis.py
------------------------
Player Analysis page:
  - Radar chart comparing up to 5 players
  - Goals vs Assists scatter (color=position, size=minutes_played)
  - Shots vs Goals scatter with manual numpy trend line
  - Searchable stats table with CSV download
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

import io

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

PLOTLY_THEME = "plotly_dark"
BG_COLOR = "#0d1117"
PAPER_COLOR = "#161b22"
GREEN = "#2ea043"

POSITION_COLORS = {
    "GK": "#f0883e",
    "DEF": "#58a6ff",
    "MID": "#2ea043",
    "FWD": "#f85149",
}

RADAR_DIMS = ["goals", "assists", "pass_accuracy", "defensive_actions", "rating"]
RADAR_LABELS = ["Goals", "Assists", "Pass Acc %", "Def. Actions", "Rating"]


def _normalize_radar(series: pd.Series, df_all: pd.DataFrame) -> list[float]:
    """Min-max normalize a row's radar values against the full filtered dataset."""
    result = []
    for col in RADAR_DIMS:
        col_min = df_all[col].min()
        col_max = df_all[col].max()
        denom = col_max - col_min
        val = (series[col] - col_min) / denom if denom > 0 else 0.0
        result.append(round(float(val), 4))
    return result


def render():
    st.title("👤 Player Analysis")

    df: pd.DataFrame = st.session_state.get("df_filtered", pd.DataFrame())

    if df.empty:
        st.warning(
            "No data matches the selected filters. "
            "Adjust Season, Team, or Position in the sidebar."
        )
        return

    # Aggregate across seasons for the radar / table views
    player_agg = (
        df.groupby(["player_id", "player_name", "team", "position"], as_index=False)
        .agg(
            goals=("goals", "sum"),
            assists=("assists", "sum"),
            shots=("shots", "sum"),
            shots_on_target=("shots_on_target", "sum"),
            pass_accuracy=("pass_accuracy", "mean"),
            defensive_actions=("defensive_actions", "sum"),
            minutes_played=("minutes_played", "sum"),
            matches_played=("matches_played", "sum"),
            yellow_cards=("yellow_cards", "sum"),
            red_cards=("red_cards", "sum"),
            clean_sheets=("clean_sheets", "sum"),
            rating=("rating", "mean"),
        )
    )
    player_agg["pass_accuracy"] = player_agg["pass_accuracy"].round(1)
    player_agg["rating"] = player_agg["rating"].round(2)

    # ── 1. Player Radar Comparison ─────────────────────────────────────────
    st.subheader("📡 Player Comparison Radar")
    all_names = sorted(player_agg["player_name"].unique().tolist())
    selected = st.multiselect(
        "Select 2–5 players to compare",
        options=all_names,
        default=all_names[:3] if len(all_names) >= 3 else all_names,
        max_selections=5,
    )

    if len(selected) < 2:
        st.info("ℹ️ Select at least 2 players to display the radar chart.")
    else:
        fig_radar = go.Figure()
        colors = ["#2ea043", "#58a6ff", "#f0883e", "#f85149", "#bc8cff"]
        for i, name in enumerate(selected):
            row = player_agg[player_agg["player_name"] == name].iloc[0]
            values = _normalize_radar(row, player_agg)
            values_closed = values + [values[0]]  # close the polygon
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=values_closed,
                    theta=RADAR_LABELS + [RADAR_LABELS[0]],
                    fill="toself",
                    name=name,
                    line=dict(color=colors[i % len(colors)], width=2),
                    opacity=0.75,
                )
            )
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], showticklabels=False),
                bgcolor=PAPER_COLOR,
            ),
            paper_bgcolor=PAPER_COLOR,
            plot_bgcolor=BG_COLOR,
            template=PLOTLY_THEME,
            legend=dict(font=dict(color="#e6edf3")),
            margin=dict(l=40, r=40, t=40, b=40),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")

    # ── 2. Goals vs Assists Scatter ────────────────────────────────────────
    st.subheader("⚽ Goals vs Assists")
    fig_ga = px.scatter(
        df,
        x="goals",
        y="assists",
        color="position",
        size="minutes_played",
        hover_data=["player_name", "team", "season", "rating"],
        color_discrete_map=POSITION_COLORS,
        labels={"goals": "Goals", "assists": "Assists", "position": "Position"},
        title="Goals vs Assists (bubble size = minutes played)",
        template=PLOTLY_THEME,
    )
    fig_ga.update_layout(
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig_ga, use_container_width=True)

    st.markdown("---")

    # ── 3. Shots vs Goals Scatter with numpy trend line ────────────────────
    st.subheader("🎯 Shots vs Goals")
    fig_sg = px.scatter(
        df,
        x="shots",
        y="goals",
        color="position",
        hover_data=["player_name", "team", "season"],
        color_discrete_map=POSITION_COLORS,
        labels={"shots": "Shots", "goals": "Goals", "position": "Position"},
        title="Shots vs Goals with Linear Trend",
        template=PLOTLY_THEME,
        opacity=0.7,
    )

    # Manual numpy trend line (avoids statsmodels dependency)
    if len(df) >= 2:
        x_vals = df["shots"].values.astype(float)
        y_vals = df["goals"].values.astype(float)
        m, b = np.polyfit(x_vals, y_vals, 1)
        x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
        y_line = m * x_line + b
        fig_sg.add_trace(
            go.Scatter(
                x=x_line,
                y=y_line,
                mode="lines",
                name="Trend",
                line=dict(color="#f0883e", width=2, dash="dash"),
            )
        )

    fig_sg.update_layout(
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig_sg, use_container_width=True)

    st.markdown("---")

    # ── 4. Searchable Stats Table + CSV Download ───────────────────────────
    st.subheader("📋 Player Statistics Table")

    search = st.text_input("🔍 Search player name", placeholder="e.g. James Smith")
    display_df = player_agg.copy()
    if search:
        display_df = display_df[
            display_df["player_name"].str.contains(search, case=False, na=False)
        ]

    display_df = display_df.sort_values("rating", ascending=False).reset_index(drop=True)
    st.dataframe(
        display_df.drop(columns=["player_id"]),
        use_container_width=True,
        hide_index=True,
    )

    # CSV download
    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download filtered data as CSV",
        data=csv_bytes,
        file_name="football_players_filtered.csv",
        mime="text/csv",
    )


render()
