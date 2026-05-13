
import streamlit as st
import json
import random
from pathlib import Path
from datetime import date
import pandas as pd

st.set_page_config(
    page_title="Zion SmashBoard",
    page_icon="🏸",
    layout="wide"
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

PLAYERS_FILE = DATA_DIR / "players.json"
MATCHES_FILE = DATA_DIR / "matches.json"
CONFIG_FILE = DATA_DIR / "config.json"

DEFAULT_PASSWORD = "zion123"

def load_json(path, default):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

players = load_json(PLAYERS_FILE, [])
matches = load_json(MATCHES_FILE, [])
config = load_json(CONFIG_FILE, {"password": DEFAULT_PASSWORD})

# ---------- AUTH ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_screen():
    st.markdown(
        '''
        <style>
        .main {
            background-color: #f7f7f7;
        }
        .title {
            text-align:center;
            font-size:48px;
            font-weight:700;
            color:#111;
            margin-top:50px;
        }
        .subtitle {
            text-align:center;
            color:#666;
            margin-bottom:40px;
        }
        </style>
        ''',
        unsafe_allow_html=True
    )

    st.markdown('<div class="title">🏸 Zion SmashBoard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Daily Badminton Tournament Tracker</div>', unsafe_allow_html=True)

    password = st.text_input("Enter Password", type="password")

    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        if st.button("Login", use_container_width=True):
            if password == config["password"]:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Wrong Password")

if not st.session_state.logged_in:
    login_screen()
    st.stop()

# ---------- HEADER ----------
st.title("🏸 Zion SmashBoard")
st.caption("Minimal Sports Tournament Dashboard")

# ---------- SIDEBAR ----------
menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Players",
        "Generate Fixtures",
        "Match Results",
        "Daily Leaderboard",
        "Overall Leaderboard",
        "Match History",
        "Settings"
    ]
)

# ---------- HELPERS ----------
today = str(date.today())

def today_matches():
    return [m for m in matches if m["date"] == today]

def calculate_daily_scores():
    scores = {}

    for player in players:
        scores[player] = 0

    for match in today_matches():
        for winner in match["winner"]:
            scores[winner] += 1

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def calculate_overall_scores():
    scores = {}

    for player in players:
        scores[player] = {
            "wins": 0,
            "matches": 0,
            "streak": 0
        }

    for match in matches:
        team1 = match["team1"]
        team2 = match["team2"]
        winners = match["winner"]

        for p in team1 + team2:
            if p in scores:
                scores[p]["matches"] += 1

        for p in winners:
            if p in scores:
                scores[p]["wins"] += 1

    rows = []

    for player, stats in scores.items():
        rows.append({
            "Player": player,
            "Wins": stats["wins"],
            "Matches": stats["matches"]
        })

    return pd.DataFrame(rows).sort_values(by="Wins", ascending=False)

def generate_pairs(selected_players):
    random.shuffle(selected_players)

    pairs = []

    for i in range(0, len(selected_players), 2):
        if i + 1 < len(selected_players):
            pairs.append([selected_players[i], selected_players[i+1]])

    return pairs

def generate_fixtures(pairs):
    fixtures = []

    for i in range(0, len(pairs), 2):
        if i + 1 < len(pairs):
            fixtures.append({
                "team1": pairs[i],
                "team2": pairs[i+1]
            })

    return fixtures

# ---------- DASHBOARD ----------
if menu == "Dashboard":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Players", len(players))

    with col2:
        st.metric("Today's Matches", len(today_matches()))

    with col3:
        total_matches = len(matches)
        st.metric("All-Time Matches", total_matches)

    st.divider()

    st.subheader("Today's Fixtures")

    tm = today_matches()

    if not tm:
        st.info("No matches generated today.")
    else:
        for idx, m in enumerate(tm):
            st.markdown(
                f'''
                ### Match {idx+1}
                🟦 {m["team1"][0]} & {m["team1"][1]}

                vs

                🟥 {m["team2"][0]} & {m["team2"][1]}
                '''
            )

# ---------- PLAYERS ----------
elif menu == "Players":

    st.subheader("Manage Players")

    with st.form("add_player"):
        new_player = st.text_input("Player Name")

        submitted = st.form_submit_button("Add Player")

        if submitted:
            if new_player and new_player not in players:
                players.append(new_player)
                save_json(PLAYERS_FILE, players)
                st.success("Player Added")
                st.rerun()

    st.divider()

    st.subheader("Player List")

    for p in players:
        col1, col2 = st.columns([4,1])

        with col1:
            st.markdown(f"🏸 {p}")

        with col2:
            if st.button("Delete", key=p):
                players.remove(p)
                save_json(PLAYERS_FILE, players)
                st.rerun()

# ---------- GENERATE FIXTURES ----------
elif menu == "Generate Fixtures":

    st.subheader("Generate Daily Fixtures")

    available_players = st.multiselect(
        "Select Available Players",
        players
    )

    if st.button("Generate Fixtures"):

        if len(available_players) < 4:
            st.error("Need at least 4 players")
        else:
            pairs = generate_pairs(available_players)
            fixtures = generate_fixtures(pairs)

            today_existing = [m for m in matches if m["date"] != today]

            for f in fixtures:
                today_existing.append({
                    "date": today,
                    "team1": f["team1"],
                    "team2": f["team2"],
                    "winner": []
                })

            save_json(MATCHES_FILE, today_existing)

            st.success("Fixtures Generated")
            st.balloons()

# ---------- MATCH RESULTS ----------
elif menu == "Match Results":

    st.subheader("Update Match Results")

    tm = today_matches()

    if not tm:
        st.info("No matches found")
    else:
        for idx, match in enumerate(tm):

            st.markdown(f"### Match {idx+1}")

            team1 = f'{match["team1"][0]} & {match["team1"][1]}'
            team2 = f'{match["team2"][0]} & {match["team2"][1]}'

            winner = st.radio(
                "Select Winner",
                [team1, team2],
                key=f"winner_{idx}"
            )

            if st.button("Save Result", key=f"save_{idx}"):

                if winner == team1:
                    match["winner"] = match["team1"]
                else:
                    match["winner"] = match["team2"]

                save_json(MATCHES_FILE, matches)

                st.success("Result Saved")
                st.balloons()

# ---------- DAILY LEADERBOARD ----------
elif menu == "Daily Leaderboard":

    st.subheader("🏆 Daily Leaderboard")

    scores = calculate_daily_scores()

    rank = 1

    for player, points in scores:

        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "🏸"

        st.markdown(
            f'''
            ### {medal} #{rank} - {player}
            Wins Today: **{points}**
            '''
        )

        rank += 1

# ---------- OVERALL LEADERBOARD ----------
elif menu == "Overall Leaderboard":

    st.subheader("🔥 Overall Leaderboard")

    df = calculate_overall_scores()

    st.dataframe(df, use_container_width=True)

# ---------- MATCH HISTORY ----------
elif menu == "Match History":

    st.subheader("📜 Match History")

    if not matches:
        st.info("No match history")
    else:
        for idx, match in enumerate(reversed(matches)):

            winner_text = "Pending"

            if match["winner"]:
                winner_text = f'{match["winner"][0]} & {match["winner"][1]}'

            st.markdown(
                f'''
                ### Match #{len(matches)-idx}
                📅 {match["date"]}

                🟦 {match["team1"][0]} & {match["team1"][1]}

                vs

                🟥 {match["team2"][0]} & {match["team2"][1]}

                🏆 Winner: {winner_text}
                '''
            )

# ---------- SETTINGS ----------
elif menu == "Settings":

    st.subheader("⚙️ Settings")

    current = st.text_input("Current Password", type="password")
    new = st.text_input("New Password", type="password")

    if st.button("Reset Password"):

        if current == config["password"]:

            config["password"] = new

            save_json(CONFIG_FILE, config)

            st.success("Password Updated")

        else:
            st.error("Wrong Current Password")

st.sidebar.divider()

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
