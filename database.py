import sqlite3
from contextlib import contextmanager

DB_PATH = "attendance.db"

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                google_event_id TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                user_id TEXT NOT NULL,
                username TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('attending', 'maybe', 'not_attending')),
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(session_id, user_id),
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        """)
        conn.commit()

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def create_session(title, description, start_time, end_time=None):
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO sessions (title, description, start_time, end_time) VALUES (?, ?, ?, ?)",
            (title, description, start_time, end_time)
        )
        conn.commit()
        return cur.lastrowid

def update_google_event_id(session_id, event_id):
    with get_db() as conn:
        conn.execute(
            "UPDATE sessions SET google_event_id = ? WHERE id = ?",
            (event_id, session_id)
        )
        conn.commit()

def set_attendance(session_id, user_id, username, status):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO attendance (session_id, user_id, username, status)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(session_id, user_id) DO UPDATE SET
                status = excluded.status,
                username = excluded.username,
                updated_at = CURRENT_TIMESTAMP
        """, (session_id, user_id, username, status))
        conn.commit()

def get_session(session_id):
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM sessions WHERE id = ?", (session_id,)
        ).fetchone()

def get_latest_session():
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM sessions ORDER BY start_time DESC LIMIT 1"
        ).fetchone()

def get_attendance(session_id):
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM attendance WHERE session_id = ? ORDER BY status, username",
            (session_id,)
        ).fetchall()

def get_all_sessions():
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM sessions ORDER BY start_time DESC"
        ).fetchall()
