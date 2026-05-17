import sqlite3

DB_PATH = "wordle.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            word TEXT,
            solved BOOLEAN,
            attempts_count INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            total_games INTEGER DEFAULT 0,
            total_wins INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def get_today_game(user_id: int, date: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM games WHERE user_id = ? AND date = ?",
        (user_id, date)
    )
    row = cur.fetchone()
    conn.close()
    return row

def save_game(user_id: int, username: str, date: str, word: str, solved: bool, attempts_count: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO games (user_id, date, word, solved, attempts_count)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, date, word, solved, attempts_count))
    cur.execute("""
        INSERT INTO users (user_id, username, total_games, total_wins)
        VALUES (?, ?, 1, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            total_games = total_games + 1,
            total_wins = total_wins + ?
    """, (user_id, username, int(solved), int(solved)))
    conn.commit()
    conn.close()

def get_stats(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT total_games, total_wins FROM users WHERE user_id = ?",
        (user_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row