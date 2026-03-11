import sqlite3
from datetime import datetime

DB_NAME = "study_sessions.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time TEXT,
        end_time TEXT,
        duration INTEGER
    )
    """)

    conn.commit()
    conn.close()


def save_session(start, end, duration):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO sessions(start_time, end_time, duration)
    VALUES (?, ?, ?)
    """, (start, end, duration))

    conn.commit()
    conn.close()


def get_sessions():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM sessions")
    data = c.fetchall()

    conn.close()
    return data