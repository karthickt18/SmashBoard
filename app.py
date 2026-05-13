import streamlit as st
import sqlite3
import random
import pandas as pd
from datetime import date
import os

# ═══════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="🏸 Smash League",
    page_icon="🏸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════════
# CUSTOM CSS — Dark Neon Sports Theme
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&display=swap');

/* ── Root & Background ── */
.stApp {
    background: #080c14;
    background-image:
        radial-gradient(ellipse 80% 60% at 50% -10%, rgba(0,200,120,0.08) 0%, transparent 70%),
        radial-gradient(ellipse 40% 40% at 90% 80%, rgba(0,150,255,0.06) 0%, transparent 60%);
    min-height: 100vh;
}
.block-container { padding: 1.5rem 2.5rem !important; max-width: 1400px !important; }

/* ── Typography ── */
* { font-family: 'Rajdhani', sans-serif; }
h1 { font-family: 'Bebas Neue', sans-serif !important; }
h2 { font-family: 'Bebas Neue', sans-serif !important; color: #e8ffe8 !important; letter-spacing: 2px; }
h3 { font-family: 'Bebas Neue', sans-serif !important; color: #00ff88 !important; letter-spacing: 1px; }
p, div, span, label { color: #c8d8c8; }

/* ── Buttons ── */
.stButton > button {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 2px;
    font-size: 1rem !important;
    border-radius: 6px !important;
    border: none !important;
    transition: all 0.2s ease !important;
    padding: 0.45rem 1.2rem !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #00c853, #00e676) !important;
    color: #000 !important;
    box-shadow: 0 0 20px rgba(0, 230, 118, 0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 32px rgba(0, 230, 118, 0.6) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.06) !important;
    color: #aaa !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.12) !important;
    color: #fff !important;
    border-color: rgba(0,255,136,0.4) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-bottom: 1px solid rgba(0,255,136,0.15) !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 2px !important;
    color: #556 !important;
    padding: 0.7rem 1.8rem !important;
    border-bottom: 3px solid transparent !important;
    border-radius: 0 !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #00ff88 !important;
    border-bottom: 3px solid #00ff88 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem !important; }

/* ── Inputs ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0,255,136,0.25) !important;
    border-radius: 6px !important;
    color: #fff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(0,255,136,0.6) !important;
    box-shadow: 0 0 0 2px rgba(0,255,136,0.1) !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0,255,136,0.25) !important;
    border-radius: 6px !important;
    color: #fff !important;
}
.stSelectbox [data-baseweb="select"] { background: transparent !important; }
.stSelectbox svg { fill: #00ff88 !important; }

/* ── Color Picker ── */
.stColorPicker > div { background: transparent !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(0,255,136,0.15) !important;
    border-radius: 8px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 2px !important;
    font-size: 1.05rem !important;
    color: #00ff88 !important;
}
.streamlit-expanderContent {
    background: rgba(0,0,0,0.2) !important;
    border: 1px solid rgba(0,255,136,0.1) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
}

/* ── Metric ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,255,136,0.15);
    border-radius: 10px;
    padding: 1rem;
}
[data-testid="stMetricLabel"] { color: #778 !important; font-family: 'Rajdhani'; font-size: 0.9rem; }
[data-testid="stMetricValue"] { color: #00ff88 !important; font-family: 'Bebas Neue' !important; font-size: 2rem; }

/* ── Alerts ── */
.stAlert { border-radius: 8px !important; }

/* ── Divider ── */
hr { border-color: rgba(0,255,136,0.15) !important; }

/* ── Checkbox ── */
.stCheckbox { color: #ccc; }
.stCheckbox > label > div { background: rgba(255,255,255,0.05) !important; border-color: rgba(0,255,136,0.4) !important; }

/* ── Custom Cards ── */
.player-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1rem;
    transition: all 0.2s;
    height: 100%;
}
.player-card:hover {
    border-color: rgba(0,255,136,0.3);
    background: rgba(0,255,136,0.04);
}
.lb-row {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin: 0.35rem 0;
    transition: all 0.2s;
}
.lb-row:hover { border-color: rgba(0,255,136,0.25); }
.court-card {
    background: rgba(0,30,15,0.6);
    border: 1px solid rgba(0,255,136,0.2);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
}
.team-box {
    background: rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    text-align: center;
}
.team-box-winner {
    background: rgba(0,255,136,0.1);
    border: 1px solid rgba(0,255,136,0.5);
    box-shadow: 0 0 16px rgba(0,255,136,0.15);
}
.vs-badge {
    font-family: 'Bebas Neue';
    font-size: 1.6rem;
    color: #ff4444;
    text-align: center;
    letter-spacing: 2px;
}
.shuttle-divider {
    text-align: center;
    font-size: 1.4rem;
    margin: 0.2rem 0;
    opacity: 0.6;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# DATABASE SETUP
# ═══════════════════════════════════════════════════════════════════
DB_PATH = "badminton.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        color TEXT DEFAULT "#00e676"
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_date TEXT UNIQUE NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER,
        team1_p1 TEXT, team1_p2 TEXT,
        team2_p1 TEXT, team2_p2 TEXT,
        winner INTEGER DEFAULT 0,
        score TEXT DEFAULT "",
        FOREIGN KEY(session_id) REFERENCES sessions(id)
    )''')
    conn.commit()
    conn.close()

# ── Players ──────────────────────────────────────────────────────
def get_players():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM players ORDER BY name", conn)
    conn.close()
    return df

def add_player(name, color):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO players (name, color) VALUES (?, ?)", (name.strip(), color))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def delete_player(pid):
    conn = get_conn()
    conn.execute("DELETE FROM players WHERE id=?", (pid,))
    conn.commit()
    conn.close()

# ── Sessions ─────────────────────────────────────────────────────
def get_or_create_session(today=None):
    if today is None:
        today = date.today().isoformat()
    conn = get_conn()
    conn.execute("INSERT OR IGNORE INTO sessions (session_date) VALUES (?)", (today,))
    conn.commit()
    row = conn.execute("SELECT id FROM sessions WHERE session_date=?", (today,)).fetchone()
    conn.close()
    return row[0]

def get_all_sessions():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM sessions ORDER BY session_date DESC", conn)
    conn.close()
    return df

# ── Matches ──────────────────────────────────────────────────────
def get_session_matches(session_id):
    conn = get_conn()
    df = pd.read_sql(f"SELECT * FROM matches WHERE session_id={session_id} ORDER BY id", conn)
    conn.close()
    return df

def save_match(session_id, t1p1, t1p2, t2p1, t2p2):
    conn = get_conn()
    conn.execute(
        "INSERT INTO matches (session_id, team1_p1, team1_p2, team2_p1, team2_p2) VALUES (?,?,?,?,?)",
        (session_id, t1p1, t1p2, t2p1, t2p2)
    )
    conn.commit()
    conn.close()

def update_match(match_id, winner, score):
    conn = get_conn()
    conn.execute("UPDATE matches SET winner=?, score=? WHERE id=?", (winner, score, match_id))
    conn.commit()
    conn.close()

def delete_session_matches(session_id):
    conn = get_conn()
    conn.execute("DELETE FROM matches WHERE session_id=?", (session_id,))
    conn.commit()
    conn.close()

# ── Stats ────────────────────────────────────────────────────────
STATS_QUERY = """
WITH all_p AS (
    SELECT team1_p1 AS player, (winner=1) AS won FROM matches WHERE winner!=0 AND session_filter
    UNION ALL SELECT team1_p2, (winner=1) FROM matches WHERE winner!=0 AND session_filter
    UNION ALL SELECT team2_p1, (winner=2) FROM matches WHERE winner!=0 AND session_filter
    UNION ALL SELECT team2_p2, (winner=2) FROM matches WHERE winner!=0 AND session_filter
)
SELECT
    player,
    COUNT(*)          AS played,
    SUM(won)          AS wins,
    COUNT(*)-SUM(won) AS losses,
    ROUND(100.0*SUM(won)/COUNT(*),1) AS win_pct,
    SUM(won)*3 + (COUNT(*)-SUM(won)) AS points
FROM all_p
WHERE player IS NOT NULL AND player!=''
GROUP BY player
ORDER BY points DESC, win_pct DESC
"""

def get_overall_stats():
    conn = get_conn()
    q = STATS_QUERY.replace("AND session_filter", "")
    df = pd.read_sql(q, conn)
    conn.close()
    return df

def get_daily_stats(session_id):
    conn = get_conn()
    q = STATS_QUERY.replace("session_filter", f"session_id={session_id}")
    df = pd.read_sql(q, conn)
    conn.close()
    return df

# ═══════════════════════════════════════════════════════════════════
# INIT
# ═══════════════════════════════════════════════════════════════════
init_db()
if "today_players" not in st.session_state:
    st.session_state.today_players = []
if "bench" not in st.session_state:
    st.session_state.bench = []

PLAYER_COLORS = [
    "#00e676","#ff6b6b","#48dbfb","#ffd700","#ff9ff3",
    "#54a0ff","#ff9f43","#10ac84","#ee5a24","#a29bfe",
    "#fd79a8","#00cec9","#6c5ce7","#fdcb6e","#e17055"
]
RANK_ICONS = ["🥇","🥈","🥉"] + [f"#{i}" for i in range(4, 50)]

# ═══════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center; padding: 1.2rem 0 1.8rem;">
    <div style="font-size: 3.5rem; line-height:1; margin-bottom: 0.3rem; 
                filter: drop-shadow(0 0 20px rgba(0,255,136,0.5));">🏸</div>
    <div style="font-family:'Bebas Neue',sans-serif; font-size: 3.8rem; line-height:1;
                background: linear-gradient(135deg, #00ff88 0%, #00cfff 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                letter-spacing: 8px; margin-bottom: 0.2rem;">SMASH LEAGUE</div>
    <div style="font-family:'Share Tech Mono',monospace; font-size: 0.8rem; 
                color: #445; letter-spacing: 6px; text-transform:uppercase;">
        Badminton Tournament Manager
    </div>
</div>
""", unsafe_allow_html=True)

# ── Global stats bar ──
players_df = get_players()
today_session_id = get_or_create_session()
all_stats = get_overall_stats()
conn = get_conn()
total_matches_played = pd.read_sql("SELECT COUNT(*) as n FROM matches WHERE winner!=0", conn).iloc[0]['n']
today_matches_played = pd.read_sql(f"SELECT COUNT(*) as n FROM matches WHERE session_id={today_session_id} AND winner!=0", conn).iloc[0]['n']
conn.close()

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("👥 Players", len(players_df))
with m2:
    st.metric("🏸 Total Matches", int(total_matches_played))
with m3:
    st.metric("📅 Today's Matches", int(today_matches_played))
with m4:
    leader = all_stats.iloc[0]['player'] if len(all_stats) > 0 else "—"
    st.metric("👑 All-time Leader", leader)

st.markdown("<div style='margin-bottom:1.5rem'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════
tab_game, tab_boards, tab_players, tab_history = st.tabs([
    "🎮  TODAY'S GAME",
    "🏆  LEADERBOARDS",
    "👥  PLAYERS",
    "📋  HISTORY"
])

# ══════════════════════════════════════════════════════════
# TAB 1 — TODAY'S GAME
# ══════════════════════════════════════════════════════════
with tab_game:
    today_str = date.today().strftime("%A, %d %B %Y")
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:1.2rem;">
        <div style="font-family:'Bebas Neue'; font-size:1.8rem; color:#00ff88; letter-spacing:2px;">
            📅 {today_str}
        </div>
    </div>
    """, unsafe_allow_html=True)

    players_df = get_players()

    if players_df.empty:
        st.info("🎾 No players yet — head to the **Players** tab to add your squad!")
    else:
        color_map = dict(zip(players_df["name"], players_df["color"]))

        # ── Player Selection ──
        st.markdown("""
        <div style="font-family:'Bebas Neue'; font-size:1.4rem; color:#ccc; letter-spacing:3px; 
                    margin-bottom:0.8rem;">👥 SELECT TODAY'S PLAYERS</div>
        """, unsafe_allow_html=True)

        all_names = players_df["name"].tolist()
        n_cols = min(5, len(all_names))
        col_groups = [all_names[i::n_cols] for i in range(n_cols)]
        btn_cols = st.columns(n_cols)
        for ci, group in enumerate(col_groups):
            with btn_cols[ci]:
                for name in group:
                    is_sel = name in st.session_state.today_players
                    label = f"✓ {name}" if is_sel else name
                    btype = "primary" if is_sel else "secondary"
                    if st.button(label, key=f"sel_{name}", type=btype, use_container_width=True):
                        if is_sel:
                            st.session_state.today_players.remove(name)
                        else:
                            st.session_state.today_players.append(name)
                        st.rerun()

        selected = st.session_state.today_players
        n_sel = len(selected)

        st.markdown("<br>", unsafe_allow_html=True)
        n_matches = n_sel // 4
        n_bench = n_sel % 4
        info_html = f"""
        <div style="background:rgba(0,255,136,0.07); border:1px solid rgba(0,255,136,0.2);
                    border-radius:8px; padding:0.7rem 1rem; margin-bottom:1rem;
                    font-family:'Rajdhani'; font-size:1.05rem; color:#aaa;">
            <b style="color:#00ff88">{n_sel}</b> players selected →
            <b style="color:#00cfff">{n_matches}</b> doubles match{'es' if n_matches!=1 else ''} possible
            {'• <b style="color:#ffd700">' + str(n_bench) + '</b> on bench' if n_bench else ''}
        </div>
        """
        st.markdown(info_html, unsafe_allow_html=True)

        # ── Actions ──
        gc1, gc2, gc3 = st.columns([2, 1, 1])
        with gc1:
            gen_disabled = n_sel < 4
            if st.button("🎲  GENERATE RANDOM PAIRS", type="primary", disabled=gen_disabled, use_container_width=True):
                pool = selected.copy()
                random.shuffle(pool)
                delete_session_matches(today_session_id)
                while len(pool) >= 4:
                    t1p1, t1p2, t2p1, t2p2 = pool.pop(), pool.pop(), pool.pop(), pool.pop()
                    save_match(today_session_id, t1p1, t1p2, t2p1, t2p2)
                st.session_state.bench = pool
                st.rerun()
        with gc2:
            if st.button("🔀  RESHUFFLE", use_container_width=True):
                pool = selected.copy()
                random.shuffle(pool)
                delete_session_matches(today_session_id)
                while len(pool) >= 4:
                    t1p1, t1p2, t2p1, t2p2 = pool.pop(), pool.pop(), pool.pop(), pool.pop()
                    save_match(today_session_id, t1p1, t1p2, t2p1, t2p2)
                st.session_state.bench = pool
                st.rerun()
        with gc3:
            if st.button("🗑️  CLEAR ALL", use_container_width=True):
                delete_session_matches(today_session_id)
                st.session_state.bench = []
                st.rerun()

        # ── Bench ──
        if st.session_state.bench:
            bench_str = " • ".join(st.session_state.bench)
            st.markdown(f"""
            <div style="background:rgba(255,200,0,0.07); border:1px solid rgba(255,200,0,0.2);
                        border-radius:8px; padding:0.6rem 1rem; margin:0.6rem 0;
                        font-family:'Rajdhani'; font-size:1rem;">
                🪑 <b style="color:#ffd700">Bench this round:</b>
                <span style="color:#aaa"> {bench_str}</span>
            </div>
            """, unsafe_allow_html=True)

        # ── Matches ──
        matches_df = get_session_matches(today_session_id)

        if not matches_df.empty:
            st.markdown(f"""
            <div style="font-family:'Bebas Neue'; font-size:1.4rem; color:#ccc; 
                        letter-spacing:3px; margin:1rem 0 0.5rem;">
                ⚡ {len(matches_df)} COURT{'S' if len(matches_df)!=1 else ''} TODAY
            </div>
            """, unsafe_allow_html=True)

            for idx, match in matches_df.iterrows():
                mid = int(match["id"])
                winner = int(match["winner"]) if match["winner"] else 0
                t1w = winner == 1
                t2w = winner == 2

                c1, c2, c3, c_score, c_win = st.columns([3, 0.7, 3, 2, 3])

                with c1:
                    bc1 = color_map.get(match["team1_p1"], "#00e676")
                    bc2 = color_map.get(match["team1_p2"], "#00e676")
                    extra = ' team-box-winner' if t1w else ''
                    st.markdown(f"""
                    <div class="team-box{extra}">
                        <div style="font-family:'Bebas Neue'; font-size:1.2rem; letter-spacing:1px;">
                            <span style="color:{bc1}">⬤</span> {match["team1_p1"]}
                            &nbsp;<span style="color:#444">+</span>&nbsp;
                            <span style="color:{bc2}">⬤</span> {match["team1_p2"]}
                        </div>
                        {'<div style="color:#00ff88; font-size:0.8rem; margin-top:2px;">🏆 WINNER</div>' if t1w else ''}
                    </div>
                    """, unsafe_allow_html=True)

                with c2:
                    st.markdown("""
                    <div class="vs-badge" style="padding-top:0.5rem">VS</div>
                    """, unsafe_allow_html=True)

                with c3:
                    bc3 = color_map.get(match["team2_p1"], "#ff6b6b")
                    bc4 = color_map.get(match["team2_p2"], "#ff6b6b")
                    extra2 = ' team-box-winner' if t2w else ''
                    st.markdown(f"""
                    <div class="team-box{extra2}">
                        <div style="font-family:'Bebas Neue'; font-size:1.2rem; letter-spacing:1px;">
                            <span style="color:{bc3}">⬤</span> {match["team2_p1"]}
                            &nbsp;<span style="color:#444">+</span>&nbsp;
                            <span style="color:{bc4}">⬤</span> {match["team2_p2"]}
                        </div>
                        {'<div style="color:#00ff88; font-size:0.8rem; margin-top:2px;">🏆 WINNER</div>' if t2w else ''}
                    </div>
                    """, unsafe_allow_html=True)

                with c_score:
                    new_score = st.text_input(
                        "Score", value=match["score"] or "",
                        placeholder="21-18, 19-21...",
                        key=f"sc_{mid}",
                        label_visibility="collapsed"
                    )

                with c_win:
                    opts = [
                        "⏳ No result yet",
                        f"🏆 {match['team1_p1']} & {match['team1_p2']}",
                        f"🏆 {match['team2_p1']} & {match['team2_p2']}"
                    ]
                    chosen = st.selectbox(
                        "Winner", opts, index=winner,
                        key=f"win_{mid}",
                        label_visibility="collapsed"
                    )
                    new_winner = opts.index(chosen)
                    if new_winner != winner or new_score != (match["score"] or ""):
                        update_match(mid, new_winner, new_score)
                        st.rerun()

                st.markdown("<div style='border-bottom:1px solid rgba(255,255,255,0.05); margin:0.5rem 0'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# TAB 2 — LEADERBOARDS
# ══════════════════════════════════════════════════════════
with tab_boards:
    lb_overall, lb_today = st.columns(2)

    def render_leaderboard(df, accent):
        if df.empty:
            st.markdown("""
            <div style="color:#556; text-align:center; padding:2rem; font-family:'Rajdhani';">
                No matches recorded yet.
            </div>
            """, unsafe_allow_html=True)
            return
        for i, row in df.iterrows():
            rank = i + 1
            icon = RANK_ICONS[i]
            medal_colors = {1: "#ffd700", 2: "#b0b8c8", 3: "#cd7f32"}
            rank_color = medal_colors.get(rank, "#445")
            bar_w = int(100 * int(row["points"]) / max(df["points"].max(), 1))
            st.markdown(f"""
            <div class="lb-row" style="border-left: 3px solid {rank_color};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <span style="font-family:'Bebas Neue'; font-size:1.4rem; 
                                     color:{rank_color}; min-width:2rem; text-align:center;">{icon}</span>
                        <span style="font-family:'Rajdhani'; font-size:1.15rem; font-weight:700; color:#ddd;">
                            {row['player']}
                        </span>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-family:'Bebas Neue'; font-size:1.5rem; color:{accent}; letter-spacing:1px;">
                            {int(row['points'])} <span style="font-size:0.85rem; color:#556;">PTS</span>
                        </span>
                    </div>
                </div>
                <div style="display:flex; align-items:center; gap:16px; margin-top:5px;">
                    <div style="flex:1; height:4px; background:rgba(255,255,255,0.06); border-radius:2px;">
                        <div style="width:{bar_w}%; height:100%; background:{accent}; border-radius:2px; 
                                    opacity:0.7; transition:width 0.4s;"></div>
                    </div>
                    <span style="font-size:0.85rem; color:#667; white-space:nowrap; font-family:'Share Tech Mono';">
                        {int(row['wins'])}W&nbsp;{int(row['losses'])}L&nbsp;·&nbsp;{row['win_pct']}%
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with lb_overall:
        st.markdown("""
        <div style="font-family:'Bebas Neue'; font-size:1.8rem; letter-spacing:3px; 
                    color:#ffd700; margin-bottom:0.8rem;">🏆 ALL-TIME RANKINGS</div>
        """, unsafe_allow_html=True)
        render_leaderboard(get_overall_stats(), "#ffd700")

    with lb_today:
        st.markdown("""
        <div style="font-family:'Bebas Neue'; font-size:1.8rem; letter-spacing:3px;
                    color:#00ff88; margin-bottom:0.8rem;">📅 TODAY'S STANDINGS</div>
        """, unsafe_allow_html=True)
        render_leaderboard(get_daily_stats(today_session_id), "#00ff88")

    # Points system legend
    st.divider()
    st.markdown("""
    <div style="text-align:center; font-family:'Rajdhani'; font-size:0.95rem; color:#445; padding:0.5rem 0;">
        🏆 Win = <b style="color:#00ff88">3 pts</b> &nbsp;|&nbsp; 
        💔 Loss = <b style="color:#aaa">1 pt</b> &nbsp;|&nbsp;
        Ranking: <b style="color:#ccc">Points → Win %</b>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# TAB 3 — PLAYERS
# ══════════════════════════════════════════════════════════
with tab_players:
    st.markdown("""
    <div style="font-family:'Bebas Neue'; font-size:1.8rem; letter-spacing:3px; 
                color:#00ff88; margin-bottom:1rem;">👥 PLAYER ROSTER</div>
    """, unsafe_allow_html=True)

    # ── Add player form ──
    with st.expander("➕  ADD NEW PLAYER", expanded=True):
        fc1, fc2, fc3 = st.columns([3, 1.5, 1.2])
        with fc1:
            new_name = st.text_input("Name", placeholder="Enter player name", key="new_name",
                                     label_visibility="collapsed")
        with fc2:
            new_color = st.color_picker("Color", value=random.choice(PLAYER_COLORS), key="new_color",
                                        label_visibility="collapsed")
        with fc3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ADD  →", type="primary", use_container_width=True):
                if new_name.strip():
                    if add_player(new_name, new_color):
                        st.success(f"✅ {new_name} added to the roster!")
                        st.rerun()
                    else:
                        st.error(f"'{new_name}' already exists.")
                else:
                    st.warning("Please enter a player name.")

    # ── Player grid ──
    players_df = get_players()
    if players_df.empty:
        st.markdown("""
        <div style="color:#445; text-align:center; padding:3rem; font-family:'Rajdhani';">
            No players yet. Add some above!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="font-family:'Rajdhani'; font-size:0.9rem; color:#556; margin:0.5rem 0 1rem;">
            {len(players_df)} registered players
        </div>
        """, unsafe_allow_html=True)

        cols_per_row = 3
        rows = [players_df.iloc[i:i+cols_per_row] for i in range(0, len(players_df), cols_per_row)]

        for row_df in rows:
            row_cols = st.columns(cols_per_row)
            for j, (_, player) in enumerate(row_df.iterrows()):
                pid = int(player["id"])
                pname = player["name"]
                pcolor = player["color"]

                # Get player stats
                conn = get_conn()
                safe = pname.replace("'", "''")
                pstats = pd.read_sql(f"""
                    WITH p AS (
                        SELECT team1_p1 AS pl, (winner=1) AS w FROM matches WHERE winner!=0 AND team1_p1='{safe}'
                        UNION ALL SELECT team1_p2, (winner=1) FROM matches WHERE winner!=0 AND team1_p2='{safe}'
                        UNION ALL SELECT team2_p1, (winner=2) FROM matches WHERE winner!=0 AND team2_p1='{safe}'
                        UNION ALL SELECT team2_p2, (winner=2) FROM matches WHERE winner!=0 AND team2_p2='{safe}'
                    )
                    SELECT COUNT(*) AS played, COALESCE(SUM(w),0) AS wins FROM p
                """, conn)
                conn.close()

                played = int(pstats.iloc[0]["played"])
                wins = int(pstats.iloc[0]["wins"])
                losses = played - wins
                pts = wins * 3 + losses

                with row_cols[j]:
                    st.markdown(f"""
                    <div class="player-card" style="border-top: 3px solid {pcolor};">
                        <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
                            <div style="width:44px; height:44px; border-radius:50%; 
                                        background:{pcolor}; display:flex; align-items:center;
                                        justify-content:center; font-family:'Bebas Neue';
                                        font-size:1.4rem; color:#000; flex-shrink:0;">
                                {pname[0].upper()}
                            </div>
                            <div>
                                <div style="font-family:'Bebas Neue'; font-size:1.3rem; 
                                            color:#eee; letter-spacing:1px;">{pname}</div>
                                <div style="font-size:0.85rem; color:#556; font-family:'Share Tech Mono';">
                                    {played}G · {wins}W · {pts}PTS
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Remove {pname}", key=f"del_{pid}", use_container_width=True):
                        delete_player(pid)
                        if pname in st.session_state.today_players:
                            st.session_state.today_players.remove(pname)
                        st.rerun()

# ══════════════════════════════════════════════════════════
# TAB 4 — HISTORY
# ══════════════════════════════════════════════════════════
with tab_history:
    st.markdown("""
    <div style="font-family:'Bebas Neue'; font-size:1.8rem; letter-spacing:3px;
                color:#00ff88; margin-bottom:1rem;">📋 MATCH HISTORY</div>
    """, unsafe_allow_html=True)

    sessions_df = get_all_sessions()

    if sessions_df.empty:
        st.markdown("""
        <div style="color:#445; text-align:center; padding:3rem; font-family:'Rajdhani';">
            No sessions recorded yet.
        </div>
        """, unsafe_allow_html=True)
    else:
        for _, session in sessions_df.iterrows():
            sid = int(session["id"])
            sdate = session["session_date"]
            m_df = get_session_matches(sid)
            completed = len(m_df[m_df["winner"] != 0]) if not m_df.empty else 0
            total = len(m_df)

            is_today = (sdate == date.today().isoformat())
            badge = " 🟢 TODAY" if is_today else ""

            with st.expander(f"📅  {sdate}{badge}  —  {total} matches  ({completed} completed)"):
                if m_df.empty:
                    st.write("No matches for this session.")
                else:
                    for _, m in m_df.iterrows():
                        w = int(m["winner"]) if m["winner"] else 0
                        t1 = f"{m['team1_p1']} & {m['team1_p2']}"
                        t2 = f"{m['team2_p1']} & {m['team2_p2']}"
                        sc = f"  `{m['score']}`" if m["score"] else ""

                        if w == 1:
                            line = f"🏆 **{t1}** def. {t2}{sc}"
                        elif w == 2:
                            line = f"🏆 **{t2}** def. {t1}{sc}"
                        else:
                            line = f"⏳ {t1} vs {t2} — *no result*"

                        st.markdown(line)

                    # Daily stats for this session
                    ds = get_daily_stats(sid)
                    if not ds.empty:
                        st.markdown("**Session standings:**")
                        cols_s = st.columns(min(4, len(ds)))
                        for ci, (_, row) in enumerate(ds.iterrows()):
                            with cols_s[ci % len(cols_s)]:
                                st.metric(
                                    row["player"],
                                    f"{int(row['points'])} pts",
                                    f"{int(row['wins'])}W {int(row['losses'])}L"
                                )

# ── Footer ──
st.markdown("""
<div style="text-align:center; padding:2rem 0 1rem; 
            font-family:'Share Tech Mono'; font-size:0.75rem; color:#223;">
    SMASH LEAGUE · Built with Streamlit · 🏸
</div>
""", unsafe_allow_html=True)
