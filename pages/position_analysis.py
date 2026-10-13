"""
pages/position_analysis.py
---------------------------
Position Analysis page:
  - Four tabs: GK, DEF, MID, FWD
  - Box plot: rating distribution per position
  - Bar chart: average goals / assists / defensive actions per position
  - Pie chart: share of total minutes played per position
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

import pandas as pd
import plotly.express as px
import streamlit as st

PLOTLY_THEME = "plotly_dark"
BG_COLOR = "#0d1117"
PAPER_COLOR = "#161b22"

POSITION_COLORS = {
    "GK": "#f0883e",
    "DEF": "#58a6ff",
    "MID": "#2ea043",
    "FWD": "#f85149",
}

POSITION_ORDER = ["GK", "DEF", "MID", "FWD"]


def render():
    st.title("🎽 Position Analysis")
    st.markdown("Performance metrics broken down by playing position.")

    df: pd.DataFrame = st.session_state.get("df_filtered", pd.DataFrame())

    if df.empty:
        st.warning(
            "No data matches the selected filters. "
            "Adjust Season, Team, or Position in the sidebar."
        )
        return

    # Only keep positions that are present in the filtered data
    present_positions = [p for p in POSITION_ORDER if p in df["position"].unique()]

    if not present_positions:
        st.warning("No position data available for the current filter selection.")
        return

    # ── 1. Rating Distribution Box Plot ───────────────────────────────────
    st.subheader("⭐ Rating Distribution by Position")
    fig_box = px.box(
        df[df["position"].isin(present_positions)],
        x="position",
        y="rating",
        color="position",
        color_discrete_map=POSITION_COLORS,
        category_orders={"position": POSITION_ORDER},
        labels={"rating": "Player Rating (1–10)", "position": "Position"},
        template=PLOTLY_THEME,
        points="outliers",
    )
    fig_box.update_layout(
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        showlegend=False,
        margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    # ── 2. Average Stats Bar Chart per Position ────────────────────────────
    st.subheader("📊 Average Stats per Position")
    pos_avg = (
        df.groupby("position", as_index=False)
        .agg(
            avg_goals=("goals", "mean"),
            avg_assists=("assists", "mean"),
            avg_defensive_actions=("defensive_actions", "mean"),
        )
    )
    pos_avg = pos_avg[pos_avg["position"].isin(present_positions)].copy()
    pos_avg["avg_goals"] = pos_avg["avg_goals"].round(1)
    pos_avg["avg_assists"] = pos_avg["avg_assists"].round(1)
    pos_avg["avg_defensive_actions"] = pos_avg["avg_defensive_actions"].round(1)

    # Melt for grouped bar chart
    pos_melted = pos_avg.melt(
        id_vars="position",
        value_vars=["avg_goals", "avg_assists", "avg_defensive_actions"],
        var_name="metric",
        value_name="value",
    )
    pos_melted["metric"] = pos_melted["metric"].map(
        {
            "avg_goals": "Avg Goals",
            "avg_assists": "Avg Assists",
            "avg_defensive_actions": "Avg Def. Actions",
        }
    )

    fig_avg = px.bar(
        pos_melted,
        x="position",
        y="value",
        color="metric",
        barmode="group",
        color_discrete_sequence=["#2ea043", "#58a6ff", "#f0883e"],
        category_orders={"position": POSITION_ORDER},
        labels={"value": "Average", "position": "Position", "metric": "Metric"},
        text_auto=".1f",
        template=PLOTLY_THEME,
    )
    fig_avg.update_layout(
        paper_bgcolor=PAPER_COLOR,
        plot_bgcolor=BG_COLOR,
        legend=dict(font=dict(color="#e6edf3")),
        margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig_avg, use_container_width=True)

    st.markdown("---")

    # ── 3. Minutes Share Pie Chart ─────────────────────────────────────────
    st.subheader("⏱️ Share of Total Minutes Played")
    minutes_share = (
        df.groupby("position", as_index=False)["minutes_played"]
        .sum()
    )
    minutes_share = minutes_share[minutes_share["position"].isin(present_positions)]

    fig_pie = px.pie(
        minutes_share,
        values="minutes_played",
        names="position",
        color="position",
        color_discrete_map=POSITION_COLORS,
        hole=0.4,
        template=PLOTLY_THEME,
    )
    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Minutes: %{value:,}<extra></extra>",
    )
    fig_pie.update_layout(
        paper_bgcolor=PAPER_COLOR,
        legend=dict(font=dict(color="#e6edf3")),
        margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # ── 4. Per-Position Tab Detail ─────────────────────────────────────────
    st.subheader("🔍 Position Deep Dive")
    tabs = st.tabs(present_positions)

    for tab, pos in zip(tabs, present_positions):
        with tab:
            pos_df = df[df["position"] == pos]
            col1, col2, col3 = st.columns(3)
            col1.metric("Players", pos_df["player_id"].nunique())
            col2.metric("Avg Goals", f"{pos_df['goals'].mean():.1f}")
            col3.metric("Avg Rating", f"{pos_df['rating'].mean():.2f}")

            top5 = (
                pos_df.groupby("player_name", as_index=False)
                .agg(goals=("goals", "sum"), assists=("assists", "sum"), rating=("rating", "mean"))
                .sort_values("rating", ascending=False)
                .head(5)
            )
            top5["rating"] = top5["rating"].round(2)
            st.markdown(f"**Top 5 {pos} by Rating**")
            st.dataframe(top5, use_container_width=True, hide_index=True)


render()
