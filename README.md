# ⚽ Football Player Performance Analytics Dashboard

> **⚠️ SYNTHETIC DATA DISCLAIMER**  
> All player names, club names, and statistics in this project are **entirely fabricated** using a random number generator. They are provided for demonstration and portfolio purposes only and do **not** represent any real-world football player or club performance.

---

## 🖼️ Overview

An interactive, portfolio-quality football (soccer) analytics dashboard built with **Python + Streamlit**. The app lets you explore and compare synthetic player data across three seasons using dynamic sidebar filters and rich Plotly charts.

### Pages

| Page | Description |
|---|---|
| 📊 **Overview** | KPI cards (players, goals, assists, minutes, rating) + top-10 charts |
| 👤 **Player Analysis** | Radar comparison, Goals vs Assists scatter, Shots vs Goals scatter, downloadable stats table |
| 🏆 **Team Analysis** | Club-level goals/assists grouped bar, squad composition stacked bar, avg rating scatter |
| 🎽 **Position Analysis** | Rating box plots, average stats per position, minutes share pie, per-position deep-dive tabs |

### Features

- **Sidebar filters** — Season, Team, Position, Player (all fully dynamic)
- **KPI cards** — all computed live from filtered data, never hardcoded
- **CSV download** — export filtered player stats from the Player Analysis page
- **Dark green pitch theme** — professional football-inspired UI
- **Input validation** — empty-filter warnings, missing-CSV error, minimum player selection prompts
- **Reproducible synthetic dataset** — `numpy.random.seed(42)`, 144 unique players × 3 seasons = 432 rows

---

## 🗂️ Project Structure

```
Football Analysis Dashboard/
├── app.py                     # Entry point — st.navigation, sidebar, CSS
├── data_generator.py          # Script to (re)generate football_players.csv
├── football_players.csv       # Synthetic dataset (432 rows)
├── requirements.txt
├── README.md
├── assets/
│   └── style.css              # Dark/green global theme
├── utils/
│   ├── __init__.py
│   ├── data_loader.py         # load_data() + filter_data()
│   └── kpi_calculator.py      # Five KPI functions
└── pages/
    ├── overview.py
    ├── player_analysis.py
    ├── team_analysis.py
    └── position_analysis.py
```

---

## 🚀 Run Locally

### Prerequisites

- Python 3.10 or later
- pip

### Steps

```bash
# 1. Clone or download this repository
cd "Football Analysis Dashboard"

# 2. (Recommended) Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Regenerate the dataset — already included as football_players.csv
python data_generator.py

# 5. Launch the dashboard
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

---

## ☁️ Deploy to Streamlit Community Cloud

1. Push this entire folder to a **public GitHub repository**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** → select your repo, branch (`main`), and set **Main file path** to `app.py`.
4. Click **Deploy**. Streamlit Cloud installs `requirements.txt` automatically.

> The `football_players.csv` file must be committed to the repo so the cloud instance can read it. No additional secrets or API keys are needed.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| streamlit | ≥ 1.36 | App framework + multi-page navigation |
| pandas | ≥ 2.0 | Data loading, filtering, aggregation |
| numpy | ≥ 1.26 | Dataset generation, normalization, trend line |
| plotly | ≥ 5.18 | All interactive charts |

---

## 📐 Dataset Schema

| Column | Type | Notes |
|---|---|---|
| player_id | int | Unique per player (stable across seasons) |
| player_name | str | Randomly generated full name |
| team | str | One of 8 Premier League club names (stats are fake) |
| position | str | GK / DEF / MID / FWD |
| season | str | 2022/23, 2023/24, or 2024/25 |
| age | int | Age in that season |
| matches_played | int | Appearances |
| minutes_played | int | Total minutes on pitch |
| goals | int | Goals scored |
| assists | int | Assists |
| shots | int | Total shots |
| shots_on_target | int | Shots on target |
| pass_accuracy | float | Pass completion % |
| defensive_actions | int | Tackles + interceptions + clearances |
| yellow_cards | int | Bookings |
| red_cards | int | Dismissals |
| clean_sheets | int | Matches without conceding (non-zero for GK/DEF) |
| rating | float | Weighted formula, normalized to [1–10] |

**Rating formula:**  
`raw = Goals × 0.3 + Assists × 0.2 + Pass_Accuracy × 0.2 + Defensive_Actions × 0.15 + Minutes_Played × 0.15`  
→ Min-max normalized to **[1, 10]**

---

## 📸 Screenshots

_Add screenshots here after running the app locally._

---

## 📄 License

This project is released for portfolio and educational use. No real football data is used or implied.
