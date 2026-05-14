# 🏸 Smash League — Badminton Tournament Manager

A slick daily badminton tournament tracker with leaderboards, player management, and random pair generation.

---

## Features

- **Player Roster** — Add/remove players with custom colors
- **Today's Game** — Click players who are present, generate random doubles pairs with one button
- **Match Results** — Record scores and pick the winner for each court
- **Daily Leaderboard** — Today's standings update live as you record results
- **All-time Leaderboard** — Cumulative rankings with points, W/L, and win %
- **History** — Browse past sessions and their results

**Scoring:** Win = 3 pts · Loss = 1 pt

---

## Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Your browser will open at `http://localhost:8501`.  
Data is stored in `badminton.db` (SQLite) — it persists across restarts.

---

## Deploy FREE on Streamlit Community Cloud

1. **Push to GitHub**
   ```bash
   git init
   git add app.py requirements.txt README.md
   git commit -m "Initial commit"
   # Create a new repo on github.com, then:
   git remote add origin https://github.com/YOUR_USERNAME/badminton-app.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click **"New app"** → select your repo → `main` → `app.py`
   - Click **Deploy** — done! 🎉

> **Note on data persistence on Streamlit Cloud:**  
> Streamlit Community Cloud's filesystem resets when the app re-deploys.  
> For permanent persistence, either:
> - **Option A** (simple): Download your `badminton.db` backup periodically using a small export button (you can add this).
> - **Option B** (robust): Use a free [Supabase](https://supabase.com) PostgreSQL database — replace the SQLite calls with `psycopg2` + Supabase connection string stored in Streamlit Secrets.
>
> For a casual daily game played from one device/session, the built-in SQLite works great and data lasts the entire active session.

---

## Project Structure

```
badminton_app/
├── app.py           # Main Streamlit application
├── requirements.txt # Python dependencies
├── README.md        # This file
└── badminton.db     # Auto-created SQLite database (gitignore this)
```

Add `badminton.db` to `.gitignore` to avoid committing match data to GitHub.
