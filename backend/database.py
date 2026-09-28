import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "students.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            education_level TEXT NOT NULL,
            frequency TEXT NOT NULL,
            purpose TEXT NOT NULL,
            tool_count TEXT NOT NULL,
            daily_time TEXT NOT NULL,
            verification TEXT NOT NULL,
            learning_use TEXT NOT NULL,
            copying TEXT NOT NULL,
            productivity TEXT NOT NULL,
            dependency TEXT NOT NULL,
            usage_score INTEGER NOT NULL,
            learning_score INTEGER NOT NULL,
            diversity_score INTEGER NOT NULL,
            verification_score INTEGER NOT NULL,
            dependency_score INTEGER NOT NULL,
            usage_level TEXT NOT NULL,
            user_category TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_response(data):
    conn = get_connection()
    cur = conn.execute("""
        INSERT INTO responses (
            education_level, frequency, purpose, tool_count, daily_time,
            verification, learning_use, copying, productivity, dependency,
            usage_score, learning_score, diversity_score, verification_score,
            dependency_score, usage_level, user_category
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["education_level"], data["frequency"], data["purpose"],
        data["tool_count"], data["daily_time"], data["verification"],
        data["learning_use"], data["copying"], data["productivity"],
        data["dependency"], data["usage_score"], data["learning_score"],
        data["diversity_score"], data["verification_score"],
        data["dependency_score"], data["usage_level"], data["user_category"]
    ))
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id

def get_all():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM responses ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]
