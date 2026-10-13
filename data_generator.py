"""
data_generator.py
-----------------
Generates a reproducible SYNTHETIC football player dataset and saves it
to football_players.csv.

NOTE: All statistics in this dataset are entirely fabricated for
demonstration purposes. They do NOT represent real-world player or
team performance. Players and stats are randomly generated.
"""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)

TEAMS = [
    "Arsenal",
    "Chelsea",
    "Liverpool",
    "Manchester City",
    "Manchester United",
    "Newcastle United",
    "Tottenham Hotspur",
    "Aston Villa",
]

SEASONS = ["2022/23", "2023/24", "2024/25"]

# Realistic squad composition per team
POSITION_COUNTS = {
    "GK": 2,
    "DEF": 6,
    "MID": 6,
    "FWD": 4,
}

# Stat ranges per position: (low, high) for each stat
# (goals, assists, shots, pass_accuracy, defensive_actions,
#  matches_played, minutes_played, yellow_cards, red_cards, clean_sheets)
STAT_RANGES = {
    "GK": dict(
        goals=(0, 1),
        assists=(0, 2),
        shots=(0, 3),
        pass_accuracy=(55.0, 80.0),
        defensive_actions=(10, 40),
        matches_played=(10, 38),
        minutes_played=(900, 3420),
        yellow_cards=(0, 3),
        red_cards=(0, 1),
        clean_sheets=(2, 18),
    ),
    "DEF": dict(
        goals=(0, 5),
        assists=(0, 7),
        shots=(5, 30),
        pass_accuracy=(70.0, 90.0),
        defensive_actions=(40, 150),
        matches_played=(10, 38),
        minutes_played=(900, 3420),
        yellow_cards=(1, 8),
        red_cards=(0, 2),
        clean_sheets=(0, 10),
    ),
    "MID": dict(
        goals=(2, 15),
        assists=(3, 14),
        shots=(20, 80),
        pass_accuracy=(75.0, 92.0),
        defensive_actions=(20, 100),
        matches_played=(10, 38),
        minutes_played=(900, 3420),
        yellow_cards=(1, 9),
        red_cards=(0, 2),
        clean_sheets=(0, 3),
    ),
    "FWD": dict(
        goals=(5, 35),
        assists=(2, 14),
        shots=(30, 140),
        pass_accuracy=(65.0, 85.0),
        defensive_actions=(5, 40),
        matches_played=(10, 38),
        minutes_played=(600, 3420),
        yellow_cards=(0, 7),
        red_cards=(0, 1),
        clean_sheets=(0, 1),
    ),
}

FIRST_NAMES = [
    "James", "Marcus", "Raheem", "Harry", "Mason", "Bukayo", "Phil", "Jack",
    "Trent", "Jordan", "Declan", "Kalvin", "Ben", "Reece", "Luke", "Emile",
    "Ollie", "Dominic", "Ivan", "Ruben", "Bruno", "Kevin", "Erling", "Mohamed",
    "Sadio", "Diogo", "Virgil", "Thibaut", "Ederson", "Alisson",
    "Gabriel", "William", "Liam", "Noah", "Oliver", "Ethan", "Alfie",
    "Charlie", "Freddie", "George", "Henry", "Arthur", "Leo", "Max",
    "Oscar", "Theo", "Archie", "Finley", "Reuben", "Sebastian",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson",
    "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee",
    "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez",
    "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright",
    "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams",
    "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter",
    "Roberts", "Phillips",
]


def _random_name(used: set) -> str:
    for _ in range(1000):
        name = f"{RNG.choice(FIRST_NAMES)} {RNG.choice(LAST_NAMES)}"
        if name not in used:
            used.add(name)
            return name
    raise RuntimeError("Name pool exhausted")


def _rand_int(low: int, high: int) -> int:
    return int(RNG.integers(low, high + 1))


def _rand_float(low: float, high: float) -> float:
    return round(float(RNG.uniform(low, high)), 1)


def _season_variation(value: float, pct: float = 0.15) -> float:
    """Apply small random variation to a value across seasons."""
    delta = value * pct
    return value + RNG.uniform(-delta, delta)


def generate_dataset() -> pd.DataFrame:
    used_names: set = set()
    players = []

    player_id = 1
    for team in TEAMS:
        for position, count in POSITION_COUNTS.items():
            ranges = STAT_RANGES[position]
            for _ in range(count):
                name = _random_name(used_names)
                base_age = _rand_int(18, 34)

                # Generate base stats for the player once, then vary per season
                base_goals = _rand_int(*ranges["goals"])
                base_assists = _rand_int(*ranges["assists"])
                base_shots = _rand_int(*ranges["shots"])
                base_pass_acc = _rand_float(*ranges["pass_accuracy"])
                base_def = _rand_int(*ranges["defensive_actions"])
                base_matches = _rand_int(*ranges["matches_played"])
                base_minutes = _rand_int(*ranges["minutes_played"])
                base_yellows = _rand_int(*ranges["yellow_cards"])
                base_reds = _rand_int(*ranges["red_cards"])
                base_clean = _rand_int(*ranges["clean_sheets"])

                for s_idx, season in enumerate(SEASONS):
                    age = base_age + s_idx

                    goals = max(0, int(round(_season_variation(base_goals))))
                    assists = max(0, int(round(_season_variation(base_assists))))
                    shots = max(goals, int(round(_season_variation(base_shots))))
                    pass_acc = round(
                        min(99.0, max(40.0, _season_variation(base_pass_acc))), 1
                    )
                    def_actions = max(0, int(round(_season_variation(base_def))))
                    matches = max(1, int(round(_season_variation(base_matches))))
                    minutes = max(90, int(round(_season_variation(base_minutes))))
                    yellows = max(0, int(round(_season_variation(base_yellows))))
                    reds = max(0, int(round(_season_variation(base_reds))))
                    shots_on_target = max(
                        goals, int(round(shots * RNG.uniform(0.3, 0.7)))
                    )
                    clean_sheets = max(0, int(round(_season_variation(base_clean))))

                    players.append(
                        {
                            "player_id": player_id,
                            "player_name": name,
                            "team": team,
                            "position": position,
                            "season": season,
                            "age": age,
                            "matches_played": matches,
                            "minutes_played": minutes,
                            "goals": goals,
                            "assists": assists,
                            "shots": shots,
                            "shots_on_target": shots_on_target,
                            "pass_accuracy": pass_acc,
                            "defensive_actions": def_actions,
                            "yellow_cards": yellows,
                            "red_cards": reds,
                            "clean_sheets": clean_sheets,
                        }
                    )

                player_id += 1

    df = pd.DataFrame(players)
    df = _add_rating(df)
    return df


def _add_rating(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute player rating from weighted formula then normalize to [1, 10].

    raw = Goals×0.3 + Assists×0.2 + Pass_Accuracy×0.2
          + Defensive_Actions×0.15 + Minutes_Played×0.15
    """
    raw = (
        df["goals"] * 0.3
        + df["assists"] * 0.2
        + df["pass_accuracy"] * 0.2
        + df["defensive_actions"] * 0.15
        + df["minutes_played"] * 0.15
    )
    min_raw = raw.min()
    max_raw = raw.max()
    normalized = 1 + (raw - min_raw) / (max_raw - min_raw) * 9
    df["rating"] = normalized.round(2)
    return df


if __name__ == "__main__":
    df = generate_dataset()
    df.to_csv("football_players.csv", index=False)
    print(f"Dataset saved: {len(df)} rows, {df['player_id'].nunique()} unique players")
    print(df.head())
