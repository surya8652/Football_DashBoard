"""
app.py
------
Entry point for the Football Player Performance Analytics Dashboard.
Run with:  streamlit run app.py
"""

import sys
from pathlib import Path

# Ensure the project root is always on sys.path so 'utils' is importable
# whether running locally or on Streamlit Cloud.
_ROOT = Path(__file__).parent.resolve()
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st

from utils.data_loader import filter_data, load_data

# ── Page config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject global CSS theme ────────────────────────────────────────────────
css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# ── Load full dataset (cached) ─────────────────────────────────────────────
df_full = load_data()

# ── Sidebar filters ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚽ Football Analytics")
    st.markdown("---")

    all_seasons = sorted(df_full["season"].unique().tolist())
    selected_seasons = st.multiselect(
        "📅 Season",
        options=all_seasons,
        default=all_seasons,
        help="Filter by season. Select one or more.",
    )

    all_teams = sorted(df_full["team"].unique().tolist())
    selected_teams = st.multiselect(
        "🏟️ Team",
        options=all_teams,
        default=all_teams,
        help="Filter by club.",
    )

    all_positions = ["GK", "DEF", "MID", "FWD"]
    selected_positions = st.multiselect(
        "🎽 Position",
        options=all_positions,
        default=all_positions,
        help="Filter by playing position.",
    )

    # Derive the player list from the current team/position/season filters
    # (ignoring player filter itself) so the dropdown stays relevant
    temp_df = filter_data(df_full, selected_seasons, selected_teams, selected_positions)
    all_players = sorted(temp_df["player_name"].unique().tolist())
    selected_player = st.selectbox(
        "🔍 Player (optional)",
        options=["All Players"] + all_players,
        index=0,
        help="Focus on a single player across all pages.",
    )

    st.markdown("---")
    st.caption("⚠️ All data is **synthetic** and for demonstration only. "
               "Statistics do not reflect real-world performance.")

# ── Apply all filters ──────────────────────────────────────────────────────
player_filter = None if selected_player == "All Players" else selected_player
df_filtered = filter_data(
    df_full,
    selected_seasons,
    selected_teams,
    selected_positions,
    player_filter,
)

# Store in session_state so every page can access without re-filtering
st.session_state["df_filtered"] = df_filtered
st.session_state["df_full"] = df_full

# ── Multi-page navigation ──────────────────────────────────────────────────
overview_page = st.Page("pages/overview.py", title="Overview", icon="📊", default=True)
player_page = st.Page("pages/player_analysis.py", title="Player Analysis", icon="👤")
team_page = st.Page("pages/team_analysis.py", title="Team Analysis", icon="🏆")
position_page = st.Page("pages/position_analysis.py", title="Position Analysis", icon="🎽")

pg = st.navigation(
    {
        "Dashboard": [overview_page],
        "Analysis": [player_page, team_page, position_page],
    }
)

pg.run()
